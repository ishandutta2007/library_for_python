class Imos_1:
    def __init__(self,N):
        self.len=N
        self.list=[0]*(N+1)

    def add(self,F,T,C=1):
        """閉区間 [F,T] にCを加算する.
        """
        self.list[F]+=C
        self.list[T+1]-=C

    def cumulative_sum(self):
        """累積和を求める.
        """
        Y=[0]*(self.len)
        S=0
        for i in range(self.len):
            S+=self.list[i]
            Y[i]=S
        return Y

#=================================================
from collections import defaultdict
class Expanded_Imos_1:
    def __init__(self):
        self.dict=defaultdict(int)

    def add(self,F,T,C=1):
        """閉区間 [F,T] にCを加算する.
        """
        self.dict[F]+=C
        self.dict[T+1]-=C

    def cumulative_sum(self, since, until):
        """累積和を求める.

        [Output]
        (y, l, r) という形のリスト. ただし, (y, l, r) は l<=x<=y の範囲では y であるということを意味する.
        """
        Y=[]
        S=0
        t_old=since
        dic=self.dict
        for t in sorted(dic):
            if t>until:
                break
            if dic[t]==0:
                continue

            if t_old<=t-1:
                Y.append((S, t_old,t-1))

            S+=dic[t]
            t_old=t

        if t_old<=until:
            Y.append((S, t_old,until))
        return Y

#=================================================
class Imos_2:
    def __init__(self,W,H):
        self.width=W
        self.height=H
        self.list=[[0]*(W+1) for _ in range(H+1)]

    def add(self,F,T,C=1):
        """F=(Fx,Fy), T=(Tx,Ty) に対して, 閉区間 [Fx,Tx] x [Fy,Ty] にCを加算する.
        """
        Fx,Fy=F
        Tx,Ty=T

        self.list[Fx][Fy]+=C
        self.list[Fx][Ty+1]-=C
        self.list[Tx+1][Fy]-=C
        self.list[Tx+1][Ty+1]+=C

    def cumulative_sum(self):
        Y=[[0]*(self.width+1) for _ in range(self.height+1)]

        for x in range(self.width+1):
            S=0
            for y in range(self.height+1):
                S+=self.list[y][x]
                Y[y][x]=S

        for y in range(self.height+1):
            S=0
            for x in range(self.width+1):
                S+=Y[y][x]
                Y[y][x]=S
        return Y
