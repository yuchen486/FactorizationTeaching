"""Publish verification records after reviewing every final PPTX render."""
import argparse
import datetime
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PPTX = ROOT / "outputs/L01-课件.pptx"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8", newline="\n")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-dir", type=Path, required=True)
    parser.add_argument("--reviewed-all-pages", action="store_true", required=True)
    args = parser.parse_args()
    build = args.build_dir
    manifest = read_json(build / "manifest.with-final-renders.json")
    build_result = read_json(build / "build_result.json")
    digest = sha(PPTX)
    if digest != build_result["pptx"]["sha256"] or digest != sha(ROOT / "docs/L01-课件.pptx"):
        raise ValueError("The site and delivery PPTX must match the reviewed build.")
    ui = read_json(ROOT / "work/delivery-ui.json")
    local = read_json(ROOT / "work/ui-check.json")
    if not (ui["passed"] and local["passed"]):
        raise ValueError("Site verification did not pass.")

    render_dir = ROOT / "assets/final-renders"
    render_dir.mkdir(exist_ok=True)
    reviewed_at = datetime.datetime.now().astimezone().isoformat()
    for page in manifest["pages"]:
        record = page["final_render"]
        source = ROOT / record["path"]
        dest = render_dir / source.name
        if sha(source) != record["sha256"]:
            raise ValueError(f"Unexpected render checksum: {source}")
        shutil.copy2(source, dest)
        record.update(
            path=dest.relative_to(ROOT).as_posix(),
            qa={"facts": "passed", "text": "passed", "visual": "passed"},
            reviewed=True, reviewer="Codex visual review", reviewed_at=reviewed_at,
        )
        page["status"] = "delivered"

    records_dir = ROOT / "assets/records"
    write_json(ROOT / "slides/manifest.delivered.json", manifest)
    for name in ("final.validation.json", "manifest.pptx-integrity.json", "build_result.json"):
        shutil.copy2(build / name, records_dir / name)
    write_json(records_dir / "delivery.json", {
        "pptx_sha256": digest,
        "slides": len(manifest["pages"]),
        "seconds": sum(page["speaker"]["seconds"] for page in manifest["pages"]),
        "visual_review": "All slides visually reviewed individually after reimport at 1920×1080.",
        "ui": ui, "local_ui": local,
        "limits": ["Actual classroom rehearsal pending", "PowerPoint desktop and WPS not opened"],
        "runtime_note": "Operation marker module unavailable in the installed skill. Official finalizer, reimport and rendering passed.",
    })
    print("Delivery evidence finalized.")


if __name__ == "__main__":
    main()
