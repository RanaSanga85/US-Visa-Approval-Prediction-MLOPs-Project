"""import os
import sys

def error_message_detail(error, error_detail:sys):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occured python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    return error_message

class USVisaException(Exception):
    def __init__(self, error_message, error_detail):
        super().__init__(error_message)
        self.error_message = error_message_detail(
            error_message, error_detail = error_detail
        )

    def __str__(self):
        return self.error_message
        """

# US_Visa/exception.py

import sys
import traceback

class USVisaException(Exception):
    def __init__(self, error_message: Exception, error_details: sys):
        super().__init__(self.get_detailed_error_message(error_message, error_details))
        self.error_message = self.get_detailed_error_message(error_message, error_details)

    @staticmethod
    def get_detailed_error_message(error: Exception, error_details: sys) -> str:
        _, _, exec_tb = error_details.exc_info()
        line_number = exec_tb.tb_lineno if exec_tb else 'Unknown'
        file_name = exec_tb.tb_frame.f_code.co_filename if exec_tb else 'Unknown'
        error_message = f"Error occurred in script name [{file_name}] line number [{line_number}] error message [{str(error)}]"
        return error_message

    def __str__(self):
        return self.error_message
