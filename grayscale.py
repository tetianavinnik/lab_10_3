"""Grayscale ADT"""
import ctypes
import numpy as np
from PIL import Image, ImageOps
import os


class Array:
    """Creates an array with size elements."""
    def __init__(self, size):
        assert size > 0, "Array size must be > 0"
        self._size = size
        # Create the array structure using the ctypes module.
        PyArrayType = ctypes.py_object * size
        self._elements = PyArrayType()
        # Initialize each element.
        self.clear(None)

    def __len__(self):
        """
        Returns the size of the array.
        """
        return self._size


    def __getitem__(self, index):
        """
        Gets the contents of the index element.
        """
        assert 0 <= index < len(self), "Array subscript out of range"
        return self._elements[index]


    def __setitem__(self, index, value):
        """
        Puts the value in the array element at index position.
        """
        assert 0 <= index < len(self), "Array subscript out of range"
        self._elements[index] = value


    def clear(self, value):
        """
        Clears the array by setting each element to the given value.
        """
        for i in range(len(self)):
            self._elements[i] = value


    def __iter__(self):
        """
        Returns the array's iterator for traversing the elements.
        """
        return _ArrayIterator(self._elements)


class _ArrayIterator:
    """
    An iterator for the Array ADT.
    """
    def __init__(self, the_array):
        self._array_ref = the_array
        self._cur_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._cur_index < len(self._array_ref):
            entry = self._array_ref[self._cur_index]
            self._cur_index += 1
            return entry
        else:
            raise StopIteration


class Array2D:
    """Creates a 2 -D array of size numRows x numCols."""
    def __init__(self, num_rows, num_cols):
        # Create a 1 -D array to store an array reference for each row.
        self.rows = Array(num_rows)

        # Create the 1 -D arrays for each row of the 2 -D array.
        for i in range(num_rows):
            self.rows[i] = Array(num_cols)


    def num_rows(self):
        """
        Returns the number of rows in the 2 -D array.
        """
        return len(self.rows)


    def num_cols(self):
        """
        Returns the number of columns in the 2 -D array.
        """
        return len(self.rows[0])


    def clear(self, value):
        """
        Clears the array by setting every element to the given value.
        """
        for row in range(self.num_rows()):
            row.clear(value)


    def __getitem__(self, index_tuple):
        """
        Gets the contents of the element at position [i, j]
        """
        assert len(index_tuple) == 2, "Invalid number of array subscripts."
        row = index_tuple[0]
        col = index_tuple[1]
        assert 0 <= row < self.num_rows() and 0 <= col < self.num_cols(), \
            "Array subscript out of range."
        array_1d = self.rows[row]
        return array_1d[col]


    def __setitem__(self, index_tuple, value):
        """
        Sets the contents of the element at position [i,j] to value.
        """
        assert len(index_tuple) == 2, "Invalid number of array subscripts."
        row = index_tuple[0]
        col = index_tuple[1]
        assert 0 <= row < self.num_rows() and 0 <= col < self.num_cols(), \
            "Array subscript out of range."
        array_1d = self.rows[row]
        array_1d[col] = value


class GrayscaleImage:
    """Class for image representation"""
    def __init__(self, nrows, ncols):
        self._image = Array2D(nrows, ncols)
        for i in range(nrows):
            for j in range(ncols):
                self.setitem(i, j, 0)

    
    def width(self):
        """
        Return width of the image.
        """
        return self._image.num_cols()


    def height(self):
        """
        Return height of the image.
        """
        return self._image.num_rows()


    def clear(self, value):
        """
        Clears the array by setting every element to the given value.
        """
        self._image.clear(value)


    def getitem(self, row, col):
        """
        Gets the contents of the element at position [row, col]
        """
        return self._image.__getitem__((row, col))


    def setitem(self, row, col, value):
        """
        Sets the contents of the element at position [i,j] to value.
        """
        assert 0 <= value <= 255, 'Invalid value'
        self._image.__setitem__((row, col), value)


    def lzw_compression(self):
        """
        Compress object.
        """
        lst = self.from_object_to_list()
        self.compression_dict, self.compr_index = self.create_compession_dict()
        compressed = []
        i = 0
        for current_row in lst:
            current_string = current_row[0]
            compressed_row = ""
            i+=1
            for char_index in range(1, len(current_row)):
                current_char = current_row[char_index]
                if current_string+current_char in self.compression_dict:
                    current_string = current_string+current_char
                else:
                    compressed_row = compressed_row + str(self.compression_dict[current_string]) + ","
                    self.compression_dict[current_string+current_char] = self.compr_index
                    self.compr_index += 1
                    current_string = current_char
                current_char = ""
            compressed_row = compressed_row + str(self.compression_dict[current_string])
            compressed.append(compressed_row)
        return compressed


    def lzw_decompression(self, lst):
        """
        Show the result of decompression.
        """
        assert isinstance(lst, list), 'The argument should be list type'
        self.decompression_dictionary, self.decompr_dict = self.create_decompession_dict()
        image = []
        for line in lst:
            decoded_row = self.decompress_row(line)
            image.append(np.array(decoded_row))
        image = np.array(image)
        image = Image.fromarray(image)
        image.show()


    def decompress_row(self, line):
        """
        Return decompressed row.
        """
        current_row = line.split(",")
        decoded_row = ""
        word,entry = "",""
        decoded_row = decoded_row + self.decompression_dictionary[int(current_row[0])]
        word = self.decompression_dictionary[int(current_row[0])]
        for i in range(1,len(current_row)):
            new = int(current_row[i])
            if new in self.decompression_dictionary:
                entry = self.decompression_dictionary[new]
                decoded_row += entry
                add = word + entry[0]
                word = entry
            else:
                entry = word + word[0]
                decoded_row += entry
                add = entry
                word = entry
            self.decompression_dictionary[self.decompr_dict] = add
            self.decompr_dict+=1
        newRow = decoded_row.split(',')
        decoded_row = [int(x) for x in newRow if x!='']
        return decoded_row


    def from_object_to_list(self):
        """
        Return list made of object.
        """
        lst = []
        for i in self._image.rows:
            string = ''
            for j in range(len(i)):
                string += str(i.__getitem__(j))+','
            lst.append(string[:-1])
        return lst


    def create_compession_dict(self):
        """
        Return dictionary for compression.
        """
        dictionary = {}
        for i in range(10):
            dictionary[str(i)] = i
        dictionary[','] = 10
        return dictionary, 11


    def create_decompession_dict(self):
        """
        Return dictionary for decompression.
        """
        dictionary = {}
        for i in range(10):
            dictionary[i] = str(i)
        dictionary[10] = ','
        return dictionary, 11


def from_file(path):
    """
    Create an instance of the class based on an image saved in png or jpg.
    """
    assert os.path.exists(path), 'The path is not exist'
    image = Image.open(path)
    image_grayscale = ImageOps.grayscale(image)
    img = GrayscaleImage(image_grayscale.size[1], image_grayscale.size[0])
    pixels = image_grayscale.load()
    for j in range(img.width()):
        for i in range(img.height()):
            img.setitem(i, j, pixels[j, i])
    return img
