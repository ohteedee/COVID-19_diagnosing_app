# COVID-19-diagnosing application
This application takes either symptoms and/or chest X-ray as input from users and predict whether they have COVID. X-ray can help distinguish between COVID and Pneumonia

### General information
The application is based on two datasets (see dataset section). The first is based on covid-19 symptoms and the second is based on chest xray

Both were used to generate classification models. symptoms model is based on random forest classification algorithm while the chest xray dataset was used to generate a model based on convoluted neural network

### information about datasets

- ##### symptoms dataset

- COVID-19 symptoms dataset is publicly available from government of Israel. The dataset is translated into english and discussed here: https://www.nature.com/articles/s41746-020-00372-6 and https://github.com/nshomron/covidpred
- over 3 million patients were tested 
- features - headache, sore throat, age above 60, shortness of breath, fever, cough, test indication
- label - test outcome 

- ##### chest Xray dataset
-  dataset used has three classes: **Normal**, **COVID-19**, and **Pneumonia**
-  dataset downloaded from https://www.kaggle.com/pranavraikokte/covid19-image-dataset

