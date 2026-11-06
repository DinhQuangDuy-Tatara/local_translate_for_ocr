
import pytest

from translate_module.engines.argos_engine import ArgosEngine
from translate_module.exceptions import ModelNotInstalledError


class FakeTranslation:
    def __init__(self, to_lang, prefix):
        self.to_lang = to_lang
        self.prefix = prefix

    def translate(self, text):
        return f"{self.prefix}({text})"


class FakeLang:
    def __init__(self, code):
        self.code = code
        self.translations = []


def make_engine():
    ko = FakeLang("ko")
    en = FakeLang("en")
    vi = FakeLang("vi")

    ko.translations = [
        FakeTranslation(en, "ko-en")
    ]

    en.translations = [
        FakeTranslation(vi, "en-vi")
    ]

    engine = ArgosEngine.__new__(ArgosEngine)

    engine._translate = type(
        "FakeArgos",
        (),
        {
            "get_installed_languages": staticmethod(
                lambda: [ko, en, vi]
            )
        },
    )

    return engine


def test_engine_finds_and_runs_two_step_route():
    engine = make_engine()

    result = engine.translate(
        "안녕",
        "ko",
        "vi",
    )

    assert result == "en-vi(ko-en(안녕))"


def test_pairs_includes_reachable_indirect_pair():
    engine = make_engine()

    assert ("ko", "vi") in engine.pairs()
    assert ("ko", "en") in engine.pairs()


def test_engine_reports_missing_route():
    engine = make_engine()

    with pytest.raises(ModelNotInstalledError):
        engine.translate(
            "你好",
            "vi",
            "ko",
        )
