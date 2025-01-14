from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class WeatherData(BaseModel):
    location_name: List[str] = Field(default=[], description="List of location names")
    coordinates: List[tuple] = Field(default=[], description="List of geographic coordinates (latitude, longitude)")
    weather_info: List[Dict[str, Any]] = Field(default=[], description="List of lists of detailed weather information")


class DemandData(BaseModel):
    timestamp: List[str] = Field(
        default=[], description="List of timestamps in ISO 8601 format"
    )
    demand_value: List[float] = Field(
        default=[], description="List of demand values in relevant units"
    )
    region: List[str] = Field(
        default=[], description="List of region identifiers"
    )


class PlantStatus(BaseModel):
    unit_name: List[str] = Field(default=[], description="List of unit names")
    status: List[str] = Field(
        default=[], description="List of plant statuses (e.g., 'operational', 'maintenance', 'offline')"
    )
    output: List[float] = Field(
        default=[], description="List of plant outputs in relevant units"
    )
    last_maintenance: List[str] = Field(
        default=[], description="Date of last maintenance of each unit"
    )
    next_maintenance: List[str] = Field(
        default=[], description="Date of next maintenance of each unit"
    )


class CompatibilityCheckResult(BaseModel):
    check: str = Field(..., 
                       description="A description of the specific compatibility check performed.")
    result: bool = Field(..., 
                         description="The outcome of the compatibility check: True if compatible, False otherwise.")
    explanation: Optional[str] = Field(
        "-", 
        description="Additional details or reasons for the result, especially if the check failed.")
    action: str = Field("-", 
                        description="Recommended action to fix the incompatible check between the input and external data source")


# Define a list of CompatibilityCheckResultOutput items
class CompatibilityCheckResultOutput(BaseModel):
    results: List[CompatibilityCheckResult] = Field(
        ..., description="A list of compatibility check results, including checks, results, explanations, and actions."
    )
