# Basic Jinja Project

Small starter project that renders HTML with Jinja using Python's built-in HTTP server.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 collector.py
```

Open `http://127.0.0.1:8000/`.

## Files

- `collector.py` starts the server and renders templates.
- `templates/base.html` is the shared layout.
- `templates/index.html` is the page template.
