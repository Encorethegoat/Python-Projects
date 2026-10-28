class reverse:
    def number(self,a):
        rev = 0
        while a > 0:
            digit = a%10
            rev = rev*10 + digit
            a //= 10

        print(rev)
objnum = reverse()
objnum.number(1234)

for x in range(0,3):
    for y in range(0,3):
        print(x,y)