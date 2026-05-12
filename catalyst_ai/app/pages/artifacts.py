from __future__ import annotations

import re

import streamlit as st

from catalyst_ai.artifacts.generator import write_text
from catalyst_ai.artifacts.packs import (
    cicd_pack,
    demo_script_pack,
    design_pack,
    requirements_pack,
    sprint_plan_pack,
)
from catalyst_ai.config import get_paths


def _extract_first_svg(markdown: str) -> str | None:
    m = re.search(r"<svg[\s\S]*?</svg>", markdown)
    return m.group(0) if m else None


def _render_svg(svg: str, height: int) -> None:
    # Streamlit renders raw HTML/SVG reliably, unlike some markdown previewers.
    st.components.v1.html(svg, height=height, scrolling=False)


def _artifact_controls(name: str, content: str) -> None:
    """Render a generate + download UX for a single artifact."""
    paths = get_paths()

    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        generate = st.button(f"Generate {name}", key=f"gen-{name}")
    with c2:
        st.download_button(
            f"Download {name}",
            data=content,
            file_name=f"{name}.md",
            mime="text/markdown",
            key=f"dl-{name}",
        )
    with c3:
        st.caption(f"Writes to: {paths.artifacts_dir / (name + '.md')}")

    if generate:
        write_text(paths.artifacts_dir, name, content)
        st.success(f"Generated {name}.md")


def render_requirements_agent() -> None:
    st.subheader("Requirements Agent")
    st.caption("Generate a requirements document based on project goals and features.")

    with st.form("requirements_form"):
        project_name = st.text_input("Project Name")
        goals = st.text_area("Project Goals (one per line)").splitlines()
        features = st.text_area("Project Features (one per line)").splitlines()
        submitted = st.form_submit_button("Generate Requirements")

    if submitted:
        if not project_name or not goals or not features:
            st.error("Please fill in all fields.")
        else:
            with st.spinner("Generating requirements..."):
                import requests

                response = requests.post(
                    "http://localhost:8000/actions/generate-requirements",
                    json={"project_name": project_name, "goals": goals, "features": features},
                )

                if response.status_code == 200:
                    requirements = response.json()["requirements"]
                    st.success("Requirements generated successfully!")
                    st.write("\n".join(requirements))
                else:
                    st.error("Failed to generate requirements. Please try again.")


def render_design_agent() -> None:
    st.subheader("Design Agent")
    st.caption("Generate a design document based on project components and architecture style.")

    with st.form("design_form"):
        project_name = st.text_input("Project Name")
        components = st.text_area("Project Components (one per line)").splitlines()
        architecture_style = st.text_input("Architecture Style")
        submitted = st.form_submit_button("Generate Design Document")

    if submitted:
        if not project_name or not components or not architecture_style:
            st.error("Please fill in all fields.")
        else:
            with st.spinner("Generating design document..."):
                import requests

                response = requests.post(
                    "http://localhost:8000/actions/generate-design",
                    json={"project_name": project_name, "components": components, "architecture_style": architecture_style},
                )

                if response.status_code == 200:
                    design_document = response.json()["design_document"]
                    st.success("Design document generated successfully!")
                    st.text_area("Design Document", value=design_document, height=300)
                else:
                    st.error("Failed to generate design document. Please try again.")


def render_test_plan_agent() -> None:
    st.subheader("Test Plan Agent")
    st.caption("Generate a test plan based on test cases.")

    with st.form("test_plan_form"):
        project_name = st.text_input("Project Name")
        test_cases = st.text_area("Test Cases (one per line)").splitlines()
        submitted = st.form_submit_button("Generate Test Plan")

    if submitted:
        if not project_name or not test_cases:
            st.error("Please fill in all fields.")
        else:
            with st.spinner("Generating test plan..."):
                import requests

                response = requests.post(
                    "http://localhost:8000/actions/generate-test-plan",
                    json={"project_name": project_name, "test_cases": test_cases},
                )

                if response.status_code == 200:
                    test_plan = response.json()["test_plan"]
                    st.success("Test plan generated successfully!")
                    st.text_area("Test Plan", value=test_plan, height=300)
                else:
                    st.error("Failed to generate test plan. Please try again.")


def render_risk_analysis_agent() -> None:
    st.subheader("Risk Analysis Agent")
    st.caption("Generate a risk analysis report based on identified risks.")

    with st.form("risk_analysis_form"):
        project_name = st.text_input("Project Name")
        risks = st.text_area("Identified Risks (one per line)").splitlines()
        submitted = st.form_submit_button("Generate Risk Analysis")

    if submitted:
        if not project_name or not risks:
            st.error("Please fill in all fields.")
        else:
            with st.spinner("Generating risk analysis report..."):
                import requests

                response = requests.post(
                    "http://localhost:8000/actions/generate-risk-analysis",
                    json={"project_name": project_name, "risks": risks},
                )

                if response.status_code == 200:
                    risk_analysis = response.json()["risk_analysis"]
                    st.success("Risk analysis report generated successfully!")
                    st.text_area("Risk Analysis Report", value=risk_analysis, height=300)
                else:
                    st.error("Failed to generate risk analysis report. Please try again.")


