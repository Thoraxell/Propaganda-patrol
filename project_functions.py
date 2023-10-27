import streamlit as st
#from dotenv import load_dotenv
from data_preparation import data_loading
from text_functions import classify
from HtmlTemplate import css, bot_template, user_template
from chatbot_functions import get_text_chunks, get_vectorstore, get_conversation_chain, handle_userinput, get_pdf_text
from text_functions import extract_keywords
from text_functions import google_search
from text_functions import display_google_search_results
from chatbot_functions import load_pdfs_from_directory
from HtmlTemplate import css, bot_template, user_template
from text_functions import analyze_text
from text_functions import visualize_trends
 
def run_project1():
    st.caption("Disinformation news are more prominent than ever. To judge if a news article is true or disinformation, it is important to remain a well-informed and take a critical stance towards anything you read. PropagandaPatrol is a tool that assists you in assessing and judging the trustworthiness of your article, by:")
    st.caption("\U000022C5 detecting shocking language and persuasion techniques")
    st.caption("\U000022C5 using ML prediction models")
    st.caption("\U000022C5 by recognising if it's part of a bigger propaganda campaign, or triggered by significant events")
    st.caption("\U000022C5 suggesting further reading and similar articles to gain perspective")

    st.caption("If there's an article you need more insight on, paste it in below.")
 
    user_input = st.text_area("#### Analyse your article", "")
 
    if st.button("Analyse text"):
        if len(user_input) < 300:
            st.warning("Please enter at least 300 characters.")
        else:
            X, y = data_loading()  
            st.header("Results")
            st.write("Below are the results of some of those metrics to help you judge if the article text you pasted in is likely to be disinformation or not.")
            
            with st.expander ("Trend analysis", expanded=True):
                # Define the trigger words or get them dynamically
                trigger_words = ["Israel", "Hamas", "Ukraine", "Russia", "Palestine"]
                triggered_words = [word for word in trigger_words if word in user_input]
                if triggered_words:
                    visualize_trends(triggered_words)
                else:
                    st.write("No trigger words found in the input.")

            with st.expander("Emotion analysis", expanded=True):
                emotions_result, negative_sentences = analyze_text(user_input)
                if negative_sentences:
                    st.caption("Common techniques used in disinformation campaigns is to use negative, shocking, or persuasive tones. This is because our brains are more susceptible to negative news and that we give less space to information when we’re emotionally upset. From the text you pasted in, these sentences stand out as possibly containing such techniques:")
                    for sentence in negative_sentences:
                        st.markdown(f'<div class="sentence-box" style="border:0.5px solid #0E86D4; border-radius: 6px; padding:10px; margin:5px 0; color: #0E86D4;">{sentence}</div>', unsafe_allow_html=True)
                else:
                    st.write("No sentences with a persuasive or negative tone were found.")
        
            with st.expander ("ML Analysis (Logistic Regression)", expanded=True):
                classify(X, y, user_input)
        
            with st.expander ("Related articles", expanded=True):
                st.caption("Disinformation is a deliberate attempt to spread false information and is often propagated through coordinated campaigns. To assess the credibility of a piece of information and determine whether it might be disinformation, it's important to cross-reference it with multiple reputable sources on the same topic.")
                keywords = extract_keywords(user_input)
                search_results = google_search(keywords)
                display_google_search_results(search_results)
            
    
def run_project2():
    #load_dotenv()
    st.write(css, unsafe_allow_html=True)
 
        # Session state needs to be initialized
    if 'conversation' not in st.session_state:
            st.session_state.conversation = None
    if 'chat_history' not in st.session_state:
            st.session_state.chat_history = None 
    if 'button_clicked' not in st.session_state:  
            st.session_state.button_clicked = False  
 
    st.header("Learn more about FIMI")
 
    
    st.write("Do you have questions about FIMI and EU regulations?")
    pdf_files = load_pdfs_from_directory()
    if st.button("Click here to start the chatbot"):
        with st.spinner("Loading"):
            
            raw_text = get_pdf_text(pdf_files)
            text_chunks = get_text_chunks(raw_text)
            vectorstore = get_vectorstore(text_chunks)

            st.session_state.conversation = get_conversation_chain(vectorstore)
            st.session_state.button_clicked = True  
 
        # Only render the text input and chat if button_clicked is True
    if st.session_state.button_clicked:
            user_question = st.text_input("Ask your question")
            if user_question:
                handle_userinput(user_question)
 
def run_project3():
 
    st.header("What is Propaganda Patrol?")
    st.caption("""
    Propaganda Patrol has been created and designed to be an educational augmentation tool, 
    to help users identify an article as disinformation. Using machine learning classifiers, 
    linguistic analysis, and by looking at bigger search trends, we hope these metrics can 
    assist users in making more educated judgements about the news articles they come across.
    """)
 
    st.subheader("About")
    st.caption("""
    This project was created as a part of the Master’s Program in Human-Centered Artificial 
    Intelligence at the University of Gothenburg, in collaboration with RISE. The course was an 
    introduction to Human-Centered AI, dealing with topics such as bias, ethics, and designing 
    AI applications for human needs.
    """)
 
    st.subheader("Our Team")
    team_members = [
        {"name": "Hugo Anderson", "contact": "hugo.andersson@live.se"},
        {"name": "Thor Axell", "contact": "Thor.axell0@gmail.com"},
        {"name": "Arabel Maloney", "contact": "arabel.maloney@gmail.com"},
        {"name": "Wendy Zhou", "contact": "wendyzhou.design@gmail.com"},
    ]
    for member in team_members:
        st.write(f"{member['name']} - Contact @ {member['contact']}")
        
    
    

    
