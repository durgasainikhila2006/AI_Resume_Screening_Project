import joblib
import pandas as pd

# Load Model
model = joblib.load("models/logistic_regression_model.pkl")
education_encoder = joblib.load("models/education_encoder.pkl")


def predict_candidate(candidate):

    # Print extracted education
    print("Education Extracted:", candidate["Education"])

    # Encode Education
    try:
        candidate["Education"] = education_encoder.transform(
            [candidate["Education"]]
        )[0]

    except ValueError:
        print("Unknown Education:", candidate["Education"])

        # Temporary default value
        candidate["Education"] = 0

    # Convert to DataFrame
    df = pd.DataFrame([candidate])

    # Predict
    prediction = model.predict(df)

    return prediction[0]