from Modulo_Polynomial import *

def Nth_Term_of_Linearly_Recurrent_Sequence(A: list[int], C: list[int], n: int, offset: int = 0) -> int:
    """ A[i] = C[0] * A[i - 1] + C[1] * A[i - 2] + ... + C[d - 1] * A[i - d] で表される数列 (A[i]) の第 n 項を求める.

    Args:
        A (list[int]): A = (A[0], ..., A[d - 1]): 最初の d 項
        C (list[int]): C = (C[0], ..., C[d - 1]): 線形漸化式の係数
        n (int): 求める項数
        offset (int, optional): ずらす項数 (初項を第 offset 項とする). Defaults to 0.

    Raises:
        ValueError: len(A) != len(C) の場合に発生

    Returns:
        int: A[n]
    """

    if not len(A) == len(C):
        raise ValueError("len(A) == len(C) でなくてはなりません")

    d = len(A)
    n -= offset

    if n < 0:
        return 0
    elif n < d:
        return A[n] % Mod

    A = Modulo_Polynomial(A, d + 1)
    Q = Modulo_Polynomial([-C[i - 1] if i else 1  for i in range(d + 1)], d + 1)

    P = A * Q
    P[d] = 0
    return Polynominal_Coefficient(P, Q, n)

def Find_Linear_Recurrence(A: list[int]) -> list[int]:
    """ 整数列 A から推定される最小の長さの線形漸化式を求める.

    Args:
        A (list[int]): A の先頭

    Returns:
        list[int]: 整数列 A から推定される最小の長さの線形漸化式である. つまり, 以下を満たす.
            A[i] = C[0] * A[i - 1] + C[1] * A[i - 2] + ... + C[d - 1] * A[i - d] (i >= len(A))
    """

    N = len(A)
    B = [1]
    C = [1]
    l, m, p = 0, 0, 1
    for i in range(N):
        m += 1
        d = A[i]
        for j in range(1, l + 1):
            d += C[j] * A[i-j]
            d %= Mod

        if d == 0:
            continue

        T = C.copy()
        q = pow(p, -1, Mod) * d % Mod
        C.extend([0] * (len(B) + m - len(C)))

        for j in range(len(B)):
            C[j + m] -= q * B[j]
            C[j + m] %= Mod

        if 2 * l <= i:
            B = T
            l, m, p = i+1-l, 0, d

    return [Mod - c if c else 0 for c in C[1:]]

def Fibonacci(n: int) -> int:
    """ Fibonacci 列の第 n 項を求める.

    Args:
        n (int):

    Returns:
        int: Fibonacci 列の第 N 項
    """

    return Nth_Term_of_Linearly_Recurrent_Sequence([0, 1], [1, 1], n)

def Lucas(n: int) -> int:
    """ Lucas 列の第 n 項を求める.

    Args:
        n (int):

    Returns:
        int: Lucas 列の第 n 項
    """

    return Nth_Term_of_Linearly_Recurrent_Sequence([2, 1], [1, 1], n)

def Cumulative(A: list[int], n: int) -> int:
    """ d := len(A) として, A[i + d] = A[i + d - 1] + ... + A[i] で定義される A に対して, A[n] を求める.

    Args:
        A (list[int]): A の先頭
        n (int):

    Returns:
        int: A[n]
    """

    return Nth_Term_of_Linearly_Recurrent_Sequence(A, [1] * len(A), n)

def Factorial_Modulo(n: int) -> int:
    """ n! を Mod で割った余りを求める.

    Args:
        n (int):

    Returns:
        int: n! を Mod で割った余り
    """

    if n == 0:
        return 1
    elif n >= Mod:
        return 0

    n_sqrt = 0
    while (n_sqrt + 1) * (n_sqrt + 1) <= n:
        n_sqrt += 1

    A = Calc.multiple_convolution(*[[i, 1] for i in range(1, n_sqrt + 1)])
    H = Multipoint_Evaluation(Modulo_Polynomial(A, n_sqrt + 1), [i * n_sqrt for i in range(n_sqrt)])

    X = 1
    for h in H:
        X = (h * X) % Mod

    for i in range(n_sqrt * n_sqrt + 1, n_sqrt + 1):
        X = (i * X) % Mod
    return X

