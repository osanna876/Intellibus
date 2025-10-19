from flask import Flask, request, jsonify, send_from_directory, send_file
import json, os, time, subprocess

#needed for admin authorization
from functools import wraps
from flask import session, redirect, url_for, flash



app = Flask(__name__)

Report_Files = "reports.json"
base_dir = os.path.abspath(os.path.dirname(__file__))

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "grahpap")



def serve_html(name):
    """Serve a file as text/html. If an extensionless file is present (like 'main_page'),
    serve it with the text/html mimetype so browsers render it instead of downloading.
    If a file with the same name plus '.html' exists, prefer that.
    """
    # try the exact filename first
    path = os.path.join(base_dir, name)
    if not os.path.exists(path):
        # try with .html extension
        alt = path + '.html'
        if os.path.exists(alt):
            path = alt
        else:
            # fallback to send_from_directory which will return a 404 if missing
            return send_from_directory(base_dir, name)

    # serve with explicit mimetype so the browser won't download it
    return send_file(path, mimetype='text/html')


#initialize data stores for reports

if not os.path.exists(Report_Files):
    with open(Report_Files, "w") as f:
        json.dump([],f)


@app.route('/')
def index():
    # files in the workspace are named without a .html extension (e.g. 'main_page')
    return serve_html('main_page')


@app.route('/volunteer')
def volunteer_page():
    return serve_html('volunteer')

@app.route('/about')
def about_page():
    return serve_html('about')

@app.route('/saves')
def saves_page():
    return serve_html('saves')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

    # If GET, show the page. file is named 'login' (no .html)
    return serve_html('login')


@app.route('/report', methods=['GET', 'POST'])
def report_page():
    if request.method == 'POST':
        name = request.form.get('name') or 'Anonymous'
        location = request.form.get('location')
        # try to get optional lat/lon fields (may be empty)
        latitude = request.form.get('latitude') or None
        longitude = request.form.get('longitude') or None
        disaster_type = request.form.get('type') or 'Unknown'
        description = request.form.get('description') or ''

        try:
            result = subprocess.run(
            ["classify.exe"],
            input= description,
            capture_output= True,
            text= True,
            check= True
        )
            urgency = result.stdout.strip()
        except Exception as e:
            urgency = "Unknown"
            print("Classifier error:", e)


        # Load existing reports
        reports = load_reports()

        # Create new report entry
        report = {
            "Id": len(reports) + 1,
            "Name": name,
            "Location": location,
            "Latitude": latitude,
            "Longitude": longitude,
            "Type": disaster_type,
            "Description": description,
            "Urgency Level": urgency,
            "Timestamp": time.strftime("%Y-%m-%d, %H:%M:%S")
        }

        # Add and save
        reports.append(report)
        save_reports(reports)

        # Confirm to user (simple message for now)
        return jsonify({"message": "Report submitted successfully!", "report": report})

    # Show the report form if GET request (file named 'report')
    return serve_html('report')



@app.route('/distance')
def distance_page():
    """Serve the interactive distance tracker map."""
    return serve_html('distance')



def load_reports():
    with open(Report_Files, encoding='utf-8') as f:
        return json.load(f)


def save_reports(data):
    with open(Report_Files, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

#admin things

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('is_admin'):
            # not logged in -> redirect to login page
            return redirect(url_for('admin_login', next=request.path))
        return f(*args, **kwargs)
    return decorated


# Only valid credentials (demo)
ADMIN_USERNAME = "admin287"
ADMIN_PASSWORD = "admin287@31"

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    # If already logged in, go to dashboard
    if session.get('is_admin'):
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['is_admin'] = True
            # optional: store username
            session['admin_user'] = username
            # redirect to next (if provided) or admin dashboard
            next_url = request.args.get('next') or url_for('admin_dashboard')
            return redirect(next_url)
        else:
            # invalid credentials
            flash('Invalid username or password', 'error')
            return redirect(url_for('admin_login'))

    # GET -> serve the HTML login form file named 'admin_login' (or admin_login.html)
    return serve_html('admin_login')


@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    session.pop('admin_user', None)
    flash('Logged out', 'info')
    return redirect(url_for('admin_login'))

@app.route('/admin')
@login_required
def admin_dashboard():
    return serve_html('admin')   # 'admin' file served same way as others

@app.route('/api/reports')
@login_required
def get_reports():
    urgency_filter = request.args.get('urgency')
    reports = load_reports()
    if urgency_filter:
        reports = [r for r in reports if r.get('Urgency Level') == urgency_filter]
    return jsonify(reports)


@app.route('/api/report-location', methods=['POST'])
def api_report_location():
    """Accept immediate SOS reports (JSON body with latitude, longitude, optional description/location).
    This endpoint does not require admin login (it's used by clients reporting emergencies).
    """
    try:
        data = request.get_json() or {}
    except Exception:
        data = {}

    latitude = data.get('latitude') or data.get('lat') or None
    longitude = data.get('longitude') or data.get('lon') or None
    description = data.get('description') or ''
    location = data.get('location') or data.get('loc') or (f"{latitude}, {longitude}" if latitude and longitude else 'Unknown')

    # create report with defaults
    reports = load_reports()
    report = {
        "Id": len(reports) + 1,
        "Name": data.get('name') or 'Anonymous',
        "Location": location,
        "Latitude": latitude,
        "Longitude": longitude,
        "Type": data.get('type') or 'Unknown',
        "Description": description,
        "Urgency Level": data.get('urgency') or 'Unknown',
        "Timestamp": time.strftime("%Y-%m-%d, %H:%M:%S")
    }

    reports.append(report)
    save_reports(reports)

    return jsonify({"success": True, "report": report})


if __name__ == '__main__':
    app.run(debug = True)
