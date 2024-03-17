# Pylsr

[Pylsr Index](../README.md#pylsr-index) / Pylsr

> Auto-generated documentation for [pylsr](../../../pylsr/__init__.py) module.

- [Pylsr](#pylsr)
  - [LSRImage](#lsrimage)
    - [LSRImage().flatten](#lsrimage()flatten)
  - [LSRImageData](#lsrimagedata)
    - [LSRImageData().scaledImage](#lsrimagedata()scaledimage)
  - [LSRLayer](#lsrlayer)
    - [LSRLayer().flatten](#lsrlayer()flatten)
    - [LSRLayer().offsets](#lsrlayer()offsets)
  - [flattenAll](#flattenall)
  - [flattenTwoLayers](#flattentwolayers)
  - [jsonLoadsFromArchive](#jsonloadsfromarchive)
  - [rasterImageOffset](#rasterimageoffset)
  - [read](#read)
  - [renderImageOffset](#renderimageoffset)
  - [write](#write)

## LSRImage

[Show source in __init__.py:17](../../../pylsr/__init__.py#L17)

LSRImage contains data on the overall size, the layers and the name of the lsr image.

#### Signature

```python
class LSRImage:
    def __init__(
        self, size: tuple[int, int], name: str, layers: list[LSRLayer] | None = None
    ) -> None: ...
```

### LSRImage().flatten

[Show source in __init__.py:25](../../../pylsr/__init__.py#L25)

Flatten all of the layers.

#### Signature

```python
def flatten(self) -> Image.Image: ...
```



## LSRImageData

[Show source in __init__.py:69](../../../pylsr/__init__.py#L69)

LSRImageData stores the PIL Image along with the name, scale of the image and the idiom.

#### Signature

```python
class LSRImageData:
    def __init__(
        self,
        image: Image.Image,
        name: str,
        scale: str = "1x",
        idiom: str = "universal",
        offsets: tuple[int, int] = (0, 0),
    ) -> None: ...
```

### LSRImageData().scaledImage

[Show source in __init__.py:86](../../../pylsr/__init__.py#L86)

Get the scaled image.

Returns
-------
 Image.Image: The image to scale

#### Signature

```python
def scaledImage(self): ...
```



## LSRLayer

[Show source in __init__.py:33](../../../pylsr/__init__.py#L33)

LSRLayer contains data on the layer such as the list of images, the name,
the size and the centre offset.

#### Signature

```python
class LSRLayer:
    def __init__(
        self,
        images: list[LSRImageData],
        name: str,
        size: tuple[int, int],
        center: tuple[int, int],
    ) -> None: ...
```

#### See also

- [LSRImageData](#lsrimagedata)

### LSRLayer().flatten

[Show source in __init__.py:64](../../../pylsr/__init__.py#L64)

Flatten all of the layers.

#### Signature

```python
def flatten(self) -> Image.Image: ...
```

### LSRLayer().offsets

[Show source in __init__.py:50](../../../pylsr/__init__.py#L50)

Calculate the x, y offset for the top left corner.

Returns
-------
 tuple[int, int]: tuple for x, y offset

#### Signature

```python
def offsets(self) -> tuple[int, int]: ...
```



## flattenAll

[Show source in __init__.py:253](../../../pylsr/__init__.py#L253)

Flatten a list of layers and groups.

#### Arguments

----
 - `layers` *list[LSRImageData]* - A list of layers and groups
 imageDimensions (tuple[int, int]): size of the image
 been flattened. Defaults to None.

#### Returns

-------
 - `Image.Image` - Flattened image

#### Signature

```python
def flattenAll(
    layers: list[LSRImageData], imageDimensions: tuple[int, int]
) -> Image.Image: ...
```

#### See also

- [LSRImageData](#lsrimagedata)



## flattenTwoLayers

[Show source in __init__.py:228](../../../pylsr/__init__.py#L228)

Flatten two layers of an image.

#### Arguments

----
 - `layer` *LSRImageData* - lsrimagedata
 imageDimensions (tuple[int, int]): a tuple of the image dimensions
 - `flattenedSoFar` *Image.Image, optional* - Render of what has already been
 flattened. Defaults to None.

#### Returns

-------
 - `Image.Image` - Flattened image

#### Signature

```python
def flattenTwoLayers(
    layer: LSRImageData,
    imageDimensions: tuple[int, int],
    flattenedSoFar: Image.Image | None = None,
) -> Image.Image: ...
```

#### See also

- [LSRImageData](#lsrimagedata)



## jsonLoadsFromArchive

[Show source in __init__.py:13](../../../pylsr/__init__.py#L13)

#### Signature

```python
def jsonLoadsFromArchive(x): ...
```



## rasterImageOffset

[Show source in __init__.py:275](../../../pylsr/__init__.py#L275)

Render an image with offset to a given size. (deprecated, use renderImageOffset).

#### Signature

```python
@deprecated(deprecated_in="2022", removed_in="2023", details="Use renderImageOffset")
def rasterImageOffset(
    image: Image.Image, size: tuple[int, int], offsets: tuple[int, int] = (0, 0)
) -> Image.Image: ...
```



## read

[Show source in __init__.py:98](../../../pylsr/__init__.py#L98)

Read an lsr file.

#### Arguments

----
 - `filename` *str* - the path to the file

#### Returns

-------
 - [LSRImage](#lsrimage) - An lsr image representation

#### Signature

```python
def read(filename: str) -> LSRImage: ...
```

#### See also

- [LSRImage](#lsrimage)



## renderImageOffset

[Show source in __init__.py:283](../../../pylsr/__init__.py#L283)

Render an image with offset to a given size.

#### Signature

```python
def renderImageOffset(
    image: Image.Image, size: tuple[int, int], offsets: tuple[int, int] = (0, 0)
) -> Image.Image: ...
```



## write

[Show source in __init__.py:159](../../../pylsr/__init__.py#L159)

Write an lsr image to disk.

#### Arguments

----
 - `filename` *str* - filename and extension
 - `lsrImage` *LSRImage* - the lsr image representation to save

#### Signature

```python
def write(filename: str, lsrImage: LSRImage) -> None: ...
```

#### See also

- [LSRImage](#lsrimage)