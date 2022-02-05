# GraphQL
A package designed to wrap data-providing functions in 
[Strawberry](https://strawberry.rocks/) schema for GraphQL use.

## Structure
This package is divided into modules named after the different sections
(i.e. stocks, options, forex, and crypto.) This division keeps functions
organized (since the names of some functions are reused for different
sections) and helps minimize individual file size. Furthermore,
this organization system results in user requests being less confusing to
make (see GraphiQL using 
[app.py](https://github.com/anuj-p/Anuj-Patel-Quant-OA/blob/graphql-polygon-api/graphql-polygon-api/app.py) 
to better visualize how this is helpful.)

## Expansion
Functions from new APIs can easily be added to this package by 
1. defining the output of the functions as strawberry.type classes in 
"structs.py",
2. creating strawberry.field methods to convert the output of the functions,
3. placing the methods into their relevant sections (i.e. stocks, options, 
forex, and crypto.)