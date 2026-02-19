import os

from google.adk.agents.llm_agent import Agent

from .helpers import get_model
from .prompts import ROOT_INSTRUCTION
from .tools import ingest_clinical_notes, ingest_radiation_planning, ingest_hemato_oncology

MODEL = os.getenv('MODEL', 'gemini-2.5-flash')

root_agent = Agent(
    model=get_model(MODEL),
    name='ARC',
    description='You are ARC: Agentic Research Contexualizer. You contextialize Clinical Notes, Radiation Planning, and Hemato-Oncology reports.',
    instruction=ROOT_INSTRUCTION,
    tools=[ingest_clinical_notes, ingest_radiation_planning, ingest_hemato_oncology],
)
