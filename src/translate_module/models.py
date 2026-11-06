from pydantic import BaseModel, Field, ConfigDict


class TranslateRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=False, extra="forbid")
    text: str = Field(min_length=1, max_length=10000)
    source_lang: str = Field(default="auto", min_length=2, max_length=5)
    target_lang: str = Field(default="vi", min_length=2, max_length=5)


class TranslateResponse(BaseModel):
    translated_text: str
    source_lang: str
    target_lang: str


class HealthResponse(BaseModel):
    status: str
    engine: str
    models_loaded: bool


class LanguagePair(BaseModel):
    source_lang: str
    target_lang: str


class LanguagesResponse(BaseModel):
    languages: list[str]
    pairs: list[LanguagePair]
