from enum import Enum
from pydantic import BaseModel, Field

class AnalysisStatus(str, Enum):
    OK = "ok"
    UNABLE_TO_ASSESS = "unable_to_assess"

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
        min_length=2,
        max_length=4,
        description=(
            "List of 2-4 observable physique strengths. " \
            "Each item should be one short sentence, ideally under 15 words. " \
            "Keep each item focused on one clear idea."
        )
    )
    weak_points: list[str] = Field(
        ...,
        min_length=0,
        max_length=3,
        description=(
            "List of 0-3 observable physique weaknesses. " \
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

class ImprovementFocus(BaseModel):
    top_priorities: list[str] = Field(
        ...,
        min_length=1,
        max_length=3,
        description=(
            "List of 1-3 improvement priorities. " \
            "Each item should be one short sentence, ideally under 15 words. " \
            "Keep each item focused on one clear idea."
        )
    )

class AssessmentLimitations(BaseModel):
    photo_limitations: list[str] = Field(
        ...,
        min_length=0,
        max_length=3,
        description=(
            "List of 0-3 image-specific limitations that reduce assessment quality. " \
            "Each item should be one short sentence, ideally under 15 words."
        )
    )
    interpretation_notes: list[str] = Field(
        ...,
        min_length=0,
        max_length=2,
        description=(
            "List of 0-2 notes explaining how the image should be interpreted carefully. " \
            "Each item should be one short sentence, ideally under 15 words."
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
        description="Short note about image quality or visual limitations affecting the assessment."
    )
    goal: GoalSection
    physique_assessment: PhysiqueAssessment
    improvement_focus: ImprovementFocus
    assessment_limitations: AssessmentLimitations
