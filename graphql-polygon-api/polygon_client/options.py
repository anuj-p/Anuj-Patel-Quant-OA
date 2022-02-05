"""
This module contains functions for Polygon's Options API (see https://polygon.io/docs/options).
"""

from json import JSONDecodeError, loads
from polygon_client import KEY
from requests import get, RequestException


def get_aggregates(ticker: str, expiration: str, call: bool, strike: float, multiplier: int, timespan: str, from_: str, to: str, adjusted: bool = True, ascending: bool = True, limit: int = 5000) -> dict:
    """
    :param ticker: ticker symbol of the underlying stock (case-sensitive)
    :param expiration: expiration date of the option (YYYY-MM-DD)
    :param call: whether or not the option is a call (otherwise it is a put)
    :param strike: strike price of the option
    :param multiplier: size of the timespan multiplier
    :param timespan: size of the time window ('minute'/'hour'/'day'/'week'/'month'/'quarter'/'year')
    :param from_: starting date of the aggregate time window (YYYY-MM-DD)
    :param to: ending date of the aggregate time window (YYYY-MM-DD)
    :param adjusted: whether or not the results are adjusted for splits
    :param ascending: whether or not the results should be sorted by timestamp ascending (otherwise descending)
    :param limit: maximum number of base aggregates queried to create the aggregate results (<= 50000)
    :return: aggregate bars for an option over a given date range in custom time window sizes
    """

    # initial input validation
    if ticker == "":
        raise ValueError("'ticker' should be non-empty.")
    if "/" in ticker:
        raise ValueError("'ticker' should not include '/'.")
    if expiration == "":
        raise ValueError("'expiration' date should be non-empty.")
    if "/" in expiration:
        raise ValueError("'expiration' date should not include '/'.")
    if "-" not in expiration:
        raise ValueError("'expiration' date should be of format 'YYYY-MM-DD'.")
    if expiration[:2] != "20":
        raise ValueError("'expiration' date should be in the 21st century.")
    if strike < 0:
        raise ValueError("'strike' price should be greater than $0.")
    if strike > 99999.999:
        raise ValueError("'strike' price should be less than $99999.999.")
    if from_ == "":
        raise ValueError("'from_' date should be non-empty.")
    if "/" in from_:
        raise ValueError("'from_' date should not include '/'.")
    if "-" not in from_:
        raise ValueError("'from_' date should be of format 'YYYY-MM-DD'.")
    if to == "":
        raise ValueError("'to' date should be non-empty.")
    if "/" in to:
        raise ValueError("'to' date should not include '/'.")
    if "-" not in to:
        raise ValueError("'to' date should be of format 'YYYY-MM-DD'.")
    if multiplier < 1:
        raise ValueError("Timespan 'multiplier' should be at least 1.")
    possible_timespans = ["minute", "hour", "day", "week", "month", "quarter", "year"]
    if timespan not in possible_timespans:
        raise ValueError("'timespan' should be 'minute', 'hour', 'day', 'week', 'month', 'quarter', or 'year'.")
    if limit < 1:
        raise ValueError("'limit' should be at least 1.")
    if limit > 50000:
        raise ValueError("'limit' should be no more than 50000.")

    # input morphing
    expiration = expiration[2:].replace("-", "")
    strike = str(int(strike * 1000)).zfill(8)
    if call:
        ticker = f"O:{ticker}{expiration}C{strike}"
    else:
        ticker = f"O:{ticker}{expiration}P{strike}"
    if ascending:
        sort = "asc"
    else:
        sort = "desc"

    # request
    endpoint = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from_}/{to}?adjusted={adjusted}&sort={sort}&limit={limit}&apiKey={KEY}"
    try:
        response = get(endpoint)
    except RequestException:
        raise RequestException(f"Error connecting to endpoint ({endpoint}).")
    try:
        data = loads(response.text)
    except JSONDecodeError:
        raise RequestException(f"Unexpected non-JSON response from endpoint ({endpoint}).")

    # output validation
    if data["status"] == "ERROR":
        if data["error"] == "The parameter 'to' cannot be a time that occurs before 'from'":
            raise ValueError("'to' should be a date that occurs after 'from_'.")
        elif data["error"] == "Could not parse the time parameter: 'to'. Use YYYY-MM-DD or Unix MS Timestamps":
            raise ValueError("'to' should be of format 'YYYY-MM-DD'.")
        elif data["error"] == "Could not parse the time parameter: 'from'. Use YYYY-MM-DD or Unix MS Timestamps":
            raise ValueError("'from_' should be of format 'YYYY-MM-DD'.")
    if data["status"] != "OK":
        if "message" in data:
            raise Exception(f"Something went wrong. Unknown {data['status']} status received from endpoint ({endpoint}). Received message: {data['message']}.")
        elif "error" in data:
            raise Exception(f"Something went wrong. Unknown {data['status']} status received from endpoint ({endpoint}). Received error: {data['error']}.")
        else:
            raise Exception(f"Something went wrong. Unknown {data['status']} status received from endpoint ({endpoint}).")
    if data["resultsCount"] == 0:
        raise ValueError(f"Data not found for {ticker} from {from_} to {to} within {limit} {timespan} query limit. Perhaps specified option is incorrect, the market was not open in that date range, or 'limit' is too small.")

    return data


