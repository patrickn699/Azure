from flask import Flask, request


app = Flask(__name__)


@app.route('/')
def home():
    return '<html><body><h1>This is the homepage</h1></body></html>'


@app.route('/name/<string:name>',methods = ['GET','POST'])
def name(name):
    if request.method == 'GET':
        return '<html><body><h1>Hello'+ ' ' +name+','+ ' ' + 'welcome to this demo!</h1></body></html>'