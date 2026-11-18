"""Generate isolated L01 candidates with the configured Windows image channel."""

import argparse
import base64
import datetime
import hashlib
import io
import json
import os
import sqlite3
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlsplit

from PIL import Image, UnidentifiedImageError

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "work/image-v3"
MODEL = "gpt-image-2.5"
CHANNEL = "openai-next-image"
STYLE = (
    "直接生成一张 16:9 横向的七年级数学课堂投影整页图片，2048×1152。"
    "风格是清爽、有一点趣味的教材信息图：浅灰白底 #F8FAFC，深蓝 #17324D 正文，"
    "青绿 #087F8C 强调公因式，琥珀 #B45309 标记易错点。"
    "所有页统一版式：左上靠近安全区的小型浅青环节标签，下一行深蓝大标题。"
    "主视觉是高对比的大号数学公式；说明排成短行。简洁扁平插图用于解释关系，"
    "通常在右侧或提示卡内，约占画面四分之一，不穿过字。"
    "中文用清楚的黑体风格，公式用端正的数学衬线字形，变量斜体。"
    "留足四周 8% 安全区，使用平面色块和清晰笔画，不使用渐变、照片、"
    "页码、脚注、标志、徽章或 logo 占位。"
)


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def save_json(path, data):
    pending = path.with_suffix(".tmp")
    pending.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    pending.replace(path)


def valid_url(url):
    parts = urlsplit(url)
    return not (parts.username or parts.password) and (
        parts.scheme == "https"
        or parts.scheme == "http" and parts.hostname in ("localhost", "127.0.0.1", "::1")
    )


def system_proxy(url):
    origin = urlsplit(url)
    lookup = (
        '$target=[Uri][Console]::ReadLine(); '
        '$proxy=[Net.WebRequest]::GetSystemWebProxy().GetProxy($target); '
        'if($proxy -and $proxy -ne $target){[Console]::Write($proxy.AbsoluteUri)}'
    )
    result = subprocess.run(
        ["pwsh", "-NoProfile", "-NonInteractive", "-Command", lookup],
        input=f"{origin.scheme}://{origin.netloc}\n", text=True,
        capture_output=True, check=True, timeout=12,
    )
    return result.stdout.strip()


def configured_channel():
    database = Path(os.environ["USERPROFILE"]) / "new-api/one-api.db"
    with sqlite3.connect(database.as_uri() + "?mode=ro", uri=True) as connection:
        row = connection.execute("SELECT base_url,key FROM channels WHERE name=?", (CHANNEL,)).fetchone()
    if not row or not all(row) or not valid_url(row[0]):
        raise SystemExit("Image channel is unavailable or has an unsupported endpoint.")
    endpoint, key = row
    return endpoint.rstrip("/"), key, system_proxy(endpoint)


def curl_bytes(url, proxy, *, key=None, payload=None, timeout=240):
    config = [
        "url = " + json.dumps(url),
        "silent", "connect-timeout = 15", f"max-time = {timeout}",
        r'write-out = "\n%{http_code}"',
    ]
    if proxy:
        config.append("proxy = " + json.dumps(proxy))
    if key:
        config.append("header = " + json.dumps("Authorization: Bearer " + key))
    if payload is not None:
        # Preserve UTF-8 in curl's config file syntax and on the wire.
        body = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        config.extend(['header = "Content-Type: application/json; charset=utf-8"',
                       "data = " + json.dumps(body, ensure_ascii=False)])
    reply = subprocess.run(
        ["curl.exe", "-q", "--config", "-"],
        input=("\n".join(config) + "\n").encode("utf-8"),
        capture_output=True, timeout=timeout + 8,
    )
    body, _, code = reply.stdout.rpartition(b"\n")
    return reply.returncode, int(code) if code.isdigit() else 0, body


def prompt_for(page):
    text = "\n".join([page["phase"], page["title"], *page["text"]])
    return (
        f"{STYLE}\n\n"
        "版式和插图指令（这些指令不出现于画面）\n"
        f"{page['art']}\n\n"
        "以下各行是画面必须逐字显示的全部文案。首行是左上角标签，第二行是主标题。"
        "不要抄写此段说明，不添加额外文字。请精确复现每一个字、数字、运算符、括号与平方上标。"
        "求商符号是 ÷，相乘圆点是 ·，平方写作上标 ²，负号是 −。\n\n"
        f"{text}\n"
    )


