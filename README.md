# geocraft

## Requirements

```plain
python >= 3.10
```

## Installation

```bash
pip install geocraft
```

## Usage

```python
from geocraft.cn.coordinate_converter import (
    bd09_to_gcj02,
    gcj02_to_bd09,
    gcj02_to_wgs84,
    wgs84_to_gcj02,
)

print(bd09_to_gcj02(116.404, 39.915))  # (116.39762729119315, 39.90865673957631)
print(gcj02_to_bd09(116.404, 39.915))  # (116.41036949371029, 39.92133699351021)
print(gcj02_to_wgs84(116.404, 39.915))  # (116.39775550083061, 39.91359571849836)
print(wgs84_to_gcj02(116.404, 39.915))  # (116.41024449916938, 39.91640428150164)
```
