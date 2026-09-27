# monitoring/providers/base.py
class Provider:
    kind: str = "base"

    def ping(self) -> bool:
        raise NotImplementedError

    def get_summary(self, target: str) -> dict:
        """One-shot pull of headline metrics for a watch panel."""
        raise NotImplementedError
