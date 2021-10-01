#!/bin/bash

for (( i=2; i <= 6; i++))
do
	mpirun -n $i python main.py >> report/res.dat
done
