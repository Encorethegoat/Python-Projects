class Solution(object):
    def isPalindrome(self, x):
        rev = 0
        a = x
        if a > 0:
        
            while a > 0:
                digit = a%10
                rev = rev*10 + digit
                a //= 10
            if x == rev:
                return True
            else:
                return False
            

        else:
            return False

sol = Solution()
print(sol.isPalindrome(121))
print(sol.isPalindrome(-121))
print(sol.isPalindrome(10))