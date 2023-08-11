class Queue
{
private:
    int* m_queue;
    int m_length;
    int m_last{-1};
    const int m_first{0};

public:
    Queue(int length);
    ~Queue();
    void enqueue(int value);
    int dequeue();
    int last();
    int first();
    void print();
};