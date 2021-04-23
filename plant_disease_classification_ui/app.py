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
