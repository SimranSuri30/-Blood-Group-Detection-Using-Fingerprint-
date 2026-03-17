from flask import Flask, request, render_template, jsonify
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os

app = Flask(__name__)

# Load the trained model (ensure the model is in the model/ directory)
model = load_model('model/blood_group_predictor.h5')

# Define upload folder for fingerprint images
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home route: to upload an image
@app.route('/')
def home():
    return render_template('index.html')

# Prediction route: handles image upload and prediction
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # Save the uploaded image
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(img_path)

            # Load and preprocess the image
            img = image.load_img(img_path, target_size=(224, 224))
            img_array = image.img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            # Predict the blood group
            # Predict the blood group
            prediction = model.predict(img_array)
            predicted_class = np.argmax(prediction, axis=1)

            classes = ['A+', 'A-', 'AB+', 'AB-', 'B+', 'B-', 'O+', 'O-']
            print("Predicted class:", predicted_class)
            print("Classes:", classes)



            if predicted_class is None or len(predicted_class) == 0:
                return jsonify({"error": "Model did not return a valid prediction."}), 500

            predicted_blood_group = classes[predicted_class[0]]

            predicted_blood_group = classes[predicted_class[0]]
            return render_template('result.html', blood_group=predicted_blood_group)

if __name__ == '__main__':
    app.run(debug=True)
