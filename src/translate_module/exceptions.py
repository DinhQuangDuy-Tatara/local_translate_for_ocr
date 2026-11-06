class TranslateError(Exception):
    """Base exception for local translation errors."""


class InvalidTextError(TranslateError, ValueError):
    pass


class UnsupportedLanguageError(TranslateError, ValueError):
    pass


class ModelNotInstalledError(TranslateError):
    pass


class EngineError(TranslateError):
    pass
