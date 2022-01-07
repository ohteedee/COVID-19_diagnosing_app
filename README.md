# COVID-19-diagnosing application
This application takes either symptoms and/or chest X-ray as input from users and predict whether they have COVID. X-ray can help distinguish between COVID and Pneumonia

### deployment 
You can see this application in action [here](https://share.streamlit.io/ohteedee/covid-19_diagnosing_app/main/app.py)


### replication of work
Feel free to clone the repo. However acknowledgement of this work is expected. 

If you need the origninal notebooks about how the models were generated, you can reach out to me on [linkedin](https://www.linkedin.com/in/tosin-oyewale/) 
### General information
The application is based on two datasets (see dataset section). The first is based on covid-19 symptoms and the second is based on chest xray

Both were used to generate classification models. symptoms model is based on random forest classification algorithm while the chest xray dataset was used to generate a model based on convolutional neural network

### information about datasets

- ### symptoms dataset

- COVID-19 symptoms dataset is publicly available from government of Israel. The dataset is translated into english and discussed [here](https://www.nature.com/articles/s41746-020-00372-6) 
- over 3 million patients were tested 
- features - headache, sore throat, age above 60, shortness of breath, fever, cough, test indication
- label - test outcome 

- ### chest Xray dataset
-  dataset used has three classes: **Normal**, **COVID-19**, and **Pneumonia**
-  dataset downloaded from [kaggle](https://www.kaggle.com/pranavraikokte/covid19-image-dataset)

### model perfomance 
For symptoms model which is based on random forest, the training, cross validation and the test accuracy is 92%
For the chest Xray model based on convoluted neural network, the training accuracy is 96% and validation accuracy is 92%

### information for python file in this application
The app.py file is the main file for running streamlit application. it contains code used to design the application interface and also contains code for collecting inputs from users. it uses functions from other files to make decision upon inputs from users

utils.py conatins code for loading both models. 


#### processor folder/package contains three main files listed below.

The decision.py file contains functions used in the app.py file for making decions after running models

symptoms.py contains code where I defined a class 'ProcessSymptomsData'. The class can accept several symptoms data as attributes and use functions to process them. examples- it can convert temeprature into category and eventually generate a dataframe which will be used for prediction.

imagedata.py contains code where I defined class 'ProcessImageData' to accept image, process it and make prediction using two seprate functions

##### pictures folder contains image used on homepage of app.

##### the two models used were placed in the folder models.

##### sample data folder contains chest Xray images that can be used to test app.



app created by Tosin D. Oyewale (PhD) 
[Linkedin](https://www.linkedin.com/in/tosin-oyewale/ )


