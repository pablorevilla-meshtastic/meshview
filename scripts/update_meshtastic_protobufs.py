#!/usr/bin/env python3
import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run(cmd, cwd=None):
    subprocess.run(cmd, cwd=cwd, check=True)


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
        run(["git", "clone", "--depth", "1", "--branch", args.ref, args.repo, str(tmp_path)])
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

        rel_protos = [str(p.relative_to(tmp_path)) for p in protos]

        protoc = shutil.which("protoc")
        if protoc:
            cmd = [
                protoc,
                f"-I{tmp_path}",
                f"--python_out={out_root}",
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
                f"-I{tmp_path}",
                f"--python_out={out_root}",
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
