# GraphQL Polygon API
A GraphQL/Polygon API created in Python for a UIUC Quant assessment. Comments 
are spread throughout files and explain practices, purpose, and expansion. 
Most of these comments are summarized in every README.md.

## Flask Implementation
To use the Flask implementation and access a GraphiQL view, open a Python 
Powershell prompt/regular PowerShell with Python setup for PATH and run the 
following commands from inside the repository.

`pip install strawberry-graphql`

`pip install flask`

`cd .\graphql-polygon-api\`

`$env:FLASK_APP = "app"`

`flask run`

Finally, open a browser and go to http://127.0.0.1:5000/.

NOTE: [Strawberry](https://strawberry.rocks/) allows for many possible 
implementations (see integrations in their 
[docs](https://strawberry.rocks/docs).) Flask is only used here as an example.


## Format
* Dates should be in the format of 'YYYY-MM-DD'.
* If the format of anything ever gets confusing, refer to relevant files in 
[graphql_wrapper](https://github.com/anuj-p/Anuj-Patel-Quant-OA/tree/graphql-polygon-api/graphql-polygon-api/graphql_wrapper) and/or the "Docs" section in GraphiQL.
