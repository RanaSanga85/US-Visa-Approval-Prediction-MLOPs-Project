"""
import os
import sys
from US_Visa.exception import USVisaException
from US_Visa.entity.estimator import USvisaModel
from US_Visa.utils.main_utils import load_object, save_object  # Corrected import for local model operations
from pandas import DataFrame


class USvisaEstimator:
    
    This class is used to save and retrieve us_visa models locally and to make predictions
    

    def __init__(self, model_path: str):
        
        :param model_path: Local path of your model
        
        self.model_path = model_path
        self.loaded_model: USvisaModel = None

    def is_model_present(self) -> bool:
        
        Check if the model exists at the given local path
        :return: Boolean indicating if model exists
        
        try:
            return os.path.exists(self.model_path)
        except Exception as e:
            raise USVisaException(e, sys)

    def load_model(self) -> USvisaModel:
        
        Load the model from the local model_path
        :return: Loaded model
        
        try:
            if not self.is_model_present():
                raise USVisaException(f"Model not found at {self.model_path}", sys)
            return load_object(self.model_path)  # Using load_object from main_utils to load model
        except Exception as e:
            raise USVisaException(e, sys)

    def save_model(self, from_file: str, remove: bool = False) -> None:
        
        Save the model to the local model_path
        :param from_file: Your local system model path
        :param remove: If True, it will delete the model from the original location after saving
        
        try:
            save_object(self.model_path, from_file)  # Using save_object from main_utils to save model
            if remove:
                os.remove(from_file)  # Remove the model locally if specified
        except Exception as e:
            raise USVisaException(e, sys)

    def predict(self, dataframe: DataFrame):
        
        Make predictions using the loaded model
        :param dataframe: DataFrame containing input data
        :return: Model predictions
        
        try:
            if self.loaded_model is None:
                self.loaded_model = self.load_model()
            return self.loaded_model.predict(dataframe=dataframe)
        except Exception as e:
            raise USVisaException(e, sys)
"""




import os
import sys
from US_Visa.exception import USVisaException
from US_Visa.entity.estimator import USvisaModel
from US_Visa.utils.main_utils import load_object, save_object
from pandas import DataFrame
import logging
from US_Visa.entity.config_entity import USvisaPredictorConfig  # Import the config class


class USvisaEstimator:
    """
    This class is used to save and retrieve us_visa models locally and to make predictions.
    """

    def __init__(self, predictor_config: USvisaPredictorConfig):
        """
        :param predictor_config: An instance of USvisaPredictorConfig that provides model path.
        """
        self.model_path = predictor_config.model_file_path  # Get the model path from the config
        self.loaded_model: USvisaModel = None
        logging.info(f"USvisaEstimator initialized with model path: {self.model_path}")

    def is_model_present(self) -> bool:
        """
        Check if the model exists at the given local path.
        :return: Boolean indicating if model exists.
        """
        try:
            presence = os.path.exists(self.model_path)
            logging.info(f"Model presence check at {self.model_path}: {presence}")
            return presence
        except Exception as e:
            logging.error(f"Error checking model presence: {e}")
            raise USVisaException(e, sys)

    def load_model(self) -> USvisaModel:
        """
        Load the model from the local model_path.
        :return: Loaded model.
        """
        try:
            if not self.is_model_present():
                raise USVisaException(f"Model not found at {self.model_path}", sys)
            
            model = load_object(self.model_path)  # Using load_object from main_utils to load model
            logging.info(f"Model loaded successfully from {self.model_path}")

            if not isinstance(model, USvisaModel):
                raise TypeError(f"Loaded object is not a USvisaModel instance, got {type(model)} instead.")
            
            return model
        except Exception as e:
            logging.error(f"Failed to load model: {e}")
            raise USVisaException(e, sys)

    def save_model(self, model_object: object, remove: bool = False) -> None:
        """
        Save the model to the local model_path.
        :param model_object: The trained model object to save.
        :param remove: If True, it will delete the model from the original location after saving.
        """
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            
            save_object(self.model_path, model_object)  # Using save_object from main_utils to save model
            logging.info(f"Model saved successfully to {self.model_path}")
            
            if remove:
                os.remove(self.model_path)  # Remove the model locally if specified
                logging.info(f"Original model file {self.model_path} removed.")
        except Exception as e:
            logging.error(f"Error saving model: {e}")
            raise USVisaException(e, sys)

    def predict(self, dataframe: DataFrame):
        """
        Make predictions using the loaded model.
        :param dataframe: DataFrame containing input data.
        :return: Model predictions.
        """
        try:
            if self.loaded_model is None:
                logging.info("Model not loaded. Attempting to load the model.")
                self.loaded_model = self.load_model()
                logging.info("Model loaded successfully.")

            if dataframe.empty:
                raise ValueError("Input dataframe is empty.")

            logging.info(f"Input DataFrame shape: {dataframe.shape}")
            result = self.loaded_model.predict(dataframe=dataframe)
            logging.info(f"Prediction result: {result}")

            if result is None:
                raise ValueError("Model returned None for predictions.")

            return result

        except Exception as e:
            logging.error(f"Error during prediction: {e}")
            raise USVisaException(e, sys) from e

