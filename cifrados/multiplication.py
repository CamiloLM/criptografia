from collections import Counter

# Se hace un listado del afabetico clasico de 26 letras
alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# Diccionarios para facil transformación del alfabeto a su equivalente númerico
alphabetical_decimal = {char: i for i, char in enumerate(alphabet)}
decimal_alphabetical = {i: char for char, i in alphabetical_decimal.items()}

# Se calcula el modulo para las operaciones de cifrado
module = len(alphabet)
common_letters = ['E', 'A', 'O']  # Letras más comunes del español


def from_alphabetical_to_decimal(string):
    """
    Convierte una cadena de texto al valor numérico correspondiente del alfabeto.
    Cada letra se convierte en su posición en el alfabeto (A=0, B=1, ..., Z=25).

    Argumentos:
    string (str): La cadena de texto a convertir.

    Retorna:
    list: Lista de números que representan las posiciones de las letras en el alfabeto.
    """
    return [
        alphabetical_decimal[char.upper()]
        for char in string
        if char.upper() in alphabetical_decimal
    ]


def from_decimal_to_alphabetical(numbers):
    """
    Convierte una lista de valores numéricos a sus correspondientes letras del alfabeto.
    Cada número en la lista se mapea a la letra correspondiente en el alfabeto (0=A, 1=B, ..., 25=Z).

    Argumentos:
    numbers (list): Lista de números que representan las posiciones de las letras en el alfabeto.

    Retorna:
    list: Lista de letras que corresponden a los valores numéricos proporcionados
    """
    return [decimal_alphabetical[num] for num in numbers]


def displacement_encrypt(string, displacement):
    """
    Cifra una cadena de texto usando el cifrado por desplazamiento

    Argumentos:
    string (str): Texto a cifrar.

    Retorna:
    str: Texto cifrado.
    """
    # Convierte el texto a sus valores numéricos correspondientes
    numerical_value = from_alphabetical_to_decimal(string)
    cipher_values = []  # Lista para almacenar los valores cifrados

    # Itera sobre los valores numéricos y aplica el desplazamiento
    for i in numerical_value:
        cipher_values.append((i + displacement) % module)  # Desplazamiento

    # Convierte los valores numéricos cifrados de nuevo a letras y devuelve el texto cifrado
    return "".join(from_decimal_to_alphabetical(cipher_values))


def displacement_decrypt(string, displacement):
    """
    Descifra una cadena de texto utilizando el cifrado por desplazamiento

    Paramteros:
    string (str): Texto a descifrar.

    Retorna:
    str: Texto descifrado.
    """
    # Convierte el texto cifrado a sus valores numéricos correspondientes
    numerical_value = from_alphabetical_to_decimal(string)
    decrypted_values = []  # Lista para almacenar los valores numéricos descifrados

    # Itera sobre los valores numéricos y aplica el desplazamiento inverso
    for i in numerical_value:
        decrypted_values.append((i - displacement) % module)  # Desplazamiento inverso

    # Convierte los valores numéricos descifrados de nuevo a letras y devuelve el texto descifrado
    return "".join(from_decimal_to_alphabetical(decrypted_values))


def multiplicative_encrypt(text, key):
    """
    Cifra un texto utilizando el cifrado multiplicativo.

    Parámetros:
    text (str): Texto a cifrar.
    key (int): Clave de cifrado (debe ser coprima con 26).

    Retorna:
    str: Texto cifrado.
    """

    numbers = from_alphabetical_to_decimal(text)
    encrypted = [(n * key) % module for n in numbers]
    return "".join(from_decimal_to_alphabetical(encrypted))


def multiplicative_decrypt(ciphertext, key):
    """
    Descifra un texto cifrado con cifrado multiplicativo.

    Parámetros:
    ciphertext (str): Texto cifrado.
    key (int): Clave usada para cifrar (debe ser la misma).

    Retorna:
    str: Texto descifrado.
    """

    key_inv = pow(key, -1, module)
    numbers = from_alphabetical_to_decimal(ciphertext)
    decrypted = [(n * key_inv) % module for n in numbers]
    return "".join(from_decimal_to_alphabetical(decrypted))



