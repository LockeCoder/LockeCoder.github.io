"""Permit offline unit tests when the optional PyMongo wheel is unavailable.

Production installs use the real PyMongo package. This stub is test-only and is
never imported by the application's source code.
"""
import importlib.util
import sys
import types

if importlib.util.find_spec("pymongo") is None:
    pkg = types.ModuleType("pymongo")
    pkg.__path__ = []
    pkg.ASCENDING = 1
    pkg.DESCENDING = -1
    pkg.MongoClient = None
    errors = types.ModuleType("pymongo.errors")
    errors.PyMongoError = type("PyMongoError", (Exception,), {})
    sys.modules["pymongo"] = pkg
    sys.modules["pymongo.errors"] = errors
