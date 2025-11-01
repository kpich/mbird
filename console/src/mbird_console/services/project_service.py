from mbird_data import MbirdData, MbirdNode

from mbird_console.state import State


class ProjectService:
    """Manages project creation and loading."""

    def __init__(self, state: State):
        self.state = state

    def create_project(self, path: str) -> MbirdData:
        """Create new project with single root node."""
        root = MbirdNode(id="root")
        data = MbirdData(root=root)

        self.state.current_data = data
        self.state.current_path = path

        return data

    def load_project(self, path: str) -> MbirdData:
        """Load project from directory path."""
        data = MbirdData.load(path)

        self.state.current_data = data
        self.state.current_path = path

        return data

    def get_current_data(self) -> MbirdData | None:
        """Get currently loaded project data."""
        return self.state.current_data

    def get_current_path(self) -> str | None:
        """Get current project path."""
        return self.state.current_path

    def has_project(self) -> bool:
        """Check if a project is currently loaded."""
        return self.state.current_data is not None
