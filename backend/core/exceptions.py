class AppError(Exception):
    """Base class for all application errors."""
    pass

class SafetyError(AppError):
    """Raised when a path is considered unsafe (e.g. outside allowed directories)."""
    pass