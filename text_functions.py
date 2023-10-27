import streamlit as st  
from logistic_regression_model import logistic_regression_algorithm
import yake
from googlesearch import search
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from HtmlTemplate import css, bot_template, user_template
from nrclex import NRCLex
from pytrends.request import TrendReq
import datetime
import altair as alt
from nrclex import NRCLex
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')    
nltk.download('punkt')
analyzer = SentimentIntensityAnalyzer()
 
def classify(X, y, user_input):
    lr_pipeline = logistic_regression_algorithm(X, y)
    lr_result = {
        "title": "Logistic Regression \n Results:",
        "prediction": "The text is most likely TRUE." if lr_pipeline.predict([user_input])[0] == 0 else "The text is most likely MISINFORMATION. " 
    }
 
    st.columns(1)
 
    lr_content = f"""
        <div style='border:2px solid #333; border-radius:5px; padding: 5px; color: #0E86D4; margin: 5px;'>
            <p>Prediction: {lr_result['prediction']}</p>
        </div>
    """

    st.caption("Keep in mind that machine learning models are never certain, it is merely a prediction. Below you can find the prediction made by our model. To learn more about our classifiers, see the “FIMI & EU Regulations” tab.")
    st.markdown(lr_content, unsafe_allow_html=True)

def extract_keywords(text):
    language = "en"
    max_ngram_size = 3
    deduplication_thresold = 0.9
    deduplication_algo = 'seqm'
    windowSize = 1
    numOfKeywords = 20
 
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords)
    keywords = custom_kw_extractor.extract_keywords(text)
    return [kw[0] for kw in keywords]
 
def google_search(keywords):
    query = " ".join(keywords)
    search_results = search(query, num_results=5)
    return search_results
 
def display_google_search_results(results):
 
    html_content = f"""
        <div style='padding:10px; margin:5px 0px;'>
            {''.join([f'<p>• <a href="{result}" target="_blank">{result}</a></p>' for result in results])}
        </div>
    """
 
    st.markdown(html_content, unsafe_allow_html=True)
 

def analyze_text(text):
    sentences = nltk.sent_tokenize(text)
    negative_sentences = []

    for sentence in sentences:
        sentiment = analyzer.polarity_scores(sentence)
        if sentiment['neg'] > 0.3:
            negative_sentences.append(sentence)

    # Analyzing with NRCLex
    emotions = NRCLex(text)

    # Return both emotions and negative sentences
    return emotions, negative_sentences
 
# Function to visualize Google Trends data
def visualize_trends(triggered_words):
    pytrend = TrendReq()
    end_date = datetime.datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.datetime.now() - datetime.timedelta(days=90)).strftime('%Y-%m-%d')
    timeframe = f"{start_date} {end_date}"
    pytrend.build_payload(kw_list=triggered_words, timeframe=timeframe)
    interest_over_time_df = pytrend.interest_over_time()
    if 'isPartial' in interest_over_time_df.columns:
        interest_over_time_df.drop(columns=['isPartial'], inplace=True)
    interest_long = interest_over_time_df.reset_index().melt('date', var_name='keyword', value_name='value')
 
    # Check for sudden increases
    threshold = 20  # Define a threshold for a significant rate of change
    sudden_increase_keywords = []
    for keyword in triggered_words:
        interest_values = interest_over_time_df[keyword].values
        rate_of_change = [(interest_values[i] - interest_values[i-1]) for i in range(1, len(interest_values))]
        if any(change > threshold for change in rate_of_change):
            sudden_increase_keywords.append(keyword)
 
    sudden_increase_alert = None
    if sudden_increase_keywords:
        if len(sudden_increase_keywords) == 1:
            keywords_string = f"'{sudden_increase_keywords[0]}'"
        else:
            keywords_string = ", ".join([f"'{word}'" for word in sudden_increase_keywords[:-1]]) + f" and '{sudden_increase_keywords[-1]}'"
        st.warning(f"There has been a sudden increase in interest for {keywords_string} over the last 90 days. This is likely due to some significant event or situation. During events like these, people are eager for updates, and high demand can lead to rapid sharing of news that lack proper verification, are misunderstood, or based on emotional reactions. This increases the risk of news being fake, so be extra cautious, and verify the trustworthiness of your source.")
 
    # Plotting the data with Y-axis adjusted and date format modified
    chart = alt.Chart(interest_long).mark_line().encode(
        x=alt.X("date:T", title="Date", axis=alt.Axis(format="%d %b")),
        y=alt.Y("value:Q", title="Interest Over Time", scale=alt.Scale(domain=[1, 100])),
        color="keyword:N"
    ).properties(
        title="Google Trends Over Last 90 Days"
    )
    st.altair_chart(chart, use_container_width=True) 

    return chart, sudden_increase_alert

