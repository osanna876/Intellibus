from flask import Flask, request, jsonify, send_from_directory, send_file
import json, os, time


app = Flask(__name__)

Report_Files = "reports.json"
base_dir = os.path.abspath(os.path.dirname(__file__))


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
        name = request.form.get('name')
        location = request.form.get('location')
        disaster_type = request.form.get('type')
        description = request.form.get('description')

        # Load existing reports
        reports = load_reports()

        # Create new report entry
        report = {
            "id": len(reports) + 1,
            "name": name,
            "location": location,
            "type": disaster_type,
            "description": description,
            "timestamp": time.strftime("%Y-%m-%d, %H:%M:%S")
        }

        # Add and save
        reports.append(report)
        save_reports(reports)

        # Confirm to user (simple message for now)
        return jsonify({"message": "Report submitted successfully!", "report": report})

    # Show the report form if GET request (file named 'report')
    return serve_html('report')



def load_reports():
    with open(Report_Files, encoding='utf-8') as f:
        return json.load(f)


def save_reports(data):
    with open(Report_Files, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    app.run(debug = True)