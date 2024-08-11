import os
from box.exceptions import BoxValueError
import yaml
from stock_portfolio_optimazation import logger  
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any, List, Union
import yfinance as yf
import pandas as pd
import base64

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Reads a YAML file and returns its content as a ConfigBox object."""
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"YAML file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("YAML file is empty")
    except Exception as e:
        raise e

@ensure_annotations
def create_directories(path_to_directories: List[Path], verbose=True):
    """Creates a list of directories."""
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Created directory at: {path}")

@ensure_annotations
def save_json(path: Path, data: dict):
    """Saves data as a JSON file."""
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    logger.info(f"JSON file saved at: {path}")

@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """Loads data from a JSON file and returns it as a ConfigBox object."""
    with open(path) as f:
        content = json.load(f)
    logger.info(f"JSON file loaded successfully from: {path}")
    return ConfigBox(content)

@ensure_annotations
def save_bin(data: Any, path: Path):
    """Saves data as a binary file using joblib."""
    joblib.dump(value=data, filename=path)
    logger.info(f"Binary file saved at: {path}")

@ensure_annotations
def load_bin(path: Path) -> Any:
    """Loads binary data from a file using joblib."""
    data = joblib.load(path)
    logger.info(f"Binary file loaded from: {path}")
    return data

@ensure_annotations
def get_size(path: Path) -> str:
    """Returns the size of the file in KB."""
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"~ {size_in_kb} KB"

def decode_image(imgstring: str, file_name: str):
    """Decodes a base64 image string and saves it as a file."""
    imgdata = base64.b64decode(imgstring)
    with open(file_name, 'wb') as f:
        f.write(imgdata)
        f.close()

def encode_image_into_base64(image_path: str) -> str:
    """Encodes an image file into a base64 string."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read())

@ensure_annotations
def load_stock_data(tickers: List[str], start_date: str, end_date: str) -> pd.DataFrame:
    """Loads stock data from Yahoo Finance."""
    stock_data = yf.download(tickers, start=start_date, end=end_date)
    stock_data.dropna(inplace=True)
    logger.info(f"Stock data for {tickers} loaded successfully")
    return stock_data

@ensure_annotations
def load_csv_data(file_path: Union[str, Path]) -> pd.DataFrame:
    """Loads data from a CSV file."""
    data = pd.read_csv(file_path)
    logger.info(f"CSV data loaded from: {file_path}")
    return data

@ensure_annotations
def calculate_moving_average(data: pd.DataFrame, column: str, window: int) -> pd.DataFrame:
    """Calculates the moving average for a specified column."""
    data[f'MA_{window}'] = data[column].rolling(window=window).mean()
    logger.info(f"Moving average for window {window} calculated")
    return data

@ensure_annotations
def calculate_rsi(data: pd.DataFrame, column: str, window: int = 14) -> pd.DataFrame:
    """Calculates the Relative Strength Index (RSI)."""
    delta = data[column].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))
    logger.info(f"RSI calculated for window {window}")
    return data

@ensure_annotations
def create_technical_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """Creates various technical indicators."""
    data = calculate_moving_average(data, 'Close', 50)
    data = calculate_moving_average(data, 'Close', 200)
    data = calculate_rsi(data, 'Close')
    logger.info("Technical indicators created")
    return data
