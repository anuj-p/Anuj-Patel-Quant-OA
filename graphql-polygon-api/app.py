"""
This script acts as an EXAMPLE of an implementation of graphql_wrapper.
This implementation uses Flask. To use this implementation and access a
GraphiQL view, open a Python Powershell prompt/regular PowerShell with
Python setup for PATH and run the following commands from inside the
repository.

`pip install strawberry-graphql`
`pip install flask`
`cd .\graphql-polygon-api\`
`$env:FLASK_APP = "app"`
`flask run`

Finally, open a browser and go to `http://127.0.0.1:5000/`.
"""

from flask import Flask
from graphql_wrapper.schema import schema
from strawberry.flask.views import GraphQLView

app = Flask(__name__)

app.add_url_rule(
    "/",
    view_func=GraphQLView.as_view("graphql_view", schema=schema)
)
