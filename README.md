# US-Visa-Approval-Prediction-MLOPs-Project

This repository contains a machine learning project aimed at predicting US visa approval using various data processing, transformation, and machine learning techniques. The project is structured using modular components for better readability and reusability. The project also integrates with MongoDB for data storage and uses Evidently for model evaluation.

## Project Structure
The main folder for this project is the US_Visa directory, which is organized into several subfolders and components for data ingestion, transformation, evaluation, and model training. Below is an overview of the key directories and files:

### US_Visa/
The root folder containing the main components and configurations of the project.

#### 1. components/
This folder contains the core modules for the machine learning pipeline, including:
<li>data_ingestion.py: Handles the ingestion of data from MongoDB or other sources.
<li>data_transformation.py: Responsible for transforming raw data into a format suitable for modeling.
<li>data_validation.py: Ensures data quality by validating the input data.
<li>model_evaluation.py: Uses Evidently for evaluating model performance.
<li>model_trainer.py: Contains code for training machine learning models.

#### 2. configuration/
This folder contains files related to configurations and connections, including:
`mongo_db_connect.py`: Handles the connection to the MongoDB database and the extraction of data from MongoDB for model training.

#### 3. entity/
This folder contains custom classes and entities used across the project, including model handling and prediction entities.

#### 4. pipeline/
Contains scripts for the end-to-end execution of the pipeline, including prediction and model loading.

#### 5. exception/
Contains the custom exception class USVisaException for handling errors across the project.

#### 6. logger/
Contains the logging configuration for the project, enabling structured and meaningful logging for easier debugging.

#### 7. utils/
This folder contains utility functions, including:
`main_utils.py`: Contains utility functions for saving/loading models and other common tasks.
`config/`:Contains configuration files such as config.yaml which defines global settings like database configurations, file paths, and model parameters.

## Requirements
The following Python libraries are required to run this project:

pandas
numpy
scikit-learn
evidently
pymongo
pydantic
flask
pyyaml
logging
matplotlib
seaborn
You can install these dependencies via the requirements.txt file:
`pip install -r requirements.txt`

## Getting Started
#### Step 1: Clone the repository
<br> `git clone https://github.com/your-username/us-visa-approval-prediction.git`
<br> `cd us-visa-approval-prediction`

#### Step 2: Setup MongoDB Connection
You will need to configure the MongoDB connection by editing the file under `US_Visa/configuration/mongo_db_connection.py`. This will allow the pipeline to fetch the visa data from MongoDB for further processing.

