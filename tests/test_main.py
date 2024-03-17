"""Test pylsr"""

from __future__ import annotations

import sys
from pathlib import Path

from imgcompare import imgcompare

THISDIR = str(Path(__file__).resolve().parent)
sys.path.insert(0, str(Path(THISDIR).parent))
import pylsr


def aux_testCopy(baseName: str) -> None:
	pylsr.write(
		f"{THISDIR}/data/{baseName}copy.lsr",
		pylsr.read(f"{THISDIR}/data/{baseName}.lsr"),
	)
	output = f"{THISDIR}/data/{baseName}.png"
	expected = f"{THISDIR}/data/{baseName}_expected.png"
	pylsr.read(f"{THISDIR}/data/{baseName}.lsr").flatten().save(output)
	assert imgcompare.is_equal(
		output,
		expected,
		tolerance=0.2,
	)
	output = f"{THISDIR}/data/{baseName}copy.png"
	pylsr.read(f"{THISDIR}/data/{baseName}copy.lsr").flatten().save(output)
	assert imgcompare.is_equal(
		output,
		expected,
		tolerance=0.2,
	)


def test_1():
	return aux_testCopy("test1")


# Copy an image
def test_3():
	return aux_testCopy("test3")


def test_pull4():
	return aux_testCopy("pull4")


if __name__ == "__main__":
	test_1()
	test_3()
	test_pull4()
