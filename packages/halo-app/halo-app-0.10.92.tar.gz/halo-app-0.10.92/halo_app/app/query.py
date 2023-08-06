from __future__ import annotations
import abc
import logging
import uuid
from typing import List, Dict, Callable, Type, TYPE_CHECKING

# halo
from halo_app.classes import AbsBaseClass
from halo_app.app.context import HaloContext
from halo_app.app.message import AbsHaloMessage
from halo_app.settingsx import settingsx

logger = logging.getLogger(__name__)

settings = settingsx()

class AbsHaloQuery(AbsHaloMessage):
    name = None
    vars = None

    def __init__(self):
        super(AbsHaloQuery,self).__init__()


class HaloQuery(AbsHaloQuery):

    def __init__(self, name:str,vars:Dict):
        super(HaloQuery,self).__init__()
        self.name = name
        self.vars = vars







