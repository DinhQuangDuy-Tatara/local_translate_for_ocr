import uvicorn
from fastapi import FastAPI
from .api import router
from .config import Settings
from .translator import Translator


def create_app(translator=None, settings=None):
    settings = settings or Settings()
    app = FastAPI(title="Local Translate API", version="0.1.0")
    app.state.translator = translator or Translator(max_text_length=settings.max_text_length)
    app.include_router(router)
    return app


def run():
    settings = Settings()
    uvicorn.run(
        create_app(settings=settings),
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level,
    )


app = create_app()

if __name__ == "__main__":
    run()
