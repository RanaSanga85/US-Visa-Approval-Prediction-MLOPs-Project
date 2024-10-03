import logging
import os

from from_root import from_root
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" #creates log file name
log_dir = 'logs' #specifies folder where log files will be stored

logs_path = os.path.join(from_root(), log_dir, LOG_FILE)#project_root/logs/MM_DD_YYYY_HH_MM_SS.log
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename = logs_path,
    format = "[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    # it will capture all messages from DEBUG level and above (i.e., DEBUG, INFO, WARNING, ERROR, CRITICAL).
    level = logging.DEBUG,

)