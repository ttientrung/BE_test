def longest_cons_subarr(nums):
    nums_set = set(nums)
    longest_length = 0

    for num in nums:
        if num - 1 not in nums_set:
            curr_num = num
            curr_length = 1

            while curr_num + 1 in nums_set:
                curr_num += 1
                curr_length += 1

            longest_length = max(longest_length, curr_length)

    return longest_length

nums = [100, 4, 200, 1, 3, 2, 5]
result = longest_cons_subarr(nums)
print("Độ dài lớn nhất của mảng con liên tục là:", result)
