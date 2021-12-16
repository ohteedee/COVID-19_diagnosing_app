
from PIL import Image
import os
import pandas as pd
import numpy as np
# from thefuzz import fuzz, process
import joblib
from tensorflow.keras.models import load_model




# load models
new_RF_model= joblib.load("random_forest_pipeline2.pkl")

Xray_tensorflow_model = load_model("model.h5")

   

# define some needed functions to be imported into app.py

def convert_temperature_to_categories(fever):
    '''
    This functions takes users temerature and generate categorical data of fever presence
    '''
    if fever >= 38.0:
        fever = 'yes'
    else:
        fever = 'no'
    return fever

def convert_age_to_category(age):
    '''
    This functions takes users age and covert it into category of younger than 60 and older than 60. 
    It helps to discourage the user from feeling discriminated against
    '''
    if age < 60:
        age_60_and_above = 'no'
    else:
        age_60_and_above = 'yes'
    return age_60_and_above


def convert_test_indication_to_category(test_indication):
    '''
    This functions takes users test indication (four possibilities) and converts to three categories needed by the model
    '''
    if test_indication == 'I had contact with someone that tested positive for COVID-19':
        test_indication =  'Contact with confirmed'
    elif test_indication == 'I traveled abroad to a region with high COVID incidence':
        test_indication =   'Abroad'
    elif test_indication == 'both of the above':
        test_indication =  'Contact with confirmed'
    else:
        test_indication =  'Other'
    return test_indication 


def convert_symptoms_to_dataframe(cough, fever, sore_throat, shortness_of_breath, head_ache,
       age_60_and_above, test_indication):
    '''
    function to conver the input data of users into a dataframe that can be used to predict outcome
    '''
    user_input = {
    'cough': cough, 
    'fever': fever,
    'sore_throat': sore_throat,
    'shortness_of_breath': shortness_of_breath,
    'head_ache': head_ache,
    'age_60_and_above': age_60_and_above, 
    'test_indication': test_indication
    } 
    dataframe = pd.DataFrame([user_input])
    return dataframe


# def search_conditions(fuzzy_condition):
#     '''
#     does a fuzzy search of the underlying conditions and returns best matched conditions in a list of defined conditions
#     '''
#     extracted = []
#     defined_conditions = ['hypertension', 'diabetes', 'Immunocompromised', 'hiv', 'pregnant', 'overweight', 'cardiovascular', 'lung', 'heart', 'kidney', 'liver','stroke', 'cancer']
#     for condition in defined_conditions:
#         ratio1 = fuzz.ratio(fuzzy_condition, condition)
#         if ratio1 > 40:
#             extracted.append(condition)
#         else:
#             pass
#     return extracted

def TestImgPreprocessing(image_new):
    '''
    Resizes input image in to (224,224) and MinMax scales 
    Return array of images
    Adapted from https://stackoverflow.com/questions/21517879/
    python-pil-resize-all-images-in-a-folder
    '''

    imResize = image_new.resize((224,224), Image.ANTIALIAS)
    imResize = np.asarray(imResize)/255
    converted_image = np.asarray(imResize)
    processed_image = np.expand_dims(converted_image, axis=0)
    return processed_image 