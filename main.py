from fastapi.responses import FileResponse
from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

model = joblib.load("house_model.pkl")

API_KEY = "mysecret123"

def verify_key(x_api_key: str):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

@app.get("/")
def home():
    return FileResponse("index.html")

@app.post("/predict")
def predict(data: dict, x_api_key: str = Header(None)):

    # AUTH CHECK
    verify_key(x_api_key)

    try:
        # Convert input to DataFrame
        df = pd.DataFrame([data])

        # Prediction
        prediction = model.predict(df)[0]

        # Safety check
        if prediction < 0:
            return {"error": "Invalid input range"}

        return {
            "predicted_price": round(prediction * 100000, 2)
        }

    except Exception as e:
        return {"error": str(e)}
