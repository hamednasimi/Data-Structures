# This project primarily serves as a proof of concept and a platform for practice.
# It is a numerical-only, value-mutable but dimension-immutable array structure.
# Additionally, I’ve incorporated certain linear algebra algorithms.
# Numpy isn't used in the class itself but has been an inspiration when it comes to naming many of the methods.
# The class is meant to be used only with regular lists.
# e.g. [[1, 2], [3, 4], [5, 6]] is acceptable but [1, [2, 3], [4, [5], 6]] is not supported.
# Having a combination of lists and numericals in each dimension will probably not work.


if __debug__:
    import os; os.system("cls")
    # import sys; print("Version: ", sys.version)

# from Utils import numerical
from typing import Union


class Array:
    
    
    # Dunder methods
    
    def __init__(self, matrix: list) -> None:
        """
        The Initializer for the Array class.
        
        The "values" must be a single list.
        """
        if type(matrix) != list:
            raise "The 'values' argument must be a list."
        self.__ndim: int = Array.get_ndim(matrix)
        self.__shape: tuple = Array.get_shape(matrix)
        self.__flattened: list = Array.get_flattened(matrix)
        self.__size: int = Array.get_size(self.__flattened)
            
    def __str__(self) -> str:
        return str(self.__representation(self.__shape, self.__flattened))

    def __getitem__(self, indices: Union[int | slice]) -> int:
        if isinstance(indices, tuple):
            index = 0
            multiplier = 1
            for s, i in zip(reversed(self.shape), reversed(indices)):
                index += i * multiplier
                multiplier *= s
            return self.__flattened[index]
        else:
            return self.__flattened[indices]
        
    # Properties
    
    @property
    def ndim(self) -> int:
        return self.__ndim
    
    @property
    def shape(self) -> tuple:
        return self.__shape
    
    @property
    def flat(self):
        return self.__flattened
    
    @property
    def size(self) -> int:
        return self.__size
    
    # Instance methods
    
    def __representation(self, shape, flattened):
        if len(shape) == 1:
            return flattened[:shape[0]]
        else:
            split = len(flattened) // shape[0]
            return [self.__representation(shape[1:], flattened[i:i+split]) for i in range(0, len(flattened), split)]
    
    def flatten(self) -> "Array":
        return self.__flattened
    
    # Class methods
    
    @classmethod
    def get_ndim(cls, matrix):
        n_dim = 0
        checking_item = matrix
        while type(checking_item) == list:
            n_dim += 1
            checking_item = checking_item[0]
        return n_dim
    
    @classmethod
    def get_shape(cls, matrix):
        if not isinstance(matrix, list):
            return ()
        return (len(matrix),) + cls.get_shape(matrix[0])
    
    @classmethod
    def get_flattened(cls, matrix: Union["Array", list]) -> list:
        """
        Given an N-dimensional list, flattens it into a single dimensional list and returns it.
        """
        if isinstance(matrix, list):
            return [sub_elem for elem in matrix for sub_elem in cls.get_flattened(elem)]
        else:
            return [matrix]
    
    @classmethod
    def get_size(cls, array: Union["Array", list]) -> int:
        return len(array)
    
    # Static methods
    
    pass
