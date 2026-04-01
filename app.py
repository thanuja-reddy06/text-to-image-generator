from flask import Flask, render_template, request
import requests
import os
import time

app = Flask(__name__)

# 🔑 Your Hugging Face API Key
API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {
    "Authorization": "Bearer hf_xxxxxxxxxxxxxx"
}

# 🧠 Function to call API
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)

    # If model is loading → wait and retry
    if response.status_code == 503:
        print("Model loading... waiting 20 seconds")
        time.sleep(20)
        response = requests.post(API_URL, headers=headers, json=payload)

    return response
# 🏠 Home Page
@app.route('/')
def home():
    return render_template('index.html')

# 🎨 Generate Image
@app.route('/generate', methods=['GET', 'POST'])
def generate():
    image_url = None

    if request.method == 'POST':
        prompt = request.form['prompt']
        subject = request.form['subject']

        # 🎯 Enhance prompt
        if subject == "Biology":
            prompt += ", labeled biology diagram"
        elif subject == "Physics":
            prompt += ", scientific diagram"
        elif subject == "Geography":
            prompt += ", map illustration"

        # Clean filename
        filename = prompt.replace(" ", "_").lower() + ".png"
        filepath = os.path.join("static", filename)

        # Call API
        response = query({"inputs": prompt})

        # Debug info
        print("Status:", response.status_code)

        # Check if response is image
        if response.status_code == 200 and not response.content.startswith(b'{'):
            with open(filepath, "wb") as f:
                f.write(response.content)

            image_url = "/" + filepath
        else:
            print("API ERROR:", response.text)
            image_url = None

    return render_template('generate.html', image_url=image_url)

# ℹ️ About Page
@app.route('/about')
def about():
    return render_template('about.html')

# 📩 Contact Page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# ▶️ Run
if __name__ == '__main__':
    app.run(debug=True)