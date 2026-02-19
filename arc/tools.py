import os
from typing import Optional

from google import genai
from pydantic import BaseModel, Field


class ClinicalNotesExtraction(BaseModel):
    """Structured extraction from clinical notes."""

    dates: list[str] = Field(
        default_factory=list,
        description="Relevant dates mentioned (e.g. visit date, DOB, referral date, procedure dates). Use ISO-like format when possible (YYYY-MM-DD).",
    )
    patient_condition: str = Field(
        default="",
        description="Summary of the patient's condition or primary diagnosis.",
    )
    chief_complaint: Optional[str] = Field(
        default=None,
        description="Chief complaint or reason for visit if stated.",
    )
    diagnoses: list[str] = Field(
        default_factory=list,
        description="List of diagnoses or problem list items mentioned.",
    )

EXTRACTION_PROMPT = """Extract structured information from the following clinical notes. 
Output only valid JSON matching the schema. If a field cannot be determined, use null or empty list/string as appropriate.

Clinical notes:
---
{clinical_notes}
---"""


def ingest_clinical_notes(clinical_notes: str) -> ClinicalNotesExtraction:
    """Convert clinical notes into a structured Pydantic object using an LLM to extract basic features (dates, patient condition, etc.)."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is required")
    model_name = os.getenv("MODEL", "gemini-2.5-flash")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model_name,
        contents=EXTRACTION_PROMPT.format(clinical_notes=clinical_notes),
        config=genai.types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ClinicalNotesExtraction,
        ),
    )
    text = response.text
    if not text or not text.strip():
        return ClinicalNotesExtraction()
    return ClinicalNotesExtraction.model_validate_json(text)


class RadiationPlanningExtraction(BaseModel):
    """Structured extraction from radiation planning reports."""

    average_dose: dict[str, float] = Field(
        default_factory=dict,
        description="Average dose to the target volume in Gy.",
    )

    
def ingest_radiation_planning(
    dose_file: str,
    image_file: str,
    structure_file: str,
) -> RadiationPlanningExtraction:

    # DO SOMETHING WITH THE DATA
    return RadiationPlanningExtraction()


def ingest_hemato_oncology(
    report_file: str,
) -> str:

    # DO SOMETHING WITH THE DATA
    return ""

    
