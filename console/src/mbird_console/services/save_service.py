from datetime import datetime, timezone

from mbird_console.state import State
from mbird_data import MbirdData


class SaveService:
    """Manages project saving and save status tracking."""

    def __init__(self, state: State):
        self.state = state

    def save_project(self, data: MbirdData, path: str) -> datetime:
        """Save project to disk and update last saved timestamp."""
        data.save(path)
        timestamp = datetime.now(timezone.utc)
        self.state.last_saved = timestamp
        return timestamp

    def get_last_saved(self) -> datetime | None:
        """Get last saved timestamp."""
        return self.state.last_saved
