**Usage:**

```C++

# Initializing
Queue Q(8);

Q.enqueue(42);
Q.enqueue(7);

Q.print();

std::cout << Q.first() std::endl;
std::cout << Q.last() std::endl;
std::cout << Q.dequeue() std::endl;

Q.print();

```