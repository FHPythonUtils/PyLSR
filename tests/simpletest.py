"""Test pylsr"""

from __future__ import annotations

import sys
from pathlib import Path

THISDIR = str(Path(__file__).resolve().parent)
sys.path.insert(0, str(Path(THISDIR).parent))
import pylsr

# Copy an image
pylsr.write(f"{THISDIR}/data/test1copy.lsr", pylsr.read(f"{THISDIR}/data/test1.lsr"))

# Render an image
pylsr.read(f"{THISDIR}/data/test1.lsr").flatten().save(f"{THISDIR}/data/test1.png")

# Render the copy
pylsr.read(f"{THISDIR}/data/test1copy.lsr").flatten().save(f"{THISDIR}/data/test1copy.png")

# Copy an image
pylsr.write(f"{THISDIR}/data/test3copy.lsr", pylsr.read(f"{THISDIR}/data/test3.lsr"))
pylsr.read(f"{THISDIR}/data/test3.lsr").flatten().save(f"{THISDIR}/data/test3.png")
pylsr.read(f"{THISDIR}/data/test3copy.lsr").flatten().save(f"{THISDIR}/data/test3copy.png")
