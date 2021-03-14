#!/usr/bin/env python

import os
import json
import requests
import SessionState
import streamlit as st
import torch


### Streamlit code (works as a straigtht-forward script) ###
st.title("Welcome to Plant Classificastion 🌱 📸")
st.header("Identify what's in your plant photos!")
