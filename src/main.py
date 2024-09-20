import json
import requests
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, url_for

# Load the API Key
load_dotenv("../config.env")
api_key = os.getenv("ABUSEIPDB_API_KEY")

app = Flask(__name__, static_folder='static')

class CubCollector:
    def __init__(self, ip: str):
        self.ip = ip
        
    def check_ip(self):
        
        url = 'https://api.abuseipdb.com/api/v2/check'

        querystring = {'ipAddress': self.ip, 'maxAgeInDays': '90'}
        headers = {'Accept': 'application/json', 'Key': api_key}
        
        try:
            response = requests.request(method='GET', url=url, headers=headers, params=querystring)
            # Format output
            decodedResponse = json.loads(response.text)
            return json.dumps(decodedResponse, sort_keys=True, indent=4)
        except requests.RequestException as e:
            print(f"Request Error: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_ip', methods=['POST'])
def check_ip():
    ip = request.form['ip']
    collector = CubCollector(ip)
    result = collector.check_ip()
    return jsonify(json.loads(result))

if __name__ == '__main__':
    app.run(debug=True)
