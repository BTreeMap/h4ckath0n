import re
from pathlib import Path
from h4ckath0n.app import create_app
from h4ckath0n.config import Settings
settings = Settings(database_url="sqlite+aiosqlite://", password_auth_enabled=True)
app = create_app(settings)

paths = app.openapi().get("paths", {})
routes = []
for path, methods_dict in paths.items():
    for method in sorted(methods_dict.keys()):
        if method.upper() == "HEAD":
            continue
        routes.append((method.upper(), path))

print(f"Total routes: {len(routes)}")

readme_text = Path("README.md").read_text()
missing = []
for method, path in routes:
    path_re = re.escape(path)
    combined = rf"`{method}\s+{path_re}`"
    if not re.search(combined, readme_text, re.IGNORECASE):
        missing.append((method, path))
print(f"Missing: {len(missing)}")
