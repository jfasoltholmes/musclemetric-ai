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
                    "Do not infer age, hormones, ethnicity, genetics, or health status. "
                    "Do not invent details that are not visually supported by the image. "
                    "Be restrained, realistic, and specific. "
                    "The assessment must be based only on what is visible in the photo. "
                    "Do not mention muscle insertions, frame, or body structure unless clearly visible. "
                    "Do not provide meal plans, calorie targets, or medical advice. "
                    "If the image is unclear, poorly lit, heavily obscured, cropped too aggressively, "
                    "posed in a way that prevents reasonable assessment, or otherwise insufficient, "
                    "return an unable_to_assess result. "
                    "For unable_to_assess: set status='unable_to_assess', "
                    "body_fat_range='unable_to_assess', "
                    "goal.recommendation='unable_to_assess', and make the written fields briefly explain "
                    "why the image could not be assessed."
                ),
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "Return a structured physique assessment that matches the provided schema exactly. "

                            "Body fat rules: "
                            "Estimate body fat only as a range in the exact format '10-12%'. "
                            "Never return a single number. "
                            "Never include extra words with the range. "
                            "If the image is not assessable, return 'unable_to_assess'. "

                            "Status rules: "
                            "Use status='ok' only when the image supports a reasonable visual-only assessment. "
                            "Use status='unable_to_assess' when the image quality, lighting, pose, cropping, "
                            "obstruction, or incompleteness prevents a reasonable assessment. "

                            "Image quality note rules: "
                            "image_quality_note should be one short sentence summarizing the main image-quality "
                            "or visibility limitation affecting the assessment. "

                            "Goal rules: "
                            "Choose exactly one recommendation: bulk, cut, maintain, recomp, unable_to_assess. "
                            "Keep rationale to 2-3 sentences. "
                            "Keep action_summary to 1-3 short practical sentences. "
                            "Keep the recommendation aligned with the visible physique only. "

                            "Physique assessment rules: "
                            "strong_points must contain 2-4 items. "
                            "weak_points must contain 0-3 items. "
                            "Do not force weak points if they are not clearly visible. "
                            "It is better to provide fewer weak points than to invent minor flaws. "
                            "Each item should be short, specific, and visually grounded. "
                            "Do not repeat the same point in different wording. "
                            "fat_distribution should be a short visual description of where body fat appears "
                            "to be concentrated. Do not include percentages. "

                            "Improvement focus rules: "
                            "top_priorities must contain 1-3 items. "
                            "top_priorities may reflect either visible improvement areas or the most valuable next development focus. "
                            "These should be actionable priorities based on the overall physique, not just a copy "
                            "of weak_points. "
                            "They should reflect what would make the biggest visual difference next. "
                            "Each item should be short and specific. "
                            "Keep priorities high-value and non-redundant. "
                            "Do not restate weak points in slightly different wording. "
                            "If there are no clearly visible weak points, return an empty weak_points list. "
                            ""

                            "Assessment limitations rules: "
                            "photo_limitations must contain 0-3 short items describing image-specific issues "
                            "that reduce assessment quality, such as lighting, pose, cropping, blur, distance, "
                            "or covered body parts. "
                            "interpretation_notes must contain 0-2 short items describing how the result should "
                            "be interpreted carefully, such as flexing, pump, angle, or limited body visibility. "
                            "Do not speculate about pump, training status, or conditions not visually evident. "
                            "Do not make these generic disclaimers; tie them to the actual image when possible. "
                            "Do not invent limitations to satisfy a quota. "
                            "Only include real, image-specific limitations that materially affect interpretation. "
                            "If there are no meaningful image-specific limitations, return an empty list for those fields. "

                            "Unable-to-assess rules: "
                            "If status is 'unable_to_assess', do not invent physique observations. "
                            "Use list fields only for brief statements explaining why assessment was not possible. "
                            "Keep list fields minimal."

                            "General rules: "
                            "Only include observations visually supported by the image. "
                            "Avoid exaggerated praise or harsh language. "
                            "Do not sound clinical or medical. "
                            "Do not add extra keys or extra commentary outside the schema. "
                            "Do not output markdown."
                        ),
                    },
                    {"type": "input_image", "image_url": data_url},
                ],
            },
        ],
        text_format=BodyCompositionAnalysis
    )

    return response.output_parsed