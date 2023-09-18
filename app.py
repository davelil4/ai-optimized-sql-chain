from flask import Flask, render_template, request, redirect, url_for
import table_grab
import pg_help

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("form.html")

@app.route('/result')
def result():
    query = request.args.get('query')
    
    sql = table_grab.getSQL(query)
    
    sql = sql.split("```")[1]
    
    sql = sql.lstrip("SQL")
    sql = sql.lstrip("sql")
    
    print(sql)
    
    answer = pg_help.query(sql)
    
    # Use the 'query' parameter to display or process the result
    return f'Result for query: {answer}'
