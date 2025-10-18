from flask import Flask, request, jsonify
from utils.classifier import classify_urgency
import json, os, time


app = Flask(__name__)
Report_Files = "database/reports.json"

#initialize data stores for reports

if not os.path.exists:
    with open(Report_Files, "w") as f:
        json.dump([],f)

@app.route('/report', methods=['POST'])
def add_report():
    data = request.get_json()
    description = data.get('description', '')
    location = data.get('location', '')

    urgency = classify_urgency(description)
    report = {
        "id": int(time.time()),
        "location": location,
        "description": description,
        "urgency": urgency
    }

    reports = load_reports()
    reports.append(report)
    save_reports(reports)
    return jsonify({"message": "Report added successfully", "report": report}), 201

@app.route('/reports', methods=['GET'])
def get_reports():
    reports = load_reports()
    return jsonify(reports)


def load_reports():
    with open(Report_Files) as f:
        return json.load(f)

def save_reports(data):
    with open(Report_Files, "w") as f:
        json.dump(data, f, indent=2)


if __name__ == '__main__':
    app.run(debug=True)