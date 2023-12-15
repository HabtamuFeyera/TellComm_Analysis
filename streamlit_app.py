import streamlit as st

st.title('wel come to streamlit')

st.write("""
         
# Explore mlops
I select the best one here
         
""")
mydataset = st.sidebar.selectbox("Select Dataset",("Iris","Breast cancer","winne dataset"))
st.write(mydataset)