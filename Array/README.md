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
	Array<int, 2> compileTimeArray{ 7, 6 };
	for (int i{ 0 }; i < compileTimeArray.length(); i++)
	std::cout << compileTimeArray[i] << std::endl;
```