import math


def solve_affine_equations(equation1, equation2, m):
    """
    Resuelve:
        y1 ≡ a*x1 + b (mod m)
        y2 ≡ a*x2 + b (mod m)
    Retorna una lista con todas las soluciones (a, b) (posibles múltiples).
    """
    x1, y1 = equation1
    x2, y2 = equation2

    dx = (x2 - x1) % m
    dy = (y2 - y1) % m

    g = math.gcd(dx, m)
    if dy % g != 0:
        # No hay ninguna solución
        return []

    # Reducimos la ecuación dividiendo por gcd
    dx_ = dx // g
    dy_ = dy // g
    m_ = m // g

    # Inverso de dx_ mod m_
    inv_dx_ = pow(dx_, -1, m_)

    # Una solución base para 'a'
    a0 = (dy_ * inv_dx_) % m_

    solutions = []
    # Se generan las g posibles soluciones:
    for k in range(g):
        a = (a0 + k * m_) % m
        b = (y1 - a * x1) % m
        solutions.append((a, b))

    return solutions


modulus = 26
eq1 = (4, 4)
eq2 = (18, 24)

a, b = solve_affine_equations(eq1, eq2, modulus)
print(f"a = {a}, b = {b}")
