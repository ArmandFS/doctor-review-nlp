
import os
import tensorflow as tf
import pandas as pd
import numpy as np
import traceback
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional
from pydantic import BaseModel
from urllib.request import Request
from fastapi import FastAPI, Response, UploadFile


#loading the h5 model
model = tf.keras.models.load_model('doctor_review_nlp_model.h5')

tokenizer = Tokenizer()
max_sequence_length = 100

app = FastAPI()

# This endpoint is for a test (or health check) to this server
@app.get("/")
def index():
    return "Hello world from ML endpoint!"

# If your model need text input use this endpoint!
class RequestText(BaseModel):
    text:str

@app.post("/predict_text")
def predict_text(req: RequestText, response: Response):
    try:
        # In here you will get text sent by the user
        text = req.text
        print("Uploaded text:", text)
        
        # Prepare the data for your model
        input_tokens = tokenizer.texts_to_sequences([text])
        input_sequence = pad_sequences(input_tokens, maxlen=max_sequence_length)
        
        # Predict the sentiment using your model
        predictions = model.predict(input_sequence)
        predicted_label = "Positive" if predictions[0] > 0.5 else "Negative"
        
        # Step 4: Change the result your determined API output
        print("Predicted Label:", predicted_label)
        
        
        return "Endpoint not implemented"
    except Exception as e:
        traceback.print_exc()
        response.status_code = 500
        return "Internal Server Error"


# Starting the server
# Your can check the API documentation easily using /docs after the server is running
#port = os.environ.get("PORT", 8080)
#print(f"Listening to http://0.0.0.0:{port}")
#uvicorn.run(app, host='0.0.0.0',port=port)