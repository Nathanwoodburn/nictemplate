from flask import Flask, make_response, redirect, request, jsonify, render_template, send_from_directory
import os
import dotenv

app = Flask(__name__)
dotenv.load_dotenv()

@app.route('/assets/<path:path>')
def send_report(path):
    return send_from_directory('templates/assets', path)


@app.route('/')
def index():
    # Get host from request
    host = request.headers.get('host')
    tld = host.split('.')[-1]

    return render_template('index.html', tld=tld)

if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0')