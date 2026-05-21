import os
from pathlib import Path
from urllib.parse import urlparse, unquote
from urllib.request import Request, urlopen

_blood_group_model = None
_gender_model = None


def _model_base_dir() -> Path:
    model_dir_env = os.environ.get("MODEL_DIR")
    if model_dir_env:
        base = Path(model_dir_env)
    else:
        base = Path(__file__).resolve().parents[1] / "models"
    base.mkdir(parents=True, exist_ok=True)
    return base


def _download_to(url: str, dest: Path) -> None:
    if dest.exists():
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    req = Request(url, headers={"User-Agent": "fingerprint-api/1"})
    with urlopen(req, timeout=900) as resp:
        with open(tmp, "wb") as f:
            while True:
                chunk = resp.read(8 * 1024 * 1024)
                if not chunk:
                    break
                f.write(chunk)
    tmp.replace(dest)


def _infer_filename(url: str, fallback: str) -> str:
    name = Path(unquote(urlparse(url).path)).name.strip()
    if not name or name in ("/", "."):
        return fallback
    suf = Path(name).suffix.lower()
    if suf not in (".h5", ".keras"):
        return fallback
    return name


def _huggingface_repo_id():
    if os.environ.get("DISABLE_HF_MODEL_DOWNLOAD") == "1":
        return None
    raw = os.environ.get("HUGGINGFACE_MODEL_REPO", "BtechProjectPCCOE/backend_model")
    rid = (raw or "").strip()
    return rid or None


def _download_from_huggingface(repo_id: str, filename: str, dest: Path) -> None:
    if dest.exists():
        return
    from huggingface_hub import hf_hub_download

    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_HUB_TOKEN")
    hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        repo_type="model",
        local_dir=str(dest.parent),
        local_dir_use_symlinks=False,
        token=token,
    )


def ensure_remote_models() -> None:
    """
    Pull missing weights into MODEL_DIR (or backend/models) when `railway up` omits
    the local `models/` folder (see .railwayignore).

    Priority per file:
    1) Already on disk or BLOOD_GROUP_MODEL_PATH / GENDER_MODEL_PATH points to an existing file
    2) BLOOD_GROUP_MODEL_URL / GENDER_MODEL_URL (direct HTTP)
    3) Hugging Face Hub (HUGGINGFACE_MODEL_REPO, default BtechProjectPCCOE/backend_model)
    """
    base = _model_base_dir()
    hf_repo = _huggingface_repo_id()
    specs: list[tuple[str, str, str, list[str]]] = [
        ("BLOOD_GROUP_MODEL_URL", "BLOOD_GROUP_MODEL_PATH", "blood_group.h5", ["blood_group.h5", "blood_group.keras"]),
        ("GENDER_MODEL_URL", "GENDER_MODEL_PATH", "gender_model.keras", ["gender_model.keras", "gender_model.h5"]),
    ]

    for url_key, path_key, default_name, all_names in specs:
        explicit = os.environ.get(path_key)
        if explicit and Path(explicit).exists():
            continue
        if any((base / n).exists() for n in all_names):
            continue

        url = os.environ.get(url_key)
        if url:
            if explicit:
                dest = Path(explicit)
            else:
                fname = _infer_filename(url, default_name)
                dest = base / fname
            _download_to(url, dest)
        elif hf_repo is not None:
            dest = base / default_name
            _download_from_huggingface(hf_repo, default_name, dest)


def _resolve_model_path(env_name: str, default_names: list[str]) -> str:
    env_path = os.environ.get(env_name)
    candidates = []

    if env_path:
        candidates.append(Path(env_path))

    _here = Path(__file__).resolve()
    backend_root = _here.parents[1]
    try:
        monorepo_root = _here.parents[3]
    except IndexError:
        monorepo_root = None

    model_dir_env = os.environ.get("MODEL_DIR")
    if model_dir_env:
        for name in default_names:
            candidates.append(Path(model_dir_env) / name)

    # Common fallback paths (Railway: /app/models/; full repo: <repo>/models/)
    for name in default_names:
        candidates.append(backend_root / "models" / name)
        if monorepo_root is not None:
            candidates.append(monorepo_root / "models" / name)
        candidates.append(Path("/data/models") / name)

    for path in candidates:
        if path.exists():
            return str(path)

    checked = ", ".join(str(p) for p in candidates)
    raise FileNotFoundError(f"{env_name} not found. Checked: {checked}")


def load_blood_group_model():
    global _blood_group_model
    if _blood_group_model is not None:
        return _blood_group_model

    import tensorflow as tf

    model_path = _resolve_model_path("BLOOD_GROUP_MODEL_PATH", ["blood_group.h5", "blood_group.keras"])
    try:
        _blood_group_model = tf.keras.models.load_model(model_path)
    except Exception:
        _blood_group_model = tf.keras.models.load_model(model_path, compile=False)
    return _blood_group_model


def load_gender_model():
    global _gender_model
    if _gender_model is not None:
        return _gender_model

    import tensorflow as tf

    model_path = _resolve_model_path("GENDER_MODEL_PATH", ["gender_model.keras", "gender_model.h5"])
    try:
        _gender_model = tf.keras.models.load_model(model_path)
    except Exception:
        _gender_model = tf.keras.models.load_model(model_path, compile=False)
    return _gender_model
