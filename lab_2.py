
import numpy as np
from matplotlib import pyplot as plt
import math
import collections

#Сортування 
def sort_xy(x,y):
    dictionary={}
    n=len(x)
    for key in x:
        for value in y:
            dictionary[key]=value
            y.remove(value)
            break
    x.clear()
    y.clear()
    odictionary=collections.OrderedDict(sorted(dictionary.items()))
    for k,v in odictionary.items():
        x.append(k)
        y.append(v)
    res=[]
    res.append(x)
    res.append(y)
    return res
    

#Вибір типу умов
def type(an):
    func=[]
    if an==1:
        func.append(-11)
        func.append(-11)
    else:
        func.append(11)
        func.append(-11)
    return func


#СЛАР для першого типу при N<4
def slar_1_3(h,y,func,n):
    f=[]
    for i in range(n):
        f.append([])
    for i in range(n):
        for j in range(n+1):
            f[i].append(0)
    f[0][0]=1 
    f[0][n]=func[0]
    for i in range(n-2):
        f[i+1][i]=1/h[i]
        f[i+1][i+1]=2*(1/h[i]+1/h[i+1])
        f[i+1][i+2]=1/h[i+1]
        f[i+1][i+3]=3*((y[i+2]-y[i+1])/math.pow(h[i+1],2)+(y[i+1]-y[i])/math.pow(h[i],2))
    f[-1][-2]=1
    f[-1][-1]=func[1]
    return f

#СЛАР для другого типу при N<4
def slar_2_3(h,y,t,n):
    f=[]
    for i in range(n):
        f.append([])
    for i in range(n):
        for j in range(n+1):
            f[i].append(0)
    f[0][0]=-2*h[0]
    f[0][1]=-h[0]
    f[0][n]=type(t)[0]-(2/(math.pow(h[0],2)*3*(y[1]-y[0])))
    for i in range(n-2):
        f[i+1][i]=1/h[i]
        f[i+1][i+1]=2*(1/h[i]+1/h[i+1])
        f[i+1][i+2]=1/h[i+1]
        f[i+1][-1]=3*((y[i+2]-y[i+1])/math.pow(h[i+1],2)+(y[i+1]-y[i])/math.pow(h[i],2))
    f[-1][-3]=h[-2]
    f[-1][-2]=2*h[-2]
    f[-1][-1]=type(t)[1]-(2/((math.pow(h[-2],2))*3*(y[-1]-y[-2])))
    return f


#СЛАР для 1 типу умов
def slar_1(n,func, h, y):
    f=[]
    for i in range(n):
        f.append([])
    for i in range(n):
        for j in range (n+1):
            f[i].append(0)
    f[0][0]=2
    f[0][1]=1
    f[0][-1]=3*((y[1]-y[0])/math.pow(h[0],2))-3*func[0]/h[0]
    for i in range(1, n-1):
        f[i][i-1]=h[i-1]
        f[i][i]=2*(h[i]+h[i-1])
        f[i][i+1]=h[i]
        f[i][-1]=3*((y[i+1]-y[i])/h[i]-(y[i]-y[i-1])/h[i-1])
    f[-1][-3]=2*h[-2]/3
    f[-1][-2]=(h[-1]+4*h[-2]/3)
    f[-1][-1]=-func[1]+3*(y[-1]-y[-2])/h[-1]-2*(y[-2]-y[-3])/h[n-1]
    print("f="+str(f))
    return f

#СЛАР для другого типу умов
def slar_2(n, func, h, y):
    f=[]
    for i in range(n):
        f.append([])
    for i in range(n):
        for j in range (n+1):
            f[i].append(0)
    f[0][0]=1
    f[0][-1]=0.5*func[0]
    for i in range(1, n-1):
        f[i][i-1]=h[i-1]
        f[i][i]=2*(h[i]+h[i-1])
        f[i][i+1]=h[i]
        f[i][-1]=3*((y[i+1]-y[i])/h[i]-(y[i]-y[i-1])/h[i-1])
    f[-1][-3]=h[-2]
    f[-1][-2]=2*(h[-1]+h[-2])
    f[-1][-1]=-func[1]*h[-1]/2+3*((y[-1]-y[-2])/h[-1]-(y[-2]-y[-3])/h[n-1])
    print("f="+str(f))
    return f


