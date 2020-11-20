import streamlit as st
import pandas as pd
from apriori import runApriori, dataFromFile, to_str_results

st.markdown("# Apriori Streamlit")

st.sidebar.markdown(
    """The code attempts to implement the following paper:

> *Agrawal, Rakesh, and Ramakrishnan Srikant. "Fast algorithms for mining association rules." Proc. 20th int. conf. very large data bases, VLDB. Vol. 1215. 1994.*
"""
)

default_username = st.selectbox(
    "Select one of the sample csv files", ("INTEGRATED-DATASET.csv", "tesco.csv")
)

csv_file = pd.read_csv(default_username, header=None, sep="\n")
st.write(csv_file[0].str.split("\,", expand=True).head())

st.markdown("## Inputs")

st.markdown('''
            **Support** shows transactions with items purchased together in a single transaction.
            
            **Confidence** shows transactions where the items are purchased one after the other.''')

st.markdown('Support and Confidence for Itemsets A and B can be represented by formulas')

st.markdown(' > Support(A) = (Number of transactions in which A appears)/(Total Number of Transactions')
st.markdown(' > Confidence(A->B) = Support(AUB)/Support(A)')
st.markdown('---')

support = st.slider("Enter the Minimum Support Value", min_value=0.1, max_value=0.9, value=0.15)
confidence = st.slider(
    "Enter the Minimum Confidence Value", min_value=0.1, max_value=0.9, value=0.6
)

inFile = dataFromFile(default_username)

items, rules = runApriori(inFile, support, confidence)

i, r = to_str_results(items, rules)

st.markdown("## Results")

st.markdown("### Frequent Itemsets")
st.write(i)

st.markdown("### Frequent Rules")
st.write(r)
