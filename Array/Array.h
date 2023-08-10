#pragma once

template <typename T>
class Array
{
private: // Member variables
	int m_size{ 0 };
	T* m_values{ nullptr };
	int m_sum{ 0 };
	const char* m_type;

public: // Methods
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

	//~Array()
	//{
	//	if (m_values != nullptr)
	//	{
	//		for (int i{ 0 }; i < m_size; i++)
	//		{
	//			m_values[i].~T();
	//		}
	//		delete[] m_values;
	//		m_values = nullptr;
	//	}
	//}

	void resize(int new_size)
	{
		if (new_size == m_size)
		{
			return;
		}
		T* new_values = new T[new_size]{};
		int copy_size = (m_size < new_size) ? m_size : new_size;
		for (int i = 0; i < copy_size; ++i)
		{
			new_values[i] = m_values[i];
		}
		delete[] m_values;
		m_values = new_values;
		m_size = new_size;
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

	T& operator[](unsigned const int index)
	{
		return m_values[index];
	}
};