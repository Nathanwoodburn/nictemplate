from flask import Flask, make_response, redirect, request, jsonify, render_template, send_from_directory
import os
import dotenv
import requests
import datetime

app = Flask(__name__)
dotenv.load_dotenv()

not_for_sale = ['australia', 'newzealand']

@app.route('/assets/<path:path>')
def send_report(path):
    return send_from_directory('templates/assets', path)


@app.route('/')
def index():
    year = datetime.datetime.now().year
    https_redirect="<script src=\"https://nathan.woodburn/https.js\"></script>"

    # Get host from request
    host = request.headers.get('host')
    tld = host.split('.')[-1]
    tld = tld.split(':')[0]
    if tld == 'localhost' or tld == '1':
        tld = 'freeconcept'
        https_redirect = "<script>console.log('https.js not loaded on localhost')</script>"

    
    if tld in not_for_sale:
        return render_template('not_for_sale.html', tld=tld, https_redirect=https_redirect, year=year)

    # Count sales
    sales = requests.get('https://reg.woodburn.au/api?action=getMyStaked', headers={'Authorization': 'Bearer ' + os.getenv('reg_auth')})
    sales = sales.json()
    if 'data' not in sales:
        if tld.startswith('xn--'):
            tld = tld.encode('ascii').decode('idna')
        return render_template('index.html', tld=tld, https_redirect=https_redirect, sales=0, year=year)

    tld_sales = 0
    sales = sales['data']
    for sale in sales:
        if sale['tld'] == tld:
            tld_sales = sale['slds']

    if tld.startswith('xn--'):
        tld = tld.encode('ascii').decode('idna')

    if tld_sales == 0:
        not_for_sale.append(tld)
        return render_template('not_for_sale.html', tld=tld, https_redirect=https_redirect, year=year)

    return render_template('index.html', tld=tld, https_redirect=https_redirect, sales=tld_sales, year=year)

# 404 catch all
@app.errorhandler(404)
def not_found(e):
    host = request.headers.get('host')
    tld = host.split('.')[-1]
    tld = tld.split(':')[0]
    if tld == 'localhost' or tld == '1':
        tld = 'example'
    return render_template('404.html', tld=tld), 404

if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0')