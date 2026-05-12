from __future__ import annotations

import json
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from catalyst_ai.api.deps import get_con
from catalyst_ai.data.store import read_df

router = APIRouter(prefix="/actions", tags=["actions"])


class ActionCreate(BaseModel):
    study_id: str
    linked_risk_id: str | None = None
    title: str
    owner: str
    due_date: str  # ISO date
    status: str = "Open"
    created_by: str = "demo-user"


@router.get("")
def list_actions(study_id: str | None = None, con=Depends(get_con)):
    if study_id:
        df = read_df(con, "SELECT * FROM actions WHERE study_id = ? ORDER BY due_date", (study_id,))
    else:
        df = read_df(con, "SELECT * FROM actions ORDER BY due_date")
    return json.loads(df.to_json(orient="records", date_format="iso"))


@router.post("")
def create_action(payload: ActionCreate, con=Depends(get_con)):
    action_id = str(uuid4())
    created_at = datetime.now(timezone.utc).isoformat()
    con.execute(
        """
        INSERT INTO actions(action_id, study_id, linked_risk_id, title, owner, due_date, status, created_by, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            action_id,
            payload.study_id,
            payload.linked_risk_id,
            payload.title,
            payload.owner,
            payload.due_date,
            payload.status,
            payload.created_by,
            created_at,
        ),
    )
    df = read_df(con, "SELECT * FROM actions WHERE action_id = ?", (action_id,))
    return json.loads(df.to_json(orient="records", date_format="iso"))[0]


class RequirementsInput(BaseModel):
    project_name: str
    goals: list[str]
    features: list[str]


class RequirementsOutput(BaseModel):
    project_name: str
    requirements: list[str]


@router.post("/generate-requirements", response_model=RequirementsOutput)
def generate_requirements(payload: RequirementsInput):
    """
    Generate a requirements document based on project goals and features.
    """
    requirements = [
        f"The system shall support the goal: {goal}." for goal in payload.goals
    ] + [
        f"The system shall include the feature: {feature}." for feature in payload.features
    ]

    return RequirementsOutput(
        project_name=payload.project_name,
        requirements=requirements
    )


class DesignInput(BaseModel):
    project_name: str
    components: list[str]
    architecture_style: str


class DesignOutput(BaseModel):
    project_name: str
    design_document: str


@router.post("/generate-design", response_model=DesignOutput)
def generate_design(payload: DesignInput):
    """
    Generate a design document based on project components and architecture style.
    """
    design_document = f"Design Document for {payload.project_name}\n\n" + \
                      f"Architecture Style: {payload.architecture_style}\n\n" + \
                      "Components:\n" + \
                      "\n".join(f"- {component}" for component in payload.components)

    return DesignOutput(
        project_name=payload.project_name,
        design_document=design_document
    )


class TestPlanInput(BaseModel):
    project_name: str
    test_cases: list[str]


class TestPlanOutput(BaseModel):
    project_name: str
    test_plan: str


@router.post("/generate-test-plan", response_model=TestPlanOutput)
def generate_test_plan(payload: TestPlanInput):
    """
    Generate a test plan based on test cases.
    """
    test_plan = f"Test Plan for {payload.project_name}\n\n" + \
                "Test Cases:\n" + \
                "\n".join(f"- {test_case}" for test_case in payload.test_cases)

    return TestPlanOutput(
        project_name=payload.project_name,
        test_plan=test_plan
    )


class RiskAnalysisInput(BaseModel):
    project_name: str
    risks: list[str]


class RiskAnalysisOutput(BaseModel):
    project_name: str
    risk_analysis: str


@router.post("/generate-risk-analysis", response_model=RiskAnalysisOutput)
def generate_risk_analysis(payload: RiskAnalysisInput):
    """
    Generate a risk analysis report based on identified risks.
    """
    risk_analysis = f"Risk Analysis for {payload.project_name}\n\n" + \
                    "Identified Risks:\n" + \
                    "\n".join(f"- {risk}" for risk in payload.risks)

    return RiskAnalysisOutput(
        project_name=payload.project_name,
        risk_analysis=risk_analysis
    )


class TraceabilityInput(BaseModel):
    project_name: str
    requirements: list[str]
    test_cases: list[str]


class TraceabilityOutput(BaseModel):
    project_name: str
    traceability_matrix: str


@router.post("/generate-traceability-matrix", response_model=TraceabilityOutput)
def generate_traceability_matrix(payload: TraceabilityInput):
    """
    Generate a traceability matrix based on requirements and test cases.
    """
    traceability_matrix = f"Traceability Matrix for {payload.project_name}\n\n" + \
                          "Requirements to Test Cases:\n" + \
                          "\n".join(f"- {req} -> {tc}" for req, tc in zip(payload.requirements, payload.test_cases))

    return TraceabilityOutput(
        project_name=payload.project_name,
        traceability_matrix=traceability_matrix
    )


class SprintPlanInput(BaseModel):
    project_name: str
    sprints: list[str]
    milestones: list[str]


class SprintPlanOutput(BaseModel):
    project_name: str
    sprint_plan: str


@router.post("/generate-sprint-plan", response_model=SprintPlanOutput)
def generate_sprint_plan(payload: SprintPlanInput):
    """
    Generate a sprint plan with tasks and demo milestones.
    """
    sprint_plan = f"Sprint Plan for {payload.project_name}\n\n" + \
                 "Sprints:\n" + "\n".join(f"- {sprint}" for sprint in payload.sprints) + "\n\n" + \
                 "Milestones:\n" + "\n".join(f"- {milestone}" for milestone in payload.milestones)
    return SprintPlanOutput(
        project_name=payload.project_name,
        sprint_plan=sprint_plan
    )
