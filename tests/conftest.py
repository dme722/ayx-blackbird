"""Configure tests."""
import os
import sys


cur_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(cur_dir, ".."))
sys.path.append(os.path.join(cur_dir, "..", "ayx_blackbird", "sdk_mocks"))
