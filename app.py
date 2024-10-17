import traceback
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from uvicorn import run as app_run
from typing import Optional
from pydantic import BaseModel
import logging

from US_Visa.constants import APP_HOST, APP_PORT
from US_Visa.pipeline.prediction_pipeline import USvisaData, USvisaClassifier
from US_Visa.pipeline.training_pipeline import TrainPipeline
from US_Visa.exception import USVisaException

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize FastAPI app
app = FastAPI()

# Static files and templates setup
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory='templates')

# CORS setup
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model for US Visa form data
class USVisaForm(BaseModel):
    continent: Optional[str]
    education_of_employee: Optional[str]
    has_job_experience: Optional[str]
    requires_job_training: Optional[str]
    no_of_employees: Optional[int]
    company_age: Optional[int]
    region_of_employment: Optional[str]
    prevailing_wage: Optional[float]
    unit_of_wage: Optional[str]
    full_time_position: Optional[str]

    @classmethod
    async def from_form(cls, request: Request):
        form = await request.form()
        return cls(
            continent=form.get("continent"),
            education_of_employee=form.get("education_of_employee"),
            has_job_experience=form.get("has_job_experience"),
            requires_job_training=form.get("requires_job_training"),
            no_of_employees=int(form.get("no_of_employees")) if form.get("no_of_employees") else None,
            company_age=int(form.get("company_age")) if form.get("company_age") else None,
            region_of_employment=form.get("region_of_employment"),
            prevailing_wage=float(form.get("prevailing_wage")) if form.get("prevailing_wage") else None,
            unit_of_wage=form.get("unit_of_wage"),
            full_time_position=form.get("full_time_position"),
        )

@app.get("/", tags=["home"])
async def index(request: Request):
    return templates.TemplateResponse(
        "usvisa.html", {"request": request, "context": "Rendering"}
    )

@app.get("/train", response_class=HTMLResponse)
async def train_route():
    try:
        logging.info("Training pipeline initiated.")
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        logging.info("Training completed successfully.")
        return Response("Training successful!")
    except Exception as e:
        error_message = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
        logging.error(f"Error during training: {error_message}")
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

@app.post("/", response_class=HTMLResponse)
async def predict_route(request: Request):
    try:
        form_data = await USVisaForm.from_form(request)
        logging.info("Form data received and parsed.")

        usvisa_data = USvisaData(
            continent=form_data.continent,
            education_of_employee=form_data.education_of_employee,
            has_job_experience=form_data.has_job_experience,
            requires_job_training=form_data.requires_job_training,
            no_of_employees=form_data.no_of_employees,
            company_age=form_data.company_age,
            region_of_employment=form_data.region_of_employment,
            prevailing_wage=form_data.prevailing_wage,
            unit_of_wage=form_data.unit_of_wage,
            full_time_position=form_data.full_time_position,
        )

        # Prepare data for prediction
        usvisa_df = usvisa_data.get_usvisa_input_data_frame()
        logging.info(f"Input DataFrame prepared: {usvisa_df}")

        model_predictor = USvisaClassifier()
        logging.info("USvisaClassifier initialized.")

        # Get prediction
        prediction_value = model_predictor.predict(dataframe=usvisa_df)[0]
        logging.info(f"Prediction value: {prediction_value}")

        # Map prediction to visa status
        status = "Visa-approved" if prediction_value == 1 else "Visa Not-Approved"

        logging.info(f"Prediction result: {status}")

        # Render the response
        return templates.TemplateResponse(
            "usvisa.html",
            {"request": request, "context": status},
        )
    except USVisaException as ue:
        error_message = ue.error_message
        logging.error(f"USVisaException: {error_message}")
        return templates.TemplateResponse(
            "usvisa.html",
            {"request": request, "context": f"Error: {error_message}"},
        )
    except Exception as e:
        error_message = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
        logging.error(f"Unexpected error: {error_message}")
        return templates.TemplateResponse(
            "usvisa.html",
            {"request": request, "context": "An unexpected error occurred."},
        )

if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)
