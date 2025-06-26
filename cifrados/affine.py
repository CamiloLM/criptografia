from itertools import permutations
from math import gcd

# Especificacion del alfabeto
alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
# alphabet = generate_alphabet("alfabeto.txt", separator="")

# Diccionarios para facil transformación del alfabeto a su equivalente númerico
alphabetical_decimal = {char: i for i, char in enumerate(alphabet)}
decimal_alphabetical = {i: char for char, i in alphabetical_decimal.items()}

modulus = len(alphabet)

# Lista de caracteres comunes en inglés y español usando alfabeto estandar
english_common = "ETAO"
spanish_common = "EAOS"

# Lista de inversos multiplicativos para el cifrado afín
inverses = {pow(i, -1, modulus) for i in range(26) if gcd(i, modulus) == 1}


def generate_alphabet(filename, separator=None):
    """
    Extrae los caracteres de un archivo de texto y los devuelve como una lista,
    en orden para hacer un alfabeto extendido. Permite definir un separador del contenido.
    Argumentos:
    filename (str): El nombre del archivo de texto desde donde se extraerán los caracteres.
    separator (str, optional): El separador que se usa en el archivo, por defecto es None si no hay separador.
    Regresa:
    list: Una lista con los caracteres válidos que pueden usarse como alfabeto.
    """
    try:
        # Abrir el archivo y leer su contenido
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()  # Se almacena el contenido del archivo

        # Si hay un separador, separar el contenido
        if separator:
            content = content.split(separator)
        # Si no hay separador, tomar todos los caracteres
        else:
            content = list(content)

        seen = set()  # Almacena los elementos ya vistos
        characters = []  # Almacena los caracteres
        # Se lee el archivo y se almacenan los caracteres en orden
        for char in content:
            if char not in seen:
                characters.append(char)
                seen.add(char)
        # Regresa los caracteres para el diccionario extendido
        return characters
    # Excepcion por si no se encuentra el archivo
    except FileNotFoundError:
        print(f"El archivo {filename} no se encontró.")
        return []


def affine_encrypt(message, a, b):
    """
    Cifra un mensaje usando el cifrado afín.
    Argumentos:
    message (str): El mensaje a cifrar.
    a (int): El multiplicador del cifrado afín.
    b (int): El desplazamiento del cifrado afín.
    Regresa:
    str: El mensaje cifrado.
    """
    encrypted_message = []
    for char in message.upper():
        if char in alphabetical_decimal:
            x = alphabetical_decimal[char]
            encrypted_char = decimal_alphabetical[(a * x + b) % modulus]
            encrypted_message.append(encrypted_char)
        else:
            print(f"Carácter '{char}' no está en el alfabeto.")
    return "".join(encrypted_message)


def affine_decrypt(encrypted_message, a, b):
    """
    Descifra un mensaje cifrado usando el cifrado afín.
    Argumentos:
    encrypted_message (str): El mensaje cifrado a descifrar.
    a (int): El multiplicador del cifrado afín.
    b (int): El desplazamiento del cifrado afín.
    Regresa:
    str: El mensaje descifrado.
    """
    # Calcular el inverso multiplicativo de 'a' módulo 'modulus'
    a_inv = pow(a, -1, modulus)
    decrypted_message = []
    for char in encrypted_message.upper():
        if char in alphabetical_decimal:
            y = alphabetical_decimal[char]
            decrypted_char = decimal_alphabetical[(a_inv * (y - b)) % modulus]
            decrypted_message.append(decrypted_char)
        else:
            print(f"Carácter '{char}' no está en el alfabeto.")
    return "".join(decrypted_message)


def frequency_analysis(message):
    """
    Realiza un análisis de frecuencia del mensaje.
    Argumentos:
    message (str): El mensaje a analizar.
    Regresa:
    str: Una cadena que representa la frecuencia de cada carácter en el mensaje.
    """
    frequency = {}
    for char in message.upper():
        if char in alphabetical_decimal:
            frequency[char] = frequency.get(char, 0) + 1
        else:
            print(f"Carácter '{char}' no está en el alfabeto.")
    # Crea una lista de tuplas de los caracteres ordenados con su frencuencia
    sorted_frequency = sorted(frequency.items(), key=lambda item: item[1], reverse=True)
    return "".join([char[0] for char in sorted_frequency])


