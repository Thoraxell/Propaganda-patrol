from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import streamlit as st

@st.cache_resource
def create_lr_pipeline():
    lr_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english', max_df=0.7)),
        ('clf', LogisticRegression(random_state=0, max_iter=1000))  
    ])
    return lr_pipeline

@st.cache_data
def logistic_regression_algorithm(X_train, y_train, X_test=None):
    lr_pipeline = create_lr_pipeline()
    lr_pipeline.fit(X_train, y_train)
    if X_test is not None:
        lr_predictions = lr_pipeline.predict(X_test)
        return lr_pipeline, lr_predictions
    return lr_pipeline
