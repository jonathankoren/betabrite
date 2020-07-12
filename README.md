# About

Python library for communicating with Adaptive Display LED signs such as the
Betabrite via the Alpha sign serial protocol.
https://www.adaptivedisplays.com/resources/documentation-and-manuals/support-documents/bid/264113/Alpha-Sign-Communications-Protocol-pn-97088061

# Usage
## Programmatically
```from betabrite import *

transmit("/dev/serial", write_file([animation("example text")]))
```

## Command Line
``./betabrite +automode +autocolor example text`
