from flask import Flask, render_template, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image

app = Flask(__name__)

class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 
               'dog', 'frog', 'horse', 'ship', 'truck']

# Load the pre-trained model
model = load_model('my-model-cifar-10_v2.h5')

def preprocess_image(image):
    img = image.resize((32, 32))  # Resize the image to the expected input shape
    img = np.array(img) / 255.0  # Normalize the image
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        try:
            image = Image.open(file)
            img = preprocess_image(image)
            predictions = model.predict(img)
            predicted_class = np.argmax(predictions[0])
            confidence = np.max(predictions[0])
            return jsonify({
                'predicted_class': class_names[predicted_class],
                'confidence': round(confidence * 100, 2)
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'File processing failed'}), 400

if __name__ == '__main__':
    app.run(debug=True)
