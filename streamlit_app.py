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
support = st.slider("Enter the Support Value", min_value=0.1, max_value=0.9, value=0.15)
confidence = st.slider(
    "Enter the Confidence Value", min_value=0.1, max_value=0.9, value=0.6
)

inFile = dataFromFile(default_username)

items, rules = runApriori(inFile, support, confidence)

i, r = to_str_results(items, rules)

st.markdown("## Results")

st.markdown("### Frequent Itemsets")
st.write(i)

st.markdown("### Frequent Rules")
st.write(r)
