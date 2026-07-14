#!/usr/bin/env python3
"""Build and serve the exact static artifact deployed to GitHub Pages."""

from __future__ import annotations

import argparse
import functools
import subprocess
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from docs_common import ROOT


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    subprocess.run([sys.executable, "-m", "mkdocs", "build", "--strict"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "scripts/generate_site_contracts.py"], cwd=ROOT, check=True)
    subprocess.run(
        [sys.executable, "scripts/validate_docs.py", "--site", "site"],
        cwd=ROOT,
        check=True,
    )

    handler = functools.partial(SimpleHTTPRequestHandler, directory=str(ROOT / "site"))
    server = ThreadingHTTPServer((args.host, args.port), handler)
    print(f"Serving production-parity docs at http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
