#include "Stack.h"
#include <iostream>

Stack::Stack(int size)
{
	m_size = size;
	m_stack = new int[size];
	m_top = -1;
}

Stack::~Stack()
{
	delete[] m_stack;
}

void Stack::push(int value)
{
	m_top++;
	m_stack[m_top] = value;
}

int Stack::pop()
{
	int top_element = m_stack[m_top];
	m_stack[m_top] = 0;
	m_top--;
	return top_element;
}

void Stack::print()
{
	std::cout << "{ ";
	for (int i{ 0 }; i <= m_top; i++)
	{
		std::cout << m_stack[i] << " ";
	}
	std::cout << "}" << std::endl;
}

int Stack::size()
{
	return m_size;
}

int Stack::top()
{
	return m_stack[m_top];
}