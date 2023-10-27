from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import streamlit as st

def create_nb_pipeline():
    nb_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english', max_df=0.7)),
        ('clf', MultinomialNB())
    ])
    return nb_pipeline

def train_and_evaluate_nb(X_train, y_train, X_test=None):
    nb_pipeline = create_nb_pipeline()
    nb_pipeline.fit(X_train, y_train)
    if X_test is not None:
        nb_predictions = nb_pipeline.predict(X_test)
        return nb_pipeline, nb_predictions
    return nb_pipeline
