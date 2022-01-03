

import joblib
from tensorflow.keras.models import load_model




# load models
new_RF_model= joblib.load("models/random_forest_pipeline2.pkl")

Xray_tensorflow_model = load_model("models/model.h5")

   