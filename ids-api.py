import json
from flask import Flask, abort, jsonify
from ids import Check


app = Flask(__name__)
#app.secret_key = b'SECRET_KEY'


def GetConf()->dict:
    configFile = open("conf.json")
    configData = json.load(configFile)
    configFile.close()
    return configData

global CONFIG
CONFIG = GetConf()


@app.route('/check', methods=['POST'])
def make_check():
    Check()
    return jsonify({"check":"start"})


@app.route('/reports', methods=['GET'])
def get_reports():
    with open(f"{CONFIG["reportsFolder"]}/check.json") as file:
        reports = json.load(file)
        return jsonify(reports)


@app.route('/reports/<reports_id>', methods=['GET'])
def get_report(reports_id=None):
    with open(f"{CONFIG["reportsFolder"]}/check.json") as file:
        reports = json.load(file)
        if reports_id in reports:
            results = jsonify(reports[reports_id])
            return results
    
    abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
