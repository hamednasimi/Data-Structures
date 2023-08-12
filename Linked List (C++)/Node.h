#pragma once

template <typename T>
class Node
{
private: // Member variables
	T m_value{}; // The main value stored in the node
	Node* m_nextNode{ nullptr }; // Pointer to the next node

public: // Methods
	// Default constructor
	Node() {};

	// Constructor with known value
	Node(T value)
	{
		this->m_value = value;
	}

	// Copy constructor
	Node(const Node& other)
	{
		this->m_value = &other.m_value;
		this->m_nextNode = &other.m_nextNode;
	}

	// Destructor
	~Node() {};

	// Set the pointer to the next node
	void setNext(Node* node)
	{
		this->m_nextNode = node;
	}

	// Returns the value of the node
	T& value()
	{
		return m_value;
	}

	// Returns a pointer to the next node
	Node* getNext()
	{
		if (m_nextNode == nullptr)
		{
			throw std::out_of_range("Index out of range.");
		}
		else
		{
			return m_nextNode;
		}
	}
};