"""Read an LSR image."""

from __future__ import annotations

import io
import json
import zipfile

from deprecation import deprecated
from PIL import Image


def jsonLoadsFromArchive(x):
	return json.loads(x.read_text(encoding="utf-8"))


class LSRImage:
	"""LSRImage contains data on the overall size, the layers and the name of the lsr image."""

	def __init__(self, size: tuple[int, int], name: str, layers: list[LSRLayer] | None = None) -> None:
		self.size = size
		self.layers = layers if layers is not None else []
		self.name = name

	def flatten(self) -> Image.Image:
		"""Flatten all of the layers."""
		return flattenAll(
			[LSRImageData(layer.flatten(), "", offsets=layer.offsets()) for layer in self.layers],
			self.size,
		)


class LSRLayer:
	"""LSRLayer contains data on the layer such as the list of images, the name,
	the size and the centre offset.
	"""

	def __init__(
		self,
		images: list[LSRImageData],
		name: str,
		size: tuple[int, int],
		center: tuple[int, int],
	) -> None:
		self.images = images
		self.name = name
		self.size = size
		self.center = center

	def offsets(self) -> tuple[int, int]:
		"""Calculate the x, y offset for the top left corner.

		Returns
		-------
			tuple[int, int]: tuple for x, y offset

		"""
		return (
			int(self.center[0] - self.size[0] / 2),
			int(self.center[1] - self.size[1] / 2),
		)
		# return 0, 0

	def flatten(self) -> Image.Image:
		"""Flatten all of the layers."""
		return flattenAll(self.images, self.size)


class LSRImageData:
	"""LSRImageData stores the PIL Image along with the name, scale of the image and the idiom."""

	def __init__(
		self,
		image: Image.Image,
		name: str,
		scale: str = "1x",
		idiom: str = "universal",
		offsets: tuple[int, int] = (0, 0),
	) -> None:
		self.image = image
		self.name = name
		self.scale = int(scale.replace("x", ""))
		self.idiom = idiom
		self.offsets = offsets

	def scaledImage(self):
		"""Get the scaled image.

		Returns
		-------
			Image.Image: The image to scale

		"""
		width, height = self.image.size
		return self.image.resize((width * self.scale, height * self.scale))


def read(filename: str) -> LSRImage:
	"""Read an lsr file.

	Args:
	----
		filename (str): the path to the file

	Returns:
	-------
		LSRImage: An lsr image representation

	"""
	with zipfile.ZipFile(filename, "r") as zipref:
		zippath = zipfile.Path(zipref)
		contents = jsonLoadsFromArchive(zippath / "Contents.json")
		layers = contents["layers"]
		lsrLayers = []
		for layer in layers:
			lsrImageData = []
			layerContents = jsonLoadsFromArchive(
				zippath / layer["filename"] / "Contents.json",
			)["properties"]
			layerImagesList = jsonLoadsFromArchive(
				zippath / layer["filename"] / "Content.imageset/Contents.json",
			)["images"]
			for image in layerImagesList:
				with zipref.open(
					layer["filename"] + "/Content.imageset/" + image["filename"]
				) as layerImage:
					lsrImageData.append(
						LSRImageData(
							Image.open(layerImage).convert("RGBA"),
							image["filename"].replace(".png", ""),
							image.get("scale", "1x"),
							image.get("idiom", "universal"),
						)
					)
			lsrLayers.append(
				LSRLayer(
					lsrImageData[::-1],
					layer["filename"].replace(".imagestacklayer", ""),
					(
						layerContents["frame-size"]["width"],
						layerContents["frame-size"]["height"],
					),
					(
						layerContents["frame-center"]["x"],
						layerContents["frame-center"]["y"],
					),
				)
			)
		return LSRImage(
			(
				contents["properties"]["canvasSize"]["width"],
				contents["properties"]["canvasSize"]["height"],
			),
			filename.replace(".lsr", ""),
			lsrLayers[::-1],
		)


