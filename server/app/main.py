import uvicorn

from app.infrastructure.config.settings import get_settings
from app.interfaces.http.app import create_app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=get_settings().port)
