import pandas as pd
from sklearn.model_selection import train_test_split
import streamlit as st
import os

def data_loading(split_data=False):
    # List of file names
    file_names = ['datasetp1.xlsx', 'datasetp2.xlsx', 'datasetp3.xlsx', 'datasetp4.xlsx', 'datasetp5.xlsx']
 
    # Read each file and append to a list
    data_frames = [pd.read_excel(file, engine='openpyxl') for file in file_names]
 
    # Concatenate all data frames into one
    data = pd.concat(data_frames, ignore_index=True)
 
    # Ensure all entries in the 'text' column are strings
    data['text'] = data['text'].apply(str)
 
    # Remove rows where 'text' column is blank
    data = data[~(data['text'].str.strip() == '')]
 
    # Remove rows where 'text' column is numeric
    data = data[~data['text'].str.isnumeric()]
 
    # Remove rows where 'label' column is blank
    data = data[~data['label'].isna()]
 
    # Remove rows where 'label' column is not a number
    data = data[data['label'].apply(lambda x: str(x).isnumeric())]
 
    # Convert the 'label' column to numeric
    data['label'] = pd.to_numeric(data['label'])
 
    X = data['text']
    y = data['label']
 
    if split_data:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
        return X_train, X_test, y_train, y_test
 
    return X, y  # Return X and y if no split is needed