
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from utils import convert_age_to_category, convert_test_indication_to_category, convert_symptoms_to_dataframe, convert_temperature_to_categories, TestImgPreprocessing
from models import predict_symptoms_outcome, predict_covid_with_Xray
from decisions import optional_recommendations_when_positive_outcome, decision_for_covid_dual_model, decision_for_normal_dual_model, decision_for_Pneumonia_dual_model
from PIL import Image

 # this section generates the sidebar   
navigation = st.sidebar.radio('contents', ('main app', 'about'))

st.sidebar.write('app designed by Tosin D. Oyewale (Ph.D)')
st.sidebar.write('Linkedin - https://www.linkedin.com/in/tosin-oyewale/')
st.sidebar.write('email- tosinoyewale@yahoo.co.uk')


if navigation == 'main app':  
    st.image('END_COVID.jpeg')
    st.title("ohteedee's COVID-diagnosing application")
    st.write("This application predicts status of covid of users' using symptoms and/or chest X-ray as input" )
    st.write("It is useful especially when there is no access to PCR test")
  
  
    # let the user decide what inpute type they want to use- symptoms, xray or both
    st.subheader('what input would you like to use to diagnose COVID-19?')
    input_method = st.radio('select input methods. both symptoms and chest Xray is recommended for highest accuracy', ('none','I want to provide only symptoms', 'I want to use only chest Xray', 'I prefer using both symptoms and chest Xray'))
    if input_method != 'none':
        if input_method == 'I want to provide only symptoms':
            st.subheader('Tell me some of the syptoms you have')
            
            form = st.form(key='my-form')
            # I am collecting users input data for symptoms 
            cough = form.selectbox('Are you coughing now or in the last five days?', ('yes', 'no'))
            fever = form.number_input('What is your body temperature in Celcius?', min_value=33.0, max_value=42.0, step=0.1, value=37.0)
            sore_throat = form.selectbox('do you have sore throat now or in the last five days?', ('yes', 'no'))
            shortness_of_breath = form.selectbox('do you have some difficulties breathing now or in the last five days?', ('yes', 'no'))
            head_ache = form.selectbox('are you experiencing headache now or in the last five days?', ('yes', 'no'))
            # age = int(st.text_input('How old are you?'))
            test_indication = form.selectbox('`which of these situations is applicable to you`', 
            ('I had contact with someone that tested positive for COVID-19', 
            'I traveled abroad to a region with high COVID incidence', 
            'both of the above', 
            'none of the above'))
            form.subheader('optional inputs')
            age = form.number_input('How old are you?', min_value=16, max_value=150,  step=1, value=45)
            
            # codition = form.selectbox('Do you have other underlying medical conditions?', ('no','yes'))
            serious_underlying_condition = False
            condition1 = form.radio('other undelying condition?', 
                ('I would keep this to myself','Diabetes', 'lung disease', 'heart or cardivascular disease',
                'cancer', 'kidney disease' 
                ))
            if condition1 != 'I would keep this to myself':
                serious_underlying_condition = True
            submit = form.form_submit_button(label= "predict my COVID-19 status")
            
            if submit:
                fever = convert_temperature_to_categories(fever)
                age_60_and_above = convert_age_to_category(age)
                test_indication = convert_test_indication_to_category(test_indication)
                # I will then convert users data into dataframe that the model can use to predict
                dataframe = convert_symptoms_to_dataframe(cough, fever, sore_throat, shortness_of_breath, head_ache,
                    age_60_and_above, test_indication)
                # st.write('dataframe generated by user', dataframe)
                probability, symptoms_outcome = predict_symptoms_outcome(dataframe)
                covid_pobability= probability[0][2]
                covid_pobability_percent = covid_pobability * 100
                covid_pobability_percent = round(covid_pobability_percent, 0)
                st.markdown(f"<h3 style='text-align: left; color: blue;'>Based on your symptoms, you have {covid_pobability_percent} percent probability that you are positive for COVID-19</h3>", unsafe_allow_html=True)
                optional_recommendations_when_positive_outcome(symptoms_outcome,serious_underlying_condition,age)

        

        elif input_method == 'I want to use only chest Xray':

            st.subheader('prediction with chest Xray')

            form = st.form(key='my-form')
            uploaded_file = form.file_uploader("please upload a jpeg image of your chest Xray", type="jpeg")
            form.subheader('optional inputs')
            age = form.number_input('How old are you?', min_value=16, max_value=150,  step=1, value=45)
            serious_underlying_condition = False
            condition1 = form.radio('other undelying condition?', 
                ('I would keep this to myself','Diabetes', 'lung disease', 'heart or cardivascular disease',
                'cancer', 'kidney disease' 
                ))
            if condition1 != 'I would keep this to myself':
                serious_underlying_condition = True
            submit = form.form_submit_button(label= "predict my COVID-19 status")

            if submit:
                if uploaded_file is None:
                    st.subheader('you need to provide image input!')
                else:
                    image = Image.open(uploaded_file)
                    processed_image = TestImgPreprocessing(image)
                    Xray_prediction = predict_covid_with_Xray(processed_image)
                    if Xray_prediction[2] == max(Xray_prediction):
                        percent_prob = round((Xray_prediction[2]*100), 1)
                        # st.subheader(f'based on your check Xray, there is {percent_prob} percent probability you have COVID-19')
                        st.markdown(f"<h3 style='text-align: left; color: blue;'>Based on your chest Xray, there is {percent_prob} percent probability you have COVID-19</h3>", unsafe_allow_html=True)
                    elif Xray_prediction[1] == max(Xray_prediction):
                        percent_prob = round((Xray_prediction[1]*100), 1)
                        # st.subheader(f'based on your check Xray, there is {percent_prob} percent probability you have you do not have COVID-19')
                        st.markdown(f"<h3 style='text-align: left; color: blue;'>Based on your chest Xray, there is {percent_prob} percent probability you have you do not have COVID-19</h3>", unsafe_allow_html=True)
                    else:
                        percent_prob = round((Xray_prediction[0]*100), 1)
                        # st.subheader(f'based on your check Xray, there is {percent_prob} percent probability you have you have Pneumonia')
                        st.markdown(f"<h3 style='text-align: left; color: blue;'>Based on your chest Xray, there is {percent_prob} percent probability you have you have Pneumonia</h3>", unsafe_allow_html=True)
                    st.subheader(f'The below graph shows the other possibilities')
                    fig, ax = plt.subplots()
                    ax = sns.barplot( x = ['Pneumonia', 'Normal', 'Covid'], y=Xray_prediction)
                    sns.despine()
                    plt.ylabel('probability')
                    st.pyplot(fig)

                    if Xray_prediction[2] == max(Xray_prediction):
                        Xray_outcome = 'positive'
                        # age, serious_underlying_condition = ask_for_recommendation(Xray_outcome)
                        optional_recommendations_when_positive_outcome(Xray_outcome,serious_underlying_condition,age)
                    elif Xray_prediction[0] == max(Xray_prediction):
                        st.subheader('Pneumonia is also a serious condition, here are some recommendations for you')
                        st.write('if you have difficulty breathing, chest pain, persistent fever of 39 Celcius or higher, or persistent cough, especially if you are coughing up pus, See your GP')
                        
                    


        elif input_method == 'I prefer using both symptoms and chest Xray':
            st.subheader('prediction with both chest Xray and symptoms')
            form = st.form(key='my-form')
            uploaded_file = form.file_uploader("please upload a jpeg image of your chest Xray and provide information about your symptoms", type="jpeg")
            # I am collecting users input data for symptoms 
            cough = form.selectbox('Are you coughing now or in the last five days?', ('yes', 'no'))
            fever = form.number_input('What is your body temperature in Celcius?', min_value=33.0, max_value=42.0, step=0.1, value=37.0)
            sore_throat = form.selectbox('do you have sore throat now or in the last five days?', ('yes', 'no'))
            shortness_of_breath = form.selectbox('do you some difficulties breathing now or in the last five days?', ('yes', 'no'))
            head_ache = form.selectbox('are you experiencing headache now or in the last five days?', ('yes', 'no'))
            # age = int(st.text_input('How old are you?'))
            test_indication = form.selectbox('`which of these situations is applicable to you`', 
            ('I had contact with someone that tested positive for COVID-19', 
            'I traveled abroad to a region with high COVID incidence', 
            'both of the above', 
            'none of the above'))

            form.subheader('optional inputs')
            age = form.number_input('How old are you?', min_value=16, max_value=150,  step=1, value=45)
            
            # codition = form.selectbox('Do you have other underlying medical conditions?', ('no','yes'))
            serious_underlying_condition = False
            condition1 = form.radio('other undelying condition?', 
                ('I would keep this to myself','Diabetes', 'lung disease', 'heart or cardivascular disease',
                'cancer', 'kidney disease' 
                ))
            if condition1 != 'I would keep this to myself':
                serious_underlying_condition = True
            submit = form.form_submit_button(label= "predict my COVID-19 status")
        
            if submit:
                if uploaded_file is None:
                    st.subheader('you need to provide image input!')
                else:
                    image = Image.open(uploaded_file)
                    processed_image = TestImgPreprocessing(image)
                    Xray_prediction = predict_covid_with_Xray(processed_image)
                    fever = convert_temperature_to_categories(fever)
                    age_60_and_above = convert_age_to_category(age)
                    test_indication = convert_test_indication_to_category(test_indication)
                    # I will then convert users data into dataframe that the model can use to predict
                    dataframe = convert_symptoms_to_dataframe(cough, fever, sore_throat, shortness_of_breath, head_ache,
                    age_60_and_above, test_indication)
                        # st.write('dataframe generated by user', dataframe)
                    symptoms_outcome = predict_symptoms_outcome(dataframe)
                    if Xray_prediction[2] == max(Xray_prediction):
                        decision_for_covid_dual_model(Xray_prediction, symptoms_outcome)
                        # age, serious_underlying_condition = ask_for_recommendation(symptoms_outcome)
                        optional_recommendations_when_positive_outcome(symptoms_outcome,serious_underlying_condition,age)
                    elif Xray_prediction[1] == max(Xray_prediction):
                        decision_for_normal_dual_model(symptoms_outcome)
                        # age, serious_underlying_condition = ask_for_recommendation(symptoms_outcome)
                        optional_recommendations_when_positive_outcome(symptoms_outcome,serious_underlying_condition,age)
                    elif Xray_prediction[0] == max(Xray_prediction):
                        decision_for_Pneumonia_dual_model(Xray_prediction, symptoms_outcome)
                        # age, serious_underlying_condition = ask_for_recommendation(symptoms_outcome)
                        optional_recommendations_when_positive_outcome(symptoms_outcome,serious_underlying_condition,age)
    st.write("Disclaimer- this application was designed as a proof of concept. To diagnose COVID-19, please contact your doctor")

