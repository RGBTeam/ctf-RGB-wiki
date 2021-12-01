from Crypto.Util.number import *
import gmpy2
#a fraction can be expressed as a numerator divided by denominator
#It's like numerator / denominator

#求解连分数,仅接受整数参数
def continuedFrac(x,y):
    cf = []
    while y:
        cf.append(x//y)
        #对于直接分解小数的情况，可以用下面的方法
        # cf.append(int(x/y)
        x, y = y, x%y
    return cf

#对于一定长度的连分数表示，转换成分数形式
def Simplify(ctnf):
    numerator = 0
    denominator = 1
    for x in ctnf[:0:-1]:
        numerator, denominator = denominator, x * denominator + numerator
    return (numerator+ctnf[0]*denominator,denominator)

#展示所有分数形式的连分数
def calculateFrac(x,y):
    cf=continuedFrac(x,y)
    return map(Simplify,(cf[0:i] for i in range(1,len(cf))))

def vieta(a,b,c):
    # print(a,b,c)
    try:
        par = gmpy2.isqrt(b*b - 4*a*c)
    except:
        return 0,0
    return (-b + par) // (2*a),(-b - par) // (2*a)

def wienerAttack(e,n):
    for (k,d) in calculateFrac(e,n):
        if k==0:
            continue
        if (e*d - 1) % k != 0:
            continue
        phi = (e*d - 1) // k
        #此时有，p*q=n，p+q=n+1-phi，构造x^2-(p+q)*x+p*q=0，则其解为p和q
        p,q = vieta(1,phi-n-1,n)
        if p*q == n:
            return abs(int(p)),abs(int(q))
    print("not found")

a=continuedFrac(415,93)
print(a)
print(Simplify(a))
