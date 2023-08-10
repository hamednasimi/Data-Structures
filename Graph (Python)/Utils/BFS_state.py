from enum import Enum


class BFSState(Enum):
    
    UNSEEN = 0
    SEEN = 1
    VISITED = 2