def solve_affine_equations(equation1, equation2):
    """
    Resuelve un sistema de ecuaciones lineales para encontrar los valores de 'a' y 'b'
    en el cifrado afín, donde la ecuacion es de la forma: y = ax + b (mod m).
    Argumentos:
    equation1 (tuple): Primera ecuación en forma (x, y).
    equation2 (tuple): Segunda ecuación en forma (x, y).
    Regresa:
    tuple: Una tupla con los valores de 'a' y 'b'.
    """
    x1, y1 = equation1
    x2, y2 = equation2
    # Calcular el inverso multiplicativo de (x2 - x1) mod m
    try:
        inv = pow(x2 - x1, -1, modulus)
        # Calcular 'a'
        a = ((y2 - y1) * inv) % modulus
        # Calcular 'b'
        b = (y1 - a * x1) % modulus
        return a, b
    except ValueError:
        return None, None


def mapping(cipher_freq, plain_freq):
    """
    Mapea los caracteres mas frecuentes del texto cifrado a los del texto plano.
    Argumentos:
    cipher_text (str): Los caracteres más comunes del texto cifrado.
    plain_text (str): Los caracteres más comunes del texto plano.
    Regresa:
    list: Una lista que contiene las parejas de caracteres mapeados.
    """
    # Todas las permutaciones posibles de 2 caracteres
    cipher_pairs = list(permutations(cipher_freq, 2))
    plain_pairs = list(permutations(plain_freq, 2))
    unique_mappings = set()
    for c_pair in cipher_pairs:
        for p_pair in plain_pairs:
            mapping = frozenset(zip(c_pair, p_pair))  # Evitar duplicados
            unique_mappings.add(mapping)
    # Convertir a listas ordenadas por la letra cifrada
    result = []
    for mapping in unique_mappings:
        ordered = sorted(mapping, key=lambda pair: pair[0])  # ordena por letra cifrada
        result.append(ordered)
    return result


def affine_solver(cipher_text, common_language):
    """
    Resuelve el cifrado afín dado un texto cifrado.
    Argumentos:
    cipher_text (str): El texto cifrado a resolver.
    common_language (str): El idioma que se cree se usó para cifrar el texto.
    Regresa:
    list: Una lista de posibles soluciones (pares de 'a' y 'b').
    """
    solutions = []
    # Realizar análisis de frecuencia del texto cifrado
    freq = frequency_analysis(cipher_text)
    # Mapeo de caracteres más frecuentes, por defeco usando los 4 más comunes
    mappings = mapping(freq[:4], common_language[:4])
    print(freq[:4], common_language[:4])
    for m in mappings:
        x1, y1 = alphabetical_decimal[m[0][0]], alphabetical_decimal[m[0][1]]
        x2, y2 = alphabetical_decimal[m[1][0]], alphabetical_decimal[m[1][1]]
        a, b = solve_affine_equations((x1, y1), (x2, y2))
        if m == [("E", "E"), ("Y", "S")]:
            print(m)
            print(x1, y1)
            print(x2, y2)
            print(a, b)
            print()
        # Verifica que la ecuacuión tenga solución
        if a is not None and b is not None:
            # Verificar que 'a' y 'b' sean válidos
            if a in inverses and 0 <= b < modulus:
                solutions.append((a, b))
    return solutions


lm = """
BWYYEREYZMICPWYPEQEYGFCIWYEYDERCPVCCIWROYWBMQGWPEYCTEQEYEBEYLMERVWPWWJFGEPEREYMBFCXWYGPIEXGCFWYDERWQWPQWPYFCPQGCODCYGWPDWXEIWYCBQCPVCRPMEYFRWYYMEPWY
"""
lm = lm.replace("\n", "")

# Solution a = 7 and b = 2
# posible = affine_solver(lm, spanish_common)
# for a, b in posible:
#     decrypted = affine_decrypt(lm, a, b)
#     print(f"a: {a}, b: {b} -> {decrypted[:50]}...")

print(solve_affine_equations((4, 4), (24, 18)))
