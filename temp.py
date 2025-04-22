import os
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)





list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    "src/prediction.py",
    "src/schemas.py",
    "DataSets",
    "requirements.txt"
    ".env",
    ".env.example",
    "frontend.py",
    "backend.py",
]





for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(name=filedir, exist_ok=True)
        logging.info(f"The filedir: {filedir} created.")

    if (not os.path.exists(filepath)):
        if filename in ["DataSets"]:
            os.makedirs(name=filename, exist_ok=True)
            logging.info(f"The filedir: {filedir} created.")
        with open(file=filepath, mode="w") as f:
            logging.info(f"The filepath: {filedir} created.")
            pass
    else:
        print("file already exists")

