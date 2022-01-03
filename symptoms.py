import pandas as pd
from utils import new_RF_model


# since processing of the symptoms data has several related elements, I deceided to wrap it into a class
# this makes it easier for someone reading the code that all these function address on the synptoms data and has nothing to do with the image data

class ProcessSymptomsData: 
    def __init__(self, cough, temperature, sore_throat, shortness_of_breath, head_ache,
       age, test_indication):
       '''
       the attributes of the '''

       self.cough = cough
       self.temperature = temperature
       self.sore_throat= sore_throat
       self.shortness_of_breath = shortness_of_breath 
       self.head_ache = head_ache
       self.age_60_and_above = age
       self.test_indication = test_indication
       self.fever = None
       self.new_test_indication = None

    def convert_temperature_to_categories(self):
        '''
        This functions takes users temerature and generate categorical data of fever presence
        '''
        if self.temperature >= 38.0:
            self.fever = 'yes'
        else:
            self.fever = 'no'
        return self.fever

    def convert_age_to_category(self):
        '''
        This functions takes users age and covert it into category of younger than 60 and older than 60. 
        It helps to discourage the user from feeling discriminated against
        '''
        if self.age_60_and_above  < 60:
            age_60_and_above = 'no'
        else:
            age_60_and_above = 'yes'
        return age_60_and_above


    def convert_test_indication_to_category(self):
        '''
        This functions takes users test indication (four possibilities) and converts to three categories needed by the model
        '''
        if self.test_indication == 'I had contact with someone that tested positive for COVID-19':
            self.new_test_indication =  'Contact with confirmed'
        elif self.test_indication == 'I traveled abroad to a region with high COVID incidence':
            self.new_test_indication =   'Abroad'
        elif self.test_indication == 'both of the above':
            self.new_test_indication =  'Contact with confirmed'
        else:
            self.new_test_indication =  'Other'
        return self.new_test_indication 


    def convert_symptoms_to_dataframe(self):
        '''
        function to conver the input data of users into a dataframe that can be used to predict outcome
        '''
        user_input = {
        'cough': self.cough, 
        'fever': self.fever,
        'sore_throat': self.sore_throat,
        'shortness_of_breath': self.shortness_of_breath,
        'head_ache': self.head_ache,
        'age_60_and_above': self.age_60_and_above, 
        'test_indication': self.new_test_indication,
        } 
        self.dataframe = pd.DataFrame([user_input])
        return self.dataframe


    def predict_probability(self):
        '''
        This function imports Random forest model from utils and predict the probability of COVID-19 infection oucome using symptoms of user.
        it takes a dataframe as input
        '''
        predicted_probability = new_RF_model.predict_proba(self.dataframe)
        return predicted_probability

    def predict_symptoms_outcome(self):
        '''
        This function imports Random forest model from utils and predict class with hihest probability using symptoms of user.
        it takes a dataframe as input
        '''
        predicted_class = new_RF_model.predict(self.dataframe)
        return predicted_class


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