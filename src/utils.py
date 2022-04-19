def removeLongestSubstrings(string):
    result = string
    start, end = longestRepeatedSubstring(result)
    while end - start > 1:
        result = result[0 : start] + result[end :]
        start, end = longestRepeatedSubstring(result)
    return result

def longestRepeatedSubstring(string):
    length = len(string)
    L = [[0 for _ in range(length + 1)] for _ in range(length + 1)]
    maxLength, start, end = 0, 0, 0
    for i in range(1, length + 1):
        for j in range(i + 1, length + 1):
            if string[i - 1] == string[j - 1] and L[i - 1][j - 1] < (j - i):
                L[i][j] = L[i - 1][j - 1] + 1
                if L[i][j] > maxLength:
                    maxLength = L[i][j]
                    start = j - maxLength
                    end = j
            else:
                L[i][j] = 0

    """
    # Debug
    for line in L[1:]:
        print(line[1:])
    """

    return start, end

def needed_directions(maze):
    (xi, yi), (xf, yf) = maze.get_start_position(), maze.get_end_position()
    directions = []

    if xf > xi:
        directions.append('R')
    elif xf < xi:
        directions.append('L')
    
    if yf > yi:
        directions.append('D')
    elif yf < yi:
        directions.append('U')
    
    return directions

# Testing
if __name__ == "__main__":
    print(removeLongestSubstrings("rulurdru"))