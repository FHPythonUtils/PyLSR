<a name=".make"></a>
## make

Makefile for python. Run one of the following subcommands:

install: Poetry install
build: Building docs, requirements.txt, setup.py, poetry build

<a name=".pylsr"></a>
## pylsr

Read an LSR image

<a name=".pylsr.LSRImage"></a>
### LSRImage

```python
class LSRImage():
 |  LSRImage(size, name, layers=[])
```

LSRImage contains data on the overall size, the layers and the name of
the lsr image

<a name=".pylsr.LSRImage.flatten"></a>
#### flatten

```python
 | flatten()
```

Flatten all of the layers

<a name=".pylsr.LSRLayer"></a>
### LSRLayer

```python
class LSRLayer():
 |  LSRLayer(images, name, size, center)
```

LSRLayer contains data on the layer such as the list of images, the name
the size and the centre offset

<a name=".pylsr.LSRLayer.offsets"></a>
#### offsets

```python
 | offsets()
```

Calculate the x, y offset for the top left corner

**Returns**:

  (int, int): Tuple for x, y offset

<a name=".pylsr.LSRLayer.flatten"></a>
#### flatten

```python
 | flatten()
```

Faltten all of the layers

<a name=".pylsr.LSRImageData"></a>
### LSRImageData

```python
class LSRImageData():
 |  LSRImageData(image, name, scale="1x", idiom="universal", offsets=(0, 0))
```

LSRImageData stores the PIL Image along with the name, scale of the image
and the idiom

<a name=".pylsr.LSRImageData.scaledImage"></a>
#### scaledImage

```python
 | scaledImage()
```

Get the scaled image

**Returns**:

- `PIL.Image` - The image to scale

<a name=".pylsr.read"></a>
#### read

```python
read(filename)
```

Read an lsr file

**Arguments**:

- `filename` _string_ - the path to the file
  

**Returns**:

- `LSRImage` - An lsr image representation

<a name=".pylsr.write"></a>
#### write

```python
write(filename, lsrImage)
```

Write an lsr image to disk

**Arguments**:

- `filename` _string_ - filename and extension
- `lsrImage` _LSRImage_ - the lsr image representation to save

<a name=".pylsr.flattenTwoLayers"></a>
#### flattenTwoLayers

```python
flattenTwoLayers(layer, imageDimensions, flattenedSoFar=None)
```

Flatten two layers of an image

**Arguments**:

- `layer` _LSRLayer_ - an lsr layer
  imageDimensions ((int, int)): a tuple of the image dimensions
- `flattenedSoFar` _PIL.Image, optional_ - Raster of what has already been
  flattened. Defaults to None.
  

**Returns**:

- `[type]` - [description]

<a name=".pylsr.flattenAll"></a>
#### flattenAll

```python
flattenAll(layers, imageDimensions)
```

Flatten a list of layers and groups

**Arguments**:

- `layers` _[Layer|Group]_ - A list of layers and groups
  imageDimensions ((int, int)): size of the image
  been flattened. Defaults to None.
  

**Returns**:

- `PIL.Image` - Flattened image

<a name=".pylsr.rasterImageOffset"></a>
#### rasterImageOffset

```python
rasterImageOffset(image, size, offsets=(0, 0))
```

Rasterise an image with offset to a given size