#метод перегонки
def dist(f,n):
    #обчислюємо коефіцієнти
    a=[]
    b=[]
    c=[]
    d=[]

    a.append(0)
    for i in range(1, n):
        a.append(f[i][i-1])
    for i in range(n):
        b.append(-f[i][i])
        d.append(f[i][-1])
    for i in range(n-1):
        c.append(f[i][i+1])
    c.append(0)
    print("Коефіцієнти перегонки: ")
    print("a= "+str(a))
    print("b= "+str(b))
    print("c= "+str(c))
    print("d= "+str(d))

    #Обчислюємо перегоночні поефіцієнти
    p=[]
    q=[]

    p.append(c[0]/b[0]) 
    q.append(-d[0]/b[0])
    for i in range(1,n):
        p.append(c[i]/(b[i]-a[i]*p[i-1]))
        q.append((a[i]*q[i-1]-d[i])/(b[i]-a[i]*p[i-1]))

    print("Коефіцієнти перегонки: ")
    print("p= "+str(p))
    print("q= "+str(q))
    m=[]
    for i in range(n):
        m.append(0)
    m[-1]=q[-1]
    for i in range(n-2,-1,-1):
        m[i]=p[i]*m[i+1]+q[i]
    return m

#обчислення значення функціїї та її похідної у заданій точці
def der(coef,x):
    xav=float(input("Введіть задане значення x: "))
    a=coef[0]
    b=coef[1]
    c=coef[2]
    d=coef[3]
    for i in range(len(x)-1):
        if xav<x[i+1] and xav>x[i]:
            iav=i
    fx=a[iav]+b[iav]*(xav-x[iav])+c[iav]*math.pow((xav-x[iav]),2)+d[iav]*math.pow((xav-x[iav]),3)
    fdx=2*c[iav]+6*d[iav]*(xav-x[iav])
    print("Функція в точці "+str(xav)+" дорівнює "+str(fx))
    print("Друга похідна функції в точці "+str(xav)+" дорівнює "+str(fdx))

#обчислення значення функціїї та її похідної у заданій точці при N<4
def der_3(x,s):
    xav=float(input("Введіть задане значення x: "))
    for i in range(len(x)-1):
        if xav<x[i+1] and xav>x[i]:
            iav=i
    fx=math.pow(xav,3)*s[iav][0]+math.pow(xav,2)*s[iav][1]+xav*s[iav][2]+s[iav][3]
    fdx=6*s[iav][0]*xav+2*s[iav][1]
    print("Функція в точці "+str(xav)+" дорівнює "+str(fx))
    print("Друга похідна функції в точці "+str(xav)+" дорівнює "+str(fdx))

#Обчислення коефіцієнтів для умов другого типу
def coefficient_2(c,n, func,y,h):
    
    a=[]
    b=[]
    d=[]
    for i in range(n):
        a.append(y[i])

    for i in range(n):
        b.append(0)
    b[-1]=((y[-1]-y[-2])/h[-1])-(func[1]*h[-1]/6)-(c[-1]*h[-1]*2/3)
    for i in range(n-2,-1,-1):
        b[i]=b[i+1]-(h[i]*(c[i]+c[i+1]))
    
    for i in range(n-1):
        d.append((c[i+1]-c[i])/(3*h[i]))
    d.append((func[1]-2*c[-1])/(6*h[-1]))    
    coef=[]
    coef.append(a)
    coef.append(b)
    coef.append(c)
    coef.append(d)
    print("Коефіцієнти:")
    print("a= "+str(a))
    print("b= "+str(b))
    print("c= "+str(c))
    print("d= "+str(d))
    return coef

#Обчислення коефіцієнтів для умов першого типу
def coefficient_1(c,n,func, y,h):
    a=[]
    b=[]
    d=[]
    for i in range(n):
        a.append(y[i])
    for i in range(n-1):
        b.append((y[i+1]-y[i])/h[i]-h[i]*(c[i+1]+2*c[i])/3)
    b.append((y[-2]-y[-3])/h[-2]+h[-2]*(2*c[-1]+c[-2])/3)
    for i in range(n-1):
        d.append((c[i+1]-c[i])/(3*h[i]))
    d.append(((y[-1]-y[-2])/h[-1]-(y[-2]-y[-3])/h[-2]-h[-2]*(c[-2]+2*c[-1])/3-c[-1]*h[-1])/math.pow(h[-1],2))
    coef=[]
    coef.append(a)
    coef.append(b)
    coef.append(c)
    coef.append(d)
    print("Коефіцієнти:")
    print("a= "+str(a))
    print("b= "+str(b))
    print("c= "+str(c))
    print("d= "+str(d))
    return coef

