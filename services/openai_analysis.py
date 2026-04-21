from openai import OpenAI
from schemas.analysis import BodyCompositionAnalysis

client = OpenAI()

def analyze_physique(data_url: str) -> BodyCompositionAnalysis:
    response = client.responses.parse(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": (
                    "You are a fitness assistant performing a visual-only physique assessment "
                    "from a user-submitted image. Only describe visually observable features. "
                    "Do not make medical claims, diagnoses, or health-risk judgments. "
                    "Do not infer age, hormones, ethnicity, or health status. "
                    "If the image is unclear, incomplete, poorly lit, heavily obscured, or otherwise "
                    "insufficient for a reasonable physique assessment, return status='unable_to_assess', "
                    "body_fat_range='unable_to_assess', confidence='low', and "
                    "goal.recommendation='unable_to_assess'."
                ),
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "Return a structured physique assessment. "
                            "Estimate body fat only as a range in the format '10-12%'. "
                            "Never return a single-number body fat estimate. "
                            "Choose exactly one recommendation: bulk, cut, maintain, recomp, unable_to_assess. "
                            "Keep rationale to 2-3 sentences. "
                            "Keep action_summary to 1-3 short practical sentences. "
                            "Strong points should contain 2-4 items. "
                            "Weak points should contain 1-4 items. "
                            "Only include observations visually supported by the image. "
                            "If uncertain, lower confidence rather than overstating certainty. "
                            "Use image_quality_note to briefly explain any image limitations affecting confidence."
                        ),
                    },
                    {"type": "input_image", "image_url": data_url},
                ],
            },
        ],
        text_format=BodyCompositionAnalysis
    )

    return response.output_parsed