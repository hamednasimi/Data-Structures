#pragma once

template <typename T>
class Array
{
private:
	T* m_values;
public:
	template <typename... Args>
	Array(int size, Args... args)
	{
		this->m_values = new T[size]{args...};
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