#Обчислення сплайну
def spline(n,x,coef):
    a=coef[0]
    b=coef[1]
    c=coef[2]
    d=coef[3]
    print("Рівняння сплана:")
    for i in range(n):
        print("S"+str(i)+"="+str(a[i])+"+"+str(b[i])+"(x-"+str(x[i])+")+"+str(c[i])+"(x-"+str(x[i])+")^2+"+str(d[i])+"(x-"+str(x[i])+")^3, для хє["+str(x[i])+", "+str(x[i+1])+"]")
    
#обчислення сплайну при N<4
def spline_3(x,y,m,h,n):
    st=[]
    s=[]
    for i in range(n):
        st.append([])
        s.append([])
    for i in range(n-1):
        st[i].append(2*y[i]-2*y[i+1]-m[i]*h[i]+m[i+1]*h[i])
        st[i].append(-3*y[i]+3*y[i+1]-m[i+1]*h[i])
        st[i].append(m[i]*h[i])
        st[i].append(y[i])
    #print("St: "+str(st))

    for i in range(n):
        s[i].append(st[i][0]/math.pow(h[i],3))
        s[i].append(-3*x[i]/math.pow(h[i],3)+st[i][1]/math.pow(h[i],2))
        s[i].append(3*st[i][0]*math.pow(x[i],2)/math.pow(h[i],3)-2*x[i]*st[i][1]/math.pow(h[i],2)+st[i][2]/h[i])
        s[i].append(-math.pow(x[i],3)*st[i][0]/math.pow(h[i],3)+math.pow(x[i],2)*st[i][1]/math.pow(h[i],2)-x[i]*st[i][2]/h[i]+st[i][3])

    for i in range(n):
        print("S"+str(i)+"=x^3*"+str(s[i][0])+"+x^2*"+str(s[i][1])+"+x*"+str(s[i][2])+"+"+str(s[i][3])+", для x є ["+ str(x[i])+", "+ str(x[i+1])+"]")
    return s

#Побудова сплайну
def drawspline(x,y,coef):
    a=coef[0]
    b=coef[1]
    c=coef[2]
    d=coef[3]
    fig, ax=plt.subplots(figsize=(8,8))
    x_plot=[x[0]]
    y_plot=[]
    step=(x[-1]-x[0])/10000
    for i in range(1,10000):
        x_plot.append(x_plot[i-1]+step)
        for k in range(1, len(x)+1):
            omega_list=[]
            if x[k-1]<=x_plot[i-1]<=x[k]:
                omega=x_plot[i-1]-x[k-1]
                y_plot.append(a[k-1]+b[k-1]*omega+c[k-1]*(omega**2)+d[k-1]*(omega**3))
    ax.grid()
    y_plot.append(y[-1])
    ax.plot(np.array(x_plot), np.array(y_plot), c="red")
    ax.plot(x,y,"bo")
    plt.show()

#Виконання звдання для першого типу умов
def first(x,n,func,h,y):
    if n>=3:
        f=slar_1(n,func,h,y)
        c=dist(f,n)
        coef=coefficient_1(c,n,func,y,h)
        spline(n,x,coef)
        der(coef,x)
    else:
        f=slar_1_3(n,y,func,n)
        m=dist(f,n)
        s=spline_3(x,y,m,h,n)
        der_3(x,s)
    drawspline(x,y, coef)

#Виконання звдання для другого типу умов
def second(x,n,func,h,y):
    if n>=3:
        f=slar_2(n,func,h,y)
        c=dist(f,n)
        coef=coefficient_2(c,n,func,y,h)
        spline(n,x,coef)
        der(coef,x)
    else:
        f=slar_2_3(n,y,func,n)
        m=dist(f,n)
        s=spline_3(x,y,m,h,n)
        der_3(x,s)
    drawspline(x,y, coef)

def lab2():
    x=[-8.1,0.7,2.3,-4.9,7.4]
    y=[3.325,1.172,1.552,1.14,2.93]
    h=[]
    N=len(x)

    x=sort_xy(x,y)[0]
    y=sort_xy(x,y)[1]
    print(x)
    print(y)
    n=N-1
    for i in range(n):
        h.append(x[i+1]-x[i])
    t=int(input("Оберіть тип умов (введіть 1, якщо бажаєте обрати перший тип, або 2, якшщо другий):"))
    
    an="Y"
    while an!="n":
        func=type(t)
        if t==2:
            second(x,n,func,h,y)   
        else:
            first(x,n,func,h,y)

        

        an=input("Бажаєте побудувати сплайн з іншими граничними умоваим? (Y/n): ")
        if an=="n":
            break
        else:
            if t==2:
                t=1
            else:
                t=2
    
lab2()
