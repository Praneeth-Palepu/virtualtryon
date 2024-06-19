import streamlit as st
from PIL import Image
import os
from gradio_client import Client, file

st.set_page_config(page_title="Fashion Tryon", layout="wide")

# Title of the app
st.title("Virtual Change Room...")

banner = """
<style>
    header {visibility: hidden;}
    .css-18ni7ap.e8zbici2 {visibility: hidden;}
</style>
"""
st.markdown(banner, unsafe_allow_html=True)


# Instructions
st.write("Upload the base image of the person and the garment to try")

# Upload two images
uploaded_image1 = st.file_uploader("Model's image", type=["jpg", "jpeg", "png"])
default_working_directory = os.getcwd()
if uploaded_image1:
    model_image_path = os.path.join(default_working_directory, uploaded_image1.name)
    with open(model_image_path, "wb") as f:
        f.write(uploaded_image1.getbuffer())
    model_image_size = Image.open(model_image_path).size
uploaded_image2 = st.file_uploader("Garment image", type=["jpg", "jpeg", "png"])
if uploaded_image2:
    garment_image_path = os.path.join(default_working_directory, uploaded_image2.name)
    with open(garment_image_path, "wb") as f:
        f.write(uploaded_image2.getbuffer())

# Initialize a variable to store the selected image path
selected_image_path = None

# Display image placeholders and save uploaded images
if uploaded_image1 and uploaded_image2:
    col1, col2, col3 = st.columns(3)

    image1_path, image2_path = '', ''

    with col1:
        if uploaded_image1:
            st.image(Image.open(model_image_path), caption="First Image", use_column_width=True)

    with col2:
        if uploaded_image2:
            st.image(Image.open(garment_image_path), caption="Second Image", use_column_width=True)

    with col3:
        client = Client("yisol/IDM-VTON")
        result = client.predict(
                dict={"background":file(model_image_path)},
                garm_img=file(garment_image_path),
                garment_des="Hello!!",
                is_checked=True,
                is_checked_crop=False,
                denoise_steps=25,
                seed=42,
                api_name="/tryon"
        )
        st.image(Image.open(result[0]).resize(model_image_size), caption='Swapped Garment', use_column_width=True)
