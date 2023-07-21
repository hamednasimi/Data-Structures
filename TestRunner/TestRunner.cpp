#include "D:\Documents\Code\C++\Learning\Practice\Array\Array.h"
#include <iostream>

int main()
{
	Array<double, 60> arr {0.45, 1.012, 2.986, 4.2, 6.0004};
	double a = arr[2] + arr[3];
	std::cout << a << std::endl;
	for (int i{ 0 }; i < 60; i++)
		std::cout << arr[i] << std::endl;
}