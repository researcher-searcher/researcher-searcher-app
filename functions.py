import requests
import pandas as pd

API_URL = "https://bdsn-api.mrcieu.ac.uk"

def api_search(text:str,method:str='full'):
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
        return df[['person_name','count','org','wa']]
    else:
        return df

def api_person(text:str,top:int=100):
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
    print(df.shape)
    return df


def api_collab(text:str,method:str='no'):
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
    print(df.shape)
    if not df.empty:
        df['org'] = df['org'].str[:1]
        df['score'] = df['score'].round(4)
        return df[['name','org','score']]
    else:
        return df
    return df

