# monitoring/registry.py
class SourceRegistry:
    def __init__(self):
        self._sources = {}  # name -> Provider instance

    def add(self, name: str, provider):
        self._sources[name] = provider

    def remove(self, name: str):
        self._sources.pop(name, None)

    def get(self, name: str):
        return self._sources.get(name)

    def all(self) -> dict:
        return dict(self._sources)

    def find_by_kind(self, kind: str) -> list:
        return [(n, p) for n, p in self._sources.items() if p.kind == kind]
