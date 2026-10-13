import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal 

# Load the trained ML model
model = joblib.load("Mental_Health_Model.pkl")
top_countries = [
    "India", "USA", "Canada", "Australia", "UK",
    "Germany", "Mexico", "turkey", "France"
]

# Create the FastAPI application
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)
# Define the input data expected from a student
class StudentData(BaseModel):
    Age: int = Field(..., ge=0, le=100)
    Gender: Literal["Male", "Female"]
    Country: str
    Academic_Level: Literal["High School", "Undergraduate", "Graduate", "Postgraduate"]
    Most_Used_Platform: Literal['Facebook', 'LinkedIn', 'Instagram', 'Snapchat', 'Twitter',
       'YouTube', 'TikTok', 'LINE', 'KakaoTalk', 'VKontakte', 'WhatsApp',
       'WeChat']
    Purpose_Of_Use: Literal['Networking', 'Education', 'Entertainment', 'News']
    Avg_Daily_Usage_Hours: float = Field(..., ge=0, le=24)
    Daily_Unlocks: int = Field(..., ge=0)
    Study_Hours: float = Field(..., ge=0, le=24)
    Physical_Activity_Hours: float = Field(..., ge=0, le=24)
    Sleep_Hours_Per_Night: float = Field(..., ge=0, le=24)
    Stress_Level: Literal['Low', 'Medium', 'Very High', 'High']
    Group_countries: str

#describe what we send back
class PredictionResponse(BaseModel):
    predicted_mental_health_score: float 



# Home route
@app.get("/")
def greet():
    return {"message": "Welcome to the Mental Health Prediction API!"}





# Prediction route
@app.post("/predict", response_model=PredictionResponse)
def predict(data: StudentData):

    # Group countries not included in our selected list as "other"
    group_country = (
        data.Country if data.Country in top_countries else "other"
    )

    # Convert the student's input into a DataFrame
    input_row = pd.DataFrame([
        {
            "Age": data.Age,
            "Gender": data.Gender,
            "Country": data.Country,
            "Academic_Level": data.Academic_Level,
            "Most_Used_Platform": data.Most_Used_Platform,
            "Purpose_Of_Use": data.Purpose_Of_Use,
            "Avg_Daily_Usage_Hours": data.Avg_Daily_Usage_Hours,
            "Daily_Unlocks": data.Daily_Unlocks,
            "Study_Hours": data.Study_Hours,
            "Physical_Activity_Hours": data.Physical_Activity_Hours,
            "Sleep_Hours_Per_Night": data.Sleep_Hours_Per_Night,
            "Stress_Level": data.Stress_Level,
            "Group_countries": group_country
        }
    ])

    # Predict the mental health score
    prediction = model.predict(input_row)[0]

    # Return the prediction as JSON
    return PredictionResponse(predicted_mental_health_score=round(float(prediction), 2))
