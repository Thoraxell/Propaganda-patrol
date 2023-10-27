from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
from data_preparation import data_loading
from logistic_regression_model import create_lr_pipeline
from naive_bayes_model import create_nb_pipeline
from sklearn.model_selection import train_test_split
from naive_bayes_model import train_and_evaluate_nb
from logistic_regression_model import logistic_regression_algorithm
from streamlit_interface import display_results
import streamlit as st
from sklearn.metrics import accuracy_score

def call_testing_buttons():
     

    
    if st.button("Compare classifiers"):
        X, y = data_loading()  
        test_classifiers(X, y)


    if st.button("Cross Evaluate"):
        perform_cross_evaluation()

def perform_cross_evaluation():
    st.write("Performing Cross Evaluation...")
    X, y = data_loading()
    models = [
        ('Naive Bayes', create_nb_pipeline()),
        ('Logistic Regression', create_lr_pipeline())
    ]
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)  # shuffle set to True, random_state specified
    for model_name, model in models:
        st.write(f"Evaluating {model_name}...")
        cv_results = cross_val_predict(model, X, y, cv=cv, method='predict')  
        avg_accuracy = (cv_results == y).mean()
        st.write(f"Average Accuracy: {avg_accuracy}")

        # Metrics for each split
        for i, (train_index, test_index) in enumerate(cv.split(X, y)):
            X_train, X_test = X.iloc[train_index], X.iloc[test_index]
            y_train, y_test = y.iloc[train_index], y.iloc[test_index]
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            accuracy = (predictions == y_test).mean()
            precision = precision_score(y_test, predictions, average='micro')
            recall = recall_score(y_test, predictions, average='micro')
            f1 = f1_score(y_test, predictions, average='micro')
            confusion = confusion_matrix(y_test, predictions)
            st.write(f"Split {i + 1} - Accuracy: {accuracy}, Precision: {precision}, Recall: {recall}, F1 Score: {f1}")
            st.write(f"Confusion Matrix:\n{confusion}")


def test_classifiers(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    nb_pipeline, nb_predictions = train_and_evaluate_nb(X_train, y_train, X_test)
    lr_pipeline, lr_predictions = logistic_regression_algorithm(X_train, y_train, X_test)
    nb_result = {
        "title": "Naive Bayes \n Results:",
        "accuracy": accuracy_score(y_test, nb_predictions),
        "predictions": nb_predictions,
    }
    lr_result = {
        "title": "Logistic Regression \n Results:",
        "accuracy": accuracy_score(y_test, lr_predictions),
        "predictions": lr_predictions,
    }
    col1, col2 = st.columns(2)
    display_results(nb_result, col1, y_test)
    display_results(lr_result, col2, y_test)
