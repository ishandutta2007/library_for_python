class Permutation():
    def __init__(self, n, p=[]):
        if p==[]:
            self.p=[i for i in range(n)]
            self.ind=[i for i in range(n)]
        else:
            self.p=p
            self.ind=[0]*n

            for i in range(n):
                self.ind[p[i]]=i

        self.n=n

    def __getitem__(self, k):
        return self.p[k]

    def __str__(self):
        return str(self.p)

    __repr__=__str__

    def __eq__(self,other):
        return (self.n==other.n) and (self.p==other.p)

    def __mul__(self,other):
        assert self.n==other.n

        p=self.p; q=other.p
        return Permutation(self.n,  [p[q[i]] for i in range(self.n)])

    def __pow__(self, n):
        if n<0:
            return pow(self,-n).inverse()

        a=list(range(self.n))
        e=self.p[:]

        while n:
            if n&1:
                a=[a[e[i]] for i in range(self.n)]
            e=[e[e[i]] for i in range(self.n)]
            n>>=1

        return Permutation(self.n, a)

    def __truediv__(self,other):
        pass

    def sgn(self):
        """ 置換の符号を求める (偶置換 → 1, 奇置換 → -1)

        """
        return -1 if self.minimum_transposition()%2 else 1

    def inverse(self):
        return Permutation(self.n, self.ind)

    def inversion(self):
        BIT=[0]*(self.n+1)
        Y=(self.n*(self.n-1))//2

        for a in self.p:
            s=a
            while 1<=s:
                Y-=BIT[s]
                s-=s&(-s)

            r=a+1
            while r<=self.n:
                BIT[r]+=1
                r+=r&(-r)
        return Y

    def swap(self, i, j):
        """ i 番目と j 番目を交換する ※ i と j を交換ではない"""

        u=self.p[i]; v=self.p[j]

        self.p[i]=v; self.p[j]=u
        self.ind[v]=i; self.ind[u]=j

    def transposition(self, u, v):
        """ u,v のある場所を交換する ※ u 番目とv 番目ではない"""

        a=self.ind[u]; b=self.ind[v]

        self.p[a]=v; self.p[b]=u
        self.ind[u]=b; self.ind[v]=a

    def minimum_transposition(self):
        """ 互換の最小回数を求める. """

        return self.n-len(self.cycle_division())

    def cycle_division(self, mode=True):
        """ 置換を巡回置換の積に分解する.

        mode: 自己ループを入れるか否か"""

        p=self.p
        T=[False]*self.n
        A=[]

        for k in range(self.n):
            if not T[k]:
                a=[k]

                T[k]=True
                v=p[k]
                while v!=k:
                    T[v]=True
                    a.append(v)
                    v=p[v]

                if mode or len(a)>=2:
                    A.append(a)
        return A

    def operate_list(self, list):
        assert self.n==len(list),"置換の長さとリストの長さが違います."

        return [list[self.ind[i]] for i in range(self.n)]


    def order(self):
        from math import gcd

        x=1
        for m in self.cycle_division():
            g=gcd(x,len(m))
            x=(x//g)*len(m)
        return x

#=================================================
def Permutation_Inversion(P,Q):
    """ P から Q へ隣接項同士の入れ替えのみの最小回数を求める.
    """
    R=Q*(P.inverse())
    return R.inversion()

def List_Inversion(A,B,default=-1):
    """長さが等しいリスト A,B に対して, 以下の操作の最小回数を求める.
    列 A[i] と A[i+1] を入れ替え, B と一致させる.
    """

    from collections import defaultdict

    if len(A)!=len(B):
        return default

    N=len(A)
    D=defaultdict(list)

    for i in range(N):
        D[A[i]].append(i)

    for lis in D:
        D[lis].reverse()

    try:
        return Permutation(N,[D[B[i]].pop() for i in range(N)]).inversion()
    except:
        return default

#=================================================
#ランダムに置換を生成する.
def Random_Permutation(N):
    from random import shuffle
    L=list(range(N))
    shuffle(L)
    return Permutation(N,L)

def Is_Identity(P):
    for k,a in enumerate(P.p):
        if k!=a:
            return False
    return True

def Generate_Permutation(P, Q):
    """ P を Q にする変換を表す置換を生成する.

    """
    assert len(P)==len(Q)
    N=len(P)
    X=[-1]*N
    for i in range(N):
        X[P[i]]=Q[i]
    return Permutation(N, X)
