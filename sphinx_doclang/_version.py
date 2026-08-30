#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 15 Feb 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
__all__ = (
    "MAJOR", "MINOR", "MICRO", "REVISION",
    "S_STABLE", "VERSION_STRING"
)

#//| Version variables
#//|>--------------------------------------------------------<|
MAJOR: int = 26
MINOR: int = 8
MICRO: int = 30
VERSION_STRING: str = f"{MAJOR}.{MINOR}.{MICRO}"


#//| Development | Revision
#//|>--------------------------------------------------------<|
REVISION: int = 0
S_STABLE: bool = True

# If is not a stable state, update `VERSION_STRING` to reflect that
if not S_STABLE:
    VERSION_STRING = f"{VERSION_STRING}.dev{max(1, REVISION)}"
elif REVISION > 0:
    VERSION_STRING = f"{VERSION_STRING}.rev{REVISION}"


#//| exec'd
#//|>--------------------------------------------------------<|
__version__: str = VERSION_STRING

