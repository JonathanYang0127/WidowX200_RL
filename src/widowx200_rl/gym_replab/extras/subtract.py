import numpy as np

X = np.random.uniform(size=(5, 3))
Y = np.random.uniform(size=(5, 3))

(N, D) = X.shape
(M, _) = Y.shape

s = 0

for i in range(3):
     for k in range(M):
         a = X[:, i]
         b = Y[k, i]
         s += np.sum((a-b)**2)

print(s)
err = X[None, :, :] - Y[:, None, :]
err = err ** 2
print(np.sum(err))

