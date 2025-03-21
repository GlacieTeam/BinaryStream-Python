# BinaryStream-Python
BinaryStream Library written in Python  
**A python version of [Binarystream](https://github.com/GlacieTeam/BinaryStream)**

## Install
```bash
pip install mcbe-binarystream
```

## Usage
```Python
from binarystream import *

stream = BinaryStream()
stream.write_byte(1)
stream.write_unsigned_char(2)
stream.write_unsigned_short(3)
stream.write_unsigned_int(4)
stream.write_unsigned_int64(5)
stream.write_bool(True)
stream.write_double(6)
stream.write_float(7)
stream.write_signed_int(8)
stream.write_signed_int64(9)
stream.write_signed_short(10)
stream.write_unsigned_varint(11)
stream.write_unsigned_varint64(12)
stream.write_varint(13)
stream.write_varint64(14)
stream.write_normalized_float(1.0)
stream.write_signed_big_endian_int(16)
stream.write_string("17")
stream.write_unsigned_int24(18)
```

## License
- Please note that this project is licensed under the LGPLv3.
- If you modify or distribute this project, you must comply with the requirements of the LGPLv3 license, including but not limited to providing the complete source code and retaining the copyright notices. For more detailed information, please visit the GNU Official Website.

### Copyright © 2025 GlacieTeam. All rights reserved.