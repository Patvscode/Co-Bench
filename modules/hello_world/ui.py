import streamlit as st

def render():
    st.subheader("👋 Hello, World!")
    st.write("This is a minimal example module loaded dynamically.")
    if st.button("Say hi again"):
        st.success("Hi again!")