def run(page, channel, round_number):
    page_id = page["id"]
    prefix = f"{page_id}-api-r{round_number}"
    folder = WORK / "candidates"
    record_path = folder / f"{prefix}.json"
    output = folder / f"{prefix}.png"
    prompt_path = WORK / "prompts" / f"{prefix}.md"
    if record_path.exists():
        record = json.loads(record_path.read_text(encoding="utf-8"))
        if record["status"] != "downloaded" or (
            output.exists() and hashlib.sha256(output.read_bytes()).hexdigest() == record["sha256"]
        ):
            return record
        raise RuntimeError(f"Recorded candidate file changed: {page_id} round {round_number}")
    if round_number == 1:
        prompt_path.write_text(prompt_for(page), encoding="utf-8", newline="\n")
    prompt_bytes = prompt_path.read_bytes()
    endpoint, key, proxy = channel
    start = time.monotonic()
    record = {
        "id": prefix, "page_id": page_id, "lane": "configured_api", "model": MODEL,
        "prompt": prompt_path.relative_to(ROOT).as_posix(),
        "prompt_sha256": hashlib.sha256(prompt_bytes).hexdigest(),
        "status": "submitted", "submitted_at": now(),
    }
    save_json(record_path, record)
    try:
        payload = {"model": MODEL, "prompt": prompt_bytes.decode("utf-8"), "n": 1,
                   "size": "2048x1152", "quality": "medium", "response_format": "b64_json"}
        rc, code, body = curl_bytes(endpoint + "/v1/images/generations", proxy, key=key, payload=payload)
        record.update(http_status=code, transport_exit=rc)
        if rc or code != 200:
            raise ValueError("API request did not return an image response")
        item = json.loads(body)["data"][0]
        record["completed_at"] = now()
        if item.get("b64_json"):
            raw = base64.b64decode(item["b64_json"], validate=True)
        else:
            url = item["url"]
            if not valid_url(url):
                raise ValueError("Unsupported image download location")
            rc, code, raw = curl_bytes(url, system_proxy(url), timeout=120)
            if rc or code != 200:
                raise ValueError("Image download failed")
        with Image.open(io.BytesIO(raw)) as image:
            fmt, size = image.format, image.size
            image.verify()
        if fmt != "PNG" or min(size) == 0:
            raise ValueError("Response is not a valid PNG")
        temporary = output.with_suffix(".part")
        temporary.write_bytes(raw)
        temporary.replace(output)
        record.update(status="downloaded", downloaded_at=now(), dimensions=list(size),
                      sha256=hashlib.sha256(raw).hexdigest(), path=output.relative_to(ROOT).as_posix())
    except (ValueError, KeyError, IndexError, OSError, UnidentifiedImageError, subprocess.SubprocessError) as error:
        record.update(status="failed", failed_at=now(), error_type=type(error).__name__)
    record["seconds"] = round(time.monotonic() - start, 2)
    save_json(record_path, record)
    print(f'{prefix}: {record["status"]} ({record["seconds"]:.1f}s, HTTP {record.get("http_status", 0)})',
          flush=True)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pages", nargs="*", help="Stable page IDs. Empty means all 15.")
    parser.add_argument("--round", choices=(1, 2), default=1, type=int)
    parser.add_argument("--probe", action="store_true")
    args = parser.parse_args()
    endpoint, key, proxy = channel = configured_channel()
    rc, status, _ = curl_bytes(endpoint + "/v1/models", proxy, key=key, timeout=25)
    print(f"Channel preflight: HTTP {status}, Windows system proxy {'on' if proxy else 'off'}", flush=True)
    if rc or status != 200:
        raise SystemExit("Image channel preflight failed.")
    if args.probe:
        return
    for path in (WORK / "prompts", WORK / "candidates"):
        path.mkdir(parents=True, exist_ok=True)
    spec = json.loads((ROOT / "slides/L01-api-v3.json").read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in spec}
    order = ["L01-S02B", "L01-S06B", "L01-S08A"]
    selected = args.pages or [*order, *(pid for pid in by_id if pid not in order)]
    if len(set(selected)) != len(selected) or not set(selected) <= by_id.keys():
        parser.error("Provide unique L01 page IDs from the visual specification")
    with ThreadPoolExecutor(max_workers=2) as pool:
        records = list(pool.map(lambda pid: run(by_id[pid], channel, args.round), selected))
    if any(record["status"] != "downloaded" for record in records):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
