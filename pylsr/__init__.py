"""Read an LSR image
"""
import zipfile
import json
import io
from PIL import Image

class LSRImage():
	"""LSRImage contains data on the overall size, the layers and the name of
	the lsr image
	"""
	def __init__(self, size, name, layers=[]):
		self.size = size
		self.layers = layers
		self.name = name

	def flatten(self):
		""" Flatten all of the layers """
		return flattenAll([LSRImageData(layer.flatten(), "",
		offsets=layer.offsets()) for layer in self.layers], self.size)


class LSRLayer():
	"""LSRLayer contains data on the layer such as the list of images, the name
	the size and the centre offset
	"""
	def __init__(self, images, name, size, center):
		self.images = images
		self.name = name
		self.size = size
		self.center = center

	def offsets(self):
		"""Calculate the x, y offset for the top left corner

		Returns:
			(int, int): Tuple for x, y offset
		"""
		print(self.center[0] - self.size[0]/2, self.center[1] - self.size[1]/2)
		return (self.center[0] - self.size[0]/2, self.center[1] - self.size[1]/2)
		#return 0, 0

	def flatten(self):
		""" Faltten all of the layers """
		return flattenAll(self.images, self.size)


class LSRImageData():
	"""LSRImageData stores the PIL Image along with the name, scale of the image
	and the idiom
	"""
	def __init__(self, image, name, scale="1x", idiom="universal", offsets=(0, 0)):
		self.image = image
		self.name = name
		self.scale = int(scale.replace("x", ""))
		self.idiom = idiom
		self.offsets = offsets

	def scaledImage(self):
		"""Get the scaled image

		Returns:
			PIL.Image: The image to scale
		"""
		width, height = self.image.size
		return self.image.resize((width * self.scale, height * self.scale))


def read(filename):
	"""Read an lsr file

	Args:
		filename (string): the path to the file

	Returns:
		LSRImage: An lsr image representation
	"""
	lsrImage = None
	with zipfile.ZipFile(filename, 'r') as zipref:
		contents = json.load(zipref.open("Contents.json"))
		layers = contents["layers"]
		lsrLayers = []
		for layer in layers:
			lsrImageData = []
			layerContents = json.load(zipref.open(layer["filename"] + "/Contents.json"))["properties"]
			layerImagesList = json.load(zipref.open(layer["filename"] +
			"/Content.imageset/Contents.json"))["images"]
			for image in layerImagesList:
				with zipref.open(layer["filename"] + "/Content.imageset/" + image['filename']) as layerImage:
					lsrImageData.append(LSRImageData(Image.open(layerImage).convert('RGBA'),
					image["filename"].replace(".png", ""), image["scale"], image["idiom"]))
			lsrLayers.append(LSRLayer(lsrImageData[::-1], layer["filename"].replace(".imagestacklayer", ""),
			(layerContents["frame-size"]["width"], layerContents["frame-size"]["height"]),
			(layerContents["frame-center"]["x"], layerContents["frame-center"]["y"])))
		lsrImage = LSRImage((contents["properties"]["canvasSize"]["width"],
		contents["properties"]["canvasSize"]["height"]), filename.replace(".lsr", ""), lsrLayers[::-1])
	return lsrImage


def write(filename, lsrImage):
	"""Write an lsr image to disk

	Args:
		filename (string): filename and extension
		lsrImage (LSRImage): the lsr image representation to save
	"""
	INFO = {"version": 1, "author": "pylsr"}

	with zipfile.ZipFile(filename, 'w') as zipref:
		layers = [{"filename": layer.name+ ".imagestacklayer"} for layer in lsrImage.layers[::-1]]
		zipref.writestr("Contents.json",
		json.dumps({"info": INFO,
		"layers": layers,
		"properties": {"canvasSize": {"width": lsrImage.size[0], "height": lsrImage.size[1]}}}))
		for layer in lsrImage.layers[::-1]:
			zipref.writestr(layer.name + ".imagestacklayer/Contents.json",
			json.dumps({"info": INFO,
			"properties": {"frame-size": {"width": layer.size[0], "height": layer.size[1],
			"frame-center": {"x": layer.center[0], "y": layer.center[1]}}}}))
			for image in layer.images[::-1]:
				images = [{"idiom": image.idiom, "filename": image.name + ".png",
				"scale": str(image.scale) + "x"} for image in layer.images[::-1]]
				zipref.writestr(layer.name + ".imagestacklayer/Content.imageset/Contents.json",
				json.dumps({"info": INFO,
				"images": images}))
				imgByteArr = io.BytesIO()
				image.image.save(imgByteArr, format='PNG')
				imgByteArr.seek(0)
				zipref.writestr(layer.name + ".imagestacklayer/Content.imageset/" +
				image.name + ".png", imgByteArr.read())

def flattenTwoLayers(layer, imageDimensions, flattenedSoFar=None):
	"""Flatten two layers of an image

	Args:
		layer (LSRLayer): an lsr layer
		imageDimensions ((int, int)): a tuple of the image dimensions
		flattenedSoFar (PIL.Image, optional): Raster of what has already been
		flattened. Defaults to None.

	Returns:
		[type]: [description]
	"""
	foregroundRaster = rasterImageOffset(layer.scaledImage(), imageDimensions,
	layer.offsets)
	if flattenedSoFar is None:
		return foregroundRaster
	return Image.alpha_composite(flattenedSoFar, foregroundRaster)



def flattenAll(layers, imageDimensions):
	"""Flatten a list of layers and groups

	Args:
		layers ([Layer|Group]): A list of layers and groups
		imageDimensions ((int, int)): size of the image
		been flattened. Defaults to None.

	Returns:
		PIL.Image: Flattened image
	"""
	flattenedSoFar = flattenTwoLayers(layers[0], imageDimensions)
	for layer in range(1, len(layers)):
		flattenedSoFar = flattenTwoLayers(layers[layer], imageDimensions,
		flattenedSoFar=flattenedSoFar)
	return flattenedSoFar


def rasterImageOffset(image, size, offsets=(0, 0)):
	""" Rasterise an image with offset to a given size"""
	imageOffset = Image.new("RGBA", size)
	imageOffset.paste(image.convert("RGBA"), (int(offsets[0]), int(offsets[1])), image.convert("RGBA"))
	return imageOffset
