import string


def crear_matriz_clave(clave):
    clave = clave.upper().replace("J", "I")
    alfabeto = string.ascii_uppercase.replace("J", "")
    matriz = []
    vista = set()

    for c in clave + alfabeto:
        if c not in vista and c in alfabeto:
            matriz.append(c)
            vista.add(c)

    return [matriz[i : i + 5] for i in range(0, 25, 5)]


def preparar_pares(texto):
    texto = texto.upper().replace("J", "I")
    texto = "".join(filter(str.isalpha, texto))
    pares = []
    i = 0

    while i < len(texto):
        a = texto[i]
        b = texto[i + 1] if i + 1 < len(texto) else "X"
        if a == b:
            pares.append((a, "X"))
            i += 1
        else:
            pares.append((a, b))
            i += 2
    return pares


def buscar_posicion(matriz, letra):
    for i, fila in enumerate(matriz):
        if letra in fila:
            return i, fila.index(letra)
    return None


def cifrar_par(matriz, a, b):
    fila_a, col_a = buscar_posicion(matriz, a)
    fila_b, col_b = buscar_posicion(matriz, b)

    if fila_a == fila_b:
        return matriz[fila_a][(col_a + 1) % 5], matriz[fila_b][(col_b + 1) % 5]
    elif col_a == col_b:
        return matriz[(fila_a + 1) % 5][col_a], matriz[(fila_b + 1) % 5][col_b]
    else:
        return matriz[fila_a][col_b], matriz[fila_b][col_a]


def descifrar_par(matriz, a, b):
    fila_a, col_a = buscar_posicion(matriz, a)
    fila_b, col_b = buscar_posicion(matriz, b)

    if fila_a == fila_b:
        return matriz[fila_a][(col_a - 1) % 5], matriz[fila_b][(col_b - 1) % 5]
    elif col_a == col_b:
        return matriz[(fila_a - 1) % 5][col_a], matriz[(fila_b - 1) % 5][col_b]
    else:
        return matriz[fila_a][col_b], matriz[fila_b][col_a]


def cifrar_playfair(texto, clave):
    matriz = crear_matriz_clave(clave)
    pares = preparar_pares(texto)
    resultado = ""
    for a, b in pares:
        c1, c2 = cifrar_par(matriz, a, b)
        resultado += c1 + c2
    return resultado


def descifrar_playfair(texto, clave):
    matriz = crear_matriz_clave(clave)
    pares = preparar_pares(texto)
    resultado = ""
    for a, b in pares:
        d1, d2 = descifrar_par(matriz, a, b)
        resultado += d1 + d2
    return resultado


# ====== Prueba del cifrado Playfair ======
clave = "KEYWORD"
mensaje = "WHYDONTYOU"

cifrado = cifrar_playfair(mensaje, clave)
descifrado = descifrar_playfair(cifrado, clave)

print(f"Mensaje original: {mensaje}")
print(f"Cifrado: {cifrado}")
print(f"Descifrado: {descifrado}")
