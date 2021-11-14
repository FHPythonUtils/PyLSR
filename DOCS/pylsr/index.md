# pylsr

> Auto-generated documentation for [pylsr](../../pylsr/__init__.py) module.

Read an LSR image.

- [Pylsr](../README.md#pylsr-index) / [Modules](../README.md#pylsr-modules) / pylsr
    - [LSRImage](#lsrimage)
        - [LSRImage().flatten](#lsrimageflatten)
    - [LSRImageData](#lsrimagedata)
        - [LSRImageData().scaledImage](#lsrimagedatascaledimage)
    - [LSRLayer](#lsrlayer)
        - [LSRLayer().flatten](#lsrlayerflatten)
        - [LSRLayer().offsets](#lsrlayeroffsets)
    - [flattenAll](#flattenall)
    - [flattenTwoLayers](#flattentwolayers)
    - [rasterImageOffset](#rasterimageoffset)
    - [read](#read)
    - [write](#write)

## LSRImage

[[find in source code]](../../pylsr/__init__.py#L12)

```python
class LSRImage():
    def __init__(
        size: tuple[(int, int)],
        name: str,
        layers: list[LSRLayer] | None = None,
    ):
```

LSRImage contains data on the overall size, the layers and the name of the lsr image.

### LSRImage().flatten

[[find in source code]](../../pylsr/__init__.py#L20)

```python
def flatten() -> Image.Image:
```

Flatten all of the layers.

## LSRImageData

[[find in source code]](../../pylsr/__init__.py#L56)

```python
class LSRImageData():
    def __init__(
        image: Image.Image,
        name: str,
        scale: str = '1x',
        idiom: str = 'universal',
        offsets: tuple[(int, int)] = (0, 0),
    ):
```

LSRImageData stores the PIL Image along with the name, scale of the image and the idiom.

### LSRImageData().scaledImage

[[find in source code]](../../pylsr/__init__.py#L73)

```python
def scaledImage():
```

Get the scaled image.

#### Returns

- `Image.Image` - The image to scale

## LSRLayer

[[find in source code]](../../pylsr/__init__.py#L28)

```python
class LSRLayer():
    def __init__(
        images: list[LSRImageData],
        name: str,
        size: tuple[(int, int)],
        center: tuple[(int, int)],
    ):
```

LSRLayer contains data on the layer such as the list of images, the name...

the size and the centre offset.

### LSRLayer().flatten

[[find in source code]](../../pylsr/__init__.py#L51)

```python
def flatten() -> Image.Image:
```

Faltten all of the layers.

### LSRLayer().offsets

[[find in source code]](../../pylsr/__init__.py#L42)

```python
def offsets() -> tuple[(int, int)]:
```

Calculate the x, y offset for the top left corner.

#### Returns

- `tuple[int,` *int]* - tuple for x, y offset

## flattenAll

[[find in source code]](../../pylsr/__init__.py#L216)

```python
def flattenAll(
    layers: list[LSRImageData],
    imageDimensions: tuple[(int, int)],
) -> Image.Image:
```

Flatten a list of layers and groups.

#### Arguments

- `layers` *list[LSRImageData]* - A list of layers and groups
imageDimensions (tuple[int, int]): size of the image
been flattened. Defaults to None.

#### Returns

- `Image.Image` - Flattened image

## flattenTwoLayers

[[find in source code]](../../pylsr/__init__.py#L194)

```python
def flattenTwoLayers(
    layer: LSRImageData,
    imageDimensions: tuple[(int, int)],
    flattenedSoFar: Image.Image | None = None,
) -> Image.Image:
```

Flatten two layers of an image.

#### Arguments

- `layer` *LSRImageData* - lsrimagedata
imageDimensions (tuple[int, int]): a tuple of the image dimensions
- `flattenedSoFar` *Image.Image, optional* - Raster of what has already been
flattened. Defaults to None.

#### Returns

- `Image.Image` - Flattened image

#### See also

- [LSRImageData](#lsrimagedata)

## rasterImageOffset

[[find in source code]](../../pylsr/__init__.py#L235)

```python
def rasterImageOffset(
    image: Image.Image,
    size: tuple[(int, int)],
    offsets: tuple[(int, int)] = (0, 0),
) -> Image.Image:
```

Rasterise an image with offset to a given size.

## read

[[find in source code]](../../pylsr/__init__.py#L83)

```python
def read(filename: str) -> LSRImage:
```

Read an lsr file.

#### Arguments

- `filename` *str* - the path to the file

#### Returns

- `LSRImage` - An lsr image representation

#### See also

- [LSRImage](#lsrimage)

## write

[[find in source code]](../../pylsr/__init__.py#L136)

```python
def write(filename: str, lsrImage: LSRImage):
```

Write an lsr image to disk.

#### Arguments

- `filename` *str* - filename and extension
- `lsrImage` *LSRImage* - the lsr image representation to save

#### See also

- [LSRImage](#lsrimage)
