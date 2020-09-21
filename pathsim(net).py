import numpy as np
import scipy.sparse as sp
import time
from decimal import Decimal
# function to construct a single matrix
def construct_matrix(filename, m1, m2):
    matrix = np.zeros((m1, m2), dtype = np.float)   
    #print(matrix)
    with open(filename, "r") as f:
        for line in f:
            entry = [i for i in line.split()]
            entry[0]=int(entry[0])
            entry[1]=int(entry[1])
            #print(entry[0])
            #print(entry[1])
            #print(entry[2])
            matrix[entry[0]-1][entry[1]-1] = entry[2]
    #out = sp.csc_matrix(matrix)
    out = sp.csc_matrix(matrix)
    return out, sp.csc_matrix.transpose(out)

# the algorithm
def PathSim(x, m, k, num):
    """ # this is significantly slower
    candidates = set()
    for i in matrix.getrow(x-1).indices:
        for j in matrix.getrow(i-1).indices:
            candidates.add(j)
    """     
    out = []
    
    for i in range(num):
        value = 2.0 * m[x-1,i] / (m[x-1,x-1] + m[i,i])
        out.append((value, i+1))
        
    out.sort()
    out.reverse()
    return out[:k]

# find how many of these items
def find_max():
    vul,device,attack,OS,port,service = 0,0,0,0,0,0
    with open("./data/VD.txt", "r") as f1:
        for line in f1:
            entry = line.split()
            device = max(device, int(entry[0]))
            vul = max(vul, int(entry[1]))
            
    with open("./data/VA.txt", "r") as f2:
        for line in f2:
            entry = line.split()
            vul = max(vul, int(entry[0]))
            attack = max(attack, int(entry[1]))
            
    with open("./data/DO.txt", "r") as f3:
        for line in f3:
            entry = line.split()
            device = max(device, int(entry[0]))
            OS = max(OS, int(entry[1]))
    with open("./data/DP.txt", "r") as f3:
        for line in f3:
            entry = line.split()
            device = max(device, int(entry[0]))
            port = max(port, int(entry[1]))
    with open("./data/PS.txt", "r") as f3:
        for line in f3:
            entry = line.split()
            port = max(port, int(entry[0]))
            service = max(service, int(entry[1]))
       
    return vul, device, attack, OS, port, service

