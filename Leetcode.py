class Solution(object):
    def twoSum(self, nums, target):
        for x in range(0,len(nums)+1):
            for y in range(0,len(nums)):
                if x == y:
                    continue
                else:
                    if target == nums[x] + nums[y]:
                        return x,y

nums = [3,2,4]
target = 6
sol = Solution()
print(sol.twoSum(nums,target))
