from fastapi import APIRouter, HTTPException, Request
from .exceptions import InvalidTextError, ModelNotInstalledError, UnsupportedLanguageError, EngineError
from .models import TranslateRequest, TranslateResponse, HealthResponse, LanguagesResponse, LanguagePair

router = APIRouter()


@router.post("/translate", response_model=TranslateResponse)
def translate(payload: TranslateRequest, request: Request):
    translator = request.app.state.translator
    try:
        result, detected_source = translator.translate(
            payload.text, payload.source_lang, payload.target_lang
        )
        return TranslateResponse(
            translated_text=result,
            source_lang=detected_source,
            target_lang=payload.target_lang,
        )
    except InvalidTextError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except UnsupportedLanguageError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except ModelNotInstalledError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except EngineError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/health", response_model=HealthResponse)
def health(request: Request):
    engine = request.app.state.translator.engine
    return HealthResponse(status="ok", engine=engine.name, models_loaded=engine.models_loaded())


@router.get("/languages", response_model=LanguagesResponse)
def languages(request: Request):
    engine = request.app.state.translator.engine
    return LanguagesResponse(
        languages=engine.languages(),
        pairs=[LanguagePair(source_lang=s, target_lang=t) for s, t in engine.pairs()],
    )
