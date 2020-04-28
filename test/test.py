"""Test pylsr
"""
import sys
import os
from pathlib import Path
THISDIR = str(Path(__file__).resolve().parent)
sys.path.insert(0, os.path.dirname(THISDIR))
import pylsr

# Copy an image
pylsr.write(THISDIR + "/test1copy.lsr", pylsr.read(THISDIR + "/test1.lsr"))

# Render an image
pylsr.read(THISDIR + "/test1.lsr").flatten().save(THISDIR + "/test1.png")
