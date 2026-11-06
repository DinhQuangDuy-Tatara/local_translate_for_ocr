
from collections import deque

from ..exceptions import EngineError, ModelNotInstalledError


class ArgosEngine:
    name = "argos"

    def __init__(self):
        try:
            import argostranslate.translate as argos_translate
            self._translate = argos_translate

        except ImportError as exc:
            raise EngineError(
                "Argos Translate is not installed"
            ) from exc

    def _installed_languages(self):
        return self._translate.get_installed_languages()

    def languages(self) -> list[str]:
        return sorted({
            lang.code
            for lang in self._installed_languages()
        })


    def _translation_graph(self, installed_languages=None):
        languages = (
            installed_languages
            if installed_languages is not None
            else self._installed_languages()
        )

        graph = {}

        for source in languages:
            translations = getattr(
            source,
            "translations_from",
            None,
        )

            if translations is None:
                translations = getattr(
                source,
                "translations",
                [],
            )

            graph[source.code] = [
                translation
                for translation in translations
                if getattr(translation, "to_lang", None) is not None
            ]

        return graph
    def _find_path(
        self,
        source_lang: str,
        target_lang: str,
        graph=None,
    ):
        """Find the shortest installed-model route using BFS."""

        if graph is None:
            graph = self._translation_graph()

        if source_lang not in graph:
            return None

        queue = deque([(source_lang, [])])
        visited = {source_lang}

        while queue:
            current, path = queue.popleft()

            if current == target_lang:
                return path

            for translation in graph.get(current, []):
                next_code = translation.to_lang.code

                if next_code not in visited:
                    visited.add(next_code)

                    queue.append((
                        next_code,
                        path + [translation],
                    ))

        return None

    def pairs(self) -> list[tuple[str, str]]:
        """Return all reachable language pairs, including indirect routes."""

        graph = self._translation_graph()
        result = []

        for source_code in graph:
            for target_code in graph:

                if source_code == target_code:
                    continue

                if self._find_path(
                    source_code,
                    target_code,
                    graph,
                ) is not None:
                    result.append((source_code, target_code))

        return sorted(result)

    def models_loaded(self) -> bool:
        return bool(self._installed_languages())

    def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
    ) -> str:

        languages = {
            lang.code: lang
            for lang in self._installed_languages()
        }

        if source_lang not in languages or target_lang not in languages:
            raise ModelNotInstalledError(
                f"Language model not installed: "
                f"{source_lang} -> {target_lang}"
            )

        graph = self._translation_graph(
            list(languages.values())
        )

        path = self._find_path(
            source_lang,
            target_lang,
            graph,
        )

        if path is None:
            raise ModelNotInstalledError(
                f"No installed Argos translation route "
                f"for {source_lang} -> {target_lang}"
            )

        result = text

        try:
            for translation in path:
                result = translation.translate(result)

            return result

        except Exception as exc:
            raise EngineError(
                f"Argos translation failed on route "
                f"{source_lang} -> {target_lang}"
            ) from exc
