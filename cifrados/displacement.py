# Se hace un listado del afabetico clasico de 26 letras
alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# Diccionarios para facil transformación del alfabeto a su equivalente númerico
alphabetical_decimal = {char: i for i, char in enumerate(alphabet)}
decimal_alphabetical = {i: char for char, i in alphabetical_decimal.items()}

# Se calcula el modulo para las operaciones de cifrado
module = len(alphabet)


def set_custom_alphabet(new_alphabet):
    """
    Actualiza los diccionarios y módulo según un nuevo alfabeto personalizado.

    Argumentos:
    new_alphabet (list): Lista de caracteres que forman el nuevo alfabeto.
    """
    global alphabet, alphabetical_decimal, decimal_alphabetical, module

    alphabet = new_alphabet
    alphabetical_decimal = {char: i for i, char in enumerate(alphabet)}
    decimal_alphabetical = {i: char for i, char in enumerate(alphabet)}
    module = len(alphabet)


def generate_alphabet(filename, separator=None):
    """
    Extrae los caracteres de un archivo de texto y los devuelve como una lista,
    en orden para hacer un alfabeto extendido. Permite definir un separador del contenido.

    Parametros:
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


def caesar_encrypt(string):
    """
    Cifra una cadena de texto usando el cifrado César con un desplazamiento de 3 posiciones.

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
        cipher_values.append((i + 3) % module)  # Desplazamiento de 3 posiciones

    # Convierte los valores numéricos cifrados de nuevo a letras y devuelve el texto cifrado
    return "".join(from_decimal_to_alphabetical(cipher_values))


def caesar_decrypt(string):
    """
    Descifra una cadena de texto utilizando el cifrado César con un desplazamiento de 3 posiciones.

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
        decrypted_values.append(
            (i - 3) % module
        )  # Desplazamiento inverso de 3 posiciones

    # Convierte los valores numéricos descifrados de nuevo a letras y devuelve el texto descifrado
    return "".join(from_decimal_to_alphabetical(decrypted_values))


if __name__ == "__main__":
    while True:
        print("\n=== Cifrado Cesar ===")
        print("1. Cifrar texto")
        print("2. Descifrar texto")
        print("3. Generar alfabeto extendido desde archivo")
        print("4. Salir")

        opcion = input("Selecciona una opción (1-4): ").strip()

        if opcion == "1":
            texto = input("Ingresa el texto a cifrar: ")
            cifrado = caesar_encrypt(texto)
            print(f"Texto cifrado: {cifrado}")

        elif opcion == "2":
            texto = input("Ingresa el texto a descifrar: ")
            descifrado = caesar_decrypt(texto)
            print(f"Texto descifrado: {descifrado}")

        elif opcion == "3":
            file = input("Nombre del archivo de texto: ")
            sep = input("Separador (presiona Enter si no hay): ")
            sep = sep if sep else None
            new_alphabet = generate_alphabet(file, separator=sep)
            if new_alphabet:
                set_custom_alphabet(new_alphabet)
                print("Alfabeto generado correctamente.")
            else:
                print("No se pudo cargar el alfabeto.")

        elif opcion == "4":
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Intenta de nuevo.")
