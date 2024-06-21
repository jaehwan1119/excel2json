def validationCheck(list1, list2):
    length = len(list1)
    for i in range(length):
        dict1, dict2 = list1[i], list2[i]
        if dict1 != dict2:
            print(f"Difference found at index {i}:")
            print(dict1)
            print(dict2)
