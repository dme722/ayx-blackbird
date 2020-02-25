"""Configure tests."""
import os
import sys

import ayx_blackbird

blackbird_dir = os.path.dirname(ayx_blackbird.__file__)
sys.path.append(os.path.join(blackbird_dir, "mocks"))

from .fixtures import *  # noqa
