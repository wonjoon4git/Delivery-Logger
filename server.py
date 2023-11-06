
"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python3 server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, abort, jsonify

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)




# Create a database engine that knows how to connect to the URI.
DATABASEURI = "postgresql://wc2852:278599@34.74.171.121/proj1part2"
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
conn = engine.connect()

# conn.execute("""CREATE TABLE IF NOT EXISTS test (
#   id serial,
#   name text
# );""")
# conn.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
#
# see for routing: https://flask.palletsprojects.com/en/2.0.x/quickstart/?highlight=routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def login():
  return render_template("login.html")

@app.route('/main')
def index():
  return render_template("index.html")

#
# This is an example of a different path.  You can see it at:
#
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
# @app.route('/another')
# def another():
#   return render_template("another.html")

# Get the column labels of table
@app.route('/_get_columns')
def get_columns():
    table_name = request.args.get('selected_table', type=str)
    if not table_name:
        return jsonify(error='No table selected'), 400

    inspector = inspect(engine)
    try:
        # Get all column names for the selected table
        columns = inspector.get_columns(table_name)
        column_names = [column['name'] for column in columns]
    except Exception as e:
        return jsonify(error=str(e)), 500

    # Return the column names as a list
    return jsonify(column_names=column_names)

# @app.route('/select', methods=['POST'])
# def select():
#     table_name = request.form['table']
#     query = text(f"SELECT * FROM {table_name}")
#     try:
#       results = engine.execute(query).fetchall()
#       rows = [dict(row) for row in results]
#       return jsonify(rows=rows)
#     except Exception as e:
#       return str(e), 500

# Rendering the entire table for user's selection from "Select Table"
@app.route('/_get_table_data')
def get_table_data():
    table_name = request.args.get('table_name', '', type=str)
    query = text(f"SELECT * FROM {table_name}")
    results = engine.execute(query).fetchall()
    return render_template('partials/table_data.html', rows=results)


# Rendering the entire table for user's selection from "Select Table"
@app.route('/_get_column_data')
def get_column_data():
    table_name = request.args.get('table_name', '', type=str)
    column = request.args.get('column', '', type=str)
    view_type = request.args.get('view_type', '', type=str)

    if view_type == "attribute":
      query = text(f"SELECT {column} FROM {table_name}")
    else:
      query = text(f"SELECT * FROM {table_name}")
    
    results = engine.execute(query).fetchall()
    return render_template('partials/table_data.html', rows=results)

  
@app.route('/_get_constraint_data')
def get_constraint_data():
    table_name = request.args.get('table_name', '', type=str)
    column = request.args.get('column', '', type=str)
    keyword = request.args.get('keyword', '', type=str)
    search_type = request.args.get('search_type', '', type=str)
    view_type = request.args.get('view_type', '', type=str)

    if view_type == "attribute":
      view = column
    else:
      view = "*"
      
    # Determine the type of search
    if search_type == "exact":
      query = text(f"SELECT {view} FROM {table_name} WHERE {table_name}.{column} = \'{keyword}\'")
    elif search_type == "similar":
      query = text(f"SELECT {view} FROM {table_name} WHERE {table_name}.{column} LIKE \'%{keyword}%\'")
    elif search_type == "caseInsensitive":
      query = text(f"SELECT {view} FROM {table_name} WHERE {table_name}.{column} ILIKE \'%{keyword}%\'")

    results = engine.execute(query).fetchall()
    return render_template('partials/table_data.html', rows=results)
  
  
@app.route('/_get_range_data')
def get_range_data():
    table_name = request.args.get('table_name', '', type=str)
    column = request.args.get('column', '', type=str)
    range_start = request.args.get('range_start', '', type=str)
    range_end = request.args.get('range_end', '', type=str)
    order_by = request.args.get('order_by', 'asc', type=str)  # Default to ascending
    view_type = request.args.get('view_type', '', type=str)

    if view_type == "attribute":
      view = column
    else:
      view = "*"

    # Adjust query for range
    query = text(f"SELECT {view} FROM {table_name} WHERE {table_name}.{column} BETWEEN \'{range_start}\' AND \'{range_end}\' ORDER BY {column} {order_by.upper()}")

    results = engine.execute(query).fetchall()
    return render_template('partials/table_data.html', rows=results)

# @app.route('/filter1', methods=['POST'])
# def filter():


# @app.route('/login')
# def login():
#     abort(401)
#     this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python3 server.py

    Show the help text using:

        python3 server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=True, threaded=threaded)

  run()
