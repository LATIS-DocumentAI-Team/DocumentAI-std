# Documentation for `datasets`

## Package Overview

## File: `wildreceipt.py`

### Method `X1X2X3X4_to_xywh`

Converts bounding box coordinates from the format `(x1, y1, x2, y2, x3, y3, x4, y4)` to `(x, y, w, h)`.

### Method `X1X2_to_xywh`

Converts bounding box coordinates from the format `(x1, y1, x2, y2)` to `(x, y, w, h)`.

### Class `Wildreceipt`

Represents the WildReceipt dataset, used in the paper ["Spatial Dual-Modality Graph Reasoning for Key Information Extraction"](https://arxiv.org/abs/2103.14470v1). The dataset can be downloaded from [this repository](https://download.openmmlab.com/mmocr/data/wildreceipt.tar).

**Args:**
- `img_folder (str)`: Directory containing all the dataset images.
- `label_path (str)`: Path to the dataset annotations file.
- `train (bool, optional)`: Indicates whether the subset is for training. Defaults to `True`.

**Attributes:**
- `data (List[DocumentEntityClassification])`: List of document entities in the dataset.
- `root (str)`: Root directory of the document image files.
- `train (bool)`: Indicates if the dataset is for training.

**Example:**
```python
>>> dataset = Wildreceipt(
...     img_folder="/path/to/images",
...     label_path="/path/to/annotations.json",
...     train=True
... )
```

### Method `__init__`

Initializes the `Wildreceipt` instance. Refer to `help(type(self))` for the precise signature.

## File: `xfund.py`

### Class `XFUND`

Represents the XFUND dataset, detailed in the paper ["XFUND"](https://openreview.net/pdf?id=SJl3z659UH).

**Args:**
- `img_folder (str)`: Directory containing all the dataset images.
- `label_path (str)`: Path to the dataset annotations file.
- `train (bool, optional)`: Indicates whether the subset is for training. Defaults to `True`.

**Attributes:**
- `data (List[DocumentEntityClassification])`: List of document entities in the dataset.
- `root (str)`: Root directory of the document image files.
- `train (bool)`: Indicates if the dataset is for training.

**Example:**
```python
>>> dataset = XFUND(
...     data_folder="/path/to/xfund/",
...     train=True
... )
```

### Method `__init__`

Initializes the `XFUND` instance. Refer to `help(type(self))` for the precise signature.

## File: `funsd.py`

### Class `FUNSD`

Represents the FUNSD dataset, used in the paper ["CORD: A Consolidated Receipt Dataset for Post-OCR Parsing"](https://openreview.net/pdf?id=SJl3z659UH).

**Args:**
- `img_folder (str)`: Directory containing all the dataset images.
- `label_path (str)`: Path to the dataset annotations file.
- `train (bool, optional)`: Indicates whether the subset is for training. Defaults to `True`.

**Attributes:**
- `data (List[DocumentEntityClassification])`: List of document entities in the dataset.
- `root (str)`: Root directory of the document image files.
- `train (bool)`: Indicates if the dataset is for training.

**Example:**
```python
>>> dataset = FUNSD(
...     data_folder="/path/to/funsd/",
...     train=True
... )
```

## File: `cord.py`

### Class `CORD`

Represents the CORD dataset, described in the paper ["CORD: A Consolidated Receipt Dataset for Post-OCR Parsing"](https://openreview.net/pdf?id=SJl3z659UH).

**Args:**
- `img_folder (str)`: Directory containing all the dataset images.
- `label_path (str)`: Path to the dataset annotations file.
- `train (bool, optional)`: Indicates whether the subset is for training. Defaults to `True`.

**Attributes:**
- `data (List[DocumentEntityClassification])`: List of document entities in the dataset.
- `root (str)`: Root directory of the document image files.
- `train (bool)`: Indicates if the dataset is for training.

**Example:**
```python
>>> dataset = CORD(
...     img_folder="/path/to/cord_train/image",
...     label_path="/path/to/cord_train/json",
...     train=True
... )
>>> dataset = CORD(
...     img_folder="/path/to/cord_test/image",
...     label_path="/path/to/cord_test/json",
...     train=False
... )
```

### Method `__init__`

Initializes the `CORD` instance. Refer to `help(type(self))` for the precise signature.

