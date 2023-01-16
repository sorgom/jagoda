## installation
```bash
pip install "fastapi[all]"
```
You can also install it part by part.
```bash

pip install fastapi
pip install "uvicorn[standard]"
```

installation bug
```python
AttributeError: module 'h11' has no attribute 'Event'
```

```bash
pip install --force-reinstall httpcore==0.15
```

