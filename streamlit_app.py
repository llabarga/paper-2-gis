import streamlit as st

st.title("Paper2GIS demo")
st.write("Sube una imagen y conviértela en shapefile")

uploaded = st.file_uploader("Sube una foto", type=["jpg", "png"])

if uploaded:
    st.image(uploaded)
    st.success("Imagen recibida 🚀")