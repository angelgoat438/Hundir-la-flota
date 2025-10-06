
import numpy as np
import random
import time as tm

print("\n Bienvenido grumete, es hora de asumir el cargo de armero y luchar con valentia")
print(" ")
print("VAMOOOOS A POR ELLOOOOSS !!!!")


# ----------------- Fase inicial ---------------------
# hola

def crear_tablero(lado=10):
    return np.full((lado, lado), " ")

def mostrar_tablero(tablero):
    print("   " + " ".join(str(i) for i in range(tablero.shape[1])))
    for i, fila in enumerate(tablero):
        print(f"{i:2} " + " ".join(fila))

def compro_victoria(tablero):
    return np.count_nonzero(tablero == "O") == 0

# barcos: {cantidad : eslora}
barcos = {3:2, 2:3, 1:4}
esloras = []
for n_barcos, l_eslo in barcos.items():
    esloras.extend([l_eslo] * n_barcos)

def colocar_barco(tablero, barco):
    tablero_nuevo = tablero.copy()
    num_filas, num_columnas = tablero.shape
    for fila, columna in barco:
        if fila < 0 or fila >= num_filas:
            return False
        elif columna < 0 or columna >= num_columnas:
            return False
        elif tablero[fila, columna] in ["X", "O"]:
            return False
        tablero_nuevo[fila, columna] = "O"
    return tablero_nuevo

def barco_random(tablero, eslora, n_intentos=100):
    num_filas, num_columnas = tablero.shape
    for _ in range(n_intentos):
        barco = []
        fila = random.randint(0, num_filas - 1)
        columna = random.randint(0, num_columnas - 1)
        direccion = random.choice(["N", "S", "E", "O"])
        barco.append((fila, columna))

        f, c = fila, columna
        for _ in range(eslora - 1):
            if direccion == "N":
                f -= 1
            elif direccion == "S":
                f += 1
            elif direccion == "E":
                c += 1
            elif direccion == "O":
                c -= 1
            barco.append((f, c))

        tablero_nuevo = colocar_barco(tablero, barco)
        if isinstance(tablero_nuevo, np.ndarray):
            return tablero_nuevo
    return tablero  # si falla tras intentos

def disparos(tablero_pmq, tablero_dm, a, b):
    if tablero_pmq[a, b] == "O":
        tablero_pmq[a, b] = "X"
        tablero_dm[a, b] = "X"
        return "Barco alcanzado"
    elif tablero_pmq[a, b] == " ":
        tablero_pmq[a, b] = "-"
        tablero_dm[a, b] = "-"
        return "Agua!"
    else:
        return "Ya has disparado aquí"

def disparo_maquina(tablero_pm, tablero_dmq):
    num_filas, num_columnas = tablero_pm.shape
    while True:
        a = random.randint(0, num_filas - 1)
        b = random.randint(0, num_columnas - 1)
        if tablero_dmq[a, b] in ["X", "-"]:
            continue
        if tablero_pm[a, b] == "O":
            tablero_pm[a, b] = "X"
            tablero_dmq[a, b] = "X"
            print(f"La máquina disparó en ({a},{b}) y alcanzó un barco!")
            return "Barco alcanzado"
        elif tablero_pm[a, b] == " ":
            tablero_pm[a, b] = "-"
            tablero_dmq[a, b] = "-"
            print(f"La máquina disparó en ({a},{b}) y fue agua.")
            return "Agua"

# ----------------- Juego ---------------------

def jugar(esloras, lado=10):
    # Crear tableros
    tablero_pm = crear_tablero(lado)  # Tablero principal mio
    tablero_dm = crear_tablero(lado)  # registro de mis disparos
    tablero_pmq = crear_tablero(lado) # tablero principal maquina
    tablero_dmq = crear_tablero(lado) # registro disparos maquina

    # Colocar barcos
    for eslora in esloras:
        tablero_pm = barco_random(tablero_pm, eslora)
        tablero_pmq = barco_random(tablero_pmq, eslora)

    print("\n -----------EMPIEZA LA BATALLA--------")

    while True:
        # --- Mostrar tableros ---
        print("\nTu tablero:")
        mostrar_tablero(tablero_pm)
        print("\nTus disparos sobre la máquina:")
        mostrar_tablero(tablero_dm)

        # --- Turno del jugador ---
        disparo = input("Vamos a disparar ! Dime una coordenada (fila,columna) o escribe 'salir': ")
        if disparo.lower() == "salir":
            print("Has salido de la partida.")
            break
        try:
            a, b = map(int, disparo.split(","))
        except:
            print("Formato no válido, vuelve a intentarlo.")
            continue

        if a < 0 or a >= tablero_pmq.shape[0] or b < 0 or b >= tablero_pmq.shape[1]: #Aqui controlo que el disparo esté en la matriz
            print("No existe esa coordenada, dime otra.")
            continue

        resultado = disparos(tablero_pmq, tablero_dm, a, b)
        print("Resultado:", resultado)

        if compro_victoria(tablero_pmq):
            print("Ya no le quedan barcos al enemigo, ¡HEMOS GANADOO!") #En cada ronda compruebo si ya se han cambiado todos los barcos a "X"
            break
        if resultado == "Barco alcanzado":
            print("¡Has dado en un barco! Dispara otra vez.")
            continue

        # --- Turno de la máquina ---
        resultado_maquina = disparo_maquina(tablero_pm, tablero_dmq)

        if compro_victoria(tablero_pm):
            print("El enemigo ha acabado con todos tus barcos. PERDIMOS")
            break
        if resultado_maquina == "Barco alcanzado":
            print("La máquina acertó y sigue disparando...")
            continue

        print("Ahora te toca otra vez.")
        tm.sleep(4)

# ----------------- INICIO ---------------------

jugar(esloras, lado=10)







