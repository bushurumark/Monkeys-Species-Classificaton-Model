#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!pip install tensorflow


# In[2]:


#!pip install gdown


# In[3]:


import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import gdown
import os

# Direct download link of the model file from Google Drive
url = 'https://drive.google.com/uc?id=1ulzwaxgv_sU4VAGIy5EuxwWzcuvuRohn'

# Path to save the downloaded model file
model_path = 'model.h5'

# Download the model if it does not exist
if not os.path.exists(model_path):
    with st.spinner('Downloading model...'):
        gdown.download(url, model_path, quiet=False)

# Load the model
model = tf.keras.models.load_model(model_path)

# Define the species names
species_names = [
    "Mantled Howler",
    "Patas Monkey",
    "Bald Monkey",
    "Japanese Macaque",
    "Pygmy Marmoset",
    "White Headed Capuchin",
    "Silver Marmoset",
    "Common Squirrel Monkey",
    "Black Headed Night Monkey",
    "Nilgiri Langur"
]

# Define a function to preprocess the image
def preprocess_image(image):
    image = image.resize((64, 64))  # Adjust size to match model input (64x64)
    image = image.convert("RGB")  # Ensure image is in RGB mode
    image = np.array(image)
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    image = image / 255.0  # Normalize
    return image

# Define a function to make predictions
def predict(image):
    processed_image = preprocess_image(image)
    prediction = model.predict(processed_image)
    return prediction

# Custom CSS for background and other elements
st.markdown("""
    <style>
    .main {
        background-color: violet;
    }
    .title {
        color: red;
        font-family: 'Arial';
        text-align: center;
    }
    .uploader {
        text-align: center;
    }
    .prediction {
        font-size: 20px;
        color: #4CAF50;
        font-weight: bold;
        text-align: center;
    }
    .uploaded-image {
        display: block;
        margin-left: auto;
        margin-right: auto;
        border: 5px solid #ccc;
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit interface with custom styles
st.markdown('<h1 class="title">Monkeys Species Classification Model</h1>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True, output_format='JPEG', channels='RGB')
    st.write("")
    st.markdown('<div class="prediction">Classifying...</div>', unsafe_allow_html=True)
    
    # Make prediction
    prediction = predict(image)
    
    # Get the index of the highest probability
    predicted_index = np.argmax(prediction, axis=1)[0]
    
    # Get the corresponding species name
    predicted_species = species_names[predicted_index]
    
    # Display the prediction
    st.markdown(f'<div class="prediction">Prediction: {predicted_species}</div>', unsafe_allow_html=True)



# In[ ]:




