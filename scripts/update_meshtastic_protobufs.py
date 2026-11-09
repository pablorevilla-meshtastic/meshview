#!/usr/bin/env python3
import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run(cmd, cwd=None):
    subprocess.run(cmd, cwd=cwd, check=True)


def clone_ref(repo, ref, tmp_path):
    if re.fullmatch(r"[0-9a-fA-F]{40}", ref):
        run(["git", "clone", "--no-checkout", "--depth", "1", repo, str(tmp_path)])
        run(["git", "fetch", "--depth", "1", "origin", ref], cwd=tmp_path)
        run(["git", "checkout", "--detach", "FETCH_HEAD"], cwd=tmp_path)
        return

    run(["git", "clone", "--depth", "1", "--branch", ref, repo, str(tmp_path)])


def stage_meshtastic_package(proto_root, tmp_path):
    """Map upstream meshtastic/*.proto files to Meshview's vendored package path."""
    if proto_root != tmp_path / "meshtastic":
        return tmp_path, proto_root

    stage_root = tmp_path / "_meshview_proto_stage"
    staged_proto_root = stage_root / "meshtastic" / "protobuf"
    staged_proto_root.mkdir(parents=True, exist_ok=True)

    for proto in sorted(proto_root.glob("*.proto")):
        text = proto.read_text(encoding="utf-8")
        text = text.replace('import "meshtastic/', 'import "meshtastic/protobuf/')
        text = text.replace('import "nanopb.proto"', 'import "meshtastic/protobuf/nanopb.proto"')
        text = text.replace("package meshtastic;", "package meshtastic.protobuf;")
        # Custom options are qualified with the upstream package name too.
        text = text.replace("(meshtastic.", "(meshtastic.protobuf.")
        (staged_proto_root / proto.name).write_text(text, encoding="utf-8")

    nanopb = tmp_path / "nanopb.proto"
    if nanopb.exists():
        shutil.copy2(nanopb, staged_proto_root / "nanopb.proto")

    return stage_root, staged_proto_root


def main():
    parser = argparse.ArgumentParser(description="Update Meshtastic protobufs")
    parser.add_argument(
        "--repo",
        default="https://github.com/meshtastic/protobufs.git",
        help="Meshtastic protobufs repo URL",
    )
    parser.add_argument(
        "--ref",
        default="master",
        help="Git ref to fetch (branch, tag, or commit)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Only check if protobufs are up to date for the given ref",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    out_root = repo_root

    with tempfile.TemporaryDirectory(prefix="meshtastic-protobufs-") as tmp:
        tmp_path = Path(tmp)
        print(f"Cloning {args.repo} ({args.ref}) into {tmp_path}...")
        clone_ref(args.repo, args.ref, tmp_path)
        upstream_rev = (
            subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=tmp_path).decode().strip()
        )

        rev_file = out_root / "meshtastic" / "protobuf" / "UPSTREAM_REV.txt"
        current_rev = None
        if rev_file.exists():
            current_rev = rev_file.read_text(encoding="utf-8").strip()

        if args.check:
            if current_rev == upstream_rev:
                print(f"Up to date: {current_rev}")
                return 0
            print(f"Out of date. Local: {current_rev or 'unknown'} / Upstream: {upstream_rev}")
            return 1

        proto_root = None
        # Common locations in the meshtastic/protobufs repo
        candidates = [
            tmp_path / "meshtastic" / "protobuf",
            tmp_path / "meshtastic",
            tmp_path / "protobufs",
            tmp_path / "protobuf",
            tmp_path / "proto",
        ]
        for candidate in candidates:
            if candidate.exists() and list(candidate.glob("*.proto")):
                proto_root = candidate
                break

        if proto_root is None:
            # Fallback: search for any directory containing .proto files
            for candidate in tmp_path.rglob("*.proto"):
                proto_root = candidate.parent
                break

        if proto_root is None:
            print("Proto root not found in cloned repo.", file=sys.stderr)
            return 1

        protos = sorted(proto_root.glob("*.proto"))
        if not protos:
            print(f"No .proto files found in {proto_root}", file=sys.stderr)
            return 1

        proto_base, proto_root = stage_meshtastic_package(proto_root, tmp_path)
        protos = sorted(proto_root.glob("*.proto"))
        rel_protos = [str(p.relative_to(proto_base)) for p in protos]

        protoc = shutil.which("protoc")
        if protoc:
            cmd = [
                protoc,
                f"-I{proto_base}",
                f"--python_out={out_root}",
                f"--pyi_out={out_root}",
                *rel_protos,
            ]
            print("Running protoc...")
            run(cmd, cwd=tmp_path)
        else:
            try:
                import grpc_tools.protoc  # noqa: F401
            except Exception:
                print(
                    "protoc not found. Install it with your package manager, "
                    "or install grpcio-tools and re-run.",
                    file=sys.stderr,
                )
                return 1
            cmd = [
                sys.executable,
                "-m",
                "grpc_tools.protoc",
                f"-I{proto_base}",
                f"--python_out={out_root}",
                f"--pyi_out={out_root}",
                *rel_protos,
            ]
            print("Running grpc_tools.protoc...")
            run(cmd, cwd=tmp_path)

        rev_file.parent.mkdir(parents=True, exist_ok=True)
        rev_file.write_text(upstream_rev + "\n", encoding="utf-8")

    print("Protobufs updated in meshtastic/protobuf/.")
    print("Review changes and commit them if desired.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
