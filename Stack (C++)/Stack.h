#pragma once

class Stack
{
private:
	int m_size;
	int m_top{ -1 };
	int* m_stack;
public:
	Stack(int size);
	~Stack();
	void push(int value);
	int pop();
	void print();
	int size();
	int top();
};