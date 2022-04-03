from typing import List
import pandas as pd

class DataLoadError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

def load_quotes_data(period: str) -> pd.DataFrame:
    ''' 
        Loads the quote information for a given period (YYYYMM) from CVM.
    
        RETURNS
        pd.DataFrame
    '''
    filename = f'inf_diario_fi_{period}.csv'
    url = f'http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/{filename}'
    # url = 'inf_diario_fi_202202.csv'
    cols = [
        'CNPJ_FUNDO',
        'DT_COMPTC',
        'VL_QUOTA',
        'VL_PATRIM_LIQ',
        'CAPTC_DIA',
        'RESG_DIA',
        'NR_COTST'
    ]
    try:
        print(f'--> Loading quotes data from file {url}')
        funds_quotes = pd.read_csv(url, delimiter=';', encoding='ISO-8859-1', dtype='str', usecols=cols)
        return funds_quotes
    except:
        print(f'Failed to load quotes data from the file {url}')
        raise DataLoadError(f'Failed to load quote data for the period {period}')

def filter_data(funds: pd.DataFrame, cnpjs: list) -> pd.DataFrame:
    '''
        Filters the data selecting only the rows that matches the CNPJs passed in the function argument

        RETURNS
        pd.DataFrame
    '''
    funds_info = funds.loc[funds['CNPJ'].isin(cnpjs), :]
    funds_info.reset_index(drop=True, inplace=True)

    return funds_info

def fix_columns(funds: pd.DataFrame) -> pd.DataFrame:
    '''
        Updates the column names in the pd.DataFrame based on the new_cols list.
        
        RETURNS
        pd.DataFrame
    '''
    new_cols = [
        'CNPJ',
        'DATA',
        'VALOR_QUOTA',
        'VALOR_PATRIMONIAL',
        'CAPTACAO_DIA',
        'RESGATE_DIA',
        'COTISTAS'
    ]

    funds.columns = new_cols

    return funds

def convert_to_dict(funds: pd.DataFrame) -> List:
    '''
        Converts the DataFrame to a dictionary
        The 'records' orientation is used so each row becomes a dictionary.

        RETURNS
            A list of dict
    '''
    funds_dict = funds.to_dict(orient='records')

    return funds_dict

def load_funds_quotes(cnpjs: List, period: str) -> List:
    df = load_quotes_data(period)
    df = fix_columns(df)
    df = filter_data(df, cnpjs)

    quotes = convert_to_dict(df)

    return quotes


if __name__ == '__main__':
    # Recebe um CNPJ e o periodo (YYYYMM)
    d = load_funds_quotes(['21.917.184/0001-29'], '202201')
    print(d)