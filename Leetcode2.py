class Solution(object):
    def mergeTwoLists(self, list1, list2):
        for x in range(0,len(list2)):
            list1.append(list2[x])
        return sorted(list1)

list1 = [1,2,4]
list2 = [1,3,4]
sol = Solution()
print(sol.mergeTwoLists(list1,list2))