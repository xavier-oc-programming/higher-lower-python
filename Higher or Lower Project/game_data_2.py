# treasure map matrix

treasure_matrix = [[0 for _ in range(3)] for _ in range(3)]
print(treasure_matrix)

treasure_matrix[1][1] = "x"

for i in treasure_matrix:
    for j in i:
        print(j, end=',')
    print()
