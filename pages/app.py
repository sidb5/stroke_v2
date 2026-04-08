import streamlit as st
import os
import uuid
from PIL import Image
from ultralytics import YOLO

from pages.config_loader import load_config
from pages.functions import create_drive_service, upload_file_to_drive

model = YOLO("assets/model_best.pt")

def detect_disease(img_path):
    results = model(img_path)
    if not results:
        return None

    result_img = results[0].plot()
    results_img_path = f".temp_results{uuid.uuid4()}.png"
    Image.fromarray(result_img).save(results_img_path)
    return results_img_path

_, col1, _ = st.columns([1, 4.5, 1])

config = load_config()
default_folder_id = config["google_drive"]["folders"]["default"]
service = create_drive_service()

if "detection_done" not in st.session_state:
    st.session_state.detection_done = False

if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = False

with col1:
    uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        temp_img_path = f"./data/temp_uploaded_img_{uuid.uuid4()}.png"
        image = Image.open(uploaded_file)
        directory = os.path.dirname(temp_img_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        image.save(temp_img_path)
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        upload_file_to_drive(service, uploaded_file, default_folder_id)

        button_style = """
            <style>
            .stButton > button {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 12px 24px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                transition-duration: 0.4s;
                cursor: pointer;
                border-radius: 8px;
            }

            .stButton > button:hover {
                background-color: white;
                color: black;
                border: 2px solid #4CAF50;
            }
            </style>
        """
        st.markdown(button_style, unsafe_allow_html=True)

        if st.button("Detect Stroke", type="primary", use_container_width=True):
            results_img_path = detect_disease(temp_img_path)

            if results_img_path:
                result_img = Image.open(results_img_path)
                result_img = result_img.resize((350, 350))
                st.image(result_img, caption="Detection Results", use_column_width=True)

                st.session_state.detection_done = True
                st.session_state.feedback_given = False
            else:
                st.write("No detections found.")
                st.session_state.detection_done = False
        else:
            st.image(image, caption="Uploaded Image", use_column_width=True)
