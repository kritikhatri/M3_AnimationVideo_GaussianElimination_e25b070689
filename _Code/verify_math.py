"""
Independent check of every number shown in the video (run: python verify_math.py).
Uses exact fractions, so there is no rounding.
"""
from fractions import Fraction as F

M = [[F(1), F(1), F(1), F(6)],
     [F(2), F(1), F(-1), F(1)],
     [F(1), F(-1), F(2), F(5)]]
original = [r[:] for r in M]


def replace(i, c, j):            # R_i -> R_i + c R_j
    M[i] = [a + c * b for a, b in zip(M[i], M[j])]
    print(f"R{i+1} -> R{i+1} {'+' if c > 0 else '-'} {abs(c)}R{j+1}:  {[str(x) for x in M[i]]}")


replace(1, -2, 0)                # expect [0, -1, -3, -11]
replace(2, -1, 0)                # expect [0, -2, 1, -1]
replace(2, -2, 1)                # expect [0, 0, 7, 21]
assert M[1] == [0, -1, -3, -11] and M[2] == [0, 0, 7, 21]

# back-substitution
z = M[2][3] / M[2][2]
y = (M[1][3] - M[1][2] * z) / M[1][1]
x = (M[0][3] - M[0][1] * y - M[0][2] * z) / M[0][0]
print("solution:", x, y, z)
assert (x, y, z) == (1, 2, 3)

# substitute into the ORIGINAL equations
for r in original:
    assert r[0] * x + r[1] * y + r[2] * z == r[3]

# the plane after each step still passes through (1, 2, 3)  (Scene 3)
for r in M:
    assert r[0] * x + r[1] * y + r[2] * z == r[3]
print("all checks passed")
