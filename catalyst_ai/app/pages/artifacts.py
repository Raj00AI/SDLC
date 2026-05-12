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
