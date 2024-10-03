// TensorFlow.js CIFAR-10 model URL
const modelUrl = 'https://storage.googleapis.com/tfjs-models/tfjs/cifar10_v2/model.json';

// Load CIFAR-10 labels
const classNames = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck'];

// Load the TensorFlow.js model
let model;
(async function () {
    model = await tf.loadGraphModel(modelUrl);
    console.log('Model loaded');
})();

// Handling file uploads
document.getElementById('upload').addEventListener('change', async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // Display image preview
    const reader = new FileReader();
    reader.onload = (e) => {
        const img = document.createElement('img');
        img.src = e.target.result;
        img.id = 'preview-img';
        img.style.maxWidth = '100%';
        document.getElementById('preview').innerHTML = '';
        document.getElementById('preview').appendChild(img);
        document.getElementById('preview').style.display = 'block';

        // Classify the image
        classifyImage(img);
    };
    reader.readAsDataURL(file);
});

// Function to preprocess image and classify using TensorFlow.js model
async function classifyImage(img) {
    // Preprocess the image
    const tensor = tf.browser.fromPixels(img)
        .resizeNearestNeighbor([32, 32])
        .toFloat()
        .expandDims();

    // Make predictions
    const predictions = await model.predict(tensor).data();

    // Get the highest confidence index
    const predictedIndex = predictions.indexOf(Math.max(...predictions));

    // Display the result
    document.getElementById('class-name').innerText = classNames[predictedIndex];
    document.getElementById('confidence-value').innerText = `${(predictions[predictedIndex] * 100).toFixed(2)}%`;
}
