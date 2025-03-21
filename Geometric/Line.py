from Point import *

class Segment():
    __slots__=["begin","end","id"]

    def __init__(self,P,Q):
        """2点 P, Q (P!=Q) を端点とする線分を生成する.

        P,Q: Point
        """
        assert P!=Q
        self.begin=P
        self.end=Q
        self.id=2

    def __str__(self):
        return "[Segment] {}, {}".format(self.begin,self.end)

    __repr__=__str__

    def __eq__(self,other):
        return (
            (self.begin==other.begin) and (self.end==other.end) or
            (self.begin==other.end) and (self.end==other.begin)
            )

    def __contains__(self,point):
        return (self.begin==point) or (self.end==point) or (iSP(self.begin,self.end,point)==0)

    def vectorize(self):
        return self.end-self.begin

    def counter_vectorize(self):
        return self.begin-self.end

class Ray():
    __slots__=["begin","end","id"]

    def __init__(self,P,Q):
        """ P を端点とし, Q を通る半直線を通る.

        P,Q: Point
        """
        assert P!=Q
        self.begin=P
        self.end=Q
        self.id=3

    def __str__(self):
        return "[Ray] {} -> {}".format(self.begin,self.end)

    __repr__=__str__

    def __eq__(self,other):
        if self.begin!=other.begin:
            return False

        m=iSP(self.begin,self.end,other.end)
        return m==0 or m==2

    def __contains__(self,point):
        m=iSP(self.begin,self.end,point)
        return m==0 or m==2

    def vectorize(self):
        return self.end-self.begin

    def counter_vectorize(self):
        return self.begin-self.end

class Line:
    __slots__ = ("begin", "end")

    def __init__(self, P: Point, Q: Point):
        """ 2 点 P, Q を通る直線を生成する.

        Args:
            P (Point): 始点
            Q (Point): 終点
        """
        assert P != Q
        self.begin = P
        self.end = Q

    def __str__(self) -> str:
        return f"[Line] {self.begin}, {self.end}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.begin)}, {repr(self.end)})"

    def __iter__(self):
        yield self.begin
        yield self.end

    def __eq__(self, other: "Line") -> bool:
        return (other.bein in self) and (other.end in self)

    def __contains__(self, point: Point) -> bool:
        return abs(iSP(self.begin, point, self.end)) != 1

    def vectorize(self) -> Point:
        """ この直線の方向ベクトルを求める.

        Returns:
            Point: 方向ベクトル
        """

        return self.end - self.begin

    def counter_vectorize(self) -> Point:
        return self.begin - self.end

#=== 生成
def Line_from_General_Form(a,b,c):
    """ ax+by+c=0 という形の直線を生成する.

    a,b,c: int or float ((a,b) neq (0,0))
    """

    assert (a!=0) or (b!=0)

    k=sqrt(a*a+b*b)

    if b==0:
        x=-c/a; y=0
    else:
        x=0; y=-c/b

    return Line(Point(x,y),Point(x-b/k, y+a/k))

#=== 一般形
def General_Form_from_Line(L, lattice=False):
    """ 直線 L が満たす式 ax+by+c=0 の a,b,c を求める.
    """

    s=L.begin.x; t=L.begin.y
    v=L.vectorize(); alpha=v.x; beta=v.y

    sgn=compare(beta,0)
    if sgn==0:
        sgn=compare(-alpha,0)

    k=alpha*t-beta*s
    if lattice:
        g=gcd(gcd(alpha,beta),k)
        alpha//=g; beta//=g; k//=g

    return (sgn*beta,sgn*(-alpha),sgn*k)

#=== 交差判定
def has_Intersection_between_Segment_and_Segment(L,M,endpoint=True):
    """ 線分 L,M が交わるかどうかを判定する.

    L,M: 直線
    """

    a=L.begin; b=L.end; c=M.begin; d=M.end
    if not(iSP(a,b,c)*iSP(a,b,d)<=0 and iSP(c,d,a)*iSP(c,d,b)<=0):
        return False

    if endpoint:
        return True

