
import re
import unicodedata

from .exceptions import InvalidTextError, UnsupportedLanguageError
from .engines.argos_engine import ArgosEngine


class Translator:
    """Validate requests, detect source scripts, and delegate translation."""

    SUPPORTED_LANGUAGES = {"ko", "ja", "zh", "zt", "en", "vi"}

    def __init__(self, engine=None, max_text_length: int = 10000):
        self.engine = engine or ArgosEngine()
        self.max_text_length = max_text_length

    @staticmethod
    def normalize_text(text: str) -> str:
        if not isinstance(text, str):
            raise InvalidTextError("text must be a string")

        value = unicodedata.normalize("NFC", text).strip()

        if not value:
            raise InvalidTextError("text must not be empty")

        return value

    @staticmethod
    def detect_language(text: str) -> str | None:
        """Best-effort script detection."""

        if re.search(r"[\uac00-\ud7af]", text):
            return "ko"

        if re.search(r"[\u3040-\u30ff]", text):
            return "ja"

        if re.search(r"[\u3400-\u4dbf\u4e00-\u9fff]", text):
            return "zh"

        return None

    def translate(
        self,
        text: str,
        source_lang: str = "auto",
        target_lang: str = "vi",
    ):
        value = self.normalize_text(text)

        if len(value) > self.max_text_length:
            raise InvalidTextError(
                f"text exceeds maximum length of {self.max_text_length}"
            )

        if source_lang not in ({"auto"} | self.SUPPORTED_LANGUAGES):
            raise UnsupportedLanguageError(
                f"Unsupported source language: {source_lang}"
            )

        if target_lang not in {"vi", "en"}:
            raise UnsupportedLanguageError(
                f"Unsupported target language: {target_lang}"
            )

        actual_source = source_lang

        if source_lang == "auto":
            actual_source = self.detect_language(value)

            if actual_source is None:
                raise UnsupportedLanguageError(
                    "Could not detect source language from its writing system; "
                    "specify source_lang explicitly"
                )

        if actual_source == target_lang:
            raise UnsupportedLanguageError(
                "Source and target languages must differ"
            )

        translated = self.engine.translate(
            value,
            actual_source,
            target_lang,
        )

        return translated, actual_source
