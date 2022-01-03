import streamlit as st





def optional_recommendations_when_positive_outcome(outcome,serious_underlying_condition,age):
    '''
    This function is executed when the prediction of model is positive for covid infection. 
    it makes recomendations based on being positive and two additional optional inputs; age and presence of other serious underlying condtions
    '''
    
    if outcome == 'positive' and age >= 60 and serious_underlying_condition == True:
        st.subheader('Based on your age and your medical profile, you are at high risk of severe COVID-19 infection!')
        st.subheader('please contact your general practitions for urgent advice')
    elif outcome == 'positive' and serious_underlying_condition == True:
        st.subheader('Based on your medical profile, you are at high risk of severe COVID-19 infection!')
        st.subheader('please contact your general practitional for urgent advice')
    elif outcome == 'positive' and age >= 60 :
        st.subheader('Based on your age, you are at high risk of severe COVID-19 infection!')
        st.subheader('please contact your general practitional for urgent advice')
    elif outcome == 'positive':
        st.subheader('Here are some recommendations for you')
        st.write('you are adviced to self quarantine for the next ten days')
        st.write('Have lots of rest and drink fluids to prevent dehydation')
        st.write('if headache persists, take over the counter pain medications such as paracetamol')
        # st.subheader('For more comprehensive report, please fill the optional inputs on the left sidebar')
        


def decision_for_covid_dual_model(Xray_outcome, outcome_symptoms):
    '''
    this function is useful when both models are to be used. 
    it helps to make decision when Xray model predicts covid and after symptoms is checked
    it takes the result of Xray model prediction and model based symptoms as input
    '''
    if outcome_symptoms == 'positive':
        # st.markdown(f"<h3 style='text-align: left; color: blue;'>Based on your chest Xray and your symptoms, with very high level of certainty, you are {outcome_symptoms[0]} for COVID-19</h3>", unsafe_allow_html=True)
        st.success(f" ###  Based on your chest Xray and your symptoms, with very high level of certainty, you are {outcome_symptoms[0]} for COVID-19")
    else:
        percent_prob = round((Xray_outcome[2]*100), 1)
        # st.markdown(f"<h3 style='text-align: left; color: blue;'>Although your chest Xray suggests {percent_prob} percent chance of COVID-19, your symptoms suggest otherwise</h3>", unsafe_allow_html=True)
        st.success(f" ###  Although your chest Xray suggests {percent_prob} percent chance of COVID-19, your symptoms suggest otherwise")
        # st.markdown(f"<h3 style='text-align: left; color: blue;'>Overall, with {percent_prob} percent chance, you may have COVID-19</h3>", unsafe_allow_html=True)
        st.success(f" ### Overall, with {percent_prob} percent chance, you may have COVID-19 ")


def decision_for_normal_dual_model(symptoms_outcome, confidence_prob):
    '''
    this function is useful when both models are to be used. 
    it helps to make decision when Xray model predicts normal and after symptoms is checked
    it takes the result of Xray model prediction and model based symptoms as input
    '''
    if symptoms_outcome == 'positive':
        # st.markdown(f"<h3 style='text-align: left; color: blue;'>your chest Xray suggests that your lungs are fine but your symptoms you are {symptoms_outcome[0]} for COVID-19; with {confidence_prob} percent confidence </h3>", unsafe_allow_html=True)
        st.success(f" ### your chest Xray suggests that your lungs are fine but your symptoms you are {symptoms_outcome[0]} for COVID-19; with {confidence_prob} percent confidence ")
    else:
        # st.markdown(f"<h3 style='text-align: left; color: blue;'>Based on your chest Xray and your symptoms, with very high level of certainty, you are {symptoms_outcome[0]} for COVID-19</h3>", unsafe_allow_html=True)
        st.success(f" ###  Based on your chest Xray and your symptoms, with very high level of certainty, you are {symptoms_outcome[0]} for COVID-19")


def decision_for_Pneumonia_dual_model(Xray_prediction, symptoms_outcome):
    '''
    this function is useful when both models are to be used. 
    After Xray model predicts covid, it helps to make decision when symptoms model is completed
    it takes the result of Xray model prediction and model based symptoms as input
    '''
    prob_covid = round((Xray_prediction[2]*100), 1)
    prob_pneumonia = round((Xray_prediction[0]*100), 1)
    if symptoms_outcome == 'positive':
        # st.markdown(f"<h3 style='text-align: left; color: blue;'>your Xray suggests that you have {prob_pneumonia} pecent possibility it is Pneumonia and {prob_covid} percent it is COVID-19 but you are {symptoms_outcome[0]} for COVID-19 based on symptoms</h3>", unsafe_allow_html=True)
        st.success(f" ### your Xray suggests that you have {prob_pneumonia} pecent possibility it is Pneumonia and {prob_covid} percent it is COVID-19 but you are {symptoms_outcome[0]} for COVID-19 based on symptoms ")
        # st.markdown(f"<h3 style='text-align: left; color: blue;'>Overall, with some degree of certainty, you may have COVID-19'</h3>", unsafe_allow_html=True)
        st.success(f" ### Overall, with some degree of certainty, you may have COVID-19")
    else:
        # st.markdown(f"<h3 style='text-align: left; color: blue;'>Based on you Xray and symptoms, you most likely have Pnemonia and not COVID-19</h3>", unsafe_allow_html=True)
        st.success(f" ###  Based on you Xray and symptoms, you most likely have Pnemonia and not COVID-19")
        # st.markdown(f"<h3 style='text-align: left; color: blue;'>The percent probabilities for COVID and Pneumonia are {prob_covid} and {prob_pneumonia}, respectively</h3>", unsafe_allow_html=True)
        st.success(f" ###  The percent probabilities for COVID and Pneumonia are {prob_covid} and {prob_pneumonia}, respectively")
        st.subheader('you still need to take this seriously')
        
# st.markdown(f"<h3 style='text-align: left; color: blue;'></h3>", unsafe_allow_html=True)


        
