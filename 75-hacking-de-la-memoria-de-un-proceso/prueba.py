from sys import argv, exit

def read_write_heap(pid, read_str, write_str):
    """
        Find @read_str in the heap of @pid and replace it with @write_str
        esta funcion va a buscar una cadena de texto en memoria, en este caso en el heap y va a sustituirla por una cadena de texto que le proporcionemos
    """
    try:
        maps_file = open("/proc/{}/maps".format(pid), 'r')
    except IOError as e:
        print("Can't open file /proc/{}/maps: IOError: {}".format(pid, e))
        exit(1)
    heap_info = None
    for line in maps_file:
        if 'heap' in line:
                heap_info = line.split() # linea que hace referencia al heap
                # heap_info = ["62e42869c000-62e42948d000", "rw-p", "00000000", "00:00 0", "[heap]"]
    maps_file.close()
    if heap_info is None:
        print('No heap found!')
        exit(1)
    addr = heap_info[0].split('-') # addr = ["62e42869c000", "62e42948d000"]
    perms = heap_info[1] # perms = "rw-p"
    if 'r' not in perms or 'w' not in perms:
        print('Heap does not have read and/or write permission')
        exit(0)

    # abro el fichero /proc/12013/mem
    try:
        mem_file = open("/proc/{}/mem".format(pid), 'rb+')
    except IOError as e:
        print("Can't open file /proc/{}/maps: IOError: {}".format(pid, e))
        exit(1)
    
    # convierto la direccion de comienzo del heap (62e42869c000 en hexadecimal) a su equivalente en decimal
    heap_start = int(addr[0], 16) # 108732070084608
    
    # convierto la direccion de final del heap (62e42869c000 en hexadecimal) a su equivalente en decimal
    heap_end = int(addr[1], 16) # 108732084703232

    # mem_file.seek(108732070084608)
    # dentro de /proc/12013/mem, posiciono el cursor a la posicion de memoria donde empieza el heap
    # es decir, ahora voy a empezar a leer desde donde comienza el heap y donde probablemente se encuentre esa informacion que tiene emacs ahora mismo escrita en el editor ("este es un texto de pruebas escrito por santi")
    mem_file.seek(heap_start)

    # heap = mem_file.read(108732084703232 - 108732070084608)
    # heap = mem_file.read(14618624)
    # con el cursor ya posicionado en la posicion de memoria 108732070084608, que es donde comienza el heap, leo la porcion de texto que nos interesa ("este es un texto de pruebas escrito por santi"), es decir, las proximas 14618624 posiciones de memoria, es decir, leo hasta el final del de la estructura en memoria RAM heap
    heap = mem_file.read(heap_end - heap_start)
    # en este punto, en esta variable "heap", ya tenemos toda la informacion que contiene el heap (estructura de la memora RAM)

    # aca buscamos el substring almacenado en el parametro read_str en el contenido de heap
    str_offset = heap.find(bytes(read_str, "ASCII"))
    # en esta variable almacenamos el offset, es decir, 
    # str_offset = heap.find(read_str) -> hice pruebas locales, y esto retorinaria la posicion del primer caracter de read_str en heap (suponiendo que heap es un string). 
    # bytes(read_str, "ASCII") -> este codigo crea una secuencia de bytes a partir de una cadena de texto read_str utilizando la codificación ASCII (ChatGTP)

    # validamos si se encontro el string buscado en la porcion de memoria de la estructura heap dentro de la RAM
    if str_offset < 0:
        print("Can't find {} in /proc/{}/mem".format(read_str, pid))
        exit(1)

    # posiciono el cursor donde empieza la cadena de texto hallada
    mem_file.seek(heap_start + str_offset)

    diff = len(read_str) - len(write_str) + 1
    
    if diff > 0:
        write_str += ' '*diff
    mem_file.write(bytes(write_str, "ASCII"))


linea_original_heap = "62e42869c000-62e42948d000 rw-p 00000000 00:00 0                          [heap]"

heap_info = linea_original_heap.split() # ['62e42869c000-62e42948d000', 'rw-p', '00000000', '00:00', '0', '[heap]']
addr = heap_info[0].split('-') # ['62e42869c000', '62e42948d000']
perms = heap_info[1] # perms = "rw-p"
heap_start = int(addr[0], 16)
heap_end = int(addr[1], 16)


# print(heap_info)
# print(addr)
# print(addr[1])
# print(perms)
# print("------")
# print(addr[0])
# print(heap_start)
# print("------")
# print(addr[1])
# print(heap_end)

# 108732070084608 | 1087320 70084608
# 108732084703232 | 1087320 84703232
# 108732084703232 - 108732070084608 = 14618624

read_str = "hola"
write_str = ""
print(write_str)

diff = len(read_str) - len(write_str) + 1
print(diff)

if diff > 0:
    write_str += 'x'*diff
print(write_str)
