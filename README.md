# geocraft

## Requirements

```plain
python >= 3.9
```

## Installation

```bash
pip install geocraft
```

## Usage

```python
from geocraft.coord_converter import CoordConverter

converter = CoordConverter(src=CoordConverter.BD09, target=CoordConverter.GCJ02)
print(converter.convert(116.404, 39.915))  # (116.39762729119315, 39.90865673957631)
```

Supported conversions:

- Conversions between different coordinate systems (Non-Mercator):

  - `WGS84` <-> `GCJ02`
  - `GCJ02` <-> `BD09`
  - `BD09` <-> `WGS84`

- Conversions between same coordinate systems (Non-Mercator <-> Mercator):
  - `WGS84` <-> `WGS84MC`
  - `GCJ02` <-> `GCJ02MC`
  - `BD09` <-> `BD09MC`