def render_traceability_agent() -> None:
    st.subheader("Traceability Agent")
    st.caption("Generate a traceability matrix based on requirements and test cases.")

    with st.form("traceability_form"):
        project_name = st.text_input("Project Name")
        requirements = st.text_area("Requirements (one per line)").splitlines()
        test_cases = st.text_area("Test Cases (one per line)").splitlines()
        submitted = st.form_submit_button("Generate Traceability Matrix")

    if submitted:
        if not project_name or not requirements or not test_cases:
            st.error("Please fill in all fields.")
        else:
            with st.spinner("Generating traceability matrix..."):
                import requests

                response = requests.post(
                    "http://localhost:8000/actions/generate-traceability-matrix",
                    json={"project_name": project_name, "requirements": requirements, "test_cases": test_cases},
                )

                if response.status_code == 200:
                    traceability_matrix = response.json()["traceability_matrix"]
                    st.success("Traceability matrix generated successfully!")
                    st.text_area("Traceability Matrix", value=traceability_matrix, height=300)
                else:
                    st.error("Failed to generate traceability matrix. Please try again.")


def render_sprint_plan_agent() -> None:
    st.subheader("Sprint Plan Agent")
    st.caption("Generate a sprint plan with tasks and demo milestones.")

    with st.form("sprint_plan_form"):
        project_name = st.text_input("Project Name")
        sprints = st.text_area("Sprints (one per line)").splitlines()
        milestones = st.text_area("Milestones (one per line)").splitlines()
        submitted = st.form_submit_button("Generate Sprint Plan")

    if submitted:
        if not project_name or not sprints or not milestones:
            st.error("Please fill in all fields.")
        else:
            with st.spinner("Generating sprint plan..."):
                import requests
                response = requests.post(
                    "http://localhost:8000/actions/generate-sprint-plan",
                    json={"project_name": project_name, "sprints": sprints, "milestones": milestones},
                )
                if response.status_code == 200:
                    sprint_plan = response.json()["sprint_plan"]
                    st.success("Sprint plan generated successfully!")
                    st.text_area("Sprint Plan", value=sprint_plan, height=300)
                else:
                    st.error("Failed to generate sprint plan. Please try again.")


def render_data_generator_agent() -> None:
    st.subheader("Data Generator Agent")
    st.caption("Generate synthetic operational dataset and public study metadata extract.")

    with st.form("data_generator_form"):
        dataset_name = st.text_input("Dataset Name")
        num_records = st.number_input("Number of Records", min_value=1, value=100)
        submitted = st.form_submit_button("Generate Data")

    if submitted:
        if not dataset_name or num_records < 1:
            st.error("Please provide a dataset name and a positive number of records.")
        else:
            with st.spinner("Generating synthetic data..."):
                # Placeholder for actual data generation logic
                st.success(f"Synthetic dataset '{dataset_name}' with {num_records} records generated (stub).")
                st.info("Implement actual data generation logic as needed.")


def render_test_automation_agent() -> None:
    st.subheader("Test Automation Agent")
    st.caption("Generate unit, integration, and UI test templates.")

    with st.form("test_automation_form"):
        test_type = st.selectbox("Test Type", ["Unit Test", "Integration Test", "UI Smoke Test"])
        component = st.text_input("Component/Feature Name")
        submitted = st.form_submit_button("Generate Test Template")

    if submitted:
        if not component:
            st.error("Please provide a component or feature name.")
        else:
            with st.spinner("Generating test template..."):
                # Placeholder for actual test template generation logic
                st.success(f"{test_type} template for '{component}' generated (stub).")
                st.info("Implement actual test template generation logic as needed.")


def render_cicd_agent() -> None:
    st.subheader("CI/CD Agent")
    st.caption("Generate pipeline configuration and source control integration templates.")

    with st.form("cicd_form"):
        pipeline_tool = st.selectbox("Pipeline Tool", ["Jenkins", "GitHub Actions", "GitLab CI", "Bitbucket Pipelines"])
        repo_type = st.selectbox("Source Control", ["GitHub", "Bitbucket", "GitLab"])
        submitted = st.form_submit_button("Generate CI/CD Config")

    if submitted:
        with st.spinner("Generating CI/CD configuration..."):
            # Placeholder for actual CI/CD config generation logic
            st.success(f"{pipeline_tool} pipeline and {repo_type} integration config generated (stub).")
            st.info("Implement actual CI/CD config generation logic as needed.")


