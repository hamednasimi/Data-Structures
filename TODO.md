---
Add these functions to Matrix.h
```

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
```
