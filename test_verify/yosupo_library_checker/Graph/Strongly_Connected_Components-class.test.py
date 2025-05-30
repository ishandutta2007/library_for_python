# verification-helper: PROBLEM https://judge.yosupo.jp/problem/scc

#==================================================
from Strongly_Connected_Components import *

import sys
input=sys.stdin.readline
write=sys.stdout.write

#==================================================
def verify():
    N,M=map(int,input().split())
    S=Strongly_Connected_Components(N)
    for _ in range(M):
        a,b=map(int,input().split())
        S.add_arc(a,b)

    S.decomposition()
    print(len(S.components))
    for component in S.components:
        write(f"{len(component)} {' '.join(map(str, component))}\n")

#==================================================
verify()
