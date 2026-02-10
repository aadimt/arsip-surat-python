import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
import pickle

class CNNClassifier:
    def __init__(self, model_path='letter_cnn_model.h5', tokenizer_path='tokenizer.json', label_path='label_encoder.pkl'):
        self.model_path = model_path
        self.tokenizer_path = tokenizer_path
        self.label_path = label_path
        self.model = None
        self.tokenizer = None
        self.label_encoder = None
        self.max_length = 50

    def load_resources(self):
        """Memuat model dan resource pendukung (tokenizer & label encoder)"""
        if os.path.exists(self.model_path):
            self.model = tf.keras.models.load_model(self.model_path)
        
        if os.path.exists(self.tokenizer_path):
            with open(self.tokenizer_path, 'r') as f:
                data = json.load(f)
                self.tokenizer = tokenizer_from_json(data)
        
        if os.path.exists(self.label_path):
            with open(self.label_path, 'rb') as f:
                self.label_encoder = pickle.load(f)

    def preprocess(self, text):
        """Melakukan tokenisasi dan padding pada input teks"""
        sequences = self.tokenizer.texts_to_sequences([text])
        padded = pad_sequences(sequences, maxlen=self.max_length, padding='post', truncating='post')
        return padded

    def predict(self, text):
        """Memprediksi kategori (Bagian/Disposisi) berdasarkan input teks"""
        if not self.model or not self.tokenizer or not self.label_encoder:
            self.load_resources()
        
        if not self.model:
            return None, "Model belum dilatih"

        processed_text = self.preprocess(text)
        prediction = self.model.predict(processed_text)
        class_idx = np.argmax(prediction)
        confidence = float(np.max(prediction))
        
        label = self.label_encoder.inverse_transform([class_idx])[0]
        return label, confidence

def create_cnn_model(vocab_size, num_classes, max_length=50):
    """Membangun arsitektur 1D Convolutional Neural Network"""
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(vocab_size, 32, input_length=max_length),
        tf.keras.layers.Conv1D(64, 5, activation='relu'),
        tf.keras.layers.GlobalMaxPooling1D(),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(optimizer='adam', 
                  loss='sparse_categorical_crossentropy', 
                  metrics=['accuracy'])
    return model
