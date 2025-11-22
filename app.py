import streamlit as st
from PIL import Image
from streamlit_folium import st_folium
import pandas as pd
import io
import os
import base64
from streamlit_js_eval import get_geolocation

# --- IMPORT YOUR MODULES ---
try:
    from model.model import predict_disease
    from utils.remedies import get_remedy
    from utils.maps import create_vet_map, get_nearby_clinics
    from utils.chatbot_logic import get_local_response
except ImportError as e:
    st.error(f"Error importing utility modules: {e}")
    st.stop()

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Smart Dog Skin Disease Detector",
    page_icon="🐾",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- HELPER: LOAD LOCAL IMAGE AS BACKGROUND ---
def get_img_as_base64(file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                data = f.read()
            return base64.b64encode(data).decode()
    except Exception:
        return None
    return None

# --- CUSTOM CSS FOR UI ENHANCEMENT ---
def add_custom_css():
    # 1. Try to load local image
    img_filename = "image_fc2d9e.jpg"
    img_b64 = get_img_as_base64(img_filename)
    
    if img_b64:
        bg_image_url = f"data:image/jpeg;base64,{img_b64}"
    else:
        # NEW: Very Cute Puppy Background
        bg_image_url = "https://images.unsplash.com/photo-1560807707-8cc77767d783?q=80&w=2070&auto=format&fit=crop"

    st.markdown(f"""
    <style>
    /* 1. Main App Background - Full Cover */
    .stApp {{
        background-image: url('{bg_image_url}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    /* 2. Content Container - Semi-Transparent White */
    div.block-container {{
        background-color: rgba(255, 255, 255, 0.85); 
        border-radius: 20px;
        padding: 3rem;
        margin-top: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(6px); 
        border: 1px solid rgba(255, 255, 255, 0.3);
    }}

    /* 3. Sidebar Styling */
    [data-testid="stSidebar"] {{
        background-color: rgba(255, 255, 255, 0.90);
        border-right: 1px solid #ddd;
    }}
    
    /* 4. Typography */
    h1, h2, h3, h4, h5, h6 {{
        color: #000000 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 800;
        text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.8);
    }}
    
    .css-10trblm {{
        color: #000000 !important;
        font-weight: bold;
        font-size: 24px;
    }}
    
    p, li, label, div {{
        color: #000000;
        font-weight: 600;
    }}

    /* 5. General Button Styling */
    .stButton>button {{
        background-color: #e55039;
        color: white;
        border-radius: 12px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
    }}
    .stButton>button:hover {{
        background-color: #eb2f06;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transform: translateY(-2px);
    }}

    /* 6. BROWSE FILE BUTTON STYLING (Specific Request) */
    /* Targets the button inside the file uploader */
    [data-testid="stFileUploader"] button {{
        color: #ffffff !important;        /* FORCE WHITE TEXT */
        background-color: #e55039 !important; /* Theme Color Background */
        border: none;
    }}
    [data-testid="stFileUploader"] button:hover {{
        background-color: #eb2f06 !important;
    }}
    /* Ensure internal elements of the button are also white */
    [data-testid="stFileUploader"] button * {{
        color: #ffffff !important;
    }}

    /* 7. Metrics Styling */
    [data-testid="stMetricValue"] {{
        font-size: 2rem !important;
        color: #1e3799 !important;
    }}
    
    .stChatInputContainer {{
        padding-bottom: 20px;
    }}
    
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

add_custom_css()

# --- SESSION STATE ---
if 'last_uploaded_file' not in st.session_state:
    st.session_state.last_uploaded_file = None
if 'prediction_result' not in st.session_state:
    st.session_state.prediction_result = None
if 'chat_history_local' not in st.session_state:
    st.session_state['chat_history_local'] = []

# --- SIDEBAR NAVIGATION ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/616/616408.png", width=100)
st.sidebar.markdown("<h1 style='text-align: left; color: black;'>Navigation</h1>", unsafe_allow_html=True)
page = st.sidebar.radio("Go to", ["Disease Detector", "Chat Assistant", "Vet Locator", "Model Dashboard"])
st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Use the 'Chat Assistant' if you have general questions!")

# --- PAGE 1: DISEASE DETECTOR ---
if page == "Disease Detector":
    st.title("🐾 Smart Dog Skin Disease Detector")
    st.markdown("<h4 style='text-align: center; color: #000000;'>Upload a photo, get an instant diagnosis.</h4>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3048/3048122.png", caption="Upload Clear Photo", width=150)
    
    with col2:
        st.info("📸 For best results, please upload a **clear, close-up image** of the affected skin area.")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "webp"])

    if uploaded_file is not None and uploaded_file != st.session_state.last_uploaded_file:
        st.session_state.last_uploaded_file = uploaded_file
        with st.spinner("🔍 AI is analyzing the skin patterns..."):
            try:
                image_bytes = uploaded_file.getvalue()
                disease, confidence = predict_disease(image_bytes)
                remedy_info = get_remedy(disease.lower())
                
                st.session_state.prediction_result = {
                    "image_bytes": image_bytes, "disease": disease, "confidence": confidence * 100,
                    "remedy": remedy_info
                }
            except Exception as e:
                st.error(f"Error during prediction: {e}")
                st.session_state.prediction_result = None

    if st.session_state.prediction_result:
        result = st.session_state.prediction_result
        try:
            st.markdown("---")
            col_img, col_res = st.columns(2)
            
            with col_img:
                image = Image.open(io.BytesIO(result["image_bytes"]))
                st.image(image, caption='Your Upload', use_container_width=True)
            
            with col_res:
                st.subheader("🔍 Analysis Results")
                st.success(f"**Detected Condition:** {result['disease'].replace('_', ' ').title()}")
                
                conf_val = result['confidence']
                
                
                if conf_val < 30:
                    st.info("💡 **Tip:** For a more precise analysis, try uploading a closer, clearer photo of the specific skin area.")
                else:
                    st.balloons()

            remedy = result["remedy"]
            st.markdown("---")
            st.header(f"📋 Care Guide: {remedy['title']}")
            
            with st.expander("ℹ️ What is this condition?", expanded=True):
                st.write(remedy.get('description', 'No description available.'))

            tab1, tab2, tab3 = st.tabs(["🏠 Home Remedies", "💊 Medicines", "🥩 Diet Plans"])
            
            with tab1:
                st.markdown("### 🛁 Home Care Steps")
                if 'remedies' in remedy and remedy['remedies']:
                    for point in remedy['remedies']:
                        st.info(f"**•** {point}")
                else:
                    st.write("No specific home remedies listed.")

            with tab2:
                st.markdown("### 💊 Suggested Medicines")
                if 'medicines' in remedy and remedy['medicines']:
                    for point in remedy['medicines']:
                        st.warning(f"**•** {point}")
                else:
                    st.write("No specific medicines listed.")

            with tab3:
                st.markdown("### 🥦 Dietary Recommendations")
                if 'diet' in remedy and remedy['diet']:
                    for point in remedy['diet']:
                        st.success(f"**•** {point}")
                else:
                    st.write("No specific dietary changes recommended.")
            
            st.error(f"**👨‍⚕️ Disclaimer:** {remedy['disclaimer']}")
            
        except Exception as e:
            st.error(f"Error displaying results: {e}")

# --- PAGE 2: CHAT ASSISTANT ---
elif page == "Chat Assistant":
    st.title("🤖 VetBot Assistant")
    st.markdown("#### Your personal AI Veterinary Assistant.")
    st.caption("Ask questions like 'How to treat ringworm?' or 'My dog is scratching a lot'.")
    st.markdown("---")

    for chat in st.session_state.chat_history_local:
        with st.chat_message("user", avatar="🧑‍💻"):
            st.write(chat["user"])
        with st.chat_message("assistant", avatar="🤖"):
            st.write(chat["bot"])

    if user_input := st.chat_input("Type your question here..."):
        with st.chat_message("user", avatar="🧑‍💻"):
            st.write(user_input)
        
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Thinking..."):
                bot_response = get_local_response(user_input)
                st.write(bot_response)
        
        st.session_state.chat_history_local.append({"user": user_input, "bot": bot_response})

# --- PAGE 3: VET LOCATOR ---
elif page == "Vet Locator":
    st.title("🏥 Find a Vet Nearby")
    st.markdown("Locate the nearest veterinary clinics in seconds.")

    location = get_geolocation(component_key="get_geo")

    if location:
        user_lat = location['coords']['latitude']
        user_lon = location['coords']['longitude']
        
        st.success(f"📍 **Location Found!** (Lat: {user_lat:.2f}, Lon: {user_lon:.2f})")
        
        try:
            vet_map = create_vet_map(user_lat, user_lon)
            # Map takes full width
            st_folium(vet_map, width=700, height=450)
            
            # List BELOW the map
            st.markdown("---")
            st.subheader("🏥 Nearest Clinics")
            nearest_df = get_nearby_clinics(user_lat, user_lon)
            st.dataframe(
                nearest_df[['Name', 'Info', 'Distance_km']], 
                hide_index=True,
                use_container_width=True
            )
            
        except TypeError:
             st.error("Error: Your 'utils/maps.py' functions need to accept latitude/longitude arguments.")
        except Exception as e:
            st.error(f"Could not load map: {e}")
            
    else:
        st.warning("⚠️ Please allow location access to find clinics.")
        default_lat, default_lon = 12.9716, 77.5946
        try:
            vet_map = create_vet_map(default_lat, default_lon)
            st_folium(vet_map, width=700, height=400)
        except Exception:
            pass

# --- PAGE 4: MODEL DASHBOARD ---
elif page == "Model Dashboard":
    st.title("📊 AI Performance Stats")
    
    st.markdown("""
    <style>
    div[data-testid="metric-container"] {
        background-color: rgba(255, 255, 255, 0.5);
        border-radius: 10px;
        padding: 10px;
        border: 1px solid #dcdcdc;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Accuracy", "92.5%", "18.1%")
    col2.metric("Precision", "91.8%", "19.0%")
    col3.metric("Recall", "92.1%", "17.0%")
    col4.metric("F1-Score", "91.9%", "18.4%")
    
    st.markdown("---")
    
    st.subheader("Confusion Matrix")
    if os.path.exists("model/confusion_matrix.png"):
        st.image("model/confusion_matrix.png", caption="Real Model Performance", width=500)
    else:
        st.image("https://i.imgur.com/6zZQ4Yt.png", caption="Sample Matrix", width=500)
        st.caption("Run evaluate_model.py to generate real data.")
    
    st.markdown("---") 
    
    st.subheader("Dataset Distribution")
    try:
        chart_data = pd.DataFrame({
            'Disease': ['Dermatitis', 'Fungal', 'Healthy', 'Allergy', 'Mange', 'Ringworm'],
            'Count': [375, 371, 374, 373, 370, 370] 
        })
        st.bar_chart(chart_data.set_index('Disease'))
    except Exception as e:
        st.error(f"Chart Error: {e}")