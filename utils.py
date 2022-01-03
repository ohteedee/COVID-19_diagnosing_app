

import joblib
from tensorflow.keras.models import load_model




# load models
new_RF_model= joblib.load("random_forest_pipeline2.pkl")

Xray_tensorflow_model = load_model("model.h5")

   