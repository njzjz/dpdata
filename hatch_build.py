"""Hatch build hook for dpdata."""

import os
import subprocess
from pathlib import Path
from shutil import copytree, rmtree
from typing import Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface



class CustomBuildHook(BuildHookInterface):
    """Customized build hook for dpdata."""

    PLUGIN_NAME = "custom"

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        """Initialize the build hook."""
        subprocess.check_call(
            [
                "stubgen",
                "-m",
                "dpdata.system",
                "--inspect-mode",
                "--output",
                ".",
            ]
        )
        
