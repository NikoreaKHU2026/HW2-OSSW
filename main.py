import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from deepface import DeepFace

app = FastAPI(
    title="Lightweight Expression Prediction API",
    description="A simple API server to predict expression/emotion from uploaded face images.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Expression Prediction API. Send a POST request to /predict with an image."}

@app.post("/predict")
async def predict_expression(file: UploadFile = File(...)):
    """
    Upload an image file to predict the expression (emotion) of the person(s) in the image.
    """
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    try:
        # Read image to memory
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(status_code=400, detail="Failed to decode image.")

        # Analyze image using DeepFace
        # Modify DeepFace actions to include both 'emotion' and 'gender'
        results = DeepFace.analyze(img_path=img, actions=['emotion', 'gender'], enforce_detection=True)

        # DeepFace returns a list of dictionaries if multiple faces are found
        if isinstance(results, list):
            predictions = []
            for face in results:
                predictions.append({
                    "emotion": face["dominant_emotion"],
                    "all_emotions": face["emotion"],
                    "gender": face["dominant_gender"],
                    "gender_probabilities": face["gender"],
                    "face_region": face.get("region", {})
                })
            return {"status": "success", "predictions": predictions}
        else:
            return {
                "status": "success", 
                "predictions": [{
                    "emotion": results["dominant_emotion"],
                    "all_emotions": results["emotion"],
                    "gender": results["dominant_gender"],
                    "gender_probabilities": results.get("gender"),
                    "face_region": results.get("region", {})
                }]
            }

    except ValueError:
        return JSONResponse(status_code=400, content={"status": "error", "message": "No face detected in the provided image."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

if __name__ == "__main__":
    import uvicorn
    # Keep standard execution via script entrypoint as an option
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