def get_daily_open_close(ticker: str, expiration: str, call: bool, strike: float, date: str, adjusted: bool = True) -> dict:
    """
    :param ticker: ticker symbol of the underlying stock (case-sensitive)
    :param expiration: expiration date of the option (YYYY-MM-DD)
    :param call: whether or not the option is a call (otherwise it is a put)
    :param strike: strike price of the option
    :param date: date of the requested open/close (YYYY-MM-DD)
    :param adjusted: whether or not the results are adjusted for splits
    :return: open prices, close prices, afterhours prices, and more (see Polygon's API docs)
    """

    # initial input validation
    if ticker == "":
        raise ValueError("'ticker' should be non-empty.")
    if "/" in ticker:
        raise ValueError("'ticker' should not include '/'.")
    if expiration == "":
        raise ValueError("'expiration' date should be non-empty.")
    if "/" in expiration:
        raise ValueError("'expiration' date should not include '/'.")
    if "-" not in expiration:
        raise ValueError("'expiration' date should be of format 'YYYY-MM-DD'.")
    if expiration[:2] != "20":
        raise ValueError("'expiration' date should be in the 21st century.")
    if strike < 0:
        raise ValueError("'strike' price should be greater than $0.")
    if strike > 99999.999:
        raise ValueError("'strike' price should be less than $99999.999.")
    if date == "":
        raise ValueError("'date' should be non-empty.")
    if "/" in date:
        raise ValueError("'date' should not include '/'.")
    if "-" not in date:
        raise ValueError("'date' should be of format 'YYYY-MM-DD'.")

    # input morphing
    expiration = expiration[2:].replace("-", "")
    strike = str(int(strike * 1000)).zfill(8)
    if call:
        ticker = f"O:{ticker}{expiration}C{strike}"
    else:
        ticker = f"O:{ticker}{expiration}P{strike}"

    # request
    endpoint = f"https://api.polygon.io/v1/open-close/{ticker}/{date}?adjusted={adjusted}&apiKey={KEY}"
    try:
        response = get(endpoint)
    except RequestException:
        raise RequestException(f"Error connecting to endpoint ({endpoint}).")
    try:
        data = loads(response.text)
    except JSONDecodeError:
        raise RequestException(f"Unexpected non-JSON response from endpoint ({endpoint}).")

    # output validation
    if data["status"] == "ERROR":
        if data["error"] == "today's Date not supported yet":
            raise ValueError("'date' is not supported yet. Perhaps 'date' is in the future.")
        elif data["error"] == "could not parse from Date. use YYYY-MM-DD timestamps":
            raise ValueError("'date' should be of format 'YYYY-MM-DD'.")
        elif data["error"] == "Ticker was incorrectly formatted":
            raise ValueError("'ticker' was incorrectly formatted.")
        elif data["error"] == "You've exceeded the maximum requests per minute, please wait or upgrade your subscription to continue.":
            raise RequestException("Maximum requests per minute has been exceeded. Perhaps use a premium API key.")
    elif data["status"] == "NOT_FOUND":
        if data["message"] == "Data not found.":
            raise ValueError(f"Data not found for {ticker} on {date}. Perhaps 'ticker' is incorrect or the market was not open on 'date'.")
    if data["status"] != "OK":
        if "message" in data:
            raise Exception(f"Something went wrong. Unknown {data['status']} status received from endpoint ({endpoint}). Received message: {data['message']}.")
        elif "error" in data:
            raise Exception(f"Something went wrong. Unknown {data['status']} status received from endpoint ({endpoint}). Received error: {data['error']}.")
        else:
            raise Exception(f"Something went wrong. Unknown {data['status']} status received from endpoint ({endpoint}).")

    return data


