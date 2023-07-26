from enum import Enum

class Direction(Enum):
    
    # For self.is_directed
    FALSE = 0
    TRUE = 1
    MIXED = 2
    
    # For method arguments
    IN = 3
    OUT = 4
    BOTH = 5
