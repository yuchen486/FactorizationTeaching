"""Record visually reviewed page images and emit the image-first packager inputs."""

import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "slides/pages.json"
ALL_PASSED = {"facts": "passed", "text": "passed", "visual": "passed"}


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def candidate(pid, suffix, path, source, prompt, version, reason, status):
    with Image.open(ROOT / path) as picture:
        width, height = picture.size
        picture.verify()
    return {
        "id": f"{pid}-{suffix}",
        "project_id": "L01",
        "status": status,
        "path": path,
        "sha256": sha(path),
        "source": source,
        "prompt": {"path": prompt, "version": version, "sha256": sha(prompt)},
        "quality": {"rating": "accept", "reason": reason},
        "dimensions": {"width_px": width, "height_px": height},
    }


def main():
    pages = json.loads(PAGES.read_text(encoding="utf-8"))
    manifest = {
        "schema_version": 1,
        "project": {
            "id": "L01",
            "title": "因式分解——提公因式法入门",
            "target_seconds": 600,
            "timing_tolerance_seconds": 0,
            "generation_policy": {
                "mode": "local_typesetting_with_dual_lane_sample",
                "required_lanes": ["native_imagegen", "web_chatgpt"],
                "candidates_per_page_per_lane": 1,
                "budget_reason": "两条图像生成链路用于 S08A 样张。全套采用本地排版，共用公式字体和对齐规则。",
            },
        },
        "pages": [],
    }
    cards = ["# L01 讲者提示卡\n\n15 个状态共 600 秒。\n"]
    for number, page in enumerate(pages, 1):
        pid = page["page_id"]
        visible = page["text"]
        notes = page["script"]
        if page.get("teacher_only"):
            notes += "\n\n" + page["teacher_only"]
        adopted = candidate(
            pid, "typeset-v2", f"assets/slides/{pid}.png",
            {"kind": "local_typesetting", "reference": "scripts/render_slide_images.py + slides/pages.json"},
            page["prompt_path"], "v2",
            "逐字比对更新包的画面文案、数学符号和字号，并核对整套版式。", "adopted",
        )
        entry = {
            "page_number": number, "page_id": pid, "project_id": "L01",
            "status": "adopted", "topic": page["title"], "visible_text": visible,
            "evidence": [{"reference": "slides/L01-detailed-design-v2.md", "supports": "逐页文字与节奏"}],
            "candidates": [adopted], "adopted_candidate_id": adopted["id"], "qa": ALL_PASSED,
            "speaker": {
                "seconds": page["seconds"], "keywords": [page["title"]],
                "idea": page["script"],
                "transition": "进入下一画面" if number < len(pages) else "结束试讲",
                "notes_text": f"{page['title']}｜预算 {page['seconds']} 秒。\n{notes}",
            },
        }
        if number == 1:
            entry["evidence"].append({
                "reference": "assets/branding/huainan-normal-university.png",
                "supports": "从用户修改版 PPTX 首页嵌入对象提取的院校标识",
            })
        if pid == "L01-S08A":
            gen_prompt = "slides/prompts/L01-S08A-candidate-v2.md"
            specifications = [
                ("chrome", "web_chatgpt", "https://chatgpt.com/c/6afcf6c0-d274-83e8-ad89-1a68ea3a4e0b",
                 "公式与三项要求正确，题目字重和双色分隔线与整套排版不同。",
                 "2026-11-18T00:52:14.741Z", "2026-11-18T00:55:19.690Z"),
                ("native", "native_imagegen", "exec-b5b3ecd4-4b1c-4a48-b13c-984315b58c0b.png",
                 "公式与三项要求正确，公式行更宽，双分隔线和题头纵向位置有变化。",
                 "2026-11-18T00:52:33.672Z", "2026-11-18T00:53:02.520Z"),
            ]
            compared = []
            for suffix, lane, reference, reason, submitted, completed in specifications:
                alternate = candidate(pid, suffix, f"assets/candidates/v2/{pid}-{suffix}.png",
                                      {"kind": lane, "reference": reference}, gen_prompt,
                                      "candidate-v2", reason, "verified")
                alternate.update(lane=lane, page_id=pid, qa=ALL_PASSED, generation={
                    "task_status": "downloaded",
                    "submitted_at": submitted,
                    "completed_at": completed,
                    "completed_at_kind": "first_observation" if suffix == "chrome" else "tool_return",
                })
                entry["candidates"].append(alternate)
                compared.append({"id": alternate["id"], "lane": lane, "sha256": alternate["sha256"],
                                 "prompt_sha256": alternate["prompt"]["sha256"], "qa_result": "passed",
                                 "reason": reason})
            entry["selection"] = {
                "status": "compared", "compared_candidates": compared,
                "adopted": {"id": adopted["id"], "lane": "local_typesetting", "sha256": adopted["sha256"]},
                "reason": "本地版沿用前页字号、题头和公式基线，教学文案与公式由审定文本直接排版。",
                "deck_style_consistency": "与全套 1920×1080 页面共用排版源。",
            }
        manifest["pages"].append(entry)
        cards.append(f"## {pid} {page['title']} · {page['seconds']} 秒\n\n{notes}\n")
    (ROOT / "slides/manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                                               encoding="utf-8", newline="\n")
    (ROOT / "outputs/L01-提示卡.md").write_text("\n".join(cards), encoding="utf-8", newline="\n")
    print(f"Prepared manifest for {len(pages)} pages.")


if __name__ == "__main__":
    main()
