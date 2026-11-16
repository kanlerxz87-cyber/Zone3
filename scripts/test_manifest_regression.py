#!/usr/bin/env python3
"""Regression test for 71-F-01 (fixed by session 81bc99d0).

Before the fix, `tools/build_site.py --out <fresh dir>` crashed with FileNotFoundError on
<out>/data/z3/build-manifest.json, and the manifest's `files` map stored content digests where
`tools/verify_site.py` expected on-disk paths — so no generated page was recognized as owned and
its hard checks were silently downgraded to advisories.

This test builds into an empty temporary directory and asserts:
  1. the build succeeds (the output parent directory is created),
  2. build-manifest.json exists and records a non-empty `paths` map,
  3. every recorded path exists on disk,
  4. tools.verify_site.generated_set() recognizes those paths as generated pages.

Exit 0 on success; non-zero on any failure.
"""
import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    failures = []
    with tempfile.TemporaryDirectory() as tmp:
        out = pathlib.Path(tmp)
        proc = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "build_site.py"), "--out", str(out)],
            capture_output=True, text=True,
        )
        if proc.returncode != 0:
            failures.append(f"build_site.py --out fresh dir failed (exit {proc.returncode}):\n"
                            f"{proc.stderr}")
            return report(failures)

        mpath = out / "data" / "z3" / "build-manifest.json"
        if not mpath.exists():
            failures.append("build-manifest.json was not written into the fresh --out dir")
            return report(failures)

        manifest = json.loads(mpath.read_text())
        paths = manifest.get("paths")
        if not paths:
            failures.append("manifest has no `paths` map")
            return report(failures)

        missing = [v for v in paths.values() if not (out / v).exists()]
        if missing:
            failures.append(f"manifest paths that do not exist on disk: {missing[:5]}")

        # The verifier must recognize the generated pages via the manifest.
        verify = load_module(ROOT / "tools" / "verify_site.py", "verify_site_under_test")
        recognized = verify.generated_set(out)
        unrecognized = [v for v in paths.values() if str(pathlib.PurePosixPath(v)) not in recognized]
        if unrecognized:
            failures.append(
                f"generated_set() did not recognize {len(unrecognized)} generated path(s): "
                f"{unrecognized[:5]}")

    return report(failures)


def report(failures):
    if failures:
        print("MANIFEST REGRESSION TEST: FAIL")
        for f in failures:
            print(" -", f)
        return 1
    print("MANIFEST REGRESSION TEST: PASS — fresh --out builds, manifest lists real paths, "
          "verifier recognizes them")
    return 0


if __name__ == "__main__":
    sys.exit(main())
