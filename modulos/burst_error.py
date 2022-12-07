from bitarray import bitarray
import random

def burst_err(msg:bitarray,n:int,seed:int)->bitarray:
    orig_msg = msg.copy()
    #print(f"Original msg: {orig_msg} len: {len(orig_msg)}")
    random.seed(seed)
    inicio = random.randint(0,(len(msg)-n)-1)
    #print(f"Burst error lenght: {n}")
    if msg[inicio]==1:
        msg[inicio]=0
    else:
        msg[inicio]=1
    for i in range(inicio+1,(n+inicio)-1):
        invertir = random.randint(0,1)
        if invertir:
            if msg[i]==0:
                msg[i]=1
            else:
                msg[i]=0
    if msg[i+1]==0:
        msg[i+1]=1
    else:
        msg[i+1]=0
    #print(f"Corrupted msg: {msg} len: {len(msg)}")
    return bitarray(msg)
#"""
#TEST BENCH
if __name__=='__main__':
    rem = burst_err(bitarray('111111111111'),6,12)
    print(rem)
#"""
