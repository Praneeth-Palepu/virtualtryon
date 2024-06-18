import streamlit as st
from PIL import Image
import os
import tempfile
from gradio_client import Client, file

st.set_page_config(page_title="Fashion Tryon", layout="wide")

# Title of the app
st.title("Virtual Change Room...")

hide_github_link = """
<style>
    .css-q16mip e10z71040 { 
        display: none; 
    }
</style>
"""
st.markdown(hide_github_link, unsafe_allow_html=True)


# Instructions
st.write("Upload the base image of the person and the garment to try")


# Function to save uploaded image to a temporary directory
def save_uploaded_file(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        return tmp_file.name


# Upload two images
uploaded_image1 = st.file_uploader("Model's image", type=["jpg", "jpeg", "png"])
uploaded_image2 = st.file_uploader("Garment image", type=["jpg", "jpeg", "png"])

# Initialize a variable to store the selected image path
selected_image_path = None

# Display image placeholders and save uploaded images
if uploaded_image1 and uploaded_image2:
    col1, col2 = st.columns(2)

    image1_path, image2_path = '', ''

    with col1:
        if uploaded_image1:
            # Save the first uploaded image
            image1_path = save_uploaded_file(uploaded_image1)
            st.image(image1_path, caption="First Image", use_column_width=True)
            if st.button('Select First Image'):
                selected_image_path = image1_path

    with col2:
        if uploaded_image2:
            # Save the second uploaded image
            image2_path = save_uploaded_file(uploaded_image2)
            st.image(image2_path, caption="Second Image", use_column_width=True)
            if st.button('Select Second Image'):
                selected_image_path = image2_path


    client = Client("yisol/IDM-VTON")
    result = client.predict(
            dict={"background":file(image1_path)},
            garm_img=file(image2_path),
            garment_des="Hello!!",
            is_checked=True,
            is_checked_crop=False,
            denoise_steps=30,
            seed=42,
            api_name="/tryon"
    )

    st.image(Image.open(result[0]), caption='Swapped Garment', use_column_width=True)
