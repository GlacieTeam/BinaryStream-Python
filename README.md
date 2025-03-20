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
stream.writeByte(1)
stream.writeUnsignedChar(2)
stream.writeUnsignedShort(3)
stream.writeUnsignedInt(4)
stream.writeUnsignedInt64(5)
stream.writeBool(True)
stream.writeDouble(6)
stream.writeFloat(7)
stream.writeSignedInt(8)
stream.writeSignedInt64(9)
stream.writeSignedShort(10)
stream.writeUnsignedVarInt(11)
stream.writeUnsignedVarInt64(12)
stream.writeVarInt(13)
stream.writeVarInt64(14)
stream.writeNormalizedFloat(1.0)
stream.writeSignedBigEndianInt(16)
stream.writeString("17")
stream.writeUnsignedInt24(18)
buffer = stream.getAndReleaseData()
```

## License
- Please note that this project is licensed under the LGPLv3.
- If you modify or distribute this project, you must comply with the requirements of the LGPLv3 license, including but not limited to providing the complete source code and retaining the copyright notices. For more detailed information, please visit the GNU Official Website.

### Copyright © 2025 GlacieTeam. All rights reserved.