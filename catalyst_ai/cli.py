from __future__ import annotations

import argparse
from pathlib import Path

from catalyst_ai.artifacts.generator import write_text
from catalyst_ai.artifacts.packs import (
    cicd_pack,
    demo_script_pack,
    design_pack,
    requirements_pack,
    sprint_plan_pack,
)
from catalyst_ai.config import get_paths
from catalyst_ai.data.store import connect, write_df
from catalyst_ai.data.synthetic import SyntheticSpec, generate_all
from catalyst_ai.risk.engine import recompute_risks_for_study


def cmd_generate_data(args: argparse.Namespace) -> None:
    paths = get_paths()
    ds = generate_all(seed=args.seed, spec=SyntheticSpec())

    con = connect(paths.db_path)
    try:
        write_df(con, "studies", ds["studies"])
        write_df(con, "sites", ds["sites"])
        write_df(con, "weekly_metrics", ds["weekly_metrics"])
        write_df(con, "milestones", ds["milestones"])

        # recompute risks for all studies
        for study_id in ds["studies"]["study_id"].tolist():
            recompute_risks_for_study(con, study_id)
    finally:
        con.close()

    print(f"Generated sample dataset and loaded DuckDB: {paths.db_path}")


def cmd_generate_artifacts(args: argparse.Namespace) -> None:
    paths = get_paths()
    out_dir = paths.artifacts_dir

    write_text(out_dir, "requirements-pack", requirements_pack())
    write_text(out_dir, "design-pack", design_pack())
    write_text(out_dir, "sprint-plan", sprint_plan_pack())
    write_text(out_dir, "cicd-pack", cicd_pack())
    write_text(out_dir, "deployment-demo-script", demo_script_pack())

    print(f"Wrote packs to: {out_dir}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="catalyst_ai")
    sub = p.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate-data", help="Generate synthetic data and load local store")
    g.add_argument("--seed", type=int, default=7)
    g.set_defaults(func=cmd_generate_data)

    a = sub.add_parser("generate-artifacts", help="Generate requirements/design/sprint/CI/CD packs")
    a.set_defaults(func=cmd_generate_artifacts)

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
