from fastapi.responses import FileResponse
from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

model = joblib.load("house_model.pkl")

@app.get("/")
def home():
    return FileResponse("index.html")

@app.post("/predict")
def predict(data: dict):
    try:
        df = pd.DataFrame([data])
        prediction = model.predict(df)[0]

        if prediction < 0:
            return {"error": "Invalid input range"}

        return {
            "predicted_price": round(prediction * 100000, 2)
        }

    except:
        return {"error": "Invalid input"}