def write(filename: str, lsrImage: LSRImage) -> None:
	"""Write an lsr image to disk.

	Args:
	----
		filename (str): filename and extension
		lsrImage (LSRImage): the lsr image representation to save

	"""
	_info = {"version": 1, "author": "pylsr"}

	with zipfile.ZipFile(filename, "w") as zipref:
		layers = [{"filename": layer.name + ".imagestacklayer"} for layer in lsrImage.layers[::-1]]
		zipref.writestr(
			"Contents.json",
			json.dumps(
				{
					"info": _info,
					"layers": layers,
					"properties": {
						"canvasSize": {
							"width": lsrImage.size[0],
							"height": lsrImage.size[1],
						}
					},
				}
			),
		)
		for layer in lsrImage.layers[::-1]:
			zipref.writestr(
				layer.name + ".imagestacklayer/Contents.json",
				json.dumps(
					{
						"info": _info,
						"properties": {
							"frame-size": {
								"width": layer.size[0],
								"height": layer.size[1],
							},
							"frame-center": {
								"x": layer.center[0],
								"y": layer.center[1],
							},
						},
					}
				),
			)
			images = [
				{
					"idiom": image.idiom,
					"filename": image.name + ".png",
					"scale": str(image.scale) + "x",
				}
				for image in layer.images[::-1]
			]
			zipref.writestr(
				layer.name + ".imagestacklayer/Content.imageset/Contents.json",
				json.dumps({"info": _info, "images": images}),
			)
			for image in layer.images[::-1]:
				imgByteArr = io.BytesIO()
				image.image.save(imgByteArr, format="PNG")
				imgByteArr.seek(0)
				zipref.writestr(
					layer.name + ".imagestacklayer/Content.imageset/" + image.name + ".png",
					imgByteArr.read(),
				)


def flattenTwoLayers(
	layer: LSRImageData,
	imageDimensions: tuple[int, int],
	flattenedSoFar: Image.Image | None = None,
) -> Image.Image:
	"""Flatten two layers of an image.

	Args:
	----
		layer (LSRImageData): lsrimagedata
		imageDimensions (tuple[int, int]): a tuple of the image dimensions
		flattenedSoFar (Image.Image, optional): Render of what has already been
		flattened. Defaults to None.

	Returns:
	-------
		Image.Image: Flattened image

	"""
	foregroundRender = renderImageOffset(layer.scaledImage(), imageDimensions, layer.offsets)
	if flattenedSoFar is None:
		return foregroundRender
	return Image.alpha_composite(flattenedSoFar, foregroundRender)


def flattenAll(layers: list[LSRImageData], imageDimensions: tuple[int, int]) -> Image.Image:
	"""Flatten a list of layers and groups.

	Args:
	----
		layers (list[LSRImageData]): A list of layers and groups
		imageDimensions (tuple[int, int]): size of the image
		been flattened. Defaults to None.

	Returns:
	-------
		Image.Image: Flattened image

	"""
	flattenedSoFar = flattenTwoLayers(layers[0], imageDimensions)
	for layer in range(1, len(layers)):
		flattenedSoFar = flattenTwoLayers(
			layers[layer], imageDimensions, flattenedSoFar=flattenedSoFar
		)
	return flattenedSoFar


@deprecated(deprecated_in="2022", removed_in="2023", details="Use renderImageOffset")
def rasterImageOffset(
	image: Image.Image, size: tuple[int, int], offsets: tuple[int, int] = (0, 0)
) -> Image.Image:
	"""Render an image with offset to a given size. (deprecated, use renderImageOffset)."""
	return renderImageOffset(image, size, offsets)


def renderImageOffset(
	image: Image.Image, size: tuple[int, int], offsets: tuple[int, int] = (0, 0)
) -> Image.Image:
	"""Render an image with offset to a given size."""
	imageOffset = Image.new("RGBA", size)
	imageOffset.paste(
		image.convert("RGBA"), (int(offsets[0]), int(offsets[1])), image.convert("RGBA")
	)
	return imageOffset
