import base64
import sys
import abuf
import json


if len(sys.argv) < 2:
    print('no argument given, please provide a base64 encoded DNS response')
    exit(1)

buf = sys.argv[1]
raw_data = abuf.AbufParser.parse(base64.b64decode(buf))
print(json.dumps(raw_data))