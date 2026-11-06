import pytest
from translate_module.exceptions import InvalidTextError, UnsupportedLanguageError
from translate_module.translator import Translator


class FakeEngine:
    name = "fake"
    def translate(self, text, source_lang, target_lang): return "ok"


@pytest.mark.parametrize("text", ["", "   ", None, 123])
def test_rejects_invalid_text(text):
    with pytest.raises(InvalidTextError):
        Translator(engine=FakeEngine()).translate(text)


def test_rejects_unsupported_target():
    with pytest.raises(UnsupportedLanguageError):
        Translator(engine=FakeEngine()).translate("hello", "en", "fr")


def test_preserves_internal_newlines():
    value = Translator.normalize_text("  line one\n line two  ")
    assert value == "line one\n line two"
