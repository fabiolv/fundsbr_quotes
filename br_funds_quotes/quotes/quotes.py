from typing import List
from http import HTTPStatus
from flask import Response, jsonify
from br_funds_quotes.database import DB, DBParametersError
from br_funds_quotes.utils import InvalidCNPJError, validate_cnpj
from .quotes_data import load_funds_quotes, DataLoadError
from ..models.quote import Quote

def quote_test(cnpjs: List, period) -> Response:
    period = '202201'
    try:
        data = load_funds_quotes(cnpjs, period)
    except DataLoadError as err:
        resp = jsonify({
            'msg': str(err),
            'error': True,
            'data': period
        })
        resp.status_code = HTTPStatus.NOT_FOUND
        return resp

    return jsonify({'msg': data})

def quote_exists(cnpj: str, date: str) -> bool:
    quotes = Quote.objects(CNPJ=cnpj, DATA=date)
    if quotes:
        return True
    
    return False

def load_quotes(cnpjs: List, period: str) -> Response:
    # Open the DB connection
    try:
        db = DB()
    except:
        print('--> Could not connect to the DB')
        resp = jsonify({
            'msg': 'Could not connect to the DB',
            'error': True,
            'data': None
        })
        resp.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        return resp

    # Load the quotes from the CVM site
    try:
        data = load_funds_quotes(cnpjs, period)
    except DataLoadError as err:
        resp = jsonify({
            'msg': str(err),
            'error': True,
            'data': period
        })
        resp.status_code = HTTPStatus.NOT_FOUND
        return resp

    # With the results, save each *new* quote in the DB
    results = list()
    for record in data:
        quote = Quote(**record)
        if quote_exists(record['CNPJ'], record['DATA']):
            continue

        print(f'--> Saving quote: {record["CNPJ"]} for the date {record["DATA"]}')
        result = quote.save()
        result = result.to_mongo().to_dict()
        result['_id'] = str(result['_id'])
        results.append(result)

    resp = jsonify({
        'msg': f'Quotes saved to the DB',
        'records': len(results),
        'data': results
    })
    resp.status_code = HTTPStatus.CREATED
    return resp

def get_quotes(cnpj: str, from_date: str='1900-01-01', to_date: str='9999-12-31') -> List:
    try:
        db = DB()
    except DBParametersError:
        raise DBParametersError

    results = list()
    for quote in Quote.objects(CNPJ=cnpj, DATA__gte=from_date, DATA__lt=to_date).order_by('-DATA'):
        result = quote.to_mongo().to_dict()
        result['_id'] = str(result['_id'])
        results.append(result)

    return results

def get_latest_quote(cnpj: str) -> Response:
    '''
        Gets the latest quote for a given fund
    '''
    # Check if the CNPJ is valid
    try:
        cnpj = validate_cnpj([cnpj])[0]
    except InvalidCNPJError as err:
        print(f'--> Invalid CNPJ: {cnpj}')
        resp = jsonify({
            'msg': str(err),
            'error': True,
            'data': None
        })
        resp.status_code = HTTPStatus.BAD_REQUEST
        return resp

    try:
        results = get_quotes(cnpj)
    except DBParametersError:
        print('--> Could not connect to the DB')
        resp = jsonify({
            'msg': 'Could not connect to the DB',
            'error': True,
            'data': None
        })
        resp.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        return resp
    
    if not results:
        resp = jsonify({
            'msg': f'Could not find any quotes for the fund {cnpj}',
            'records': 0,
            'error': True,
            'data': None
        })
        resp.status_code = HTTPStatus.NOT_FOUND
        return resp

    resp = jsonify({
        'msg': f'Latest quote for the fund {cnpj}',
        'records': 1,
        'data': results[0]
    })
    return resp