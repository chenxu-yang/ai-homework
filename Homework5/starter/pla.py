import sys
import csv
import pandas
def pla(input_data,output_path):
    data=pandas.DataFrame(input_data)
    weights=[0,0,0]
    convergence=False
    weights_history=[]
    while not convergence:
        flag = 0
        for index,row in data.iterrows():
            f=weights[0]+weights[1]*row[0]+weights[2]*row[1]
            if row[2]*f<=0:
                flag=1
                weights[0]=weights[0]+row[2]
                weights[1] = weights[1] + row[2]*row[0]
                weights[2] = weights[2] + row[2] * row[1]
                weights_history.append(weights[:])
        if not flag:
            convergence=True
    write_file=open(output_path,'w')
    for data in weights_history:
        write_file.write(str(data[1])+','+str(data[2])+','+str(data[0])+'\n')
    write_file.close()



if __name__=="__main__":
    input_file=sys.argv[1]
    output_file = sys.argv[2]
    input_data=pandas.read_csv(input_file,header=None)
    pla(input_data,output_file)