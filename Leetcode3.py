class Solution(object):
    def addTwoNumbers(self, l1, l2):
        new_x = 0
        new_y = 0
        for x in l1:
            new_x = new_x*10 + x
    
        for y in l2:
            new_y = new_y*10 + y

        return list(map(int, str(new_x + new_y)))
        

l1 = [9,9,9,9,9,9,9]
l2 = [9,9,9,9]
sol = Solution()
print(sol.addTwoNumbers(l1,l2))
