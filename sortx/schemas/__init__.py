"""
beat.config.schemas.input
 
This module contains the Pydantic schemas for the page input data.
"""

import uuid
from typing import Dict, Final, List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from sortx.schemas.meta import MetaInput


class ProjectData(BaseModel):
    meta_input: MetaInput
    page1_input: Dict
    page2_input: Dict
