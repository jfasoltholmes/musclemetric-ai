from enum import Enum
from pydantic import BaseModel, Field

class AnalysisStatus(str, Enum):
    OK = "ok"
    UNABLE_TO_ASSESS = "unable_to_assess"

class ConfidenceLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class GoalRecommendation(str, Enum):
    BULK = "bulk"
    CUT = "cut"
    MAINTAIN = "maintain"
    RECOMP = "recomp"
    UNABLE_TO_ASSESS = "unable_to_assess"

class GoalSection(BaseModel):
    recommendation: GoalRecommendation
    rationale: str = Field(
        ...,
        description="2-3 sentence explanation for the recommendation."
    )
    action_summary: str = Field(
        ...,
        description="1-3 short sentences explaining how to approach the recommended goal in practical terms."
    )

class PhysiqueAssessment(BaseModel): 
    strong_points: list[str] = Field(
        ...,
        description=(
            "List of 2-4 observable physique strengths. " \
            "Each item should be one short sentence, ideally under 15 words. " \
            "Keep each item focused on one clear idea."
        )
    )
    weak_points: list[str] = Field(
        ...,
        description=(
            "List of 1-4 observable physique weaknesses. " \
            "Each item should be one short sentence, ideally under 15 words. " \
            "Keep each item focused on one clear idea."
        )
    )
    fat_distribution: str = Field(
        ...,
        description=(
            "Short explanation of where body fat appears to be concentrated " \
            "(e.g., lower abdomen, waist, chest). Do NOT include percentages."
        )
    )

class BodyCompositionAnalysis(BaseModel):
    status: AnalysisStatus
    body_fat_range: str = Field(
        ...,
        description="Estimated body fat range in format '10-12%'. No words, no symbols other " \
        "than '-' and '%'. If unable to assess, return 'unable_to_assess'."
    )
    image_quality_note: str = Field(
        ...,
        description="Short note about image quality or limitations affecting confidence."
    )
    confidence: ConfidenceLevel
    goal: GoalSection
    physique_assessment: PhysiqueAssessment
