import numpy as np 

def get_closest(lst, K):
     lst = np.asarray(lst)
     idx = (np.abs(lst - K)).argmin()
     return idx

def prime(x, y):
	prime_list = []
	for i in range(x, y):
		if i == 0 or i == 1:
			continue
		else:
			for j in range(2, int(i/2)+1):
				if i % j == 0:
					break
			else:
				prime_list.append(i)
	return prime_list

def get_partition_size(m_p,k):
    p_table = prime(2,15000000)
    p_idx = get_closest(p_table, m_p/k)
    sum = 0
    m_f = 0
    for i in range(p_idx-k+1, p_idx+1):
        sum = sum+p_table[i]
    f1 = m_p - sum 
    j = p_idx +1
    sum = sum +p_table[j] - p_table[j-k]
    f2 = m_p - sum
    while f2<f1:
        f1 = f2
        j = j+1
        sum = sum + p_table[j] - p_table[j-k]
        f2 = abs(sum - m_p) 
    
    partition_lengths =[]
    for i in range(0,k):
        partition_len = p_table[j-k+i]
        partition_lengths.append(partition_len)
        m_f = m_f + partition_len
    return partition_lengths

def prime(x, y):
	prime_list = []
	for i in range(x, y):
		if i == 0 or i == 1:
			continue
		else:
			for j in range(2, int(i/2)+1):
				if i % j == 0:
					break
			else:
				prime_list.append(i)
	return prime_list
# starting_range = 2
# ending_range = 15000
# p_table = prime(starting_range, ending_range)

# #m_p = size of bloom filter, k = no. of paritions
# paritions_sizes =get_partition_size(m_p=10000, k=10, p_table = p_table)


# print(paritions_sizes)
