import numpy as np
A = np.array([[1,2],[3,4]])
print(type(A))
print(A.ndim) # A의 차원
print(A.shape) # 배열의 크기
print(A.dtype) # 원소 자료형

print(A.max(),A.mean(),A.min(),A.sum())
print(A.flatten()) #평탄화

B = np.array([10,100])
print(np.dot(B,B))
