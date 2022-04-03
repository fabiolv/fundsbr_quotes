import re
from string import digits
from typing import List

class InvalidCNPJError(Exception):
    def __init__(self, msg) -> None:
        super().__init__(f'Invalid CNPJ: {msg}')

def validate_cnpj(cnpjs: list) -> list:
    symbols = '-./'
    regex = re.compile('^[0-9]{2}\.[0-9]{3}\.[0-9]{3}\/[0-9]{4}\-[0-9]{2}$')
    new_cnpjs = list()

    if not cnpjs:
        raise InvalidCNPJError(str(cnpjs))
    
    for cnpj in cnpjs:
        print(cnpj)
        for digit in cnpj:
            if digit not in symbols and digit not in digits:
                raise InvalidCNPJError(cnpj)
        
        if '-' not in cnpj and '/' not in cnpj and '-' not in cnpj:
            # Numeric CNPJ given, so converting...
            cnpj = f'{cnpj[0:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}'

        if not regex.match(cnpj):
            raise InvalidCNPJError(cnpj)
        
        new_cnpjs.append(cnpj)

    return new_cnpjs

def funds_exist(list_of_funds: List, existing_funds: List) -> List:
    '''Returns a list of error messages when fund is not in the pandas results'''
    messages = list()
    existing_cnpjs = [fund['CNPJ'] for fund in existing_funds]
    for fund in list_of_funds:
        if fund not in existing_cnpjs:
            messages.append(f'Fund with CNPJ {fund} not found in the registry')

    return messages


if __name__ == '__main__':
    pass