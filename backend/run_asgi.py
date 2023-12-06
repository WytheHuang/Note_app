#!/usr/bin/env python
import os
import sys
from pathlib import Path

import warnings

warnings.filterwarnings("ignore")


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.config.settings.local")

    current_path = Path(__file__).parent.resolve()
    sys.path.append(str(current_path / "backend"))

    try:
        import uvicorn

        uvicorn.run(
            app="backend.config.asgi:application",
            host=os.environ.get("SERVER_HOST", default="127.0.0.1"),
            port=int(os.environ.get("SERVER_PORT", default=8000)),
            reload=True,
            env_file=os.environ.get("DOT_ENV_PATH", default=f".env.local"),
        )
    except Exception as e:
        raise e
