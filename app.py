
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from processor.symptoms import ProcessSymptomsData
from processor.imagedata import ProcessImageData
from processor.decisions import optional_recommendations_when_positive_outcome, decision_for_covid_dual_model, decision_for_normal_dual_model, decision_for_Pneumonia_dual_model
from PIL import Image
import os

 # this section generates the sidebar   
navigation = st.sidebar.radio('contents', ('main app', 'about'))

st.sidebar.write('app designed by Tosin D. Oyewale (Ph.D)')
st.sidebar.write('Linkedin - https://www.linkedin.com/in/tosin-oyewale/')
st.sidebar.write('email- tosinoyewale@yahoo.co.uk')


if navigation == 'main app':  
    st.image('pictures/END_COVID.jpeg')
    st.title("Ohteedee's COVID-diagnosing application")
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
            cough1 = form.selectbox('Are you coughing now or in the last five days?', ('yes', 'no'))
            temperature1 = form.number_input('What is your body temperature in Celcius?', min_value=33.0, max_value=42.0, step=0.1, value=37.0)
            sore_throat1 = form.selectbox('do you have sore throat now or in the last five days?', ('yes', 'no'))
            shortness_of_breath1 = form.selectbox('do you have some difficulties breathing now or in the last five days?', ('yes', 'no'))
            head_ache1 = form.selectbox('are you experiencing headache now or in the last five days?', ('yes', 'no'))
            # age = int(st.text_input('How old are you?'))
            test_indication1 = form.selectbox('`which of these situations is applicable to you`', 
            ('I had contact with someone that tested positive for COVID-19', 
            'I traveled abroad to a region with high COVID incidence', 
            'both of the above', 
            'none of the above'))
            form.subheader('optional inputs')
            age1 = form.number_input('How old are you?', min_value=16, max_value=150,  step=1, value=45)
            
            # codition = form.selectbox('Do you have other underlying medical conditions?', ('no','yes'))
            serious_underlying_condition = False
            condition1 = form.radio('other undelying condition?', 
                ('none','Diabetes', 'lung disease', 'heart or cardivascular disease',
                'cancer', 'kidney disease' 
                ))
            if condition1 != 'none':
                serious_underlying_condition = True
            submit = form.form_submit_button(label= "predict my COVID-19 status")
            
            # process the input after submit by users. all funtions are imported from other files. generate outcome
            if submit:
                user_symptoms_input = ProcessSymptomsData(cough1, temperature1, sore_throat1, shortness_of_breath1, head_ache1, age1, test_indication1)
                fever = user_symptoms_input.convert_temperature_to_categories()
                age_60_and_above = user_symptoms_input.convert_age_to_category()
                test_indication = user_symptoms_input.convert_test_indication_to_category()
                # I will then convert users data into dataframe that the model can use to predict
                user_dataframe = user_symptoms_input.convert_symptoms_to_dataframe()
                # st.write('dataframe generated by user', dataframe)
                symptoms_outcome = user_symptoms_input.predict_symptoms_outcome()
                probability = user_symptoms_input.predict_probability()
                confidence_prob = round (max(probability[0]) * 100, 0)
                st.success(f" ### Based on your symptoms, with a confidence of {confidence_prob} percent, you are {symptoms_outcome[0]} for COVID-19")
                optional_recommendations_when_positive_outcome(symptoms_outcome,serious_underlying_condition,age1)
                
        
        

        
        # users can decide to use xray alone. in that case, they can upload their own image or use some samples 
        # note that the processing of the image is the same, well except that for sample images, i needed to provide the path using os.
        elif input_method == 'I want to use only chest Xray':

            st.subheader('prediction with chest Xray')
            option = st.radio('', ['upload your own XRay','use available sample images'])
            # if they decide to use their own 
            if option == 'upload your own XRay':
                form = st.form(key='my-form')
                uploaded_file = form.file_uploader("please upload image of your chest Xray", type="jpeg")
                form.warning('Model was trained with chest Xray images, and can only perform accurately with chest Xray images. Inputing any other kind of image will give unwanted results')
                form.subheader('optional inputs')
                age = form.number_input('How old are you?', min_value=16, max_value=150,  step=1, value=45)
                serious_underlying_condition = False
                condition1 = form.radio('other undelying condition?', 
                    ('none','Diabetes', 'lung disease', 'heart or cardivascular disease',
                    'cancer', 'kidney disease' 
                    ))
                if condition1 != 'none':
                    serious_underlying_condition = True
                submit = form.form_submit_button(label= "predict my COVID-19 status")

                if submit:
                    if uploaded_file is None:
                        st.error('you need to provide image input!')
                    else:
                    
                        image1 = Image.open(uploaded_file)
                        user_image_input1 = ProcessImageData(image1)
                        processed_image = user_image_input1.TestImgPreprocessing()
                        Xray_prediction = user_image_input1.predict_covid_with_Xray()
                        if Xray_prediction[2] == max(Xray_prediction):
                            percent_prob = round((Xray_prediction[2]*100), 1)
                            st.success(f" ### Based on your chest Xray,  you have COVID-19, confidence is {percent_prob} percent")
                            # st.markdown(f"<h3 style='text-align: left; color: blue;'>Based on your chest Xray,  you have COVID-19, confidence is {percent_prob} percent </h3>", unsafe_allow_html=True)
                        elif Xray_prediction[1] == max(Xray_prediction):
                            percent_prob_normal = round((Xray_prediction[1]*100), 1)
                            percent_prob_covid = round((Xray_prediction[2]*100), 1)
                            st.success(f" ### Based on your chest Xray, you are normal, confidence is {percent_prob_normal} percent")
                            # st.markdown(f"<h3 style='text-align: left; color: blue;'>Based on your chest Xray, you are normal, confidence is {percent_prob_normal} percent </h3>", unsafe_allow_html=True)
                        else:
                            percent_prob_Pneumonia = round((Xray_prediction[0]*100), 1)
                            percent_prob_covid = round((Xray_prediction[2]*100), 1)
                            st.success(f" ### Based on your chest Xray, you have Pneumonia, confidence is {percent_prob_Pneumonia} percent.")
                            st.success(f" ### The confidence that you have COVID-19 is {percent_prob_covid} percent ")
                         

                        if Xray_prediction[2] == max(Xray_prediction):
                            Xray_outcome = 'positive'
                            optional_recommendations_when_positive_outcome(Xray_outcome,serious_underlying_condition,age)
                        elif Xray_prediction[0] == max(Xray_prediction):
                            st.subheader('Pneumonia is also a serious condition, here are some recommendations for you')
                            st.write('if you have difficulty breathing, chest pain, persistent fever of 39 Celcius or higher, or persistent cough, especially if you are coughing up pus, See your GP')
            if option == 'use available sample images':
                
                # I need to get some sample images to use from the sample_data folder
                form = st.form(key='my-form')
                path1 = os.listdir("sample_data")
                imge = form.selectbox(
                    'Please Select a Test Image:',
                    path1
                )
                form.subheader('optional inputs')
                age = form.number_input('How old are you?', min_value=16, max_value=150,  step=1, value=45)
                serious_underlying_condition = False
                condition1 = form.radio('other undelying condition?', 
                    ('none','Diabetes', 'lung disease', 'heart or cardivascular disease',
                    'cancer', 'kidney disease' 
                    ))
                if condition1 != 'none':
                    serious_underlying_condition = True
                submit = form.form_submit_button(label= "predict my COVID-19 status")

                if submit:
                    image4 = Image.open(os.path.join("sample_data", imge))
                    st.image(image4, caption=" your chosen XRay", use_column_width=True)
                    user_image_input4 = ProcessImageData(image4)
                    processed_image = user_image_input4.TestImgPreprocessing()
                    Xray_prediction = user_image_input4.predict_covid_with_Xray()

                    if Xray_prediction[2] == max(Xray_prediction):
                        percent_prob = round((Xray_prediction[2]*100), 1)
                        st.success(f" ### Based on your chest Xray,  you have COVID-19, confidence is {percent_prob} percent")
                        # st.markdown(f"<h3 style='text-align: left; color: blue;'>Based on your chest Xray,  you have COVID-19, confidence is {percent_prob} percent </h3>", unsafe_allow_html=True)
                    elif Xray_prediction[1] == max(Xray_prediction):
                        percent_prob_normal = round((Xray_prediction[1]*100), 1)
                        percent_prob_covid = round((Xray_prediction[2]*100), 1)
                        st.success(f" ### Based on your chest Xray, you are normal, confidence is {percent_prob_normal} percent ")
                        # st.markdown(f"<h3 style='text-align: left; color: blue;'>Based on your chest Xray, you are normal, confidence is {percent_prob_normal} percent </h3>", unsafe_allow_html=True)
                    else:
                        percent_prob_Pneumonia = round((Xray_prediction[0]*100), 1)
                        percent_prob_covid = round((Xray_prediction[2]*100), 1)
                        st.success(f" ### Based on your chest Xray, you have Pneumonia, confidence is {percent_prob_Pneumonia} percent.")
                        st.success(f" ### The confidence that you have COVID-19 is {percent_prob_covid} percent")
                    
                    if Xray_prediction[2] == max(Xray_prediction):
                        Xray_outcome = 'positive'
                        optional_recommendations_when_positive_outcome(Xray_outcome,serious_underlying_condition,age)
                    elif Xray_prediction[0] == max(Xray_prediction):
                        st.subheader('Pneumonia is also a serious condition, here are some recommendations for you')
                        st.write('if you have difficulty breathing, chest pain, persistent fever of 39 Celcius or higher, or persistent cough, especially if you are coughing up pus, See your GP')
                    

                


        elif input_method == 'I prefer using both symptoms and chest Xray':
            st.subheader('prediction with both chest Xray and symptoms')
            option = st.radio('', ['upload your own XRay','use available sample images'])
            if option == 'upload your own XRay':
                form = st.form(key='my-form')
                uploaded_file = form.file_uploader("please upload image of your chest Xray and provide information about your symptoms", type=["jpeg", "png", "jpeg"])
                form.warning('Model was trained with chest Xray images, and can only perform accurately with chest Xray images. Inputing any other kind of image will give unwanted results')
                # I am collecting users input data for symptoms 
                cough2 = form.selectbox('Are you coughing now or in the last five days?', ('yes', 'no'))
                temperature2 = form.number_input('What is your body temperature in Celcius?', min_value=33.0, max_value=42.0, step=0.1, value=37.0)
                sore_throat2 = form.selectbox('do you have sore throat now or in the last five days?', ('yes', 'no'))
                shortness_of_breath2 = form.selectbox('do you some difficulties breathing now or in the last five days?', ('yes', 'no'))
                head_ache2 = form.selectbox('are you experiencing headache now or in the last five days?', ('yes', 'no'))
                # age = int(st.text_input('How old are you?'))
                test_indication2 = form.selectbox('`which of these situations is applicable to you`', 
                ('I had contact with someone that tested positive for COVID-19', 
                'I traveled abroad to a region with high COVID incidence', 
                'both of the above', 
                'none of the above'))

                form.subheader('optional inputs')
                age2 = form.number_input('How old are you?', min_value=16, max_value=150,  step=1, value=45)
                
                # codition = form.selectbox('Do you have other underlying medical conditions?', ('no','yes'))
                serious_underlying_condition = False
                condition1 = form.radio('other undelying condition?', 
                    ('none','Diabetes', 'lung disease', 'heart or cardivascular disease',
                    'cancer', 'kidney disease' 
                    ))
                if condition1 != 'none':
                    serious_underlying_condition = True
                submit = form.form_submit_button(label= "predict my COVID-19 status")
            
                if submit:
                    if uploaded_file is None:
                        st.error('you need to provide image input!')
                    else:
                        image2 = Image.open(uploaded_file)
                        user_image_input2 = ProcessImageData(image2)
                        processed_image = user_image_input2.TestImgPreprocessing()
                        Xray_prediction = user_image_input2.predict_covid_with_Xray()
                        
                        user_symptoms_input2 = ProcessSymptomsData(cough2, temperature2, sore_throat2, shortness_of_breath2, head_ache2, age2, test_indication2)
                        fever = user_symptoms_input2.convert_temperature_to_categories()
                        age_60_and_above = user_symptoms_input2.convert_age_to_category()
                        test_indication = user_symptoms_input2.convert_test_indication_to_category()
                        # I will then convert users data into dataframe that the model can use to predict
                        user_dataframe = user_symptoms_input2.convert_symptoms_to_dataframe()
                        # st.write('dataframe generated by user', dataframe)
                        symptoms_outcome = user_symptoms_input2.predict_symptoms_outcome()
                        probability = user_symptoms_input2.predict_probability()
                        confidence_prob = round (max(probability[0]) * 100, 0)
    
                    

                        if Xray_prediction[2] == max(Xray_prediction):
                            decision_for_covid_dual_model(Xray_prediction, symptoms_outcome)
                            # age, serious_underlying_condition = ask_for_recommendation(symptoms_outcome)
                            optional_recommendations_when_positive_outcome(symptoms_outcome,serious_underlying_condition,age2)
                        elif Xray_prediction[1] == max(Xray_prediction):
                            decision_for_normal_dual_model(symptoms_outcome,confidence_prob)
                            # age, serious_underlying_condition = ask_for_recommendation(symptoms_outcome)
                            optional_recommendations_when_positive_outcome(symptoms_outcome,serious_underlying_condition,age2)
                        elif Xray_prediction[0] == max(Xray_prediction):
                            decision_for_Pneumonia_dual_model(Xray_prediction, symptoms_outcome)
                            # age, serious_underlying_condition = ask_for_recommendation(symptoms_outcome)
                            optional_recommendations_when_positive_outcome(symptoms_outcome,serious_underlying_condition,age2)
            elif option == 'use available sample images':
                

                form = st.form(key='my-form')
                path1 = os.listdir("sample_data")
                imge = form.selectbox(
                    'Please Select a Test Image:',
                    path1
                )
                # I am collecting users input data for symptoms 
                cough3 = form.selectbox('Are you coughing now or in the last five days?', ('yes', 'no'))
                temperature3 = form.number_input('What is your body temperature in Celcius?', min_value=33.0, max_value=42.0, step=0.1, value=37.0)
                sore_throat3 = form.selectbox('do you have sore throat now or in the last five days?', ('yes', 'no'))
                shortness_of_breath3 = form.selectbox('do you some difficulties breathing now or in the last five days?', ('yes', 'no'))
                head_ache3 = form.selectbox('are you experiencing headache now or in the last five days?', ('yes', 'no'))
                # age = int(st.text_input('How old are you?'))
                test_indication3 = form.selectbox('`which of these situations is applicable to you`', 
                ('I had contact with someone that tested positive for COVID-19', 
                'I traveled abroad to a region with high COVID incidence', 
                'both of the above', 
                'none of the above'))

                form.subheader('optional inputs')
                age3 = form.number_input('How old are you?', min_value=16, max_value=150,  step=1, value=45)
                
                # codition = form.selectbox('Do you have other underlying medical conditions?', ('no','yes'))
                serious_underlying_condition = False
                condition1 = form.radio('other undelying condition?', 
                    ('none','Diabetes', 'lung disease', 'heart or cardivascular disease',
                    'cancer', 'kidney disease' 
                    ))
                if condition1 != 'none':
                    serious_underlying_condition = True
                submit = form.form_submit_button(label= "predict my COVID-19 status")
            
                if submit:
                    image3 = Image.open(os.path.join("sample_data", imge))
                    st.image(image3, caption=" your chosen XRay", use_column_width=True)
                    user_image_input3 = ProcessImageData(image3)
                    processed_image = user_image_input3.TestImgPreprocessing()
                    Xray_prediction = user_image_input3.predict_covid_with_Xray()

    
                    user_symptoms_input2 = ProcessSymptomsData(cough3, temperature3, sore_throat3, shortness_of_breath3, head_ache3, age3, test_indication3)
                    fever = user_symptoms_input2.convert_temperature_to_categories()
                    age_60_and_above = user_symptoms_input2.convert_age_to_category()
                    test_indication = user_symptoms_input2.convert_test_indication_to_category()
                    # I will then convert users data into dataframe that the model can use to predict
                    user_dataframe = user_symptoms_input2.convert_symptoms_to_dataframe()
                    # st.write('dataframe generated by user', dataframe)
                    symptoms_outcome = user_symptoms_input2.predict_symptoms_outcome()
                    probability = user_symptoms_input2.predict_probability()
                    confidence_prob = round (max(probability[0]) * 100, 0)

                    if Xray_prediction[2] == max(Xray_prediction):
                        decision_for_covid_dual_model(Xray_prediction, symptoms_outcome)
                        # age, serious_underlying_condition = ask_for_recommendation(symptoms_outcome)
                        optional_recommendations_when_positive_outcome(symptoms_outcome,serious_underlying_condition,age3)
                    elif Xray_prediction[1] == max(Xray_prediction):
                        decision_for_normal_dual_model(symptoms_outcome,confidence_prob)
                        # age, serious_underlying_condition = ask_for_recommendation(symptoms_outcome)
                        optional_recommendations_when_positive_outcome(symptoms_outcome,serious_underlying_condition,age3)
                    elif Xray_prediction[0] == max(Xray_prediction):
                        decision_for_Pneumonia_dual_model(Xray_prediction, symptoms_outcome)
                        # age, serious_underlying_condition = ask_for_recommendation(symptoms_outcome)
                        optional_recommendations_when_positive_outcome(symptoms_outcome,serious_underlying_condition,age3)
                
    

elif navigation == 'about':

    '## General information'
    'The application is based on two datasets; first is based on covid-19 symptoms and the second is based on chest xray'

    'Both were used to generate classification models. symptoms model is based on random forest classification algorithm while the chest xray dataset was used to generate a model based on convolutional neural network'

    '## Information about datasets'

    '### symptoms dataset'

    '- COVID-19 symptoms dataset is a publicly available dataset'
    '- over 3 million patients were tested'
    '- features - headache, sore throat, age above 60, shortness of breath, fever, cough, test indication'
    '- label - test outcome'

    ' ### chest Xray dataset'
    '-  dataset used has three classes: **Normal**, **COVID-19**, and **Pneumonia**'

    '## Model perfomance' 
    'For symptoms model which is based on random forest, the training, cross validation and the test accuracy is 92%'
    'For the chest Xray model based on convoluted neural network, the training accuracy is 96% and validation accuracy is 92%'

    st.warning("Disclaimer- this application was designed as a proof of concept. To diagnose COVID-19, please contact your doctor")