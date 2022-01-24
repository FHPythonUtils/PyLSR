"""Test pylsr
"""
from __future__ import annotations

import sys
from pathlib import Path

from imgcompare import imgcompare
from PIL import Image

THISDIR = str(Path(__file__).resolve().parent)
sys.path.insert(0, str(Path(THISDIR).parent))


THISDIR = str(Path(__file__).resolve().parent)
sys.path.insert(0, str(Path(THISDIR).parent))
import pylsr


def test_1():
	pylsr.write(f"{THISDIR}/data/test1copy.lsr", pylsr.read(f"{THISDIR}/data/test1.lsr"))
	output = f"{THISDIR}/data/test1.png"
	expected = f"{THISDIR}/data/test1_expected.png"
	pylsr.read(f"{THISDIR}/data/test1.lsr").flatten().save(output)
	assert imgcompare.is_equal(
		output,
		expected,
		tolerance=0.2,
	)
	output = f"{THISDIR}/data/test1copy.png"
	pylsr.read(f"{THISDIR}/data/test1copy.lsr").flatten().save(output)
	assert imgcompare.is_equal(
		output,
		expected,
		tolerance=0.2,
	)


# Copy an image
def test_3():
	pylsr.write(f"{THISDIR}/data/test3copy.lsr", pylsr.read(f"{THISDIR}/data/test3.lsr"))
	output = f"{THISDIR}/data/test3.png"
	expected = f"{THISDIR}/data/test3_expected.png"
	pylsr.read(f"{THISDIR}/data/test3.lsr").flatten().save(output)
	assert imgcompare.is_equal(
		output,
		expected,
		tolerance=0.2,
	)
	output = f"{THISDIR}/data/test3copy.png"
	pylsr.read(f"{THISDIR}/data/test3copy.lsr").flatten().save(output)
	assert imgcompare.is_equal(
		output,
		expected,
		tolerance=0.2,
	)


if __name__ == "__main__":
	test_1()
	test_3()
