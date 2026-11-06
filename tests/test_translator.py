
import pytest

from translate_module.exceptions import UnsupportedLanguageError
from translate_module.translator import Translator


class FakeEngine:
    name = "fake"

    def translate(self, text, source_lang, target_lang):
        return f"{source_lang}>{target_lang}:{text}"


def test_translator_normalizes_and_translates():
    result, source = Translator(
        engine=FakeEngine()
    ).translate("  안녕  ", "ko", "vi")

    assert result == "ko>vi:안녕"
    assert source == "ko"


def test_auto_script_detection():
    result, source = Translator(
        engine=FakeEngine()
    ).translate("안녕하세요", "auto", "vi")

    assert source == "ko"
    assert result == "ko>vi:안녕하세요"


def test_auto_detects_japanese_script():
    result, source = Translator(
        engine=FakeEngine()
    ).translate("こんにちは", "auto", "vi")

    assert source == "ja"


def test_auto_does_not_guess_latin_text():
    with pytest.raises(UnsupportedLanguageError):
        Translator(
            engine=FakeEngine()
        ).translate("Hello there", "auto", "vi")
