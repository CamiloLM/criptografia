import numpy as np

# Especificacion del alfabeto
alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
# alphabet = generate_alphabet("alfabeto.txt", separator="")

# Diccionarios para facil transformación del alfabeto a su equivalente númerico
alphabetical_decimal = {char: i for i, char in enumerate(alphabet)}
decimal_alphabetical = {i: char for char, i in alphabetical_decimal.items()}

modulus = len(alphabet)


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


def hill_encrypt(plain_message, matrix):
    """
    Cifra un mensaje usando el cifrado Hill. Si el mensaje no tiene el mismo tamaño
    que la matriz, se usa X para completar el mensaje.
    Argumentos:
    plain_message (str): El mensaje a cifrar.
    matrix (np.array): La matriz de transformación para el cifrado afín.
    Regresa:
    str: El mensaje cifrado.
    """
    plain_message = plain_message.upper()
    # Verificar que el mensaje contenga solo caracteres válidos
    if not all(c in alphabetical_decimal for c in plain_message):
        raise ValueError("El mensaje contiene caracteres no válidos.")
    size = matrix.shape[0]
    encrypted_message = []
    # Asegurarse de que el mensaje tenga el tamaño adecuado
    while len(plain_message) % size != 0:
        plain_message += "X"  # Agregar 'X' para completar el mensaje
    # Recorrer el mensaje en bloques del tamaño de la matriz
    for i in range(0, len(plain_message), size):
        block = plain_message[i : i + size]
        # Multiplicar el bloque por la matriz
        block_vector = np.array([alphabetical_decimal[char] for char in block])
        encrypted_vector = block_vector @ matrix % modulus
        # Convertir el vector cifrado de nuevo a caracteres
        encrypted_block = [decimal_alphabetical[int(num)] for num in encrypted_vector]
        # Agregar los caracteres cifrados al mensaje cifrado
        encrypted_message.extend(encrypted_block)
    return "".join(encrypted_message)


def adjugate_matrix(matrix):
    """
    Calcula la matriz adjunta de una matriz dada en el contexto del cifrado Hill.
    Argumentos:
    matrix (np.array): La matriz para la cual se calculará la adjunta.
    Regresa:
    np.array: La matriz adjunta.
    """
    # Calcular la matriz de cofactores
    cofactor_matrix = np.zeros(matrix.shape, dtype=int)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            minor = np.delete(np.delete(matrix, i, axis=0), j, axis=1)
            cofactor_matrix[i, j] = (
                ((-1) ** (i + j)) * int(round(np.linalg.det(minor))) % modulus
            )
    # Transponer la matriz de cofactores para obtener la adjunta
    return cofactor_matrix.T % modulus


def inverse_matrix(matrix):
    """
    Calcula la matriz inversa de una matriz dada en el contexto del cifrado Hill.
    Argumentos:
    matrix (np.array): La matriz a invertir.
    Regresa:
    np.array: La matriz inversa.
    """
    det = int(round(np.linalg.det(matrix)))  # Determinante de la matriz
    # Asegurarse que la matriz sea invertible
    if det % modulus == 0:
        raise ValueError("La matriz no es invertible.")
    # Inverso del determinante módulo el tamaño del alfabeto
    det_inv = pow(det, -1, modulus)
    # Asegurarse de que el determinante sea invertible
    if det_inv is None:
        raise ValueError(f"El determinante no tiene inverso en el módulo {modulus}.")
    matrix_mod_inv = det_inv * adjugate_matrix(matrix) % modulus
    return matrix_mod_inv


def hill_decrypt(encrypted_message, matrix):
    """
    Descifra un mensaje usando el cifrado Hill. Si el mensaje no tiene el mismo tamaño
    que la matriz, se usa X para completar el mensaje.
    Argumentos:
    plain_message (str): El mensaje a cifrar.
    matrix (np.array): La matriz de transformación para el cifrado afín.
    Regresa:
    str: El mensaje cifrado.
    """
    encrypted_message = encrypted_message.upper()
    # Verificar que el mensaje contenga solo caracteres válidos
    if not all(c in alphabetical_decimal for c in encrypted_message):
        raise ValueError("El mensaje contiene caracteres no válidos.")
    #  Calcular la matriz inversa
    inv_matrix = inverse_matrix(matrix)
    size = inv_matrix.shape[0]
    decrypted_message = []
    # Recorrer el mensaje en bloques del tamaño de la matriz
    for i in range(0, len(encrypted_message), size):
        block = encrypted_message[i : i + size]
        # Multiplicar el bloque por la matriz inversa
        block_vector = np.array([alphabetical_decimal[char] for char in block])
        decrypted_vector = block_vector @ inv_matrix % modulus
        # Convertir el vector cifrado de nuevo a caracteres
        decrypted_block = [decimal_alphabetical[int(num)] for num in decrypted_vector]
        # Agregar los caracteres cifrados al mensaje cifrado
        decrypted_message.extend(decrypted_block)
    return "".join(decrypted_message)


A = np.array([[17, 17, 5], [21, 18, 21], [2, 2, 19]])  # Matriz de transformación|
encrypted = hill_encrypt("PAYMOREMONEY", A)
print(f"Mensaje cifrado: {encrypted}")
decrypted = hill_decrypt(encrypted, A)
print(f"Mensaje descifrado: {decrypted}")
