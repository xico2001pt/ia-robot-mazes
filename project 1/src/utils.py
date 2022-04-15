# Function that unifies the largest successive patterns
def LSRS(string, debug=False):  # LSRS - Longest Successive Repeated Substrings
    length = len(string)
    if debug: print(f"> Analysing string:   {string}")

    # The string must be 4 characters long at minimum
    if length < 4:
        return string

    # Find longest succesive substring repeated at least once
    start, maxLength, repetitions = 0, 0, 1
    for i in range(length - 4 + 1):
        subLength = length - i
        for l in range(subLength // 2, 1, -1):
            if string[i : i + l] == string[i + l : i + 2 * l]:
                if l > maxLength:                                               # Found a new largest substring
                    start, maxLength, repetitions = i, l, 1
                    if debug: print(f"> Found a substring:  start = {start:2}, length = {maxLength:2}, repetitions = {repetitions:2}")
                elif l == maxLength and i == start + maxLength * repetitions:   # Found a successive substring
                    repetitions += 1
                    if debug: print(f"> Found a repetition: start = {start:2}, length = {maxLength:2}, repetitions = {repetitions:2}")
    
    if maxLength == 0:  # No repeated substring found
        return string
    else:
        return LSRS(string[0 : start], debug) + string[start : start + maxLength] + LSRS(string[start + maxLength * (repetitions + 1) :], debug)

# Testing
if __name__ == "__main__":
    print(LSRS("adadadadadadadadahaksjdhakjaldknabcdabcdabcdaaa", True))