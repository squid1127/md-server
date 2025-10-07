"""
md-server
A tiny markdown preview server for your services.
"""

__version__ = "0.1.0"
__author__ = "squid1127"

from .main import app  # noqa: F401
from .cli import cli  # noqa: F401