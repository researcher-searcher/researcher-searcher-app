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
    df.rename(columns={'text':'Text','score':'TF-IDF Score'},inplace=True)
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


