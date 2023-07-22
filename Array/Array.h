#pragma once
#include <iostream>

template <typename T>
class Array
{
private:
	int m_size{ 0 };
	T* m_values{ 0 };
	int m_sum{ 0 };
	const char* m_type;
public:
	// Default constructor
	Array()
	{
		this->m_values = nullptr;
		this->m_type = typeid(*this).name();
	}

	// Runtime compatible
	Array(int size)
	{
		this->m_size = size;
		this->m_values = new T[m_size]{};
		this->m_type = typeid(*this).name();
		//std::cout << m_type;
	}

	// Only used when the size is known at compile time and the values are passed in through an array
	template <typename... Args>
	Array(Args... args)
	{
		this->m_size = sizeof...(args);
		if (m_size > 0)
			this->m_values = new T[m_size]{ args... };
		else
			this->m_values = new T[0]{};
		this->m_type = typeid(*this).name();
		//std::cout << m_type;
	}

	~Array()
	{
		delete[] m_values;
	}

	void resize(int new_size)
	{
		if (m_values != nullptr)
		{
			delete[] m_values;
		}
		this->m_size = new_size;
		this->m_values = new T[m_size]{};
	}

	T& operator[](unsigned const int index)
	{
		return m_values[index];
	}

	void represent()
	{
		std::cout << m_size << std::endl;
		std::cout << m_type << std::endl;
	}

	int length()
	{
		return m_size;
	}

	const char* type()
	{
		return m_type;
	}

	template<typename O>
	void populate(O obj)
	{
		for (int i{ 0 }; i < m_size; i++)
		{
			this->m_values[i] = obj;
		}
	}

	// Numerical only
	int sum()
	{
		int current_sum{ 0 };
		for (int i{ 0 }; i < m_size; i++)
		{
			current_sum += m_values[i];
		}
		this->m_sum = current_sum;
		return m_sum;
	}

	int sum_all()
	{
		int current_sum{ 0 };
		for (int i{ 0 }; i < m_size; i++)
		{
			current_sum += m_values[i].sum();
		}
		this->m_sum = current_sum;
		return m_sum;
	}
};