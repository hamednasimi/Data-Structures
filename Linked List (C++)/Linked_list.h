#pragma once
#include "Node.h"

template <typename T>
class LinkedList
{
private: // Member variables
	Node<T>* m_head{ nullptr }; // The first node in the list
	Node<T>* m_tail{ nullptr }; // The last node in the list
	int m_length{ 0 }; // The number of nodes in the list (index + 1)

public: // Instance methods
	// Default constructor
	LinkedList() {};

	// Destructor
	~LinkedList()
	{
		if (m_length == 0) // No nodes are present
		{
			return;
		}
		else if (m_length == 1) // One node is present
		{
			delete m_head;
		}
		else if (m_length > 1) // More than one node is present
		{
			Node<T>* current = m_head;
			Node<T>* next = current->getNext();
			for (int i{ 0 }; i < m_length; i++)
			{
				delete current;
				current = next;
				if (next == m_tail)
				{
					delete next;
					break;
				}
				next = next->getNext();
			}
		}
	}

	// Get the number of nodes in the linked list (index + 1)
	int length()
	{
		return m_length;
	}

	// Add a new node to the end of the linked list
	void append(T value)
	{
		if (m_length == 0) // No nodes exist yet
		{
			this->m_head = new Node<T>(value);
			this->m_tail = m_head;
		}
		else // More than one node exists
		{
			Node<T>* newObject = new Node<T>(value);
			m_tail->setNext(newObject);
			m_tail = newObject;
		}
		m_length++;
	}

	// Insert a node in the given index location
	void insert(T value, int index)
	{
		if (index > m_length || index < -1) // The given index is out of range
		{
			throw std::out_of_range("Index out of range.");
		}
		else if (index == m_length || index == -1) // The given index is at the tail end of the list (same as appending it)
		{
			append(value);
		}
		else if (index == 0) // The given index is at the head of the list
		{
			Node<T>* newObject = new Node<T>(value);
			newObject->setNext(m_head);
			m_head = newObject;
			m_length++;
		}
		else // The given index is somewhere in the middle of the list
		{
			Node<T>* newObject = new Node<T>(value);
			Node<T>* previous = m_head;
			for (int i{ 0 }; i < index; i++)
			{
				if (i == index - 1)
				{
					newObject->setNext(previous->getNext());
					previous->setNext(newObject);
					m_length++;
					break;
				}
				previous = previous->getNext();
			}
		}
	}

	// Removes the node at the given index
	void remove(int index)
	{
		if (index >= m_length || index < -1) // The given index is out of range
		{
			throw std::out_of_range("Index out of range.");
		}
		else if (index == m_length - 1 || index == -1) // The given index is at the tail end of the list
		{
			Node<T>* previous = m_head;
			for (int i{ 0 }; i < index; i++)
			{
				if (i == index - 1)
				{
					previous->setNext(nullptr);
					delete m_tail;
					m_tail = previous;
					break;
				}
				previous = previous->getNext();
			}
		}
		else if (index == 0) // The given index is at the head of the list
		{
			Node<T>* newHead = m_head->getNext();
			delete m_head;
			m_head = newHead;
		}
		else // The given index is somewhere in the middle of the list
		{
			Node<T>* previous = m_head;
			Node<T>* current;
			for (int i{ 0 }; i < index; i++)
			{
				if (i == index - 1)
				{
					current = previous->getNext();
					previous->setNext(current->getNext());
					delete current;
					break;
				}
				previous = previous->getNext();
			}
		}
		m_length--;
	}

#pragma warning(push)
#pragma warning(disable: 4715)
	// Returns the value of the node at the given index location
	T& operator[](const int index)
	{
		if (index > -1 && index < m_length) // Valid index location
		{
			Node<T>* current = m_head;
			for (int i{ 0 }; i < m_length; i++)
			{
				if (i == index)
					return current->value();
				current = current->getNext();
			}
		}
		else if (index == -1)
		{
			return m_tail->value();
		}
		else
		{
			throw std::out_of_range("Index out of range.");
		}
	}
#pragma warning(pop)
};