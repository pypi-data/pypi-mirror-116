# proto-formatter
Protocol Buffers file formatter.

## Install
```shell
pip install proto-formatter
```
## Usage
- Using default config: indents=2, equal_sign=False, all_top_comments=False
```python
from proto_formatter.parser import PackageParser
from proto_formatter.formatter import Formatter

protobuf_obj = parser.load(proto_file_path)
formatted_proto = Formatter().to_string(protobuf_obj)
```
- Specified value for all configs: indents=2, equal_sign=Ture, all_top_comments=False
```python
from proto_formatter.parser import PackageParser
from proto_formatter.formatter import Formatter

protobuf_obj = parser.load(proto_file_path)
formatted_proto = Formatter(equal_sign=True, indents=4, all_top_comments=True).to_string(protobuf_obj)
```