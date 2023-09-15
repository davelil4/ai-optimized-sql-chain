from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("form.html")

@app.route('/result')
def result():
    query = request.args.get('query')
    # Use the 'query' parameter to display or process the result
    return f'Result for query: {query}'
