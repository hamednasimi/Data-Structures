#pragma once

template <typename T, int ... S>
class Array
{
private:
	int m_size{ 0 };
	T* m_values{ 0 };
public:
	// Runtime compatible
	Array(int size)
	{
		this->m_size = size;
		this->m_values = new T[m_size];
	}

	// Only used when the size is known at compile time and the values are passed in through an array
	template <typename... Args>
	Array(Args... args)
	{
		this->m_size = { S... };
		this->m_values = new T[m_size]{ args... };
	}

	~Array()
	{
		delete[] m_values;
	}

	T& operator[](unsigned const int index)
	{
		return m_values[index];
	}
};