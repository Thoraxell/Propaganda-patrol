import streamlit as st
from project_functions import run_project1, run_project2, run_project3
from test_models import call_testing_buttons

# Set up the page
st.set_page_config(page_title="FIMI Detection & Information", page_icon=":books:")

def main():
    image = "logo.png" 

    st.sidebar.image(image, use_column_width=True)
    st.sidebar.title("Propaganda Patrol")
    st.sidebar.subheader("We help you identify disinformation")
    st.sidebar.caption("Disinformation from foreign entities are being spread across the world, and we've created this application to help you learn more about it. You can also use our analyzer to get predictions about if a news article you've found is likely to be disinformation or not.")
    
    st.header("Welcome!")
    
    tabs = st.tabs(["Analyse article", "FIMI & EU Regulations", "About"])  

    with tabs[0]:  # Content for "Analyse article" tab 
        run_project1()
    
    with tabs[1]:  # Content for "Learn more" tab
        run_project2_content()
   
    with tabs[2]:  # Content for "Learn more" tab
        run_project3()
    

def run_project2_content():
    st.subheader("What is FIMI?")
    st.caption("Foreign Information Manipulation and Interference (FIMI) describes a mostly non-legal pattern of behavior in the information space that raises or has the potential to negatively impact values, procedures and political processes. Such activity is manipulative in character, conducted in an intentional and coordinated manner, often in relation to other hybrid activities.")
    st.caption("In order to detect, combat, and deal with misinformation, as well as protect citizens in a digital world, EU has enforced regulations such as GDPR, the AI Act, the Cybersecurity Act, and others.")
    run_project2()

    st.subheader("About disinformation detection")
    st.caption("It's challenging to detect disinformation, since it's about the authors intent. Something can be false, without the intent to manipulate or negatively impact others (called misinformation). So, to detect disinformation one has to take into account multiple points of analysis, for example by combining detection of persuasion techniques in linguistics, data analysis with machine learning classifiers, and look at the bigger picture to identify disinformation campaigns.")
    
    st.subheader("What is persuasion techniques?")
    st.caption("Persuasion techniques are used to influence people's opinions, and can be detected through text analysis, either manual or using machine learning techniques.")
    
    st.subheader("Reflection on the choice of model")
    st.caption("There are many machine learning models to choose from, and research has been done on machine learning classifier performance relating to different tasks. Based on prior research on the detection of fake news, logistic regression was chosen as a primary alternative as it has the highest accuracy, which was also found in our own comparison. Another classifier that was considered was Naïve Bayes since it is a suitable classifier for the dataset used. You can make the same comparison by clicking on the “Testing tools” button below and choosing which method you want to know more about.")
    if st.button("Compare models"):
        st.session_state['show_testing_buttons'] = True

    if st.session_state.get('show_testing_buttons', False):
        st.caption("Assess our classifier's accuracy by contrasting it with other models, or perform cross evaluation on the dataset to ascertain its robustness. ")
        call_testing_buttons()

    st.subheader("How to detect disinformation campaigns?")
    st.caption("To detect disinformation campaigns, one has to look at the bigger picture. Some relevant aspects can be: Who is the author? Where is the source? What does this text, video, or image convey?")
    




if __name__ == "__main__":
    main()
