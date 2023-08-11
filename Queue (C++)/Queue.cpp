#include "Queue.h"
#include <iostream>

Queue::Queue(int length)
{
    m_length = length;
    m_queue = new int[length]{};
}

Queue::~Queue()
{
    delete[] m_queue;
}

void Queue::enqueue(int value)
{
    m_last++;
    if (m_last >= m_length)
    {
        throw "The queue is full.";
        m_last--;
    }
    else
    {
        m_queue[m_last] = value;
    }
}

int Queue::dequeue()
{
    if (m_last < m_first)
    {
        throw "The queue is empty.";
    }
    else
    {
        int element = m_queue[0];
        for (int i{0}; i < m_last; i++)
        {
            m_queue[i] = m_queue[i + 1];
        }
        m_last--;
        return element;
    }
}

int Queue::last()
{
    if (m_last < m_first)
    {
        throw "The queue is empty.";
    }
    else
    {
        return m_queue[m_last];
    }
}

int Queue::first()
{
    if (m_last < m_first)
    {
        throw "The queue is empty.";
    }
    else
    {
        return m_queue[m_first];
    }
}

void Queue::print()
{
    std::cout << "{ ";
    for (int i{0}; i <= m_last; i++)
    {
        std::cout << m_queue[i] << " ";
    }
    std::cout << "}" << std::endl;
}