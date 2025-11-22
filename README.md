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

### ⚙️ Training the Model

The training logic is handled by `train_new_model.py`. It uses **Transfer Learning with EfficientNetV2S**.

Run the training script:

```bash
python train_new_model.py

This will generate:
model/efficientnetv2s_finetuned.keras
model/classes.txt

🛠️ Installation

Clone the repository:
git clone https://github.com/SoujanyaS257/Dog_Skin_Disease_Detector.git
cd Dog_Skin_Disease_Detector

Create a virtual environment (optional but recommended):
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate

Upgrade pip:
pip install --upgrade pip


Install dependencies:
pip install -r requirements.txt

🚀 Usage

Run the Streamlit app:
streamlit run app.py


Open your browser:
http://localhost:8501


Optional: Generate the Confusion Matrix for the model dashboard:
python evaluate_model.py

📂 Project Structure

├── assets/                  # Static images and resources
├── dataset/                 # Training data (not included, see Dataset section)
├── model/
│   ├── efficientnetv2s_finetuned.keras  # Generated after training
│   ├── classes.txt                       # Generated after training
│   └── model.py                          # Prediction logic
├── utils/
│   ├── chatbot_logic.py     # Chatbot responses
│   ├── maps.py              # Folium map logic
│   └── remedies.py          # Database of cures/medicines
├── .gitignore               # Files/folders to exclude from Git
├── app.py                   # Main Streamlit application
├── requirements.txt         # Python dependencies
├── train_new_model.py       # Training script
└── README.md                # Project documentation

⚠️ Disclaimer
This tool is intended for informational purposes only and does not replace professional veterinary advice. Always consult a vet for a definitive diagnosis and treatment plan.

Made with ❤️ for 🐶 by SoujanyaS257