elif navigation == 'about':

    '## General information'
    'The application is based on two datasets; first is based on covid-19 symptoms and the second is based on chest xray'

    'Both were used to generate classification models. symptoms model is based on random forest classification algorithm while the chest xray dataset was used to generate a model based on convolutional neural network'

    '## Information about datasets'

    '### symptoms dataset'

    '- COVID-19 symptoms dataset is publicly available from government of Israel. The dataset is translated into english and discussed here: https://www.nature.com/articles/s41746-020-00372-6 and https://github.com/nshomron/covidpred'
    '- over 3 million patients were tested'
    '- features - headache, sore throat, age above 60, shortness of breath, fever, cough, test indication'
    '- label - test outcome'

    ' ### chest Xray dataset'
    '-  dataset used has three classes: **Normal**, **COVID-19**, and **Pneumonia**'
    '-  dataset downloaded from https://www.kaggle.com/pranavraikokte/covid19-image-dataset'

    '## Model perfomance' 
    'For symptoms model which is based on random forest, the training, cross validation and the test accuracy is 92%'
    'For the chest Xray model based on convoluted neural network, the training accuracy is 96% and validation accuracy is 92%'


#     st.markdown('#### COVID-19 symptoms dataset is publicly available from government of Israel')
#     st.write(' ')
#     st.markdown(""" - ##### dataset translated into english and discussed here: https://www.nature.com/articles/s41746-020-00372-6 and https://github.com/nshomron/covidpred
# - ##### over 3 million patients were tested 
# - ##### dataset contains: headache, sore throat, age above 60, shortness of breath, fever, cough, test indication, test outcome 
# """)

#     st.markdown('#### COVID-19 chest Xray images are available on Kaggle')
#     st.markdown(""" -  ##### dataset used has three classes: **Normal**, **COVID-19**, and **Pneumonia**
# - ##### dataset downloaded from https://www.kaggle.com/pranavraikokte/covid19-image-dataset
#     """)