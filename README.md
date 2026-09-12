# CUCKOO LIBRARY
![CUCKOO LIBRARY - Header](https://github.com/user-attachments/assets/16bfa3d8-35a9-4927-a3f2-8f6d22b37ba6)

## Usage
**Requirements:** `Python` 3.10.0 or newer, `pytest`

### Installation
```bash
uv add cuckoo-library
# or
pip install cuckoo-library
```

### Example
```python
from cuckoo_library.model.communication import local_task_compute_time
from cuckoo_library.model.transmission import distance_2d

compute_time = local_task_compute_time(100, 10)
distance = distance_2d(0, 0, 3, 4)

print(compute_time)  # 10.0
print(distance)      # 5.0
```

### Build
Create a wheel package in `dist/`:
```bash
python -m pip wheel . --no-deps --wheel-dir dist #Recommendation
#or
python -m build 
```

### Testing
```bash
pytest
#or
python -m pytest tests -q
```