# 特別な数列
def Bernoulli(N: int) -> list[int]:
    """ Bernoulli 数 B[0], B[1], ..., B[N + 1] を求める.

    Args:
        N (int):

    Returns:
        list[int]: 第 d 項が B[d] に対応する長さ (N L 1) のリスト
    """

    P = Exp(Modulo_Polynomial([0, 1], N + 2))[1:]
    f = P.inverse().poly[:-1]

    fact = 1
    for i in range(1, N + 1):
        fact = (fact * i) % Mod
        f[i] = (f[i] * fact) % Mod

    return f

def PartitionsP(n: int) -> list[int]:
    """ k = 0, 1,..., n に対して, 以下で定義される分割数 p(k) を求める.
        p(k) := k を順序を区別せずに自然数の和に分ける場合の数

    Args:
        n (int):

    Returns:
        list[int]: 第 k 項が p(k) に対応する長さ (n + 1) の整数のリスト
    """

    f = [0] * (n + 1)
    f[0] = 1
    k = 1
    while k * (3 * k - 1) <= 2 *n:
        m = -1 if k & 1 else 1
        f[k * (3 * k - 1) // 2] += m

        if k * (3 * k + 1) <= 2 *n:
            f[k * (3 * k + 1) // 2 ]+= m
        k += 1

    return Calc.inverse(f)

def PartitionsQ(n: int) -> list[int]:
    """ k = 0, 1,..., n に対して, 以下で定義される q(k) を求める.
        q(k) := k を順序を区別せずに, なおかつ全ての項が異なる自然数の和に分ける場合の数

    Args:
        n (int):

    Returns:
        list[int]: 第 k 項が q(k) に対応する長さ (n + 1) の整数のリスト
    """

    inv = [0] * (n+1)
    inv[1] = 1
    for x in range(2, n + 1):
        q, r = divmod(Mod, x)
        inv[x] = (-q * inv[r]) % Mod

    p = [0] * (n + 1)
    for i in range(1, n + 1):
        j = i
        k = 1
        c = 1
        while j <= n:
            p[j] = (p[j] + c * inv[k]) % Mod
            c *= -1
            j += i
            k += 1
    P = Modulo_Polynomial(p, n + 1)
    return Exp(P).poly

def Stirling_1st(n: int) -> list[int]:
    """ k = 0, 1, ..., n に対する第 I 種 Stirling 数 S_{n, k} を求める.

    Args:
        n (int):

    Returns:
        list[int]: 長さが (n + 1) のリスト. 第 k 項が S_{n, k} を表す.
    """

    def g(n):
        if n==0:
            return Modulo_Polynomial([1], n + 1)
        elif n==1:
            return Modulo_Polynomial([0, 1], n + 1)
        elif n % 2 == 1:
            return Modulo_Polynomial([-n + 1, 1], n + 1) * g(n - 1)
        else:
            P = g(n // 2)
            return P * Taylor_Shift(P, -n // 2)

    return g(n).poly

def Stirling_2nd(n: int) -> list[int]:
    """ k = 0, 1, ..., n に対する第 II 種 Stirling 数 S_{n, k} を求める.

    Args:
        n (int):

    Returns:
        list[int]: 長さが (n + 1) のリスト. 第 k 項が S_{n, k} を表す.
    """

    fact = [0] * (n + 1); fact[0] = 1
    for i in range(1, n + 1):
        fact[i] = i * fact[i - 1] % Mod

    fact_inv = [0] * (n + 1); fact_inv[-1] = pow(fact[-1], -1, Mod)
    for i in range(n-1, -1, -1):
        fact_inv[i] = (i + 1) * fact_inv[i + 1] % Mod

    f = [pow(i, n, Mod) * fact_inv [i] % Mod for i in range(n + 1)]
    g = [fact_inv[i] if i & 1 == 0 else -fact_inv[i] for i in range(n + 1)]
    return Calc.convolution(f, g)[:n + 1]

def Bell(n: int) -> list[int]:
    """ Bell 数 Bell[k] ({1, 2, ..., k} の分割の数) を k = 0, 1, ..., n に対して求める.

    Args:
        n (int):

    Returns:
        list[int]: 第 k 項は Bell[k] に対応する.
    """

    # Note: Bell(X) = exp(exp(X) - 1) である.

    fact = [1] * (n + 1)
    for k in range(1, n + 1):
        fact[k] = (k * fact[k - 1]) % Mod

    fact_inv = [1] * (n + 1)
    fact_inv[-1] = pow(fact[-1], -1, Mod)
    for k in range(n - 1, 0, -1):
        fact_inv[k] = (k + 1) * fact_inv[k + 1] % Mod

    # G = exp(X) - 1
    g = [0] + fact_inv[1:]

    # F = exp(G) = exp(exp(X) - 1)
    f = Exp(Modulo_Polynomial(g, n + 1)).poly

    for k in range(1, n + 1):
        f[k] = fact[k] * f[k] % Mod

    return f

def Motzkin(n: int) -> list[int]:
    """ Motzkin 数 Mot[k] (円周上の区別がつく相異なる k 点を線分をどの2つも共通部分がない (k 点内で共有も禁止) で結ぶ方法 (結ばれない点があってもよい) の数) を k = 0, 1, ..., n に対して求める.

    Args:
        n (int):

    Returns:
        list[int]: 第 k 項は Mot[k] に対応する.
    """

    two_inv = pow(2, -1, Mod)
    F = ((Modulo_Polynomial([1, -1], n + 3) - Sqrt(Modulo_Polynomial([1,-2,-3], n + 3))) * two_inv) >> 2
    return F.poly[:n + 1]

#===
def Subset_Sum(X: list[int], K: int) -> list[int]:
    """ k = 0, 1, ..., K に対して, X の連続とは限らない部分列 Y のうち, sum(Y) = k となる Y の数 (場所が異なれば別としてカウント) を求める.

    Args:
        X (list[int]):
        K (int):

    Returns:
        list[int]: 第 k 項は「X の連続とは限らない部分列 Y のうち, sum(Y) = k となる Y の数 (場所が異なれば別としてカウント)」
    """

    chi = [0] * (K + 1)
    for x in X:
        if x <= K:
            chi[x] += 1

    inv = [0] * (K+1)
    inv[1] = 1
    for i in range(2,K+1):
        q, r = divmod(Mod, i)
        inv[i] = (-q * inv[r]) % Mod

    f = [0] * (K + 1)
    for i in range(1,K+1):
        if chi[i] == 0:
            continue

        c = 1
        for k in range(1, K // i + 1):
            f[i * k] = (f[i * k] + c * inv[k] * chi[i]) % Mod
            c *= -1

    return Exp(Modulo_Polynomial(f, K + 1)).poly

# 多項式和
def Polynominal_Sigma(P: Modulo_Polynomial) -> Modulo_Polynomial:
    """ 多項式 P に対して, Q(n) = P(1) + P(2) + ... + P(n) を満たす多項式 Q を求める.

    Args:
        P (Modulo_Polynomial):

    Returns:
        Modulo_Polynomial: Q
    """

    from itertools import accumulate

    n = len(P.poly)
    y_pre = Multipoint_Evaluation(P, list(range(1, n + 2)))
    y = list(accumulate(y_pre, lambda x, y: (x + y) % Mod))
    return Polynominal_Interpolation(list(range(1, n + 2)), y)

def Differences(P: Modulo_Polynomial, k: int = 1) -> Modulo_Polynomial:
    """ 以下で定義される P の k 回差分 D^k(P) を求める.
        D^t(P(n)) = D^{t-1}(P(n+1)-P(n)), D^0(P)=P.

    Args:
        P (Modulo_Polynomial):
        k (int, optional): 差分の階数. Defaults to 1.

    Returns:
        Modulo_Polynomial: D^k(P)
    """

    n = len(P.poly)

    fact = [1] * (k + 1)
    for i in range(1, k + 1):
        fact[i] = i * fact[i - 1] % Mod

    fact_inv = [1] * (k + 1)
    fact_inv[-1] = pow(fact[i], -1, Mod)
    for i in range(k - 1, -1, -1):
        fact_inv[i] = (i + 1) *fact_inv[i + 1] % Mod

    q = [0] * (n - k)
    sgn = 1 if k % 2 == 0 else -1

    for r in range(k + 1):
        alpha = sgn * fact[k] * (fact_inv[r] * fact_inv[k - r] % Mod) % Mod
        for j in range(n - k):
            q[j] += alpha * P[j] % Mod

        if r == k:
            break

        sgn *= -1
        P = Taylor_Shift(P, 1)

    return Modulo_Polynomial(q, P.max_degree)
