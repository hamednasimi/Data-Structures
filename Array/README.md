Usage:

```c++
	// Runtime usage
	int size;
	std::cin >> size;
	Array<int> runtimeArray(size);

	for (int i = 0; i < size; i++)
		std::cin >> runtimeArray[i];

	for (int i{ 0 }; i < size; i++)
		std::cout << runtimeArray[i] << std::endl;

	// Compile time usage
	const int size_{ 5 };
	Array<int, size_> compileTimeArray {1, 2, 3, 4, 5};
	for (int i{ 0 }; i < size_; i++)
		std::cout << compileTimeArray[i] << std::endl;
```