def has_Intersection_between_Line_and_Segment(L,M,endpoint=True):
    """ 直線 L と線分 M が交わるかどうかを判定する.

    L: 直線
    M: 線分
    """

    a=L.begin; b=L.end; c=M.begin; d=M.end
    return iSP(a,b,c)*iSP(a,b,d)<=0

def has_Intersection_between_Line_and_Line(L,M):
    """ 直線 L,M が交わるかどうかを判定する.

    L,M: 直線
    """

    return not equal(L.vectorize().det(M.vectorize()), 0)

#=== 交点を求める
def Intersection_between_Line_and_Line(L,M,Mode=False):
    """ 直線 L,M の交点を求める.

    L,M: 直線
    Mode=False: 交点が一意に定まらない場合エラーを吐く.
    Mode=True: 一致する場合, True, 交点が存在しない場合 False を返す.
    """

    if L==M:
        if Mode:
            return True
        else:
            assert 0,"直線が一致します"
    if is_Parallel(L,M):
        if Mode:
            return False
        else:
            assert 0,"交点が存在ません"

    a=L.begin; b=L.end; c=M.begin; d=M.end
    k=(d-a).det(d-c)/(b-a).det(d-c)
    return a+k*(b-a)

#=== 垂直二等分線
def Perpendicular_Bisector(S, lattice=False):
    """ 線分 S の垂直二等分線を求める."""

    u=S.vectorize()

    M=S.begin+S.end
    if lattice:
        M.x//=2; M.y//=2
    else:
        M.x/=2; M.y/=2
    return Line(M,M+u*Point(0,1))

#=== 2直線の関係
def is_Parallel(L,M):
    """2つの直線 (線分) L,M が平行かどうかを判定する.

    L,M: 直線 or 線分
    """

    u=L.vectorize(); v=M.vectorize()
    return equal(u.det(v), 0)

def is_Orthogonal(L,M):
    """2つの直線 (線分) L,M が直行するかどうかを判定する.

    L,M: 直線 or 線分
    """

    u=L.vectorize(); v=M.vectorize()
    return equal(u.dot(v), 0)

#=== 点との距離
def Distance_between_Point_and_Segment(P,L):
    """ 点 P と線分 L の距離を求める.

    """

    A=L.begin; B=L.end
    if Angle_Type(P,A,B)==-1:
        return abs(P-A)
    elif Angle_Type(P,B,A)==-1:
        return abs(P-B)
    else:
        v=L.vectorize()
        return abs((P-L.begin).det(v)/abs(v))

def Distance_between_Point_and_Line(P,L):
    """ 点 P と直線 L の距離を求める.

    """

    v=L.vectorize()
    return abs((P-L.begin).det(v)/abs(v))

#=== 線同士の距離
def Distance_between_Line_and_Line(L,M):
    """ 2直線 L,M の距離を求める.

    L,M: 直線
    """

    if is_Parallel(L,M):
        return Distance_between_Point_and_Line(L.begin,M)
    else:
        return 0

def Distance_between_Line_and_Segment(L,M):
    """ 直線 L と線分 M の距離を求める.

    L: 直線, M: 線分
    """

    if has_Intersection_between_Line_and_Segment(L,M):
        return 0
    else:
        return min(
            Distance_between_Point_and_Line(M.begin, L),
            Distance_between_Point_and_Line(M.end, L)
            )

def Distance_between_Segment_and_Segment(L,M):
    """ 2線分 L,M の距離を求める.

    L,M: 線分
    """

    if has_Intersection_between_Segment_and_Segment(L,M):
        return 0

    return min(
        Distance_between_Point_and_Segment(L.begin,M),
        Distance_between_Point_and_Segment(L.end  ,M),
        Distance_between_Point_and_Segment(M.begin,L),
        Distance_between_Point_and_Segment(M.end  ,L)
        )

#=== 点と直線の幾何
def Projection(P,L):
    """ 点 P の直線 L 上の射影を求める.

    """

    v=L.vectorize()
    return L.begin-((L.begin-P).dot(v)/v.norm_2())*v

def Reflection(P,L):
    """ 点 P の直線 L による反射を求める.

    """

    return P+2*(Projection(P,L)-P)
