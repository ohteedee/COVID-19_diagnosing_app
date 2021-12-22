# COVID-19-diagnosing application
This application takes either symptoms and/or chest X-ray as input from users and predict whether they have COVID. X-ray can help distinguish between COVID and Pneumonia

### General information
The application is based on two datasets (see dataset section). The first is based on covid-19 symptoms and the second is based on chest xray

Both were used to generate classification models. symptoms model is based on random forest classification algorithm while the chest xray dataset was used to generate a model based on convolutional neural network

### information about datasets

- ### symptoms dataset

- COVID-19 symptoms dataset is publicly available from government of Israel. The dataset is translated into english and discussed here: https://www.nature.com/articles/s41746-020-00372-6 and https://github.com/nshomron/covidpred
- over 3 million patients were tested 
- features - headache, sore throat, age above 60, shortness of breath, fever, cough, test indication
- label - test outcome 

- ### chest Xray dataset
-  dataset used has three classes: **Normal**, **COVID-19**, and **Pneumonia**
-  dataset downloaded from https://www.kaggle.com/pranavraikokte/covid19-image-dataset

### model perfomance 
For symptoms model which is based on random forest, the training, cross validation and the test accuracy is 92%
For the chest Xray model based on convoluted neural network, the training accuracy is 96% and validation accuracy is 92%

### information for python file in this application
The app.py file is the main file for running streamlit application. it contains code used to design the application interface and also contains code for collecting inputs from users. it uses functions from other files to make decision upon inputs from users

The decision.py file contains functions used in the app.py file for making decions after running models


utils.py conatins code for loading both models. it also contains functions to process inputs. for example, fucntion to convert input image into array. fucntions to convert inputs of symptoms into categorical data. lastly, it contains function used for converting symptoms input into dataframe for model prediction.


