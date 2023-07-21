#pragma once

template <typename T, int S>
class Array
{
private:
	T* m_values = new T[S]{};
public:
	template <typename... Args>
	Array(Args... args) : m_values{ args... } {};
	~Array()
	{ 
		delete[] m_values;
	}

	T& operator[](unsigned const int index)
	{
		return m_values[index];
	}
};