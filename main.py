""" Параллельный алгоритм сегментации серого изорбражения расширением регионов """
""" (Region Growing Grayscale Image Segmentation)"""
""" Watershed algorithm"""
""" Input: исходное изображение"""
""" Output: изображение, состоящее из сегментов"""
""" Сайбель Т. А. 423 группа, 30.09.2021"""

import numpy as np
from mpi4py import MPI
from RegionGrowing import *

outputfile = 'images/res'
inputfile = 'images/input.jpg'

if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Время выполнения
    t = 0.0

    if rank == 0:

        image = Image.open(inputfile)
        mat = np.array(image.convert("L"), 'f')

        # Кластер, хранящий результат
        s = []

        if size != 1:
            for i in range(1, size):
                startPos = int(mat.shape[0] / (size - 1)) * (i - 1)
                endPos = mat.shape[0] if i == size - 1 else int(mat.shape[0] / (size - 1)) * i
                tmp = np.array(mat[startPos:endPos])
                comm.send(tmp, dest=i)

            for i in range(1, size):
                got = comm.recv(source=i)
                s.append(got)
                gotTime = comm.recv(source=i, tag=11)
                if gotTime > t:
                    t = gotTime

        else:
            t = MPI.Wtime()
            s = regionGrowing(mat, 20, 24, (0, 0))
            t = MPI.Wtime() - t

        # print('Time for {} processes: {} sec'.format(size - 1, t))
        print('{}\t{}'.format(size - 1, t))

        saveImage(image, s, outputfile)
    else:
        mat = comm.recv(source=0)
        t = MPI.Wtime()
        s = regionGrowing(mat, 20, 24, (0, 0))
        t = MPI.Wtime() - t
        comm.send(s, dest=0)
        comm.send(t, dest=0, tag=11)
