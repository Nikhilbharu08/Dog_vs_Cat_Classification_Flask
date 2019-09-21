import numpy as np 
import io
from PIL import Image
import tensorflow as tf
import keras
from keras import backend as K
from keras.backend import clear_session
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from flask import Flask, request, jsonify,render_template
import pickle
import base64
from keras.models import Sequential
from keras.models import load_model


app = Flask(__name__)


def get_model():
        
       
        global graph,model
        graph = tf.get_default_graph()
        model= load_model('VGG16_cats_and_dogs.h5')
        print("model loaded!!")

def preprocess_image(image, target_size):
        
    if image.mode !="RGB":
            image=image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image)
    image = np.expand_dims(image,axis=0) 

    return image

        #print("Not a .WAV format file")
    
print(" loading keros model")
get_model()

@app.route("/predict", methods=["POST"])
def predict():
        message = request.get_json(force=True)
        encoded = message['image']
        decoded = base64.b64decode(encoded)
        image = Image.open(io.BytesIO(decoded))
        processed_image= preprocess_image(image, target_size=(224, 224))
       
        with graph.as_default():
                prediction = model.predict(processed_image).tolist()

        

        response = {
                'prediction':{
                        'dog': prediction[0][0],
                        'cat': prediction[0][1] 
        }
    }          
        
        return jsonify(response)
if __name__=='__main__':
    app.run(debug=True)