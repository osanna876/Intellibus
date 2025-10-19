from flask import Flask, request, jsonify, send_from_directory, abort
import json, os, time


app = Flask(__name__)

Report_Files = "database/reports.json"
base_dir = os.path.abspath(os.path.dirname(__file__))


#initialize data stores for reports

if not os.path.exists(Report_Files):
    with open(Report_Files, "w") as f:
        json.dump([],f)


@app.route('/')
def index():
    return send_from_directory(base_dir, 'main page.html')


@app.route('/report', methods=['submit'])
def report_page():
    return send_from_directory(base_dir, 'report.html')

@app.route('/volunteer')
def volunteer_page():
    return send_from_directory(base_dir, 'volunteer.html')

@app.route('/about')
def about_page():
    return send_from_directory(base_dir, 'about.hmtl')

@app.route('/saves')
def saves_page():
    return send_from_directory(base_dir, 'saves.html')

@app.route('/login')
def login_page():
    return send_from_directory(base_dir,'login.html')

@app.route('/reports', methods=['GET'])
def get_reports():
    reports = load_reports()
    return jsonify(reports)


def load_reports():
    with open(Report_Files, encoding='utf-8') as f:
        return json.load(f)


def save_reports(data):
    with open(Report_Files, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    app.run(debug = True)