def get_previous_close(ticker: str, expiration: str, call: bool, strike: float, adjusted: bool = True) -> dict:
    """
    :param ticker: ticker symbol of the underlying stock (case-sensitive)
    :param expiration: expiration date of the option (YYYY-MM-DD)
    :param call: whether or not the option is a call (otherwise it is a put)
    :param strike: strike price of the option
    :param adjusted: whether or not the results are adjusted for splits
    :return: previous day's open prices, high prices, low prices, close prices, and more (see Polygon's API docs)
    """

    # initial input validation
    if ticker == "":
        raise ValueError("'ticker' should be non-empty.")
    if "/" in ticker:
        raise ValueError("'ticker' should not include '/'.")
    if expiration == "":
        raise ValueError("'expiration' date should be non-empty.")
    if "/" in expiration:
        raise ValueError("'expiration' date should not include '/'.")
    if "-" not in expiration:
        raise ValueError("'expiration' date should be of format 'YYYY-MM-DD'.")
    if expiration[:2] != "20":
        raise ValueError("'expiration' date should be in the 21st century.")
    if strike < 0:
        raise ValueError("'strike' price should be greater than $0.")
    if strike > 99999.999:
        raise ValueError("'strike' price should be less than $99999.999.")

    # input morphing
    expiration = expiration[2:].replace("-", "")
    strike = str(int(strike * 1000)).zfill(8)
    if call:
        ticker = f"O:{ticker}{expiration}C{strike}"
    else:
        ticker = f"O:{ticker}{expiration}P{strike}"

    # request
    endpoint = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev?adjusted={adjusted}&apiKey={KEY}"
    try:
        response = get(endpoint)
    except RequestException:
        raise RequestException(f"Error connecting to endpoint ({endpoint}).")
    try:
        data = loads(response.text)
    except JSONDecodeError:
        raise RequestException(f"Unexpected non-JSON response from endpoint ({endpoint}).")

    # output validation
    if data["status"] == "ERROR":
        if data["error"] == "Ticker was incorrectly formatted":
            raise ValueError("'ticker' was incorrectly formatted.")
    if data["status"] != "OK":
        if "message" in data:
            raise Exception(f"Something went wrong. Unknown {data['status']} status received from endpoint ({endpoint}). Received message: {data['message']}.")
        elif "error" in data:
            raise Exception(f"Something went wrong. Unknown {data['status']} status received from endpoint ({endpoint}). Received error: {data['error']}.")
        else:
            raise Exception(f"Something went wrong. Unknown {data['status']} status received from endpoint ({endpoint}).")
    if data["resultsCount"] == 0:
        raise ValueError(f"Data not found for {ticker}. Perhaps 'ticker' is incorrect.")

    return data
