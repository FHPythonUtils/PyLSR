"""Test pylsr
"""
import sys
from pathlib import Path

THISDIR = str(Path(__file__).resolve().parent)
sys.path.insert(0, str(Path(THISDIR).parent))
import pylsr

# Copy an image
pylsr.write(THISDIR + "/test1copy.lsr", pylsr.read(THISDIR + "/test1.lsr"))

# Render an image
pylsr.read(THISDIR + "/test1.lsr").flatten().save(THISDIR + "/test1.png")

# Render the copy
pylsr.read(THISDIR + "/test1copy.lsr").flatten().save(THISDIR + "/test1copy.png")

# Copy an image
pylsr.write(THISDIR + "/test3copy.lsr", pylsr.read(THISDIR + "/test3.lsr"))
pylsr.read(THISDIR + "/test3.lsr").flatten().save(THISDIR + "/test3.png")
pylsr.read(THISDIR + "/test3copy.lsr").flatten().save(THISDIR + "/test3copy.png")
