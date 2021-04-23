import requests
import pandas as pd
import plotly.express as px
from loguru import logger
from sklearn.manifold import TSNE
from scipy.spatial import distance
import numpy as np

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
        logger.info(df.shape)
        df.rename(columns={
            'person_name':'Name',
            'person_email':'Email',
            'count':'Count',
            'wa':'WA',
            'org':'Org'
            },inplace=True)
        logger.info(f'\n{df.head()}')
        return df[['Name','Email','Count','Org','WA','m_sent_num','q_sent_num','q_sent_text','output','scores','m_sent_text']]
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

def api_vector(text:str,method:str='sent'):
    logger.debug(f'api_vector {text} {method}')
    endpoint = "/vector/"
    url = f"{API_URL}{endpoint}"
    params = {
        "query": text,
        "method": method
    }
    r = requests.get(url, params=params)
    return r.json()["res"]
    #df = (
    #    pd.json_normalize(r.json()["res"])
    #)
    #return df

def plotly_scatter_plot(df,top=12):
    df = df[(df['org_count']>top) | (df['origin']=='query')]
    fig = px.scatter(
        df, 
        x="x", 
        y="y", 
        color="org-name",
        symbol="org-name",
        hover_data=['email']
        )
    fig.update_layout(legend_title_text=f'Organisation (>{top} people)')
    return fig

def run_tsne(query:str='data science'):
    PEOPLE_PAIRS = 'data/people_vector_pairs.pkl.gz'
    TSNE_DF = 'data/tsne.pkl.gz'

    # read in pair-pair data 
    pp_df=pd.read_pickle(PEOPLE_PAIRS)

    # read in pre-calculated tsne data
    summary_df = pd.read_pickle(TSNE_DF)
    summary_df['origin']='people'
    logger.info(f'\n{summary_df.head()}')

    # get vectors for query
    vec_res = api_vector(text=query)
    
    # parse vector query results
    vec_list=[]
    sent_list = []
    vec_data = []
    for v in vec_res:
        vec_list.append(v['vector'])
        sent_list.append(v['q_sent_text'])

        # add some more info to new data
        vec_data.append({
            'origin':'query',
            'x':0,
            'y':0,
            'org-name':'query',
            'email':v['q_sent_text']
        })

    logger.info(vec_data)
    # create two lists of vectors to run cosine on
    v1 = vec_list
    v2 = list(summary_df['vector'])
    v2_text = list(summary_df['email'])
    logger.info(f'{np.array(v1).shape} {np.array(v2).shape}')
    aaa = distance.cdist(v1, v2, 'cosine')


    # parse cosine data 
    new_data = []
    vcount=0
    for v in vec_res:
        for i in range(len(aaa[vcount])):
            new_data.append({
                'email1':v['q_sent_text'],
                'email2':v2_text[i],
                'score':1-aaa[vcount][i]
            }),
            new_data.append({
                'email2':v['q_sent_text'],
                'email1':v2_text[i],
                'score':1-aaa[vcount][i]
            }),
        vcount+=1
    #logger.info(new_data)
    # cosine distance for each query against query
    for i in range(len(vec_res)):
        for j in range(len(vec_res)):
            cos = distance.cosine(vec_res[i]['vector'],vec_res[j]['vector'])
            logger.info(f'{i} {j} {1-cos}')
            new_data.append({
                    'email1':vec_res[i]['q_sent_text'],
                    'email2':vec_res[j]['q_sent_text'],
                    'score':1-cos
                }),

    # create new df with cosine results and add to pairwise df
    new_df = pd.DataFrame(new_data)
    pp_df = pd.concat([pp_df, new_df])
    
    tSNE=TSNE(n_components=2)

    # add query data to summary_df
    vec_df = pd.DataFrame(vec_data)
    #vec_df['email']=vec_df['org-name']
    # add to existing
    summary_df = pd.concat([summary_df,vec_df])
    #sort by email to match up with pivot table
    summary_df = summary_df.sort_values(by='email')

    # this filtering is due to some email addresses dropping out with org filter in aaa.py
    email_check = list(summary_df['email']) + sent_list
    pp_df = pp_df[(pp_df['email1'].isin(email_check)) & (pp_df['email2'].isin(email_check))]

    pp_df_pivot = pp_df.pivot(index='email1', columns='email2', values='score')
    pp_df_pivot = pp_df_pivot.fillna(1)
    tSNE_result=tSNE.fit_transform(pp_df_pivot)
    x=tSNE_result[:,0]
    y=tSNE_result[:,1]

    summary_df['x']=x
    summary_df['y']=y

    #summary_df.drop_duplicates(inplace=True)
    org_counts = summary_df['org-name'].value_counts()

    # filter df to top X for plot
    summary_df['org_count']= summary_df['org-name'].map(org_counts)
    summary_df['org-name'] = summary_df['org-name'].astype(str)+' '+summary_df['org_count'].astype(str)

    logger.info(f'\n{org_counts}')
    logger.info(f'\n{summary_df}')

    fig = plotly_scatter_plot(summary_df)
    return fig

