# Human Activity Recognition - Pattern Recognition Project

This project contains a FastAPI backend and React frontend for a Human Activity Recognition dashboard.
It simulates mobile accelerometer and gyroscope readings, extracts numeric features, and classifies
activities such as walking, running, sitting, standing, and stairs.

## Project Idea

Human Activity Recognition uses phone sensor data to recognize what a person is doing. The app uses:

- Accelerometer values: `x`, `y`, `z`
- Gyroscope values: `x`, `y`, `z`
- Extracted features: magnitude, motion intensity, and tilt angle
- Classifier: trained centroid HAR classifier
- Output classes: `WALKING`, `RUNNING`, `SITTING`, `STANDING`, `STAIRS`

The backend loads `backend/model/har_model.json`. If that file is missing, the API uses safe built-in
sensor profiles so the demo still works.

## File Architecture

```text
human-activity-recog-pattern/
  backend/
    app/
      ML/
        features.py
        model.py
      models/
        schemas.py
      routers/
        predict.py
      database.py
      main.py
      utils.py
    model/
      har_model.json
    train_model.py
    DockerFile
    requirements.txt
  frontend/
    src/
      components/
        RealTimeSection.jsx
        ResultCard.jsx
        UploadSection.jsx
        ConfusionMatrix.jsx
      App.jsx
      main.jsx
      styles.css
    index.html
    package.json
  docker-compose.yml
```

## Model Training

The training script creates a synthetic mobile sensor dataset from realistic accelerometer and gyroscope
profiles, extracts features, computes class centroids, evaluates the classifier, and saves the model.

```bash
cd backend
python train_model.py
```

Current saved model:

- Model: Trained Centroid HAR Classifier
- Samples: 800
- Accuracy: 93.25%
- Features: 10
- Evaluation: confusion matrix shown in the dashboard

This keeps the project easy to run while still showing the full pattern-recognition pipeline:
data -> features -> model -> prediction -> evaluation.

## Run Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://127.0.0.1:5173`.
