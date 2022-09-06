import numpy as np

test_array = np.linspace(0, 9, 10, endpoint=True)

c1 = 0
c2 = 1
c3 = 2
Fs = [c1, c2, c3]

for i in test_array:
    print(Fs)
    c1 = c1 + 3
    c2 = c2 + 3
    c3 = c3 + 3
    Fs = [c1, c2, c3]