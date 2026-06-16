import json
import os
import tempfile
from datetime import datetime

from hudict.config import config


def now_id():
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")


def write_json_atomic(path, payload):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(prefix=".tmp-", suffix=".json", dir=os.path.dirname(path))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, path)
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def dump_lookup(image, payload):
    if not config.debug_capture:
        return
    debug_dir = config.resolved_debug_dir
    os.makedirs(debug_dir, exist_ok=True)
    ident = now_id()
    image_path = os.path.join(debug_dir, f"{ident}.png")
    json_path = os.path.join(debug_dir, f"{ident}.json")
    image.save(image_path)
    payload = {"timestamp": ident, "image_path": image_path, "json_path": json_path, **payload}
    write_json_atomic(json_path, payload)
