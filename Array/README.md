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
	Array<int> compileTimeArray{ 7, 6 };
	for (int i{ 0 }; i < compileTimeArray.length(); i++)
	std::cout << compileTimeArray[i] << std::endl;

	// ND arrays
	Array<Array<int> > arr(6);

	for (int i{ 0 }; i < arr.length(); i++)
	{
		arr[i].resize(6);
		arr[i].populate(0);
	}

	for (int i{ 0 }; i < arr.length(); i++)
	{
		for (int j{ 0 }; j < arr[i].length(); j++)
		{
			std::cout << arr[i][j] << " ";
		}
		std::cout << std::endl;
	}
	// Works with 2D arrays only for now
	std::cout << arr.sum_all() << " ";
```