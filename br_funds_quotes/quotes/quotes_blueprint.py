from http import HTTPStatus
import re
from urllib.request import Request
from flask import Blueprint, Response, request, jsonify
from .quotes import get_latest_quote, quote_test, load_quotes

funds_quotes_blueprint = Blueprint('funds_quotes_blueprint', __name__)

@funds_quotes_blueprint.route('/quotes/<cnpj>/', methods=['GET'])
def route_quotes_get(cnpj: str) -> Response:
    #TODO: make it do something, like return the all/latest quotes for the fund
    return get_latest_quote(cnpj)

    return jsonify({
        'msg': '¯\_(ツ)_/¯'
    })

def quotes_get():
    return jsonify({
        'msg': 'Usage: /quotes/<CNPJ>',
    })

def quotes_post(request: Request) -> Response:
    '''
    Loads the quote data for the funds in the request for the period given.
    POST requests are expected to pass a payload in the format below:
    {
        "period": "202203",
        "cnpjs": [
            "26.673.556/0001-32",
            "21.917.184/0001-02",
            "22.041.150/0001-86"
        ]
    }
    '''
    print(request.get_json())

    try:
        period = request.get_json()['period']
        cnpjs = request.get_json()['cnpjs']
    except (KeyError, TypeError):
        resp = jsonify({
            'msg': 'Payload must have period=str and cnpjs=List keys',
            'error': True,
            'data': request.get_json()
        })
        resp.status_code = HTTPStatus.BAD_REQUEST
        return resp

    print(f'--> Received the POST request for {period} and the CNPJs {cnpjs}')
    resp = load_quotes(cnpjs, period)
    return resp

@funds_quotes_blueprint.route('/quotes/', methods=['GET', 'POST'])
def route_quotes_root():
    if request.method == 'GET':
        print(f'--> /quotes route got a GET request:{request.method}')
        return quotes_get()
    
    if request.method == 'POST':
        print(f'--> /quotes route got a POST request: {request.method}')
        return quotes_post(request)
