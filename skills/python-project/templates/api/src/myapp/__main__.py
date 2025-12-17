"""Entry point for running as module: python -m myapp"""

import uvicorn

from myapp.config import settings


def main() -> None:
    uvicorn.run(
        "myapp.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.debug,
    )


if __name__ == "__main__":
    main()
