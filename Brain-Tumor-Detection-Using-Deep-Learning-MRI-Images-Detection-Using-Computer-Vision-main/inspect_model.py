
import tensorflow as tf
from tensorflow.keras.models import load_model
import os

try:
    model_path = 'models/model.h5'
    if not os.path.exists(model_path):
        print(f"Model not found at {model_path}")
    else:
        model = load_model(model_path)
        model.summary()
        
        print("\nLayer names:")
        for layer in model.layers:
            if 'conv' in layer.name.lower():
                print(f"Conv Layer: {layer.name}")
            elif 'pool' in layer.name.lower():
                print(f"Pool Layer: {layer.name}")
                
except Exception as e:
    print(f"Error: {e}")
