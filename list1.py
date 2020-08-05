n1=int(input())
n2=int(input())
s=[x for x in range(n1,n2+1) for y in x if x%y!=0 ]
print(s)
