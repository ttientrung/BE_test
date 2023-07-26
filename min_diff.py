def min_diff(arr1, arr2):
    arr1.sort()
    arr2.sort()

    min_diff = float('inf')
    ptr1, ptr2 = 0, 0

    while ptr1 < len(arr1) and ptr2 < len(arr2):
        curr_diff = abs(arr1[ptr1] - arr2[ptr2])
        min_diff = min(min_diff, curr_diff)

        if arr1[ptr1] < arr2[ptr2]:
            ptr1 += 1
        else:
            ptr2 += 1

    return min_diff

arr1 = [1, 3, 5, 11, 15]
arr2 = [4, 7, 10, 12]
result = min_diff(arr1, arr2)
print("Khoảng chênh lệch nhỏ nhất là:", result)
