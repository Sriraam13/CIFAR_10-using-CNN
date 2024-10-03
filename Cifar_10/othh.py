from flask import Flask, render_template, request
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image

app = Flask(__name__)

# Load CIFAR-10 class labels
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 
               'dog', 'frog', 'horse', 'ship', 'truck']

# Load the pre-trained model
model = load_model('cifar10_model_V2.h5')

# Preprocessing function for CIFAR-10 images (32x32 images)
def preprocess_image(image):
    img = image.resize((32, 32))  # Resize to 32x32
    img = np.array(img) / 255.0  # Normalize pixel values to [0,1]
    img = np.expand_dims(img, axis=0)  # Expand dimensions to batch size
    return img

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return 'No file part', 400  # No file was uploaded

    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file', 400  # Empty filename
    
    # Make sure the file is uploaded
    if file:
        # Open the image
        image = Image.open(file)

        # Preprocess the image
        img = preprocess_image(image)

        # Make predictions
        predictions = model.predict(img)
        predicted_class = np.argmax(predictions[0])  # Get the predicted class index
        confidence = np.max(predictions[0])  # Get the confidence level

        # Return the result to the user
        return f'Predicted Class: {class_names[predicted_class]}, Confidence: {confidence * 100:.2f}%'
    
    return 'File processing failed', 400

if __name__ == '__main__':
    app.run(debug=True)
