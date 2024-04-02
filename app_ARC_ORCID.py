
"""
Created on Mon Mar 25 11:15:29 2024

@author: Chun
"""

import streamlit as st

from rms_chun import rms_ci_query


import warnings
warnings.filterwarnings("ignore")
# @st.cache_data
# def get_data(name):
#      return rms_ci_query(name)
# @st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index = False).encode('utf-8')

st.set_page_config(page_title="ARC Funding History Finder",layout='wide')




st.title("ARC Grants History")
st.sidebar.title(":pencil: Settings")
form = st.sidebar.form(key='settings_form')

# test_orcid_or_name = form.selectbox("Input ORCID or Name", ['0000-0002-0802-9567', "Wenguan Wang", "Xiaojun Chang"], 0)
test_orcid_or_name = form.text_input("Input ORCID/Name, or anything", '0000-0002-0802-9567')

submit_button = form.form_submit_button(label='Submit')
col_side_0, col_side_1 = st.sidebar.columns([1,2])
col_side_0.write('RKIT©2024')
col_side_1.write("chun.xiao@uts.edu.au")

st.write("---")


df_grants = rms_ci_query(test_orcid_or_name)

columns_long_text = ['national-interest-test-statement', 'grant-summary']
df_summary = df_grants[['code'] + columns_long_text].copy()
cols_to_show = [item for item  in df_grants.columns if item not in columns_long_text]

if df_grants.shape[0] > 0:
    st.table(df_grants[cols_to_show])
    
    csv = convert_df(df_grants)
    col_0, col_1 = st.columns([5,1])
    col_1.download_button(
        label="Download table",
        data=csv,
        file_name="ARC_grants_history_{}.csv".format(test_orcid_or_name),
        mime='text/csv',
    )
    st.write("---")
    st.table(df_summary)

else:
    st.write('Nothing found in ARC database')
    
