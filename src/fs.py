#!/usr/bin/env python

import os
import logging
from dataclasses import dataclass, field


@dataclass
class FS:
    """
    This is one of those classes that essentially should be split to one, that is a 'type' describing where things are
    and then another one that uses this one to create folders, sometimes I even add minor wrapper classes for yielding cleaned up lines from large files
    and various other filesystem related operations
    """
    cwd: str = field(init=False, default=os.path.dirname(os.path.abspath(__file__)))
    storage_folder: str = field(init=False, default=None)
    data_folder: str = field(init=False, default=None)
    logs_folder: str = field(init=False, default=None)
    log_file: str = field(init=False, default=None)

    def __post_init__(self):
        self.storage_folder = os.path.abspath(f"{self.cwd}/../storage")
        self.data_folder = f"{self.storage_folder}/data"
        self.logs_folder = f"{self.storage_folder}/logs"
        self.log_file = f"{self.logs_folder}/squirro.log"
        self.scaffold_folders()

    def scaffold_folders(self):
        os.makedirs(self.storage_folder, exist_ok=True)
        os.makedirs(self.data_folder, exist_ok=True)
        os.makedirs(self.logs_folder, exist_ok=True)