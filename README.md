# COVID-19_diagnosing_app
This application takes either symptoms and/or chest X-ray as input from users and predict whether they have COVID. X-ray can help distinguish between COVID and Pneumonia

st.markdown('#### COVID-19 symptoms dataset is publicly available from government of Israel')
    st.write(' ')
    st.markdown(""" - ##### dataset translated into english and discussed here: https://www.nature.com/articles/s41746-020-00372-6 and https://github.com/nshomron/covidpred
- ##### over 3 million patients were tested 
- ##### dataset contains: headache, sore throat, age above 60, shortness of breath, fever, cough, test indication, test outcome 
""")

    st.markdown('#### COVID-19 chest Xray images are available on Kaggle')
    st.markdown(""" -  ##### dataset used has three classes: **Normal**, **COVID-19**, and **Pneumonia**
- ##### dataset downloaded from https://www.kaggle.com/pranavraikokte/covid19-image-dataset
    """)
