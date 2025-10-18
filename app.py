from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uvicorn import run as app_run

from typing import Optional

# Import your modules (make sure paths are correct)
from src.constants import APP_HOST, APP_PORT
from src.pipline.prediction_pipeline import VehicleData, VehicleDataClassifier
from src.pipline.training_pipeline import TrainPipeline

# Initialize FastAPI app
app = FastAPI()

# Mount static directory (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

# Allow CORS from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------
# Data form handler
# -------------------------------------------
class DataForm:
    """
    Handles and processes incoming form data.
    """
    def __init__(self, request: Request):
        self.request: Request = request
        self.Gender: Optional[int] = None
        self.Age: Optional[int] = None
        self.Driving_License: Optional[int] = None
        self.Region_Code: Optional[float] = None
        self.Previously_Insured: Optional[int] = None
        self.Annual_Premium: Optional[float] = None
        self.Policy_Sales_Channel: Optional[float] = None
        self.Vintage: Optional[int] = None
        self.Vehicle_Age_lt_1_Year: Optional[int] = None
        self.Vehicle_Age_gt_2_Years: Optional[int] = None
        self.Vehicle_Damage_Yes: Optional[int] = None

    async def get_vehicle_data(self):
        """
        Fetch and assign form data to attributes.
        """
        form = await self.request.form()

        self.Gender = int(form.get("Gender"))
        self.Age = int(form.get("Age"))
        self.Driving_License = int(form.get("Driving_License"))
        self.Region_Code = float(form.get("Region_Code"))
        self.Previously_Insured = int(form.get("Previously_Insured"))
        self.Annual_Premium = float(form.get("Annual_Premium"))
        self.Policy_Sales_Channel = float(form.get("Policy_Sales_Channel"))
        self.Vintage = int(form.get("Vintage"))
        self.Vehicle_Damage_Yes = int(form.get("Vehicle_Damage_Yes"))

        # Handle new single-select Vehicle Age field
        vehicle_age = form.get("Vehicle_Age")
        self.Vehicle_Age_lt_1_Year = 1 if vehicle_age == "lt_1" else 0
        self.Vehicle_Age_gt_2_Years = 1 if vehicle_age == "gt_2" else 0
        # For "btw_1_2", both values are 0 (default)

# -------------------------------------------
# Routes
# -------------------------------------------

@app.get("/", tags=["UI"])
async def index(request: Request):
    """
    Renders the main form page.
    """
    return templates.TemplateResponse("vehicledata.html", {"request": request, "context": "Rendering"})


@app.post("/", tags=["Prediction"])
async def predict_route(request: Request):
    """
    Handles form submission and prediction.
    """
    try:
        form = DataForm(request)
        await form.get_vehicle_data()

        # Wrap form data into schema
        vehicle_data = VehicleData(
            Gender=form.Gender,
            Age=form.Age,
            Driving_License=form.Driving_License,
            Region_Code=form.Region_Code,
            Previously_Insured=form.Previously_Insured,
            Annual_Premium=form.Annual_Premium,
            Policy_Sales_Channel=form.Policy_Sales_Channel,
            Vintage=form.Vintage,
            Vehicle_Age_lt_1_Year=form.Vehicle_Age_lt_1_Year,
            Vehicle_Age_gt_2_Years=form.Vehicle_Age_gt_2_Years,
            Vehicle_Damage_Yes=form.Vehicle_Damage_Yes,
        )

        vehicle_df = vehicle_data.get_vehicle_input_data_frame()

        # Run prediction
        model = VehicleDataClassifier()
        prediction = model.predict(vehicle_df)[0]

        result = "Response-Yes" if prediction == 1 else "Response-No"

        return templates.TemplateResponse(
            "vehicledata.html",
            {"request": request, "context": result}
        )

    except Exception as e:
        return templates.TemplateResponse(
            "vehicledata.html",
            {"request": request, "context": f"Error: {e}"}
        )


@app.get("/train", tags=["Training"])
async def train_model():
    """
    Triggers the training pipeline.
    """
    try:
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        return Response("Training completed successfully.")
    except Exception as e:
        return Response(f"Training failed: {e}")


# -------------------------------------------
# App Entry Point
# -------------------------------------------

if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)
