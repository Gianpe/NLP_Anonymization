from pathlib import Path
from spacy.util import load_model_from_init_py, get_model_meta

from . import rel_model
from . import rel_pipe

__version__ = get_model_meta(Path(__file__).parent)['version']


def load(**overrides):
    return load_model_from_init_py(__file__, **overrides)
