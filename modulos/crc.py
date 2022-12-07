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

def xor(a, b):
    resultado = []
    for i in range(1, len(b)):
        if a[i] == b[i]:
            resultado.append('0')
        else:
            resultado.append('1')
    #convertir a str
    return ''.join(resultado)

def mod2div(divident:bitarray, divisor:bitarray)-> bitarray:
    divident = divident.to01()
    divisor = divisor.to01()
    # Number of bits to be XORed at a time.
    div_longitud = len(divisor)
    # el dividendo debe tener una longitud igual al divisor para poder realizar las operaciones, entonces
    # lo hacemos mas chico
    tmp = divident[0 : div_longitud]
    while div_longitud < len(divident):
        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + divident[div_longitud]
        else: 
            #si tenenmos un cero al principio, significa que tenemos que multiplicar por  
            # puros ceros
            tmp = xor('0'*div_longitud, tmp) + divident[div_longitud]
        div_longitud += 1
    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0'*div_longitud, tmp)
    checkword = tmp
    #comprobacion(bitarray(divident),bitarray(checkword),bitarray(divisor))
    return bitarray(checkword)

def compute(filename: str, divisor: bitarray, len_crc: int) -> tuple[bitarray, bitarray]:
	check_arr = bitarray(len_crc)
	check_arr.setall(0)
	file = open(filename, 'r')
	texto = file.read()
	characters = len(texto)
	print(f"Characters: {characters}")
	#print(f"Texto original: {texto}")
	bin_texto = (''.join(format(ord(x), 'b') for x in texto))
	#print(f"Texto en Bits: {bin_texto}")
	r = len_crc
	bin_texto_redundancia = bin_texto+('0'*r)
	residuo = mod2div(bitarray(bin_texto_redundancia),divisor)
	check = mod2div(bitarray(bin_texto)+residuo,divisor)
	print(f"Check: {check}")
	if check.to01() != check_arr.to01():
		print("Error")
	else:
		print(f"CRC: {residuo.to01()}")
		return [bitarray(bin_texto),bitarray(residuo)]