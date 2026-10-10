#!/usr/bin/env python3
"""
Controlla: Clean, fast container & process orchestration CLI.
Built autonomously by Auto Qwen AI.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from typing import Dict, List, Optional


class ContainerEngine:
    def __init__(self):
        self.docker_bin = shutil.which("docker") or shutil.which("podman")

    def _check_engine(self):
        if not self.docker_bin:
            raise RuntimeError("No container runtime (docker or podman) found in PATH.")

    def list_containers(self, all_containers: bool = False) -> List[dict]:
        self._check_engine()
        cmd = [self.docker_bin, "ps", "--format", "{{json .}}"]
        if all_containers:
            cmd.insert(2, "-a")

        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"Engine error: {res.stderr.strip()}")

        containers = []
        for line in res.stdout.strip().split("\n"):
            if line.strip():
                try:
                    containers.append(json.loads(line))
                except Exception:
                    pass
        return containers

    def start_container(self, name: str, image: str = "alpine:latest", ports: Optional[List[str]] = None) -> str:
        self._check_engine()
        cmd = [self.docker_bin, "run", "-d", "--name", name]
        if ports:
            for p in ports:
                cmd.extend(["-p", p])
        cmd.append(image)

        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"Failed to start container: {res.stderr.strip()}")
        return res.stdout.strip()

    def stop_container(self, name_or_id: str) -> bool:
        self._check_engine()
        res = subprocess.run([self.docker_bin, "stop", name_or_id], capture_output=True, text=True)
        return res.returncode == 0

    def remove_container(self, name_or_id: str, force: bool = False) -> bool:
        self._check_engine()
        cmd = [self.docker_bin, "rm"]
        if force:
            cmd.append("-f")
        cmd.append(name_or_id)
        res = subprocess.run(cmd, capture_output=True, text=True)
        return res.returncode == 0

    def get_logs(self, name_or_id: str, tail: int = 50) -> str:
        self._check_engine()
        res = subprocess.run(
            [self.docker_bin, "logs", "--tail", str(tail), name_or_id], capture_output=True, text=True
        )
        return res.stdout or res.stderr


def main():
    parser = argparse.ArgumentParser(description="Controlla: Clean, fast container management CLI")
    subparsers = parser.add_subparsers(dest="action", help="Action to perform")

    # ps
    ps_p = subparsers.add_parser("ps", help="List containers")
    ps_p.add_argument("-a", "--all", action="store_true", help="Show all containers (default shows just running)")
    ps_p.add_argument("--json", action="store_true", help="Output in JSON format")

    # run
    run_p = subparsers.add_parser("run", help="Run a new container")
    run_p.add_argument("--name", required=True, help="Container name")
    run_p.add_argument("--image", default="alpine:latest", help="Container image (default: alpine:latest)")
    run_p.add_argument("-p", "--port", action="append", default=[], help="Port forward (e.g. 8080:80)")

    # stop
    stop_p = subparsers.add_parser("stop", help="Stop a container")
    stop_p.add_argument("name", help="Container name or ID")

    # rm
    rm_p = subparsers.add_parser("rm", help="Remove a container")
    rm_p.add_argument("name", help="Container name or ID")
    rm_p.add_argument("-f", "--force", action="store_true", help="Force removal")

    # logs
    log_p = subparsers.add_parser("logs", help="Get container logs")
    log_p.add_argument("name", help="Container name or ID")
    log_p.add_argument("-n", "--tail", type=int, default=50, help="Number of lines to show")

    args = parser.parse_args()
    engine = ContainerEngine()

    try:
        if args.action == "ps":
            items = engine.list_containers(all_containers=args.all)
            if args.json:
                print(json.dumps(items, indent=2))
            else:
                if not items:
                    print("No running containers.")
                else:
                    print(f"{'CONTAINER ID':<15} {'IMAGE':<25} {'STATUS':<20} {'NAMES':<20}")
                    for c in items:
                        cid = c.get("ID", "")[:12]
                        img = c.get("Image", "")[:23]
                        st = c.get("Status", "")[:18]
                        nm = c.get("Names", "")[:19]
                        print(f"{cid:<15} {img:<25} {st:<20} {nm:<20}")

        elif args.action == "run":
            cid = engine.start_container(name=args.name, image=args.image, ports=args.port)
            print(f"[+] Container '{args.name}' started. ID: {cid[:12]}")

        elif args.action == "stop":
            ok = engine.stop_container(args.name)
            print(f"[+] Container '{args.name}' stopped." if ok else f"[-] Failed to stop '{args.name}'.")

        elif args.action == "rm":
            ok = engine.remove_container(args.name, force=args.force)
            print(f"[+] Container '{args.name}' removed." if ok else f"[-] Failed to remove '{args.name}'.")

        elif args.action == "logs":
            logs = engine.get_logs(args.name, tail=args.tail)
            print(logs)

        else:
            parser.print_help()

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()