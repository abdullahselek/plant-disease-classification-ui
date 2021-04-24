#!/usr/bin/env python

import os
import json
import requests
import streamlit as st
import torch
import utils

from typing import List, Tuple
from session_state import SessionState
from plant_disease_classifier import PlantDiseaseClassifier


### Streamlit code (works as a straigtht-forward script) ###
st.title("Welcome to Plant Classification 🌱 📸")
st.header("Identify what's in your plant photos!")


@st.cache(suppress_st_warning=True)
def make_classification(image_data: bytes, model: str) -> Tuple:
    """Makes classification from given image and trained PyTorch model.
    Args:
      image (str):
        File path of image that is used for classification.
      model (str):
        Model file path.
    Returns:
      image, pred_class (Tuple):
        Predicted class.
    """

    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(dir_path, "models", model)
    if os.path.exists(path):
        plant_disease_classifier = PlantDiseaseClassifier(model_path=path)
        pred_class = plant_disease_classifier.classify(image_data=image_data)
        return image_data, pred_class
    else:
        print("Model file does not exist!")
        None


# Pick the model version
choose_model = st.sidebar.selectbox(
    label="Pick model you'd like to use, for now only one model available",
    options=["Model 1 (38 plant classes)"]
)

# set classes and model
CLASSES = utils.classes_and_models["model_1"]["classes"]
MODEL = utils.classes_and_models["model_1"]["model_name"]


# Display info about model and classes
if st.checkbox("Show classes"):
    st.write(f"You chose {MODEL}, these are the classes of plants it can identify:\n", CLASSES)


# File uploader allows user to add their own image
uploaded_file = st.file_uploader(label="Upload an image of plant",
                                 type=["png", "jpeg", "jpg"])


# Setup session state to remember state of app so refresh isn't always needed
# See: https://discuss.streamlit.io/t/the-button-inside-a-button-seems-to-reset-the-whole-app-why/1051/11 
session_state = SessionState.get(classify_button=False)


# Create logic for app flow
if not uploaded_file:
    st.warning("Please upload an image.")
    st.stop()
else:
    session_state.uploaded_image = uploaded_file.read()
    st.image(session_state.uploaded_image, use_column_width=True)
    classify_button = st.button("Classify")


# Did the user press the classify button?
if classify_button:
    session_state.classify_button = True 


# And if they did...
if session_state.classify_button:
    session_state.image, session_state.pred_class = make_classification(image_data=session_state.uploaded_image, model=MODEL)
    st.write(f"Prediction: {session_state.pred_class}")

    # Create feedback mechanism (building a data flywheel)
    session_state.feedback = st.selectbox(
        "Is this correct?",
        ("Select an option", "Yes", "No"))
    if session_state.feedback == "Select an option":
        pass
    elif session_state.feedback == "Yes":
        st.write("Thank you for your feedback!")
        # Log prediction information to terminal (this could be stored in Big Query or something...)
        print(utils.update_logger(image=session_state.image,
                                  model_used=MODEL,
                                  pred_class=session_state.pred_class,
                                  correct=True))
    elif session_state.feedback == "No":
        session_state.correct_class = st.text_input("What should the correct label be?")
        if session_state.correct_class:
            st.write("Thank you for that, we'll use your help to make our model better!")
            # Log prediction information to terminal (this could be stored in Big Query or something...)
            print(utils.update_logger(image=session_state.image,
                                      model_used=MODEL,
                                      pred_class=session_state.pred_class,
                                      correct=False,
                                      user_label=session_state.correct_class))
