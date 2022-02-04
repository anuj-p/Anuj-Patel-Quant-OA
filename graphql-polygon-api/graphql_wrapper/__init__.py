"""
The purpose of this package is to turn API functions into valid GraphQL schema.

This package is divided into modules named after the different sections
(i.e. stocks, options, forex, and crypto.) This division keeps functions
organized (since the names of some functions are reused for different
sections) and helps minimize individual file size. Furthermore,
this organization system results in user requests being less confusing to
make (see GraphiQL using app.py to better visualize how this is helpful.)

Functions from new APIs can easily be added to this package by defining the
output of the functions as strawberry.type classes, creating
strawberry.field methods to convert the output of the functions, and placing
the new classes and functions in their relevant sections (i.e. stocks,
options, forex, and crypto.)
"""

