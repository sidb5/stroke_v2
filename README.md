# Brain Stroke Detection System

Streamlit application for brain stroke image screening with a custom YOLOv8 model. The app supports optional username/password login backed by Firebase Firestore, runs inference on uploaded images, and uploads original files to Google Drive for storage.

> This repository is a simple demo application intended to showcase the underlying model behavior. It is not the full production product, and it does not include the broader UX, workflow controls, integrations, reliability features, or other product-layer capabilities that exists in customer-facing deployments built around these models.

## What the app does

- Shows a login screen with guest access.
- Creates a new user automatically if the username does not already exist in Firestore.
- Accepts `.png`, `.jpg`, and `.jpeg` uploads.
- Runs a YOLOv8 model stored at `assets/model_best.pt`.
- Displays the detection result image with plotted predictions.
- Uploads the original uploaded file to a configured Google Drive folder.

## Project structure

```text
stroke_v2/
|-- main.py                   # Streamlit entrypoint and page navigation
|-- pages/
|   |-- login.py              # Login and guest flow
|   |-- app.py                # Upload, inference, and result display
|   |-- functions.py          # Firebase, Firestore, Drive, password helpers
|   `-- config_loader.py      # YAML config loader
|-- config/
|   `-- config.yaml           # Google Drive folder IDs
|-- assets/
|   |-- logo.png
|   |-- logo_small.png
|   `-- model_best.pt         # Trained YOLOv8 weights
|-- .streamlit/
|   |-- config.toml           # Streamlit theme and client config
|   `-- secrets.toml          # Firebase and Google service account secrets
|-- requirements.txt
`-- packages.txt              # System packages for deployment
```

## How it works

1. `main.py` configures the Streamlit app and routes users to `pages/login.py` or `pages/app.py`.
2. `pages/login.py` authenticates against Firestore using bcrypt-hashed passwords.
3. `pages/app.py` loads the YOLO model, accepts an image upload, saves a temporary copy, and runs inference.
4. The prediction image is rendered with bounding boxes using `results[0].plot()`.
5. The original uploaded file is sent to a Google Drive folder defined in `config/config.yaml`.

## Requirements

- Python 3.x
- Pip
- Access to Firebase Admin credentials
- Access to a Google Cloud service account with Google Drive API enabled

Install Python dependencies:

```bash
pip install -r requirements.txt
```

If you are deploying to a Linux environment that needs OpenCV runtime libraries, install the packages listed in `packages.txt`:

```bash
sudo apt-get install libgl1-mesa-glx libglib2.0-0
```

## Configuration

### 1. Streamlit secrets

Create `.streamlit/secrets.toml` with these sections:

```toml
[firebase]
# Firebase service account fields used by pages/functions.py

[gcp_service_account]
# Google service account fields used to create the Drive API client
```

The code expects:

- A `firebase` section for Firebase Admin SDK initialization.
- A `gcp_service_account` section for Google Drive uploads.

### 2. Google Drive folder IDs

`config/config.yaml` stores Drive folder IDs:

```yaml
google_drive:
  folders:
    default: "..."
    correct_predictions: "..."
    incorrect_predictions: "..."
    partially_correct: "..."
```

At the moment, the app actively uses the `default` folder. The other folder IDs appear intended for the commented-out feedback workflow in `pages/app.py`.

## Running the app

From the repository root:

```bash
streamlit run main.py
```

Then open the local Streamlit URL shown in the terminal.

## Notes and current behavior

- The app hides the Streamlit sidebar and uses Streamlit's newer multipage navigation API.
- Passwords are hashed with `bcrypt` before being stored in Firestore.
- If a username is not found, the app creates that user on first login.
- Uploaded files are temporarily written to disk before inference and Drive upload.
- The feedback UI exists in `pages/app.py` but is currently commented out.

## Dependencies used in the code

- `streamlit` for the web UI
- `ultralytics` for YOLOv8 inference
- `Pillow` for image handling
- `firebase-admin` for Firestore access
- `bcrypt` for password hashing
- `google-api-python-client` and related auth packages for Drive uploads
- `opencv-python` as a dependency commonly used by the model/image stack

## Possible improvements

- Add a proper environment example for `secrets.toml`.
- Validate uploaded files and clean up temporary files after inference.
- Avoid auto-creating accounts during login unless that behavior is intentional.
- Add model output interpretation, confidence scores, and class labels to the UI.
- Restore and wire the feedback flow if prediction quality review is needed.
