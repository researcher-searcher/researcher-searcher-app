import requests
import pandas as pd
from loguru import logger

API_URL = "https://bdsn-api.mrcieu.ac.uk"

def api_search(text:str,method:str='full'):
    logger.debug(f'api_search {text} {method}')
    endpoint = "/search/"
    url = f"{API_URL}{endpoint}"
    params = {
        "query": text,
        "method": method
    }
    r = requests.get(url, params=params)
    df = (
        pd.json_normalize(r.json()["res"])
    )
    if not df.empty:
        df['org'] = df['org'].str[:1]
        print(df.shape)
        df.rename(columns={
            'person_name':'Name',
            'person_email':'Email',
            'count':'Count',
            'wa':'WA',
            'org':'Org'
            },inplace=True)
        return df[['Name','Email','Count','Org','WA']]
    else:
        return df

def api_search_person(text:str):
    logger.debug(f'api_search_person {text}')
    endpoint = "/search/"
    url = f"{API_URL}{endpoint}"
    params = {
        "query": text,
        "method": 'person'
    }
    r = requests.get(url, params=params)
    df = (
        pd.json_normalize(r.json()["res"])
    )
    if not df.empty:
        df['org'] = df['org'].str[:1]
        df['score'] = df['score'].round(4)
        logger.debug(df.shape)
        logger.debug(f'\n{df.head()}')
        df.rename(columns={
            'name':'Name',
            'email':'Email',
            'score':'Score',
            'org':'Org'
            },inplace=True)
        return df[['Name','Email','Org','Score']]
    else:
        return df

def api_search_output(text:str):
    logger.debug(f'api_search_output {text}')
    endpoint = "/search/"
    url = f"{API_URL}{endpoint}"
    params = {
        "query": text,
        "method": 'output'
    }
    r = requests.get(url, params=params)
    df = (
        pd.json_normalize(r.json()["res"])
    )
    if not df.empty:
        logger.debug(df.shape)
        df['score'] = df['score'].round(4)
        df['title'] = df['title']
        df.rename(columns={
            'title':'Title',
            'year':'Year',
            'score':'Score',
        },inplace=True)
        logger.debug(df.columns)
        return df[['Title','Year','Score']]
    else:
        return df

def api_person(text:str,top:int=100):
    logger.debug(f'api_person {text} {top}')
    endpoint = "/person/"
    url = f"{API_URL}{endpoint}"
    params = {
        "query": text,
        "limit": top
    }
    r = requests.get(url, params=params)
    df = (
        pd.json_normalize(r.json()["res"])
    )
    df['score'] = df['score'].round(4)
    df.rename(columns={'text':'Text','score':'TF-IDF Score'},inplace=True)
    print(df.shape)
    return df


def api_collab(text:str,method:str='no'):
    logger.debug(f'api_collab {text} {method}')
    endpoint = "/collab/"
    url = f"{API_URL}{endpoint}"
    params = {
        "query": text,
        "method": method
    }
    r = requests.get(url, params=params)
    df = (
        pd.json_normalize(r.json()["res"])
    )
    res = df
    if not df.empty:
        df['org'] = df['org'].str[:1]
        df['score'] = df['score'].round(4)
        df.rename(columns={
            'org':'Org',
            'name':'Name',
            'email':'Email',
            'score':'Score'
            }
            ,inplace=True
        )

        print(df.shape)
        return df[['Name','Email','Org','Score']]
    else:
        return df


