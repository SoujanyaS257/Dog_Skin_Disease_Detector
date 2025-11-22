# 🐾 Smart Dog Skin Disease Detector

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-orange)
![License](https://img.shields.io/badge/License-MIT-green)

An AI-powered web application designed to assist pet owners and veterinarians in identifying common skin diseases in dogs using Deep Learning. The app also features a chatbot assistant, a veterinary clinic locator, and a model performance dashboard.

---

## 📋 Features

- **📸 AI Disease Detection:** Upload an image of a dog's skin lesion to detect conditions like Demodicosis (Mange), Dermatitis, Ringworm, Fungal Infections, and Allergies.
- **🩺 Instant Remedies:** Provides home care tips, OTC medicine suggestions, and dietary advice based on the prediction.
- **🤖 VetBot Assistant:** An integrated chatbot to answer general pet health queries.
- **📍 Vet Locator:** Uses geolocation to find the nearest veterinary clinics on an interactive map.
- **📊 Model Dashboard:** Visualizes model performance metrics (Accuracy, Precision, Recall) and Confusion Matrix.

---

## 🧠 Dataset & Training 

To achieve high accuracy (~92%), this model was trained on a custom-merged dataset combining multiple open-source collections.

### 📂 Dataset Sources

Download and merge the following datasets:

- [Dog Skin Disease Dataset by Yash Motiani](https://www.kaggle.com/datasets/yashmotiani/dog-skin-disease)  
  Contains: Fungal, Bacterial Dermatitis, Hypersensitivity, Healthy.

- [Dog's Skin Diseases by Youssef Mohamed](https://www.kaggle.com/datasets/youssef/dogs-skin-diseases)  
  Contains: Demodicosis (Mange), Ringworm.

dataset/train/<disease_name>/
> **Place all datasets inside the `dataset/` folder**

---
dataset/train/<disease_name>/

### ⚙️ Training the Model

The training logic is handled by `train_new_model.py`. It uses **Transfer Learning with EfficientNetV2S**.

Run the training script:
'python train_new_model.py'

Generates:

model/efficientnetv2s_finetuned.keras
model/classes.txt


🛠️ Installation :

git clone https://github.com/SoujanyaS257/Dog_Skin_Disease_Detector.git
cd Dog_Skin_Disease_Detector


Create virtual environment:

# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate


Install dependencies:

pip install --upgrade pip
pip install -r requirements.txt


🚀 Usage

Run the Streamlit app:
'streamlit run app.py'

Browser:
'http://localhost:8501;


📂 Project Structure

├── assets/
│   └── screenshots/         # Demo images and GIF
├── dataset/                 # Training data (not included)
├── model/
│   ├── efficientnetv2s_finetuned.keras
│   ├── classes.txt
│   └── model.py
├── utils/
│   ├── chatbot_logic.py
│   ├── maps.py
│   └── remedies.py
├── .gitignore
├── app.py
├── requirements.txt
├── train_new_model.py
└── README.md


🛡️ Tech Stack

Frontend: Streamlit
Deep Learning: TensorFlow, Keras, EfficientNetV2
Visualization: Plotly, Matplotlib, Seaborn
Mapping: Folium, Streamlit-Folium
Image Processing: PIL (Pillow), OpenCV


⚠️ Disclaimer

This tool is for informational purposes only and does not replace professional veterinary advice. Always consult a vet for diagnosis and treatment.


Made with ❤️ for 🐶 by SoujanyaS257

