from modulos import crc
from modulos import divisionMod2
from modulos import burst_error
import sys
import matplotlib.pyplot as plt
from bitarray import bitarray

def main():
    # Program parameters
    filename = sys.argv[1]
    divisor = bitarray(sys.argv[2])
    crc_len = len(divisor)-1
    burst_size = int(sys.argv[3])
    seed = int(sys.argv[4])
    iter_max = int(sys.argv[5])
    print(f"""filename:{filename}
divisor:{divisor.to01()}
Bits de paridad: {crc_len}
Tamaño de burst error: {burst_size}
seed inicial: {seed}
Iteraciones: {iter_max}""")
    # Redundancy
    zero_rem = bitarray(crc_len)
    zero_rem.setall(0)
    counter = 0 # actual number of repetitions
    # Computes CRC
    msg, crc_code = crc.compute(filename, divisor, crc_len)
    print(f'CRC of text file "{filename}" equals {crc_code.to01()}')
    #print(f'MSG+CRC: {msg+crc_code}')
    # Evaluation of the CRC robustness
    probabilidad = []
    for i in range(0, iter_max):
        # Burst error generation
        corrupted_msg = burst_error.burst_err(msg + crc_code, burst_size, seed + i)
        # Computes remainder
        rem = divisionMod2.mod2div(corrupted_msg, divisor)
        #print(rem.to01())
        # Determines whether rem equals zero or not
        success = 1 if rem.to01() != zero_rem.to01() else 0
        # Compute the number of times the CRC detects the error
        counter += success
        probabilidad.append(counter/(i+1))
    print(f'Probabilidad detección/iteración = {probabilidad[-1]}')
    plt.plot([i for i in range(1, iter_max+1)], probabilidad, '-')
    plt.show()

if __name__ == '__main__':
    main()