# COVID-19-diagnosing application


<img src="pictures/END_COVID.jpeg" alt="END_COVID" width="2000"/>


I designed this application to diagnose COVID-19. 
It takes either symptoms and/or chest X-ray as input from users and predict whether they have COVID. 
X-ray can help distinguish between COVID and Pneumonia

### Deployment 

Application user interface was built using streamlit and deployed to streamlit using github. 
You can see this application in action [here](https://share.streamlit.io/ohteedee/covid-19_diagnosing_app/main/app.py)


### Replication of work
Feel free to clone the repo. 

If you have additional questions, you can send a message to me on [linkedin](https://www.linkedin.com/in/tosin-oyewale/)

### General information
The application is based on two datasets (see dataset section). 
The first is based on covid-19 symptoms dataset which I explored and used to generate a model using random forest classification algorithm. 

The second is based on chest X-ray images which I used to generate a model based on convolutional neural network (CNN). 

### Information about datasets

- ### Symptoms dataset

- COVID-19 symptoms dataset is publicly available from government of Israel. The dataset is translated into english [here](https://www.nature.com/articles/s41746-020-00372-6) 
- over 3 million patients were tested 
- features - headache, sore throat, age above 60, shortness of breath, fever, cough, test indication
- label - test outcome 

- ### Chest Xray dataset
-  dataset used has three classes: **Normal**, **COVID-19**, and **Pneumonia**
-  dataset downloaded from [kaggle](https://www.kaggle.com/pranavraikokte/covid19-image-dataset)

### Model perfomance 
For symptoms model which is based on random forest, the training, cross validation and the test accuracy is 92%
<br />

For the chest Xray model based on CNN, the training accuracy is 96% and validation accuracy is 92%. 

### Information for python file in this application
The ```app.py``` file is the main file for running streamlit application. 
It contains code used to design the application interface and also contains code for collecting inputs from users. 
It uses functions from other files to make decision upon inputs from users
<br />

```utils.py``` conatins code for loading both models. 
<br />

The processor folder contains three main files listed below.
<br />

The ```decision.py``` file contains functions used in the app.py file for making decions after running models.
<br />

The ```symptoms.py``` contains code where I defined a class 'ProcessSymptomsData'. 
The class can accept several symptoms data as attributes and use functions to process them. 
Examples- it can convert temeprature into category and eventually generate a dataframe which will be used for prediction.
<br />

The ```imagedata.py``` contains code where I defined class 'ProcessImageData' to accept image, process it and make prediction using two seprate functions
<br />

The two models used were placed in the folder models.

<br />

The sample data folder contains chest Xray images that can be used to test app.


### ------------------------------------------------------------
app created by Tosin D. Oyewale (PhD) 
[Linkedin](https://www.linkedin.com/in/tosin-oyewale/ )


