import streamlit as st
import pandas as pd
from apriori import runApriori, dataFromFile, to_str_results

st.markdown("# Apriori Streamlit")

st.sidebar.markdown(
    """The code attempts to implement the following paper:

> *Agrawal, Rakesh, and Ramakrishnan Srikant. "Fast algorithms for mining association rules." Proc. 20th int. conf. very large data bases, VLDB. Vol. 1215. 1994.*
"""
)

default_csv = st.selectbox(
    "Select one of the sample csv files", ("tesco.csv", "INTEGRATED-DATASET.csv")
)

if default_csv == 'INTEGRATED-DATASET.csv':
    st.markdown('''The dataset is a copy of the “Online directory of certified businesses with a detailed profile” file from the 
    Small Business Services (SBS) dataset in the NYC Open Data Sets http://nycopendata.socrata.com/''')
elif default_csv == 'tesco.csv':
    st.markdown('The dataset is a toy dataset contain frequently purchased grocery items')

st.markdown('Here are some sample rows from the dataset')
csv_file = pd.read_csv(default_csv, header=None, lineterminator="\n")
st.write(csv_file[0].str.split("\,", expand=True).head())

st.markdown('---')
st.markdown("## Inputs")

st.markdown('''
            **Support** shows transactions with items purchased together in a single transaction.
            
            **Confidence** shows transactions where the items are purchased one after the other.''')

st.markdown('Support and Confidence for Itemsets A and B can be represented by formulas')

support_helper = ''' > Support(A) = (Number of transactions in which A appears)/(Total Number of Transactions') '''
confidence_helper = ''' > Confidence(A->B) = Support(AUB)/Support(A)') '''
st.markdown('---')

support = st.slider("Enter the Minimum Support Value", min_value=0.1,
                    max_value=0.9, value=0.15,
                    help=support_helper)

confidence = st.slider("Enter the Minimum Confidence Value", min_value=0.1,
                       max_value=0.9, value=0.6, help=confidence_helper)

inFile = dataFromFile(default_csv)

items, rules = runApriori(inFile, support, confidence)

i, r = to_str_results(items, rules)

st.markdown("## Results")

st.markdown("### Frequent Itemsets")
st.write(i)

st.markdown("### Frequent Rules")
st.write(r)
