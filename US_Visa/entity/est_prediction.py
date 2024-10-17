import os
import sys
from US_Visa.exception import USVisaException
from US_Visa.entity.estimator import USvisaModel
from US_Visa.utils.main_utils import load_object, save_object  # Corrected import for local model operations
from pandas import DataFrame


class USvisaEstimator:
    """
    This class is used to save and retrieve us_visa models locally and to make predictions
    """

    def __init__(self, model_path: str):
        """
        :param model_path: Local path of your model
        """
        self.model_path = model_path
        self.loaded_model: USvisaModel = None

    def is_model_present(self) -> bool:
        """
        Check if the model exists at the given local path
        :return: Boolean indicating if model exists
        """
        try:
            return os.path.exists(self.model_path)
        except Exception as e:
            raise USVisaException(e, sys)

    def load_model(self) -> USvisaModel:
        """
        Load the model from the local model_path
        :return: Loaded model
        """
        try:
            if not self.is_model_present():
                raise USVisaException(f"Model not found at {self.model_path}", sys)
            return load_object(self.model_path)  # Using load_object from main_utils to load model
        except Exception as e:
            raise USVisaException(e, sys)

    def save_model(self, from_file: str, remove: bool = False) -> None:
        """
        Save the model to the local model_path
        :param from_file: Your local system model path
        :param remove: If True, it will delete the model from the original location after saving
        """
        try:
            save_object(self.model_path, from_file)  # Using save_object from main_utils to save model
            if remove:
                os.remove(from_file)  # Remove the model locally if specified
        except Exception as e:
            raise USVisaException(e, sys)

    def predict(self, dataframe: DataFrame):
        """
        Make predictions using the loaded model
        :param dataframe: DataFrame containing input data
        :return: Model predictions
        """
        try:
            if self.loaded_model is None:
                self.loaded_model = self.load_model()
            return self.loaded_model.predict(dataframe=dataframe)
        except Exception as e:
            raise USVisaException(e, sys)
