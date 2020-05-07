import sys
import pandas
import numpy as np
from plot_db import visualize_3d
import copy

def lr(df, iterations):
    beta=[0,0,0]
    output_weights=[]
    alphas = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 1.1]
    for column in df:
        mean=df.mean(axis=0)[column]
        std=df.std(axis=0)[column]
        for i in range(len(df)):
            df[column][i]= (df[column][i] - mean) / std

    for alpha in alphas:
        beta=[0,0,0]
        if alpha==1.1:
            iterations=120
        for i in range(iterations):
            r=0
            tem_beta=[0,0,0]
            xij1,xij2,xij3=0,0,0
            for j,row in df.iterrows():
                difference=beta[0]+beta[1]*row[0]+beta[2]*row[1]-row[2]
                r+=difference**2
                xij1+=difference
                xij2+=difference*row[0]
                xij3+=difference*row[1]
            R=r/(2 * len(df))
            beta[0]-= (alpha / len(df)) * xij1
            beta[1] -= (alpha / len(df)) * xij2
            beta[2] -= (alpha / len(df)) * xij3
        output_weights.append([alpha,iterations,beta[0],beta[1],beta[2]])
    return output_weights

if __name__=='__main__':
    input_file=sys.argv[1]
    input_data=pandas.read_csv(input_file,header=None)
    output_file=sys.argv[2]
    output_data = lr(input_data,100)
    write_file=open(output_file,'w')
    for data in output_data:
        visualize_3d(input_data,lin_reg_weights=data[2:],alpha=data[0])
        write_file.write(str(data[0])+','+str(data[1])+','+str(data[2])+','+str(data[3])+','+str(data[4])+'\n')
    write_file.close()