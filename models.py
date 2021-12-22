
import pandas as pd



from utils import new_RF_model, Xray_tensorflow_model

def predict_probability(dataframe):
    '''
    This function imports Random forest model from utils and predict the probability of COVID-19 infection oucome using symptoms of user.
    it takes a dataframe as input
    '''
    predicted_probability = new_RF_model.predict_proba(dataframe)
    return predicted_probability

def predict_symptoms_outcome(dataframe):
    '''
    This function imports Random forest model from utils and predict class with hihest probability using symptoms of user.
    it takes a dataframe as input
    '''
    predicted_class = new_RF_model.predict(dataframe)
    return predicted_class

def predict_covid_with_Xray(processed_image):
    '''
    This function takes users chest Xray image as input, process the image and  make covid prediction.
    model predicts one of three outcomes: COVID-19, Pneumonia, or normal
    '''
    
    predicted_Xray = Xray_tensorflow_model.predict(processed_image)
    predicted_Xray = predicted_Xray[0]
    return predicted_Xray


