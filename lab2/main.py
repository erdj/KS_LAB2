import bitstring
from codecs import decode
import struct
import math

#Функції, які перетворюють float та int в список бітів(кожний біт з float буде відповідати кожному елементу зі списку
# Може список складатись як із False так і True
def str_to_bin(s):
	res = [i == '1' for i in list(s)]
	res.reverse()
	return res


def bin_to_str(b):
	br = list(b)
	br.reverse()
	return ''.join(['1' if i else '0' for i in br])


def float_to_bin(f):
	return str_to_bin(bitstring.BitArray(float=f, length=32).bin)


def int_to_bytes(n, length):
	return decode('%%0%dx' % (length << 1) % n, 'hex')[-length:]


def bin_to_float(b):
    bf = int_to_bytes(int(bin_to_str(b), 2), 4)
    return struct.unpack('>f', bf)[0]


def int_to_bin(i):
	return str_to_bin(bitstring.BitArray('i32=' + str(i)).bin)


def bin_to_int(b):
	return bitstring.BitArray(bin=bin_to_str(b)).int

#додавання
#Задаємо дві перемінні
def add(o1, o2):
#Результат записуємо нулями
	res = [False for i in o1]
#Булева змінна яка буде в собі містити чи переносимо ми на наступний біт 1 або ні
	carry = False
	for i in range(len(o1)):
#Розраховуємо теперішній розряд результата
		res[i] = (o1[i] != o2[i]) != carry
#Булева Змінна працює так якщо дві змінні буде 1 або якась із змінної буде 1 і булева змінна
		carry = o1[i] and o2[i] or o1[i] and carry or o2[i] and carry
#Повертаємо результат і булеву змінну
	return res, carry

#Інвертуємо число
def neg(o):
	res = [not i for i in o] #Інвертуємо всі біти
	one = [False for i in o]
	one[0] = True
	res, _ = add(res, one) #До інвертованого ходу додаю 1
	return res

#Віднімання
def sub(o1, o2):
	return add(o1, neg(o2))# До першої змінної додаю інвертовану другу змінну

# Здвиг вправо(кожному молодшому біту ми присвоюємо значення кожного старшого біту)
def shr(o):
	res = o[:]
	for i in range(len(res) - 1):
		res[i] = res[i + 1]
	res[-1] = False
	return res
# Здвиг вліво
def shl(o):
	res = o[:]
	res.reverse()
	res = shr(res)
	res.reverse()
	return res


def mul(o1, o2, signed=True):
#Копіюються операнди по 32 біти
	o1c = o1[:]
	o2c = o2[:]
	s = False # Кінцевий знак
#Якщо перше число від'ємне то кінцевий знак True, якщо і друге число від'ємне то кінцевий знак стане False
	if o1[len(o1) - 1] and signed:
		o1c = neg(o1c) # Інвертуємо значення якщо вони від'ємні
		s = not s
	if o2[len(o2) - 1] and signed:
		o2c = neg(o2c) # Інвертуємо значення якщо вони від'ємні
		s = not s

	res = [False for i in range(len(o1) + len(o2))] # результат буде складатись з 64 нулів

	for i in range(len(o1)):
		if o2c[0]:#Якщо молодший біт другої змінної = 1
			r, _ = add(o1c, res[len(o1):])# То треба додати
			res[len(o1):] = r
		o2c = shr(o2c)#Зсуваємо вправо
		res = shr(res)#Зсуваємо вправо
	return neg(res) if s and signed else res#Якщо знак False число додатнє то вертаємо число, якщо треба вертати негативне то вертаємо негативний результат

# Ділення
def div(o1, o2):
# Записуємо булеві змінні
	o1s = o1[31]# Знак першої змінної ( беремо останній біт)
	o2s = o2[31]# Знак першої змінної ( беремо останній біт)

	if o1s:
		o1 = neg(o1)
	if o2s:
		o2 = neg(o2)

	q = [False for i in range(32)]#Quotient розмір 32 біта, також весь заповнений 0
	r = [False for i in range(64)]# Залишок розмір 64 біта , також весь заповнений 0
	r[:32] = o1# в ділиме записали молодші 32 біти

	for i in range(32):# 32 рази ми здвигаємо вліво remainder і Quotient , робимо молодший біт
		r = shl(r)
		q = shl(q)

		r[32:], c = sub(r[32:], o2) # віднімаємо і зберігаємо булеву функцію carry(відбулося переповнення) , відняли 2 додатніх числа
		q[0] = c# Якщо результат вийшов від'ємним то друге число воно більше, то ми більше віднімати не зможем
		if not c: # Якщо результат від'ємний
			r[32:], _ = add(r[32:], o2)# Віднова числа, яке було до ціх дій
	#Визначення знаків для результату
	if o1s:
		r = neg(r)
	if o1s != o2s:
		q = neg(q)
	return bin_to_int(q), bin_to_int(r[32:])

#Вивід множення двійкових чисел(зсув результату ввправо )
#print(bin_to_int(mul(int_to_bin(-48), int_to_bin(11))))
#print(bin_to_int(mul(int_to_bin(-12), int_to_bin(3))))
#print(bin_to_int(mul(int_to_bin(-1112), int_to_bin(11))))

#Ділення двійкових чисел(Зсув залишку вправо)
print(('(Quotient, Remainder):'),div(int_to_bin(36), int_to_bin(17)))
print(('(Quotient, Remainder):'),div(int_to_bin(112), int_to_bin(4)))
print(('(Quotient, Remainder):'),div(int_to_bin(115), int_to_bin(3)))


