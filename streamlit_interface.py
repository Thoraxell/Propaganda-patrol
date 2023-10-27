import streamlit as st
import pandas as pd
from sklearn.metrics import classification_report

def display_results(model_result, col, y_test):
    col.header(model_result["title"])
    col.write(f"Accuracy: {model_result['accuracy']:.2f}")
    report_df = pd.DataFrame.from_dict(
        classification_report(y_test, model_result['predictions'], output_dict=True)
    ).transpose()
    col.table(report_df)
 # In streamlit_interface.py

def display_classification(model_result, col):
    col.header(model_result["title"])
    col.write(f"Prediction on new article: {model_result['prediction']}")
