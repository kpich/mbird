from datetime import datetime

from mbird_data import MbirdData


class State:
    """Manages global application state."""

    def __init__(self):
        self.current_data: MbirdData | None = None
        self.current_path: str | None = None
        self.last_saved: datetime | None = None

    def reset(self) -> None:
        """Reset all state to None."""
        self.current_data = None
        self.current_path = None
        self.last_saved = None
