import numpy as np
from tools.BaseToolkit import BaseToolkit
from langchain_core.tools import tool

@tool
def calculate_mape(actual, predicted):
    """
    Calculate the Mean Absolute Percentage Error (MAPE).
    
    Args:
        actual (list or np.array): Observed total output values (actual values).
        predicted (list or np.array): Forecasted demand values (predicted values).
    
    Returns:
        float: MAPE value as a percentage.
    """
    actual, predicted = np.array(actual), np.array(predicted)
    if len(actual) > len(predicted):
        actual = actual[:len(predicted)]
    
    if len(predicted) > len(actual):
        predicted = predicted[:len(actual)]
    
    return np.mean(np.abs((actual - predicted) / actual)) * 100

@tool
def calculate_mae(actual, predicted):
    """
    Calculate the Mean Absolute Error (MAE).
    
    Args:
        actual (list or np.array): Observed total output values (actual values).
        predicted (list or np.array): Forecasted demand values (predicted values).
    
    Returns:
        float: MAE value.
    """
    actual, predicted = np.array(actual), np.array(predicted)
    # Ensure lengths match
    if len(actual) > len(predicted):
        actual = actual[:len(predicted)]
    return np.mean(np.abs(actual - predicted))

@tool
def calculate_rmse(actual, predicted):
    """
    Calculate the Root Mean Squared Error (RMSE).
    
    Args:
        actual (list or np.array): Observed total output values (actual values).
        predicted (list or np.array): Forecasted demand values (predicted values).
    
    Returns:
        float: RMSE value.
    """
    actual, predicted = np.array(actual), np.array(predicted)
    # Ensure lengths match
    if len(actual) > len(predicted):
        actual = actual[:len(predicted)]
    return np.sqrt(np.mean((actual - predicted) ** 2))

@tool
def calculate_r2_score(actual, predicted):
    """
    Calculate the R-squared (Coefficient of Determination).
    
    Args:
        actual (list or np.array): Observed total output values (actual values).
        predicted (list or np.array): Forecasted demand values (predicted values).
    
    Returns:
        float: R-squared value.
    """
    actual, predicted = np.array(actual), np.array(predicted)
    # Ensure lengths match
    if len(actual) > len(predicted):
        actual = actual[:len(predicted)]
    ss_total = np.sum((actual - np.mean(actual)) ** 2)
    ss_residual = np.sum((actual - predicted) ** 2)
    return 1 - (ss_residual / ss_total) if ss_total != 0 else np.nan


class KPIToolkit(BaseToolkit):
    """
    Toolkit for calculating various Key Performance Indicators (KPIs) 
    between observed total output and forecasted demand.
    """
    def __init__(self):
        super().__init__({
            "calculate_mape": calculate_mape,
            "calculate_mae": calculate_mae,
            "calculate_rmse": calculate_rmse,
            "calculate_r2_score": calculate_r2_score,
        })