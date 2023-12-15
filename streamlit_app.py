import streamlit as st
from sklearn import datasets

st.title('wel come to streamlit')

st.write("""
         
# Explore mlops
I select the best one here
         
""")
my_dataset = st.sidebar.selectbox("Select Dataset",("Iris","Breast Cancer","wine dataset"))
my_classifier = st.sidebar.selectbox("Select Classifier",("KNN","SVm","Random Forest"))

def get_dataset(my_dataset):
    if my_dataset == "Iris":
        data = datasets.load_iris()
    elif my_dataset == "Breast Cancer":
        data = datasets.load_breast_cancer()
    else:
        data = datasets.load_wine()

    x = data.data
    y = data.target
    return x,y

x,y = get_dataset(my_dataset)


