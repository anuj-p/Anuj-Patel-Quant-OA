"""
The purpose of this package is to facilitate the process of making
requests to Polygon's API, obtaining JSON data, and handling errors.

This package is divided into modules named after the different sections of
Polygon's API (i.e. stocks, options, forex, and crypto.) This division keeps
functions organized (since the names of some of Polygon's endpoints are
reused for different sections) and helps minimize individual file size.

This package could be replaced by Polygon's official Python client
(https://github.com/polygon-io/client-python). However, the official client
does not seem to be well maintained and lacks some features (i.e. entire
options section.) Furthermore, a custom client is better equipped to handle
errors and send readable results through GraphQL.

This package will be able to make requests to 14 market data endpoints
through 14 functions. The endpoints included will work with a free tier
Polygon API key. It did not make sense to include any premium tier endpoints
as I cannot personally test them and, therefore, cannot test the results.
That being said, new endpoints (i.e. premium tier endpoints or reference
data endpoints) can easily be added.

THIS WILL NOT PREVENT FLASK IMPLEMENTATION! However, since this package is
effectively independent, it should be installed as a regular package. This
will prevent problems with the 'graphql_wrapper' package, which currently
expects 'polygon_client' to be explained by whatever module is running it.
The best solution for this is probably Poetry (https://python-poetry.org/).
As a result, the current directory organization is very strict.
"""

# This is my API key. It will remain accessible for a while, but will need
# to be replaced.
KEY = "6mK2FCpgpyFWpbGn4O2DiGuSMlcTGc48"