from PIL import Image
import numpy as np


class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def put(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def isInside(self, item):
        return item in self.items

    def getLastN(self, n):
        if self.size() < n:
            return self.items
        else:
            return self.items[-n:]

    def __str__(self):
        return self.items


def regionGrowing(mat, epsilon, meancount, start_point):
    ST = Stack()

    s = []
    x = start_point[0]
    y = start_point[1]

    ST.put((x, y))

    while not ST.isEmpty():
        temp = ST.getLastN(meancount)
        sum = 0
        for i in temp:
            xt = i[0]
            yt = i[1]
            sum += mat[xt][yt]

        mean = float(sum) / len(temp)

        t = ST.pop()
        x = t[0]
        y = t[1]

        if t not in s:
            s.append(t)

        # Рассматривается 8-связная область
        if x < len(mat) - 1 and abs(mat[x + 1][y] - mean) <= epsilon:
            if not ST.isInside((x + 1, y)) and not (x + 1, y) in s:
                ST.put((x + 1, y))

        if x < len(mat) - 1 and y < len(mat[0]) - 1 and abs(mat[x + 1][y + 1] - mean) <= epsilon:
            if not ST.isInside((x + 1, y + 1)) and not (x + 1, y + 1) in s:
                ST.put((x + 1, y + 1))

        if y < len(mat[0]) - 1 and abs(mat[x][y + 1] - mean) <= epsilon:
            if not ST.isInside((x, y + 1)) and not (x, y + 1) in s:
                ST.put((x, y + 1))

        if x > 0 and y < len(mat[0]) - 1 and abs(mat[x - 1][y + 1] - mean) <= epsilon:
            if not ST.isInside((x - 1, y + 1)) and not (x - 1, y + 1) in s:
                ST.put((x - 1, y + 1))

        if x > 0 and abs(mat[x - 1][y] - mean) <= epsilon:
            if not ST.isInside((x - 1, y)) and not (x - 1, y) in s:
                ST.put((x - 1, y))

        if x > 0 and y > 0 and abs(mat[x - 1][y - 1] - mean) <= epsilon:
            if not ST.isInside((x - 1, y - 1)) and not (x - 1, y - 1) in s:
                ST.put((x - 1, y - 1))

        if y > 0 and abs(mat[x][y - 1] - mean) <= epsilon:
            if not ST.isInside((x, y - 1)) and not (x, y - 1) in s:
                ST.put((x, y - 1))

        if x < len(mat) - 1 and y > 0 and abs(mat[x + 1][y - 1] - mean) <= epsilon:
            if not ST.isInside((x + 1, y - 1)) and not (x + 1, y - 1) in s:
                ST.put((x + 1, y - 1))

    return s


def saveImage(image, s, outputfile):
    image.load()
    putpixel = image.im.putpixel

    for i in range(image.size[1]):
        for j in range(image.size[0]):
            if (i, j) not in s:
                putpixel((j, i), 20)
            else:
                putpixel((j, i), 250)

    image.thumbnail((image.size[0], image.size[1]), Image.ANTIALIAS)
    image.save(outputfile + ".jpeg", "JPEG")