This class is built on top of C++ arrays.

**Usage:**

```c++
	// ND Arrays
	Array<Array<long double>> a(10);
	a.populate(Array<long double>(5));

	for (int i{ 0 }; i < a.length(); i++)
	{
		for (int j{ 0 }; j < a[0].length(); j++)
		{
			a[i][j] = (i + 1) * (j + 1);
		}
	}

	for (int i{ 0 }; i < a.length(); i++)
	{
		for (int j{ 0 }; j < a[0].length(); j++)
		{
			std::cout << a[i][j] << " " << std::flush;
		}
		std::cout << std::endl;
	}

	// Runtime usage
	int size;
	std::cin >> size;
	Array<int> runtimeArray(size);

	for (int i = 0; i < size; i++)
		std::cin >> runtimeArray[i];

	for (int i{ 0 }; i < size; i++)
		std::cout << runtimeArray[i] << std::endl;
```