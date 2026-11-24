"""Optional native GIF recovery extension."""
try:
    from . import acropalypse_gif
except ImportError:
    acropalypse_gif = None

__all__ = ["acropalypse_gif"]
