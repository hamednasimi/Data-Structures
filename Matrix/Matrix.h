#pragma once
#include "..\Array\Array.h"
#include <cstdarg>

template<typename T>
class Matrix
{
private: // Member variables
	Array<Array<T>> m_matrix;
	int m_dimensionCount{ 0 };
	Array<int> m_dimensions;

private: // Methods
	template<typename AT>
	void set_dimension(AT& array, int dim_index)
	{
		if (dim_index == m_dimensionCount - 1)
		{
			for (int i{ 0 }; i < array.length(); i++)
			{
				array[i] = Array<T>(m_dimensions[dim_index]);
			}
			return;
		}
		array.resize(m_dimensions[dim_index]);
		for (int i{ 0 }; i < array.length(); i++)
		{
			array[i] = Array<AT>(0);
			set_dimension(array[i], dim_index++);
		}
	}

	//template<typename AT>
	//void print(int dim_index)
	//{
	//	for (int i{ 0 }; i < array.length(); i++)
	//	{
	//		for (int j{ 0 }; j < array.length(); j++)
	//		{
	//			std::cout << m_matrix << " ";
	//		}
	//		std::cout << std::endl;
	//	}
	//}

public: // Methods
	Matrix()
	{
		this->m_matrix = Array<T>(0);
	}

	Matrix(int D...)
	{
		// Set members
		va_list dims;
		va_start(dims, D);
		this->m_dimensionCount = D;
		this->m_dimensions = Array<int>(m_dimensionCount);
		//this->m_dimensions.resize(m_dimensionCount);
		for (int i{ 0 }; i < m_dimensionCount; i++)
		{
			this->m_dimensions[i] = va_arg(dims, int);
		}
		// Initialize m_matrix
		set_dimension(m_matrix, 0);
	}

	void represent()
	{
		for (int i{ 0 }; i < m_matrix.length(); i++)
		{
			for (int j{ 0 }; j < m_matrix[0].length(); j++)
			{
				std::cout << m_matrix[i][j] << " ";
			}
			std::cout << std::endl;
		}
	}

	Array<int> dims()
	{
		return this->m_dimensions;
	}

	T& operator[](int index)
	{
		return m_matrix[index];
	}
};