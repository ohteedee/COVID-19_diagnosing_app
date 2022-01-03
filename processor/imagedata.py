
# since image data has related elements, I deceided to wrap it into a class
# this makes it easier for someone reading the code that all these function address on the synptoms data and has nothing to do with the image data

from PIL import Image
import numpy as np
from utils import Xray_tensorflow_model

class ProcessImageData:
    def __init__(self, image_new) :
        self.image_new = image_new
        self.processed_image = None
        

    def TestImgPreprocessing(self):
        '''
        Resizes input image in to (224,224) and MinMax scales 
        Return array of images
        Adapted from https://stackoverflow.com/questions/21517879/
        python-pil-resize-all-images-in-a-folder
        '''

        imResize = self.image_new.resize((224,224), Image.ANTIALIAS)
        imResize = np.asarray(imResize)/255
        converted_image = np.asarray(imResize)
        self.processed_image = np.expand_dims(converted_image, axis=0)
        return self.processed_image 
    

    def predict_covid_with_Xray(self):
        '''
        This function takes users chest Xray image as input, process the image and  make covid prediction.
        model predicts one of three outcomes: COVID-19, Pneumonia, or normal
        '''
        
        predicted_Xray = Xray_tensorflow_model.predict(self.processed_image)
        predicted_Xray = predicted_Xray[0]
        return predicted_Xray