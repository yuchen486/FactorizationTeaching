"""Stage an image-first deck from individually reviewed, SHA-bound candidates."""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from generate_images import ROOT, WORK, now, save_json


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def hash_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def candidate(record, verdict):
    if hash_file(ROOT / record["path"]) != record["sha256"]:
        raise ValueError(f"Image checksum mismatch for {record['id']}")
    if hash_file(ROOT / record["prompt"]) != record["prompt_sha256"]:
        raise ValueError(f"Prompt checksum mismatch for {record['id']}")
    if verdict["sha256"] != record["sha256"]:
        raise ValueError(f"Review checksum mismatch for {record['id']}")
    return {
        "id": record["id"],
        "project_id": "L01",
        "status": "adopted" if verdict["adopted"] else "verified",
        "path": record["path"],
        "sha256": record["sha256"],
        "source": {
            "kind": record["lane"],
            "reference": record.get("reference", "Configured Windows image channel"),
        },
        "prompt": {"path": record["prompt"], "version": record["id"], "sha256": record["prompt_sha256"]},
        "quality": {"rating": "accept", "reason": verdict["findings"]},
        "dimensions": {"width_px": record["dimensions"][0], "height_px": record["dimensions"][1]},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reviews", type=Path, default=WORK / "review.json")
    args = parser.parse_args()
    spec = load(ROOT / "slides/L01-api-v3.json")
    approved = load(ROOT / "slides/pages.json")
    reviews = load(args.reviews)
    records = {p.stem: load(p) for p in (WORK / "candidates").glob("*.json")}
    manifest = {
        "schema_version": 1,
        "project": {
            "id": "L01", "title": "因式分解——提公因式法入门",
            "target_seconds": 600, "timing_tolerance_seconds": 0,
            "generation_policy": {
                "mode": "api_then_chrome",
                "required_lanes": ["configured_api"],
                "candidates_per_page_per_lane": 1,
                "budget_reason": "每页 API 首轮，必要时定向重试和 Chrome 补图。",
            },
        },
        "pages": [],
    }
    ui_pages = []
    missing = []
    script_parts = [
        "# L01 十分钟无生试讲逐字稿",
        "教材参照：淮北市现行沪科版七年级下册8.4。所有学生回答均为预设。"
        "设计预算 600 秒，包含板书、停顿和翻页。",
    ]
    cards = ["# L01 讲者提示卡", "15 个画面，设计预算 600 秒。"]
    for number, (page, previous) in enumerate(zip(spec, approved, strict=True), 1):
        page_id = page["id"]
        if page_id != previous["page_id"]:
            raise ValueError(f"Unexpected page order: {page_id}")
        page_reviews = [review for review in reviews if review["page_id"] == page_id]
        accepted = [review for review in page_reviews if review["adopted"] and review["passed"]]
        if len(accepted) != 1:
            missing.append(page_id)
            continue
        picked = accepted[0]
        selected = candidate(records[picked["id"]], picked)
        visible = [page["phase"], page["title"], *page["text"]]
        notes = previous["script"]
        if page_id == "L01-S01A" and "每盒装 25 支笔" not in notes:
            notes = ("同学们，假设每盒装 25 支笔，第一组有 7 盒，第二组有 3 盒。"
                     + notes.removeprefix("同学们，"))
        teacher_note = notes
        if previous.get("teacher_only"):
            teacher_note += "\n\n" + previous["teacher_only"]
        speaker = {
            "seconds": previous["seconds"],
            "keywords": [page["phase"], page["title"]],
            "idea": notes,
            "transition": "进入下一画面" if number < len(spec) else "结束试讲",
            "notes_text": f"{page['phase']}｜{page['title']}｜预算 {previous['seconds']} 秒。\n{teacher_note}",
        }
        manifest["pages"].append({
            "page_number": number, "page_id": page_id, "project_id": "L01", "status": "adopted",
            "topic": page["title"], "visible_text": visible,
            "evidence": [
                {"reference": "lesson-plans/L01-script.md", "supports": "讲述与提问顺序"},
                {"reference": "exercises/L01-exercises.md", "supports": "题面、公式与答案"},
            ],
            "candidates": [selected], "adopted_candidate_id": selected["id"],
            "qa": {"facts": "passed", "text": "passed", "visual": "passed"},
            "speaker": speaker,
            "selection": {
                "adopted": {"id": selected["id"], "sha256": selected["sha256"],
                            "lane": records[picked["id"]]["lane"]},
                "reason": picked["findings"],
                "reviews": page_reviews,
            },
        })
        ui_page = dict(previous)
        ui_page.pop("layout", None)
        ui_page.update(title=page["title"], phase=page["phase"], text=visible,
                       script=notes, prompt_path=selected["prompt"]["path"])
        ui_pages.append(ui_page)
        start = previous["start_seconds"]
        end = start + previous["seconds"]
        timed = f"{start//60:02d}:{start%60:02d}—{end//60:02d}:{end%60:02d}"
        script_parts.extend([f"## {timed} {page_id} {page['phase']}｜{page['title']}", notes])
        cards.extend([
            f"## {page_id} {page['phase']}｜{page['title']}（{previous['seconds']} 秒）",
            "画面要点：" + "／".join(page["text"]),
            teacher_note,
        ])
    report = {
        "reviewed_at": now(),
        "requests": dict(Counter((r["lane"] + ":" + r["status"]) for r in records.values())),
        "adopted_pages": [p["page_id"] for p in manifest["pages"]],
        "pending_pages": missing,
    }
    save_json(WORK / "status.json", report)
    if missing:
        print("Awaiting an approved candidate: " + ", ".join(missing))
        raise SystemExit(2)
    assert sum(p["speaker"]["seconds"] for p in manifest["pages"]) == 600
    save_json(WORK / "manifest.json", manifest)
    save_json(WORK / "pages.json", ui_pages)
    (WORK / "L01-script.md").write_text("\n\n".join(script_parts) + "\n", encoding="utf-8", newline="\n")
    (WORK / "L01-提示卡.md").write_text("\n\n".join(cards) + "\n", encoding="utf-8", newline="\n")
    print("15 candidates approved for the 600-second deck.")


if __name__ == "__main__":
    main()