def render_deployment_agent() -> None:
    st.subheader("Deployment Agent")
    st.caption("Generate Docker Compose, cloud deployment scripts, and runbooks.")

    with st.form("deployment_form"):
        deployment_type = st.selectbox("Deployment Type", ["Docker Compose", "AWS Cloud", "Azure Cloud", "GCP Cloud"])
        submitted = st.form_submit_button("Generate Deployment Script")

    if submitted:
        with st.spinner("Generating deployment script..."):
            # Placeholder for actual deployment script generation logic
            st.success(f"{deployment_type} deployment script and runbook generated (stub).")
            st.info("Implement actual deployment script generation logic as needed.")


def render_sdlc_agents():
    st.header("SDLC Agents")
    st.caption("Select an SDLC Agent to generate artifacts.")

    agent_names = [
        "Requirements Agent",
        "Design Agent",
        "Test Plan Agent",
        "Risk Analysis Agent",
        "Traceability Agent",
        "Sprint Plan Agent",
        "Data Generator Agent",
        "Test Automation Agent",
        "CI/CD Agent",
        "Deployment Agent",
    ]

    selected_agent = st.selectbox(
        "Select SDLC Agent",
        options=agent_names,
        key="main_selected_agent"
    )

    if selected_agent == "Requirements Agent":
        render_requirements_agent()
    elif selected_agent == "Design Agent":
        render_design_agent()
    elif selected_agent == "Test Plan Agent":
        render_test_plan_agent()
    elif selected_agent == "Risk Analysis Agent":
        render_risk_analysis_agent()
    elif selected_agent == "Traceability Agent":
        render_traceability_agent()
    elif selected_agent == "Sprint Plan Agent":
        render_sprint_plan_agent()
    elif selected_agent == "Data Generator Agent":
        render_data_generator_agent()
    elif selected_agent == "Test Automation Agent":
        render_test_automation_agent()
    elif selected_agent == "CI/CD Agent":
        render_cicd_agent()
    elif selected_agent == "Deployment Agent":
        render_deployment_agent()


def render() -> None:
    st.header("Generated Packs")
    st.caption("Generate and download each SDLC artifact independently.")

    st.write(f"Artifacts folder: {get_paths().artifacts_dir}")

    # Build content once per render so preview/download uses the same text.
    req = requirements_pack()
    des = design_pack()
    spr = sprint_plan_pack()
    ci = cicd_pack()
    demo = demo_script_pack()

    st.subheader("Generate")
    _artifact_controls("requirements-pack", req)
    _artifact_controls("design-pack", des)
    _artifact_controls("sprint-plan", spr)
    _artifact_controls("cicd-pack", ci)
    _artifact_controls("deployment-demo-script", demo)

    st.divider()

    st.subheader("SDLC Accelerator (Agents)")
    st.caption("Runs Discover → Define → (Grade/Iterate) → Design → Plan using an LLM. Requires CATALYST_LLM_API_KEY.")

    with st.expander("Agent settings", expanded=False):
        quality = st.slider("Quality threshold", min_value=0.5, max_value=0.95, value=0.8, step=0.05)
        max_iter = st.selectbox("Max iterations", options=[1, 2, 3, 4, 5], index=2)
        model = st.text_input("LLM model (optional override)", value="gpt-4.1-mini")

    default_ps = """Clinical Trial Teams (CTTs) need consistent, near real-time oversight of study execution..."""
    ps = st.text_area("Problem statement", value=default_ps, height=180)

    if st.button("Run agent pipeline and generate artifacts", key="run-agent-pipeline"):
        from catalyst_ai.agents.artifacts import write_agentic_artifacts
        from catalyst_ai.agents.base import AgentConfig

        cfg = AgentConfig(quality_threshold=float(quality), max_iterations=int(max_iter), llm_model=model)
        try:
            out = write_agentic_artifacts(problem_statement=ps, config=cfg)
        except Exception as e:
            st.error(str(e))
        else:
            st.success("Generated agent artifacts")
            st.json({k: str(v) for k, v in out.items()})

    st.divider()

    st.subheader("Preview")
    tabs = st.tabs(["Requirements", "Design", "Sprint Plan", "CI/CD", "Demo Script"])
    with tabs[0]:
        st.markdown(req)

    with tabs[1]:
        svg = _extract_first_svg(des)
        if svg:
            _render_svg(svg, height=560)
        st.markdown(des)

    with tabs[2]:
        svg = _extract_first_svg(spr)
        if svg:
            _render_svg(svg, height=300)
        st.markdown(spr)

    with tabs[3]:
        st.markdown(ci)

    with tabs[4]:
        st.markdown(demo)

    render_requirements_agent()
    render_design_agent()
    render_test_plan_agent()
    render_risk_analysis_agent()
    render_traceability_agent()
    render_sprint_plan_agent()
    render_data_generator_agent()
    render_test_automation_agent()
    render_cicd_agent()
    render_deployment_agent()

    render_sdlc_agents()
