import streamlit as st
from ultralytics import YOLO
from PIL import Image
import io
from pages.functions import create_drive_service, upload_file_to_drive
import os
import time
import uuid

# Load the YOLOv8 model using your trained weights
model = YOLO('assets/model_best.pt')

# Function to detect disease
def detect_disease(img_path):
    # Use YOLOv8 model for prediction
    results = model(img_path)

    # Check if any detection was made
    if len(results) > 0:
        # Get the image with bounding boxes
        result_img = results[0].plot()

        # Save the results image to a temporary file
        result_uuid = str(uuid.uuid4())
        results_img_path = f".temp_results{result_uuid}.png"
        Image.fromarray(result_img).save(results_img_path)  # Save the image

        return results_img_path
    else:
        return None


# Define layout columns
_, col1, _ = st.columns([1,4.5,1])

# Specify the default folder ID for image upload
default_folder_id = "1ZJl54Kl-kpfPY6WbbSW29YTmDxkejN1F"

# Initialize Google Drive service once
service = create_drive_service()

# Initialize session state for detection completion and feedback
if 'detection_done' not in st.session_state:
    st.session_state.detection_done = False

if 'feedback_given' not in st.session_state:
    st.session_state.feedback_given = False

with col1:
    # Upload image
    uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # Generate a unique identifier for the temporary file
        temp_uuid = str(uuid.uuid4())
        temp_img_path = f"./data/temp_uploaded_img_{temp_uuid}.png"

        # Save the uploaded image temporarily
        image = Image.open(uploaded_file)
        
        # Ensure the directory exists
        directory = os.path.dirname(temp_img_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        image.save(temp_img_path)  # Save the uploaded image temporarily
        # Save the uploaded file temporarily
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        # Upload the file to Google Drive
        file_id = upload_file_to_drive(service, uploaded_file, default_folder_id)


        button_style = """
            <style>
            .stButton > button {
                background-color: #4CAF50;  /* Green background */
                color: white;  /* White text */
                border: none;  /* Remove border */
                padding: 12px 24px;  /* Padding for the button */
                text-align: center;  /* Centered text */
                text-decoration: none;  /* Remove underline */
                display: inline-block;  /* Inline block */
                font-size: 16px;  /* Text size */
                margin: 4px 2px;  /* Space between buttons */
                transition-duration: 0.4s;  /* Animation */
                cursor: pointer;  /* Pointer cursor on hover */
                border-radius: 8px; /* Rounded corners */
            }

            .stButton > button:hover {
                background-color: white; 
                color: black; 
                border: 2px solid #4CAF50; /* Green border on hover */
            }
            </style>
        """

        st.markdown(button_style, unsafe_allow_html=True)

        # Detect disease button
        if st.button("Detect Stroke", type= "primary", use_container_width=True):
            # Detect disease
            results_img_path = detect_disease(temp_img_path)

            if results_img_path:
                # Display the result image with bounding boxes
                result_img = Image.open(results_img_path)
                result_img = result_img.resize((350, 350))  # Resize for display
                st.image(result_img, caption="Detection Results", use_column_width=True)

                #Mark detection as done in session state
                st.session_state.detection_done = True
                st.session_state.feedback_given = False  # Reset feedback state for next detection
            else:
                st.write("No detections found.")
                st.session_state.detection_done = False
        else:
            # Display the uploaded image if detection has not been done yet
            st.image(image, caption="Uploaded Image", use_column_width=True)


##FEEDBACK SYSTEM
# if st.session_state.detection_done:

#     show_sidebar_style = """
#         <style>
#         [data-testid="stSidebar"] {display: block;}
#         </style>
#         """
#     st.markdown(show_sidebar_style, unsafe_allow_html=True)
#     # Sidebar content for feedback
#     with st.sidebar:
#         # Apply custom styles for spacing between components
#         st.markdown("""<style>
#         .app-spacing {
#             margin-top: -15px;
#             margin-bottom: -30px;
#         }
#         .button-spacing {
#             margin-bottom: 10px;
#         }
#         </style>""", unsafe_allow_html=True)

#         # Improved CSS for the classification message with cleared margins
#         classification_style = """
#             <style>
#             /* Container styling with no margin at top and bottom */
#             .classification-container {
#                 padding: 11px;
#                 background-color: #f7f7f7;
#                 border: 1px solid #ddd;
#                 border-radius: 10px;
#                 box-shadow: 2px 4px 10px rgba(0, 0, 0, 0.1);
#                 text-align: center;
#                 font-family: 'Arial', sans-serif;
#                 margin-top: -40px;  /* Remove top margin */
#                 margin-bottom: -35px;  /* Remove bottom margin */
#             }

#             /* Styling for the heading */
#             .classification-container h1 {
#                 color: #22686E;
#                 font-size: 13px;
#                 font-weight: bold;
#                 margin: 0;  /* Remove margins around the heading */
#                 font-family: 'Arial', sans-serif;
#             }
#             </style>
#         """

#         # Apply the custom style
#         st.markdown(classification_style, unsafe_allow_html=True)

#         # Display the classification message inside a styled container
#         classification_message = """
#         <div class='classification-container'>
#             <h1>Your feedback improves predictions for more accurate results. Was this prediction correct?</h1>
#         </div>
#         """
#         st.markdown(classification_message, unsafe_allow_html=True)

#         # Insert a space after the markdown to ensure proper display order
#         st.markdown("<div class='button-spacing'></div>", unsafe_allow_html=True)

#         # Placeholder for the success message
#         message_placeholder = st.empty()

#         # Display feedback buttons in the sidebar only if feedback hasn't been given
#         if not st.session_state.feedback_given:
#             # Define folder IDs for feedback
#             correct_pred_folder_id = "1ncxH-PxJW7nJu9Rlwm4LUN3DQg8BGh2f"
#             incorrect_pred_folder_id = "1oUSNdHGv_jiqSfFi92kniWCnONxlnbR7"
#             partially_pred_folder_id = "1F8x6zMTuReS2_BkUMlJNZcLGbWhyw6Nv"

#             if st.button("Correct", use_container_width=True):
#                 upload_file_to_drive(service, uploaded_file, correct_pred_folder_id)
#                 st.session_state.feedback_given = True

#             if st.button("Incorrect", use_container_width=True):
#                 upload_file_to_drive(service, uploaded_file, incorrect_pred_folder_id)
#                 st.session_state.feedback_given = True

#             if st.button("Partially correct", use_container_width=True):
#                 upload_file_to_drive(service, uploaded_file, partially_pred_folder_id)
#                 st.session_state.feedback_given = True

#         # Hide all buttons once feedback is given
#         if st.session_state.feedback_given:
#             st.session_state.detection_done = False  # Mark detection as not done to hide buttons
#             message_placeholder.success("Thank you for your feedback!")
#             # Pause for 1 seconds
#             time.sleep(1)
#             # Clear the success message
#             message_placeholder.empty()
