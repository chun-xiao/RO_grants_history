"""
Created on Mon Mar 25 16:09:44 2024

@author: Chun
"""
import requests
import json
import pandas as pd

def rms_ci_query(ci_name_or_id, current = False):
    page_size = 500
    if not current:
        query_url = f'''https://dataportal.arc.gov.au/NCGP/API/grants?page%5Bnumber%5D=1&page%5Bsize%5D={page_size}&filter=("{ci_name_or_id}")'''
    r = requests.get(query_url, allow_redirects=True)
    r_json = json.loads(r.text)
        
    ## without status filter here
    try:
        grants = []
        for each in r_json['data']: grants.append(each['attributes'])
        
        ##------page loops----------
        total_pages = r_json['meta']['total-pages']
        if total_pages > 1:
            for each_page in range(2, total_pages+1, 1):
                if not current:
                    query_url = f'''https://dataportal.arc.gov.au/NCGP/API/grants?page%5Bnumber%5D={each_page}&page%5Bsize%5D={page_size}&filter=("{ci_name_or_id}")'''
                r = requests.get(query_url, allow_redirects=True)
                r_json = json.loads(r.text)
                ##----- append grants
                for each in r_json['data']:  grants.append(each['attributes'])
        grants = pd.DataFrame.from_records(grants)
        for drop_col in ['grant-priorities', 'scheme-information', 'researcher_name']:
            if drop_col in grants.columns:
                grants = grants.drop(columns = [drop_col], axis =1)
    
        grants['searched_by'] = ci_name_or_id
        if not current:
            grants['searched_DB'] = 'NCGP'
    except:
        grants = pd.DataFrame()
    return grants

    
