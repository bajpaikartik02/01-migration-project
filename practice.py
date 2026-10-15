st="[12,34,345,678,346556,4,5]"
val=""
i=0
out=[]
while i<len(st):
    if st[i]=='[':
        i+=1
        continue
    if st[i]!=',' and st[i]!=']':
        val+=st[i]
        i+=1
        continue
    else:
        out.append(int(val))
        val=""
        i+=1
        continue
print(out)
