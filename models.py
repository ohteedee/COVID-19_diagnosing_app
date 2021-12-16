
import pandas as pd



from utils import new_RF_model, Xray_tensorflow_model


def predict_symptoms_outcome(dataframe):
    '''
    This function imports Random forest model from utils and predict COVID-19 infection oucome using symptoms of user.
    it takes a dataframe as input
    '''
    
    predicted_symptoms = new_RF_model.predict(dataframe)
    return predicted_symptoms

def predict_covid_with_Xray(processed_image):
    '''
    This function takes users chest Xray image as input, process the image and  make covid prediction.
    model predicts one of three outcomes: COVID-19, Pneumonia, or normal
    '''
    
    predicted_Xray = Xray_tensorflow_model.predict(processed_image)
    predicted_Xray = predicted_Xray[0]
    return predicted_Xray

