from flask import Flask, jsonify, send_file, render_template,request
import pandas as pd
import matplotlib.pyplot as plt
import os
from openai import OpenAI
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np

# Hier starten wir die Flask-App – quasi das "Herz" des Webservers.

app = Flask(__name__)

# Hier wird der OpenAI-Client erstellt.

client = OpenAI(api_key="your api_key")
 

# Liest die CSV-Datei mit den Bildungs- und Einkommensdaten in einen DataFrame.
df = pd.read_csv("education_income.csv")



# "Education Level" (z. B. "University", "High School") wird in Zahlen umgewandelt.So kann der Algorithmus damit rechnen.

label_encoder = LabelEncoder()
df["Education_level_Encoded"] = label_encoder.fit_transform(df["Education Level"])

# Das Average Income wird in drei Kategorien eingeteilt: Low, Medium, High.

income_bins = pd.qcut(df["Average Income"], q=3, labels=["Low" , "Mediun", "High"])
df["Income_category"] = income_bins

"""
Education Level | Average Income | Education_Level_Encoded | Income_Category
****************************************************************************
Bachelor        | 32000          | 0                       | Low
Master          | 52000          | 1                       | Medium
PhD             | 80000          | 2                       | High
"""


# Der RandomForestClassifier wird mit 100 Entscheidungsbäumen trainiert.
X = df[["Education_level_Encoded"]]
y = df["Income_category"]
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X,y)


# Lädt die HTML-Startseite ("index.html" muss im templates-Ordner liegen).

@app.route("/")
def home():
    return render_template("index.html")



# Gruppiert die Daten nach Bildungsgrad....Berechnet Mean pro Bildungsgrad....Gibt die Ergebnisse als JSON zurück.

@app.route("/analysis")
def analysis():
    grouped = df.groupby("Education Level")["Average Income"].mean().to_dict()
    return jsonify(grouped)



# Erstellt ein Balkendiagramm.....Speichert es als diagram.png im static-Ordner......Schickt es als PNG zurück.

@app.route("/chart")
def chart():
    grouped = df.groupby("Education Level")["Average Income"].mean().sort_values()

    plt.figure(figsize=(6, 4))
    grouped.plot(kind="bar", title="Average Income by Education Level", color="skyblue")
    plt.ylabel("Income in €")
    plt.tight_layout()

    os.makedirs("static", exist_ok=True)
    chart_path = "static/diagram.png"
    plt.savefig(chart_path)
    plt.close()

    return send_file(chart_path, mimetype="image/png")



# Ki generiert Balkendiagram (Dall-E)
@app.route("/chart-styled")
def chart_styled():
    import requests

    # Daten auswerten
    grouped = df.groupby("Education Level")["Average Income"].mean().sort_values()
    labels = list(grouped.index)
    values = list(grouped.values)

    prompt = (
        "Create a clean, modern bar chart infographic showing average income by education level. "
        f"The categories are: {', '.join(labels)}. "
        f"The corresponding incomes in euros are: {', '.join(str(round(v,2)) for v in values)}. "
        "Use dark red tones, nature background, professional flat design, readable labels, and title 'Average Income by Education Level'."
    )

    # Dall-E generiert das Bild
    result = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024"
    )

    # Die von DALL·E generierte Bild-URL wird abgerufen. 
    image_url = result.data[0].url

    # Das Bild wird als static/diagram_styled.png gespeichert.
    styled_chart_path = "static/diagram_styled.png"
    os.makedirs("static", exist_ok=True)
    img_data = requests.get(image_url).content
    with open(styled_chart_path, "wb") as f:
        f.write(img_data)

    return send_file(styled_chart_path, mimetype="image/png")



#Vorhersage

@app.route("/predict", methods=["GET"])
def predict():
    """
    Example usage: /predict?education_level=University
    """
    education_level = request.args.get("education_level")
    if not education_level:
        return jsonify({"error": "Please provide education_level"}), 400

    try:
        encoded_level = label_encoder.transform([education_level])[0]
    except ValueError:
        return jsonify({"error": f"Unknown education level: {education_level}"}), 400

    predicted_category = model.predict(np.array([[encoded_level]]))[0]
    return jsonify({
        "education_level": education_level,
        "predicted_income_category": predicted_category
    })


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
