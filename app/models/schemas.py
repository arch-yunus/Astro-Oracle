from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from enum import Enum

class FocusArea(str, Enum):
    GENERAL = "general"
    CAREER = "career"
    RELATIONSHIPS = "relationships"
    STRATEGIC = "strategic"
    HEALTH = "health"

class PlanetInfo(BaseModel):
    sign: str
    house: int
    is_retrograde: bool = False

class ChartData(BaseModel):
    sun: PlanetInfo
    moon: PlanetInfo
    mercury: PlanetInfo
    venus: PlanetInfo
    mars: PlanetInfo
    jupiter: PlanetInfo
    saturn: PlanetInfo
    # Additional planets/points can be added as Extra
    class Config:
        extra = "allow"

class NatalRequest(BaseModel):
    user_id: str
    focus_area: FocusArea = FocusArea.GENERAL
    chart_data: Dict[str, Any]  # Flexible dict or use ChartData model
    language: str = "tr"

class InterpretationResponse(BaseModel):
    interpretation: str
    metadata: Dict[str, Any]
    citations: List[Dict[str, Any]] = []

class HealthResponse(BaseModel):
    status: str
    version: str
    engine: str
