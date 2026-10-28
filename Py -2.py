



class sum_add:
    def sum_1(self, a):
        sum = 0
        while a > 0:
            sum1 = a % 10
            sum += sum1
            a //= 10
        print("The sum of the digits is:", sum)

sum0 = sum_add()
sum0.sum_1(7894)
