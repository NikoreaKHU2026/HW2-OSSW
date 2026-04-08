# Simple Expression Prediction API

This is a simple FastAPI-based API server for predicting facial expressions (emotions) from uploaded images. It uses `deepface`, a lightweight wrapper around state-of-the-art facial recognition models, to detect faces and predict expressions easily.

## Project Structure

```text
HW2-OSSW/
│
├── main.py                 # FastAPI application and routing logic (ML prediction)
├── requirements.txt        # Python dependencies
└── README.md               # Instructions to run the application
```

## How to Run locally

1. **Set up a virtual environment (optional but highly recommended):**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Start the FastAPI server:**
   ```powershell
   uvicorn main:app --reload
   ```

4. **Access the API Documentation:**
   Once the server is running, open your browser and go to:
   - [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Swagger UI, where you can test the upload functionality right in the browser)
   - [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) (ReDoc Documentation)

## Testing the API

You can test the API directly using `curl` from a separate terminal:

```powershell
curl -X 'POST' \
  'http://127.0.0.1:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@path_to_your_image.jpg'
```

*Note: On the first run, `deepface` will download its extremely lightweight pre-trained model weights (for Emotion prediction) to your home directory (`C:\Users\nikol\.deepface\weights`). This may take a few seconds or minutes depending on your internet connection. Subsequent requests will be much faster since the model is cached.*
