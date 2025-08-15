
Flask-Webanwendung zur Analyse und Vorhersage von Einkommen auf Basis von Bildungsdaten
=======================================================================================
  4. Mehrere HTTP-Routen bereitstellt:
       - '/'              → Startseite (index.html) anzeigen
       - '/analysis'      → Durchschnittseinkommen pro Bildungsgrad als JSON zurückgeben
       - '/chart'         → Balkendiagramm mit Matplotlib erstellen und ausgeben
       - '/chart-styled'  → Gestyltes Diagramm mit OpenAI DALL·E generieren
       - '/predict'       → Einkommenskategorie für einen Bildungsgrad vorhersagen
  5. Folgende Bibliotheken integriert:
       - Flask für Routing & Webserver
       - Pandas für Datenverarbeitung
       - Matplotlib für Diagramme
       - OpenAI API für KI-generiertes Diagrammdesign
       - Scikit-learn für maschinelles Lernen
       - NumPy für Array-Berechnungen

Voraussetzungen:
----------------
- Die Datei `education_income.csv` muss im Projektverzeichnis liegen.
- Ein `templates`-Ordner mit `index.html` muss vorhanden sein.
- Ein gültiger OpenAI API-Key muss für den `OpenAI`-Client gesetzt werden.


* Installations
* pip install pandas
* pip install numpy
* pip install scikit-learn
* pip install matplotlib
* pip install openai
* pip install flask
* pip install requests



Abschluss_KI_project/
├── app.py                  # Flask API
├──templates
|  |__index.html            # Simple HTML frontend
├── education_income.csv    # Sample dataset
├── static/
|   |__diagram_styled.png   # KI generated chart image
│   └── diagram.png         # Generated chart image
└── streamlit_app.py        # Streamlit dashboard (optional)


* To Run streamlit_app:  python -m streamlit run streamlit_app.py
* To check Random Forest predictions :http://127.0.0.1:5000/predict?education_level= University / High School