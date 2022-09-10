Python Implementation of Apriori Algorithm 
==========================================

## Set up
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/asaini/apriori/python3) [![Build Status](https://travis-ci.org/asaini/Apriori.svg?branch=master)](https://travis-ci.org/asaini/Apriori) 

Edit without local environment setup

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/asaini/Apriori)


---

## Acknowledgements
The code attempts to implement the following paper:

> *Agrawal, Rakesh, and Ramakrishnan Srikant. "Fast algorithms for mining association rules." Proc. 20th int. conf. very large data bases, VLDB. Vol. 1215. 1994.*


----

Interactive Streamlit App
-------------
To view a live interactive app, and play with the input values, please click [here](https://share.streamlit.io/asaini/apriori/python3). This app was built using [Streamlit](https://www.streamlit.io) 😎, the source code for the app can be found [here](https://github.com/asaini/Apriori/blob/python3/streamlit_app.py)


Running the Streamlit app locally
-----
To run the interactive Streamlit app with dataset  

    $ pip3 install -r requirements.txt
    $ streamlit run streamlit_app.py


----

CLI Usage
-----
To run the program with dataset provided and default values for *minSupport* = 0.15 and *minConfidence* = 0.6

    python apriori.py -f INTEGRATED-DATASET.csv

To run program with dataset  

    python apriori.py -f INTEGRATED-DATASET.csv -s 0.17 -c 0.68

Best results are obtained for the following values of support and confidence:  

Support     : Between 0.1 and 0.2  

Confidence  : Between 0.5 and 0.7 

----

Datasets
-------------

#### INTEGRATED-DATASET.csv

The dataset is a copy of the “Online directory of certified businesses with a detailed profile” file from the Small Business Services (SBS) 
dataset in the `NYC Open Data Sets <http://nycopendata.socrata.com/>`_



#### tesco.csv

Toy dataset of items from shopping cart

----

License
-------
MIT-License

