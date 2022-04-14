# Longest Successive Repeated Substring
def LSRS(string):
    length = len(string)

    # The string must be 4 characters long at minimum
    if length < 4:
        return string

    # Find longest succesive substring repeated at least once
    start, maxLength = 0, 0
    for i in range(length - 4 + 1):
        subLength = length - i
        for l in range(subLength // 2, 1, -1):
            if string[i : i + l] == string[i + l : i + 2 * l]:
                if l > maxLength:
                    start, maxLength = i, l

    # Find how many times it repeats
    timesRepeated = 2
    while string[start : start + maxLength] == string[start + maxLength * timesRepeated: start + maxLength * (timesRepeated + 1)]:
        timesRepeated += 1
    
    return LSRS(string[0 : start]) + string[start : start + maxLength] + LSRS(string[start + maxLength * timesRepeated :])

if __name__ == "__main__":
    print(LSRS("babaabaaabaaabaaabaababababa"))