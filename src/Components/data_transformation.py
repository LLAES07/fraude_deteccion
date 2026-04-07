# Carga de librerias

import os
import re
import numpy as np
from dataclasses import dataclass
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from src.exception import CustomExecption
from src.logger import logging


@dataclass
class DataTransformationConfig:
    pass
