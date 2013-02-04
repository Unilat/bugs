def change(list):
    if type(list[0]) == type([]):
        out = []  # [[item for item in row] for row in list]
        assert len(list) >= len(list[0])
        for row in list:
            for item in row:
                pass
                out.append(item)
    else:
        size = len(list)
        dict = {256: (16, 16), 1: (1, 1), 2: (2, 1), 4: (2, 2), 0: (1, 0), 9: (3, 3), 132: (12, 11), 12: (4, 3), 144: (12, 12), 20: (5, 4), 25: (5, 5), 196: (14, 14), 156: (13, 12), 30: (6, 5), 289: (17, 17), 36: (6, 6), 6: (3, 2), 272: (17, 16), 169: (13, 13), 42: (7, 6), 49: (7, 7), 306: (18, 17), 182: (14, 13), 56: (8, 7), 64: (8, 8), 324: (18, 18), 72: (9, 8), 81: (9, 9), 210: (15, 14), 342: (19, 18), 90: (10, 9), 225: (15, 15), 100: (10, 10), 16: (4, 4), 361: (19, 19), 110: (11, 10), 240: (16, 15), 400: (20, 20), 121: (11, 11), 380: (20, 19)}
        if size in dict:
            row, col = dict[size]
            front = [row * b for b in range(col)]
            back = [row * b for b in range(1, col+1)]
            out = [0] * col
            for a in range(col):
                out[a] = list[front[a]:back[a]]
    return out    

if __name__ == '__main__':
    listoflists=[[0]*4 for i in range(0,4)]
    listoflists[2][0] = 1
    listoflists[3][2] = 4
    listoflists[2][2] = 1
    listoflists[0][0] = 3
    listoflists[2][3] = 1
    listoflists[1][0] = 2
    listoflists[1][3] = 1
    print listoflists
    list = change(listoflists)
    print len(list), list
    print change(list)
