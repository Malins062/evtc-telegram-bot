from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("evtc_bot")
except PackageNotFoundError:
    __version__ = "Unknown"
