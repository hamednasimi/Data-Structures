A basic linked list template class.
Provides appendage, insertion and removal of values to the list.
Each entry is managed by a Node class which contains the value and a pointer member which is used to store the address of the next node in the list.
The collection of nodes is managed by the LinkedList class.

**Usage:**

```C++

#include <iostream>
#include "Linked_list.h"

int main() {
    
    // Instantiation
    LinkedList<double> linkedList_;

    // Appending elements
    linkedList_.append(6.5);
    linkedList_.append(7.5);
    linkedList_.append(8.5);
    linkedList_.append(9.5);
    linkedList_.append(10);

    for (int i{ 0 }; i < linkedList_.length(); i++)
    {
        std::cout << "ELEMENT: " << linkedList_[i] << std::endl;
    }

    // Insertion of elements anywhere in the list as long as the index in not out of range (-1 is allowed to index the last element)
    linkedList_.insert(1.111, 5);
    linkedList_.insert(22.22, 6);
    linkedList_.insert(333.3, 2);
    
    for (int i{ 0 }; i < linkedList_.length(); i++)
    {
        std::cout << "ELEMENT_: " << linkedList_[i] << std::endl;
    }

    // Removal of elements given the index (-1 is allowed to index the last element)
    linkedList_.remove(2);
    linkedList_.remove(2);

    for (int i{ 0 }; i < linkedList_.length(); i++)
    {
        std::cout << "ELEMENT__: " << linkedList_[i] << std::endl;
    }

    return 0;
}
```