def get_initial():
    start = time.time()  
    m = find_max()
    #print(m[0],' ',m[1],' ',m[2])
    #PA, AP = construct_matrix("./data/PA.txt", m[1], m[0])
    VD, DV = construct_matrix("./data/VD.txt", m[0], m[1])
    #print(VD)
    #print('aaaaaaa')
    #print(DV)
    VA, AV = construct_matrix("./data/VA.txt", m[0], m[2])
    DO, OD = construct_matrix("./data/DO.txt", m[1], m[3])
    DP, PD = construct_matrix("./data/DP.txt", m[1], m[4])
    PS, SP = construct_matrix("./data/PS.txt", m[4], m[5])
    #PC, CP = construct_matrix("./data/PC.txt", m[1], m[2])
    #PT, TP = construct_matrix("./data/PT.txt", m[1], m[3])
    DVD =(DV*VD).todense()
    DVAVD = (DV*VA*AV*VD).todense()
    DOD = (DO*OD).todense()
    DPD = (DP*PD).todense()
    DPSPD = (DP*PS*SP*PD).todense()
    #APTPA = (AP * PT * TP * PA).todense()   
    mid = time.time()
    
    result_1=PathSim(20,DVD,20,m[1])
    result0=PathSim(20, DVAVD, 20, m[1])
    result1=PathSim(20,DOD,20,m[1])
    result2=PathSim(20,DPD,20,m[1])
    result3=PathSim(20,DPSPD,20,m[1])
    #print(result0)
    #result=result0[0]+result1[0]+result2[0]+result3[0]
    result=[0 for i in range(len(result0))]
    print(result)
    for i in range(len(result0)):
        result[result0[i][1]-1]+=result0[i][0]
        print(result0[i][1])
        result[result1[i][1]-1]+=result1[i][0]
        result[result2[i][1]-1]+=result2[i][0]
        result[result3[i][1]-1]+=result3[i][0]
        result[result_1[i][1]-1]+=result_1[i][0]
    print(result)
    print(result0)
    final_result=[]
    final_result0=[]
    final_result1=[]
    final_result2=[]
    final_result3=[]
    final_result_1=[]
    for i in range(len(result)):
        final_result.append((result[i],i))
        final_result0.append((result0[i][0],result0[i][1]-1))
        final_result1.append((result1[i][0],result1[i][1]-1))
        final_result2.append((result2[i][0],result2[i][1]-1))
        final_result3.append((result3[i][0],result3[i][1]-1))
        final_result_1.append((result_1[i][0],result_1[i][1]-1))
    final_result.sort()
    #final_result0.sort()
    #final_result1.sort()
    #final_result2.sort()
    #final_result3.sort()
    final_result.reverse()
    #final_result0.reverse()
    #final_result1.reverse()
    #final_result2.reverse()
    #final_result3.reverse()
    '''for i in range(len(result0)):
        print(result0[i],' ',i)
    print('result1:')
    for i in range(len(result1)):
        print(result1[i],' ',i)
    print('result2:')
    for i in range(len(result2)):
        print(result2[i],' ',i)
    print('result3:')
    for i in range(len(result3)):
        print(result3[i],' ',i)
    '''
    print('final_result:')
    s=0
    s0=0
    s1=0
    s2=0
    s3=0
    s_1=0
    for i in range(len(result)):
        print(final_result[i])
        if i!=0:
            s+=final_result[i][0]
            s0+=final_result0[i][0]
            s1+=final_result1[i][0]
            s2+=final_result2[i][0]
            s3+=final_result3[i][0]
            s_1+=final_result_1[i][0]
        
    f=open('initial_value.txt','w+')
    f_nor=open('initial_value_nor.txt','w+')
    f_tex=open('table_tex.txt','w+')
    
    #SUM
    f.write('SUM:')
    f.write('\n')
    f_nor.write('SUM'+'\n')
    for i in range(len(final_result)-1):
        f.write(str(final_result[i][0]))
        f.write(' ')
        f.write(str(final_result[i][1]))
        f.write('\n')
        if i!=0:
            f_nor.write(str(final_result[i][0]/s)+' '+str(final_result[i][1])+'\n')
    f_nor.write(str(final_result[19][0]/s)+' '+str(final_result[19][1])+'\n')
    f.write(str(final_result[19][0]))
    f.write(' ')
    f.write(str(final_result[19][1]))
    f.write('\n')

    #Normalized
    #f.write('Normalized:')
    #f.write('\n')

    #DVD
    f.write('DVD:')
    f.write('\n')
    f_nor.write('DVD'+'\n')
    for i in range(len(final_result)-1):
        f.write(str(final_result_1[i][0]))
        f.write(' ')
        f.write(str(final_result_1[i][1]))
        f.write('\n')
        if i!=0:
            f_nor.write(str(final_result_1[i][0]/s_1)+' '+str(final_result_1[i][1])+'\n')
    f_nor.write(str(final_result_1[19][0]/s_1)+' '+str(final_result_1[19][1])+'\n')
    f.write(str(final_result_1[19][0]))
    f.write(' ')
    f.write(str(final_result_1[19][1]))
    f.write('\n')

    #DVAVD
    f.write("DVAVD:")
    f.write('\n')
    f_nor.write('DVAVD'+'\n')
    for i in range(len(final_result)-1):
        f.write(str(final_result0[i][0]))
        f.write(' ')
        f.write(str(final_result0[i][1]))
        f.write('\n')
        if i!=0:
            f_nor.write(str(final_result0[i][0]/s0)+' '+str(final_result0[i][1])+'\n')
    f_nor.write(str(final_result0[19][0]/s0)+' '+str(final_result0[19][1])+'\n')
    f.write(str(final_result0[19][0]))
    f.write(' ')
    f.write(str(final_result0[19][1]))
    f.write('\n')

    #DOD
    f.write("DOD:")
    f.write('\n')
    f_nor.write('DOD'+'\n')
    for i in range(len(final_result)-1):
        f.write(str(final_result1[i][0]))
        f.write(' ')
        f.write(str(final_result1[i][1]))
        f.write('\n')
        if i!=0:
            f_nor.write(str(final_result1[i][0]/s1)+' '+str(final_result1[i][1])+'\n')
    f_nor.write(str(final_result1[19][0]/s1)+' '+str(final_result1[19][1])+'\n')
    f.write(str(final_result1[19][0]))
    f.write(' ')
    f.write(str(final_result1[19][1]))
    f.write('\n')

    #DPD
    f.write("DPD:")
    f.write('\n')
    f_nor.write('DPD'+'\n')
    for i in range(len(final_result)-1):
        f.write(str(final_result2[i][0]))
        f.write(' ')
        f.write(str(final_result2[i][1]))
        f.write('\n')
        if i!=0:
            f_nor.write(str(final_result2[i][0]/s2)+' '+str(final_result2[i][1])+'\n')
    f_nor.write(str(final_result2[19][0]/s2)+' '+str(final_result2[19][1])+'\n')
    f.write(str(final_result2[19][0]))
    f.write(' ')
    f.write(str(final_result2[19][1]))
    f.write('\n')

    #DPSPD
    f.write("DPSPD:")
    f.write('\n')
    f_nor.write('DPSPD'+'\n')
    for i in range(len(final_result)-1):
        f.write(str(final_result3[i][0]))
        f.write(' ')
        f.write(str(final_result3[i][1]))
        f.write('\n')
        if i!=0:
            f_nor.write(str(final_result3[i][0]/s3)+' '+str(final_result3[i][1])+'\n')
    f_nor.write(str(final_result3[19][0]/s3)+' '+str(final_result3[19][1])+'\n')
    f.write(str(final_result3[19][0]))
    f.write(' ')
    f.write(str(final_result3[19][1]))

    for i in range(len(final_result)-1):
        if i!=0:
            #print(i)
            f_tex.write(str(i)+' '+'&'+' '+str(round(final_result_1[i][0],6))+' '+'&'+' '+str(round(final_result_1[i][1]+1,6))+' '+'&'+' '+str(round(final_result_1[i][0]/s_1,6))+' '+'&'+' '+str(round(final_result0[i][0],6))+' '+'&'+' '+str(round(final_result0[i][1]+1,6))+' '+'&'+' '+str(round(final_result0[i][0]/s0,6))+\
            ' '+'&'+' '+str(round(final_result2[i][0],6))+' '+'&'+' '+str(round(final_result2[i][1]+1,6))+' '+'&'+' '+str(round(final_result2[i][0]/s2,6))+\
            ' '+'&'+' '+str(round(final_result[i][0],6))+' '+'&'+' '+str(round(final_result[i][1]+1,6))+' '+'&'+' '+str(round(final_result[i][0]/s,6))+' '+'\\'+'\\'+' '+'\hline'+'\n')
            #print('sdfsdfsdf')
    f_tex.write(str(i+1)+' '+'&'+' '+str(round(final_result_1[19][0],6))+' '+'&'+' '+str(round(final_result_1[19][1]+1,6))+' '+'&'+' '+str(round(final_result_1[19][0]/s_1,6))+' '+'&'+' '+str(round(final_result0[19][0],6))+' '+'&'+' '+str(round(final_result0[19][1]+1,6))+' '+'&'+' '+str(round(final_result0[19][0]/s0,6))+\
            ' '+'&'+' '+str(round(final_result2[19][0],6))+' '+'&'+' '+str(round(final_result2[19][1]+1,6))+' '+'&'+' '+str(round(final_result2[19][0]/s2,6))+\
            ' '+'&'+' '+str(round(final_result[19][0],6))+' '+'&'+' '+str(round(final_result[19][1]+1,6))+' '+'&'+' '+str(round(final_result[19][0]/s,6))+' '+'\\'+'\\'+' '+'\hline')   
    f_tex.close()
    f.close()
    f_nor.close()
    #print(PathSim(7696, APTPA, 5, m[0]))
    end = time.time()
    print ("\nTime:\ngenerate Mp:", mid - start, "\tPathSim:", end - mid)

if __name__ == "__main__":
    get_initial()
    
    """ cnt = {} # check if answer make sense
    with open("./data/PA.txt") as f:
        for line in f:
            author = int(line.split()[1])
            if author not in cnt:
                cnt[author] = 1
            else:
                cnt[author] += 1
    print [(i,cnt[i]) for i in cnt if cnt[i] > 80]
    """