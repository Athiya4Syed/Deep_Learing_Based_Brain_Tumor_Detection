
import tensorflow as tf
from tensorflow.keras.models import load_model
import os
import sys

# Force UTF-8 for stdout
sys.stdout.reconfigure(encoding='utf-8')

try:
    model_path = 'models/model.h5'
    if not os.path.exists(model_path):
        print(f"Model not found at {model_path}")
    else:
        model = load_model(model_path)
        
        with open('model_layers.txt', 'w', encoding='utf-8') as f:
            model.summary(print_fn=lambda x: f.write(x + '\n'))
            
            f.write("\nLayer names:\n")
            for layer in model.layers:
                if 'conv' in layer.name.lower():
                    f.write(f"Conv Layer: {layer.name}\n")
                elif 'pool' in layer.name.lower():
                    f.write(f"Pool Layer: {layer.name}\n")
        print("Done writing model_layers.txt")
                
except Exception as e:
    print(f"Error: {e}")
