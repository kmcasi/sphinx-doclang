#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 15 Feb 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|

#// IMPORT
from sphinx.application import Sphinx
from sphinx.util.typing import ExtensionMetadata

from ._version import VERSION_STRING
from .processor import setup_processor, validate_command_configuration_values
from .manager import TemplateManager


#// RUN
def setup(app: Sphinx) -> ExtensionMetadata:
    setup_processor(app)
    validate_command_configuration_values(app)
    TemplateManager._init_app(app)

    return {
        "version": VERSION_STRING,
        "parallel_read_safe": True,
        "parallel_write_safe": False,
    }
