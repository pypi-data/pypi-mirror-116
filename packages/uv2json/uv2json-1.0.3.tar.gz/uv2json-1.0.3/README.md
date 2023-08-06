[![Build & Publish](https://github.com/chanana/uv2json/actions/workflows/build.yml/badge.svg)](https://github.com/chanana/uv2json/actions/workflows/build.yml)

# uv2json

`uv2json` is a python script that converts Gilson GX-270 exported CSVs to JSON format

## Installation

```bash
pip install uv2json
```

## Usage

#### As a console script
```bash
uv2json <path/to/csv/files>
```

#### As a module
```python
from uv2json import uv2json as uv
uv.convert('path/to/filename') # Accepts single file or list of files.
```

The script will make a JSON file in the same location with the same name.
