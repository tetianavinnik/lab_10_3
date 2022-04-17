# grayscale

grayscale.py is a module for work with image as an array. LZW compression and decompression of black&white image included.

## Usage

```
from grayscale import *
picture = from_file(path_to_file)
compressed_list = picture.lzw_compression() # for compression
picture.lzw_decompression(compressed_list) # for decompression
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
