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


def vigenere_encrypt(plaintext, key):
    """
    Cifra un texto plano usando el cifrado Vigenère.
    Argumentos:
    plaintext (str): El texto plano a cifrar.
    key (str): La clave para el cifrado.
    Regresa:
    str: El texto cifrado.
    """
    ciphertext = []
    key_length = len(key)
    for i, char in enumerate(plaintext):
        if char in alphabetical_decimal:
            # Encuentra el índice del carácter en el alfabeto
            p = alphabetical_decimal[char]
            # Encuentra el índice del carácter de la clave correspondiente
            k = alphabetical_decimal[key[i % key_length]]
            # Cifra el carácter
            encrypted_index = (p + k) % modulus
            ciphertext.append(decimal_alphabetical[encrypted_index])
        else:
            print("Carácter no válido en el texto plano:", char)
    return "".join(ciphertext)


def vigenere_decrypt(ciphertext, key):
    """
    Descifra un texto cifrado usando el cifrado Vigenère.
    Argumentos:
    ciphertext (str): El texto cifrado a descifrar.
    key (str): La clave para el descifrado.
    Regresa:
    str: El texto descifrado.
    """
    plaintext = []
    key_length = len(key)
    for i, char in enumerate(ciphertext):
        if char in alphabetical_decimal:
            # Encuentra el índice del carácter en el alfabeto
            c = alphabetical_decimal[char]
            # Encuentra el índice del carácter de la clave correspondiente
            k = alphabetical_decimal[key[i % key_length]]
            # Descifra el carácter
            decrypted_index = (c - k) % modulus
            plaintext.append(decimal_alphabetical[decrypted_index])
        else:
            print("Carácter no válido en el texto cifrado:", char)
    return "".join(plaintext)


encrypted = vigenere_encrypt("WEAREDISCOVEREDSAVEYOURSELF", "DECEPTIVE")
print(encrypted)
decrypted = vigenere_decrypt(encrypted, "DECEPTIVE")
print(decrypted)
