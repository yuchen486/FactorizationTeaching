"""Promote the reviewed v3 deck and site into the local working tree."""

import argparse
import shutil
import statistics
from pathlib import Path

from generate_images import ROOT, WORK, save_json
from stage_api_deck import hash_file, load


def write_markdown(path, text):
    path.write_text(text, encoding="utf-8", newline="\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-dir", type=Path, required=True)
    parser.add_argument("--render-review", type=Path, required=True)
    args = parser.parse_args()
    deck = WORK / "deck.pptx"
    site = WORK / "site"
    build = load(args.build_dir / "build_result.json")
    packaged = load(args.build_dir / "manifest.with-final-renders.json")
    manifest = load(WORK / "manifest.json")
    pages = load(WORK / "pages.json")
    review = load(args.render_review)
    ids = [p["page_id"] for p in manifest["pages"]]
    if len(ids) != 15 or set(review) != set(ids):
        raise ValueError("Every slide needs an individual render review.")
    if hash_file(deck) != build["pptx"]["sha256"] or hash_file(site / "L01-课件.pptx") != hash_file(deck):
        raise ValueError("Reviewed PPTX and staged site download do not match.")
    if not all(load(ROOT / f"work/{name}.json")["passed"] for name in ("ui-check", "delivery-ui")):
        raise ValueError("Staged site checks must pass.")
    for page in packaged["pages"]:
        render = page["final_render"]
        pid = page["page_id"]
        if render["sha256"] != review[pid] or hash_file(ROOT / render["path"]) != review[pid]:
            raise ValueError(f"Visual QA is for a different render: {pid}")
    for page in manifest["pages"]:
        selected = page["candidates"][0]
        if hash_file(site / "assets/slides" / f"{page['page_id']}.png") != selected["sha256"]:
            raise ValueError(f"Staged HTML image does not match the deck: {page['page_id']}")

    archive = ROOT / "assets/candidates/v3"
    if archive.exists():
        raise ValueError("The v3 archive already exists.")
    archive.mkdir(parents=True)
    shutil.copytree(WORK / "candidates", archive / "candidates")
    shutil.copytree(WORK / "prompts", archive / "prompts")
    shutil.copy2(WORK / "review.json", archive / "review.json")
    shutil.copy2(args.render_review, archive / "render-review.json")
    records = [load(p) for p in (archive / "candidates").glob("*.json")]

    def archive_path(value):
        return str(value).replace("work/image-v3/", "assets/candidates/v3/", 1)

    for path in (archive / "candidates").glob("*.json"):
        record = load(path)
        for field in ("path", "prompt"):
            if record.get(field):
                record[field] = archive_path(record[field])
        save_json(path, record)
    for page, player_page in zip(manifest["pages"], pages, strict=True):
        selected = page["candidates"][0]
        source = ROOT / selected["path"]
        destination = ROOT / "assets/slides" / f"{page['page_id']}.png"
        shutil.copy2(source, destination)
        selected["path"] = archive_path(selected["path"])
        selected["prompt"]["path"] = archive_path(selected["prompt"]["path"])
        player_page["prompt_path"] = selected["prompt"]["path"]
    # Preserve the packager's original manifest and use portable paths for delivery.
    for page, portable in zip(packaged["pages"], manifest["pages"], strict=True):
        assert page["page_id"] == portable["page_id"]
        page["candidates"] = portable["candidates"]
    save_json(args.build_dir / "manifest.with-final-renders.json", packaged)
    save_json(ROOT / "slides/manifest.json", manifest)
    save_json(ROOT / "slides/pages.json", pages)
    shutil.copytree(site, ROOT / "docs", dirs_exist_ok=True)
    shutil.copy2(deck, ROOT / "outputs/L01-课件.pptx")
    shutil.copy2(WORK / "L01-script.md", ROOT / "lesson-plans/L01-script.md")
    shutil.copy2(WORK / "L01-提示卡.md", ROOT / "outputs/L01-提示卡.md")

    storyboard = ["# L01 纯图分镜（v3）", "15 个画面，600 秒。"]
    for page in pages:
        storyboard.append(
            f"- {page['page_id']}｜{page['phase']}｜{page['title']}｜{page['seconds']} 秒"
            f" — {'／'.join(page['text'][2:])}"
        )
    write_markdown(ROOT / "slides/L01-storyboard.md", "\n\n".join(storyboard) + "\n")

    reviews = load(WORK / "review.json")
    by_id = {r["id"]: r for r in records}
    baseline = [
        "# L01 v3 成图及验收",
        "",
        "15 个状态共 600 秒。前代交付版本为 Git 提交 `d9e7585`。",
        "",
        "|链路|请求|已下载|失败|通过视觉核对|最终采纳|生成耗时中位数|",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for lane, label in (("configured_api", "本地配置的图片 API"), ("web_chatgpt", "Chrome ChatGPT")):
        runs = [r for r in records if r["lane"] == lane]
        downloaded = [r for r in runs if r["status"] == "downloaded"]
        examined = [r for r in reviews if by_id[r["id"]]["lane"] == lane]
        passed = sum(r["passed"] for r in examined)
        finished = [r["seconds"] for r in downloaded if "seconds" in r]
        duration = f"{statistics.median(finished):.1f} 秒" if finished else "—"
        baseline.append(
            f"|{label}|{len(runs)}|{len(downloaded)}|{sum(r['status'] == 'failed' for r in runs)}"
            f"|{passed}/{len(examined)}|{sum(r['adopted'] for r in examined)}|{duration}|"
        )
    baseline.extend([
        "",
        "API 批次并发上限 2。逐次提交时间、HTTP 状态、下载、提示词哈希及审阅见"
        " `assets/candidates/v3/`。Chrome 生成耗时若有记录，为提交至首次观察到成图的间隔。",
        "",
        f"PPTX SHA-256 为 `{hash_file(deck)}`。PPTX 逐页重导入渲染，HTML 为同图源播放。"
        "投影尺寸按 1920×1080 模拟，实地投影与试讲计时待实测。",
    ])
    write_markdown(ROOT / "assets/records/baseline-v3.md", "\n".join(baseline) + "\n")
    print("Promoted reviewed v3 files to the local delivery paths.")


if __name__ == "__main__":
    main()
