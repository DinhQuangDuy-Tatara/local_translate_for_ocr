import pytest
from fastapi.testclient import TestClient
from translate_module.main import create_app


class FakeEngine:
    name = "argos"
    def translate(self, text, source_lang, target_lang):
        if source_lang == "auto":
            source_lang = "ko"
        return f"translated:{text}"
    def languages(self):
        return ["en", "ko", "vi"]
    def pairs(self):
        return [("ko", "vi"), ("ko", "en")]
    def models_loaded(self):
        return True
    def _detect_language(self, text, langs):
        return "ko"


@pytest.fixture
def client():
    from translate_module.translator import Translator
    app = create_app(translator=Translator(engine=FakeEngine()))
    return TestClient(app)