def frenquence_analysis(text):
    """
    Cuenta las tres letras más frecuentes en un texto.

    Parámetros:
    text (str): Texto en el que se va a contar.

    Retorna:
    list: Lista de tuplas con las tres letras más frecuentes y sus conteos. Ejemplo: [('A', 10), ('E', 8), ('O', 7)]
    """
    filtered_text = [char.upper() for char in text if char.upper() in alphabetical_decimal]
    counter = Counter(filtered_text)
    return [letter for letter, _ in counter.most_common(3)]


def guess_displacement_cipher(ciphertext):
    """
    Adivina la clave de desplazamiento usando análisis de frecuencia.

    Parámetros:
    ciphertext (str): Texto cifrado.

    Imprime las claves posibles y los textos descifrados.
    """
    # Letras más comunes del español
    spanish_common = from_alphabetical_to_decimal(common_letters)

    # Letras más frecuentes en el texto cifrado
    cipher_common = from_alphabetical_to_decimal(frenquence_analysis(ciphertext))

    # Generar posibles claves comparando todas las diferencias posibles
    candidates = []
    for cipher_letter in cipher_common:
        for spanish_letter in spanish_common:
            key = (cipher_letter - spanish_letter) % module
            candidates.append(key)

    for key in set(candidates):
        decrypted_text = displacement_decrypt(ciphertext, key)
        print(f"Probando clave de desplazamiento: {key}")
        print(f"Texto descifrado: {decrypted_text}")
        print("-" * 40)


def guess_multiplicative_cipher(ciphertext):
    """
    Adivina posibles claves del cifrado multiplicativo usando análisis de frecuencia.

    Parámetros:
    ciphertext (str): Texto cifrado.

    Si hay claves válidas, imprime las claves y los textos descifrados.
    """
    # Letras más comunes en español (E, A, O)
    spanish_common = from_alphabetical_to_decimal(common_letters)
    cipher_common = from_alphabetical_to_decimal(frenquence_analysis(ciphertext))

    keys = []

    for c_letter in cipher_common:
        for s_letter in spanish_common:
            try:
                # Resolver c ≡ k * s (mod 26) → k ≡ c * s⁻¹ (mod 26)
                s_inv = pow(s_letter, -1, module)
                k = (c_letter * s_inv) % module
                # Verificamos que k tiene inverso
                if pow(k, -1, module):
                    keys.append(k)
            except ValueError:
                pass  # No tiene inverso, no es válido
    keys = sorted(set(keys))
    if not keys:
        print("No se encontraron claves multiplicativas válidas.")
    else:
        for key in keys:
            decrypted_text = multiplicative_decrypt(ciphertext, key)
            print(f"Probando clave multiplicativa: {key}")
            print(f"Texto descifrado: {decrypted_text}")
            print("-" * 40)


if __name__ == "__main__":
    # Texto original para pruebas
    original_text = "HOLAESTOESUNAPRUEBA"
    
    # ========= CIFRADO POR DESPLAZAMIENTO =========
    print("\n--- CIFRADO POR DESPLAZAMIENTO ---")
    displacement_key = 5
    encrypted_disp = displacement_encrypt(original_text, displacement_key)
    print(f"Texto original:     {original_text}")
    print(f"Texto cifrado:      {encrypted_disp}")
    print(f"Texto descifrado:   {displacement_decrypt(encrypted_disp, displacement_key)}")
    
    print("\n--- ATAQUE POR ANÁLISIS DE FRECUENCIA (Desplazamiento) ---")
    guess_displacement_cipher(encrypted_disp)

    # ========= CIFRADO MULTIPLICATIVO =========
    print("\n--- CIFRADO MULTIPLICATIVO ---")
    multiplicative_key = 11  # Asegúrate que sea coprimo con 26
    encrypted_mult = multiplicative_encrypt(original_text, multiplicative_key)
    print(f"Texto original:     {original_text}")
    print(f"Texto cifrado:      {encrypted_mult}")
    print(f"Texto descifrado:   {multiplicative_decrypt(encrypted_mult, multiplicative_key)}")

    print("\n--- ATAQUE POR ANÁLISIS DE FRECUENCIA (Multiplicación) ---")
    guess_multiplicative_cipher(encrypted_mult)

