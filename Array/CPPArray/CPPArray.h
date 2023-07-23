#pragma once

template <typename T>
class Array
{
private:
	int m_size{ 0 };
	T* m_values{ nullptr };
	int m_sum{ 0 };
	const char* m_type;

public:
	// Default constructor
	Array()
	{
		this->m_values = nullptr;
		this->m_type = typeid(*this).name();
	}

	Array(int size)
	{
		this->m_size = size;
		this->m_values = new T[m_size]{};
		this->m_type = typeid(*this).name();
	}

	Array(const Array& array)
	{
		this->m_size = array.m_size;
		this->m_values = new T[m_size]; // allocate new array
		for (int i = 0; i < m_size; i++)
		{
			this->m_values[i] = array.m_values[i]; // copy elements from source array
		}
		this->m_type = typeid(*this).name();
	}

	void resize(int new_size)
	{
		if (m_values != nullptr)
		{
			this->m_size = new_size;
			this->m_values = new T[m_size]{};
			delete[] m_values;
		}
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
	void populate(const O obj)
	{
		for (int i{ 0 }; i < m_size; i++)
		{
			this->m_values[i] = O(obj);
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

	T& operator[](unsigned const int index)
	{
		return m_values[index];
	}
};