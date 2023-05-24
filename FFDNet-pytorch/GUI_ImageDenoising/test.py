def find_largest_number(arr):
    if len(arr)==1:
        return arr[0]
    elif len(arr)==2:
        return max(arr[0],arr[1])
    else:
        mid=len(arr)//2
        left=find_largest_number(arr[:mid])
        right=find_largest_number(arr[mid:])
        return max(left,right)
a=[3,2,1,4,5]
print(find_largest_number(a))