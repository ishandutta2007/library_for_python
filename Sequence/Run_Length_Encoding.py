def Run_Length_Encoding(S):
    """ Run Length 圧縮

    S: 列
    """
    if not S:
        return []

    R=[[S[0],1]]

    for i in range(1,len(S)):
        if R[-1][0]==S[i]:
            R[-1][1]+=1
        else:
            R.append([S[i],1])

    return R

def Alternating_Length_Encoding(S, first, second, equal = True) -> tuple[list[int], list[int]]:
    """ アルファベットサイズが 2 である列 S に対して, 最初に現れる first と残りの second について, それぞれが連続して現れる回数のリストを求める.

    Args:
        S: 列
        first: 最初に現れる文字
        second: 次に現れる文字
        equal (bool, optional): True にすると, 返り値における 2 つの配列の長さが等しくなる. Defaults to True.

    Returns:
        tuple[list[int], list[int]]: X, Y を整数のリストとしたタプル (X, Y). これは以下を意味する.
            * S = (first が連続して X[0] 個)(second が連続して Y[0] 個)(first が連続して X[1] 個)(second が連続して Y[1] 個)...
    """
    x: list[int] = []
    y: list[int] = []

    if S[0] == second:
        x.append(0)

    for a, k in Run_Length_Encoding(S):
        if a == first:
            x.append(k)
        else:
            y.append(k)

    if equal and len(x) > len(y):
        y.append(0)

    return x, y
