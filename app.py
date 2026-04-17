from flask import Flask, request, render_template_string
import joblib
import pandas as pd
import os

app = Flask(__name__)
model = joblib.load("house_model.pkl")

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>AI House Predictor</title>
<style>
body { font-family: Arial; background: #f4f6f8; display:flex; justify-content:center; align-items:center; height:100vh; }
.card { background:white; padding:30px; border-radius:12px; box-shadow:0px 4px 20px rgba(0,0,0,0.1); width:350px; }
input, button { width:100%; padding:10px; margin:5px 0; border-radius:6px; }
button { background:#4CAF50; color:white; border:none; }
</style>
</head>

<body>
<div class="card">
<h2>🏠 House Price AI</h2>

<form method="POST">
<input name="MedInc" placeholder="MedInc (1–10)">
<input name="HouseAge" placeholder="HouseAge">
<input name="AveRooms" placeholder="AveRooms">
<input name="AveBedrms" placeholder="AveBedrms">
<input name="Population" placeholder="Population">
<input name="AveOccup" placeholder="AveOccup">
<input name="Latitude" placeholder="Latitude (32–42)">
<input name="Longitude" placeholder="Longitude (-124 to -114)">
<button type="submit">Predict 💰</button>
</form>

{% if result %}
<h3>{{result}}</h3>
{% endif %}

</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        try:
            df = pd.DataFrame([{
                "MedInc": float(request.form["MedInc"]),
                "HouseAge": float(request.form["HouseAge"]),
                "AveRooms": float(request.form["AveRooms"]),
                "AveBedrms": float(request.form["AveBedrms"]),
                "Population": float(request.form["Population"]),
                "AveOccup": float(request.form["AveOccup"]),
                "Latitude": float(request.form["Latitude"]),
                "Longitude": float(request.form["Longitude"])
            }])

            pred = model.predict(df)[0]

            if pred < 0:
                result = "⚠️ Invalid input range"
            else:
                result = f"💰 Price: ${pred*100000:,.2f}"

        except:
            result = "❌ Invalid input"

    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
