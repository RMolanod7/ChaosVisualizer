import matplotlib.pyplot as plt
import numpy as np
import cmath

def calcular_distancia(a:tuple[float, float], b:tuple[float, float]) -> float:
    d = np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
    return d

def calcular_vertices(centro_x, centro_y, radio) -> list[tuple[float, float]]:
    """Calcula los vertices de un triangulo equilatero inicial dado su centro y su radio"""

    vertice_1 = (centro_x, centro_y + radio) #vertice superior
    vertice_2 = (centro_x - (0.866*radio), centro_y - (radio / 2)) #vertice inferior izquierdo
    vertice_3 = (centro_x + (0.866*radio), centro_y - (radio / 2)) #vertice inferior derercho
    vertices = [vertice_1, vertice_2, vertice_3]
    return vertices

def subdividir_segmentos(p_1:tuple[float, float], p_2:tuple[float, float], nivel:int)->list[tuple[float, float]]:
    """Dado dos puntos q determinan un segmento del triangulo inicial, divide dicho segmento en 3 partes iguales
    y forma un triangulo equilatero con base en el segmento central, devolviendo dichos puntos de particion, 
    el tercer punto del triangulo y el p_2 del segmento"""

    if nivel==0:
        return [p_1, p_2]
    
    z1 = complex(p_1[0], p_1[1])
    z2 = complex(p_2[0], p_2[1])

    pa = z1 + (z2 - z1) / 3 #primer punto de partir en 1/3
    pb = z1 + 2 * (z2 - z1) / 3 #segundo punto de partir en 1/3
    p_a = (pa.real, pa.imag) #convertirlos a complejo para q sea mas facil
    p_b = (pb.real, pb.imag)


    v = pb - pa 

    rot_60 = complex(cmath.cos(-cmath.pi/3), cmath.sin(-cmath.pi/3)) 

    pico = pa + v*rot_60
    pic = (pico.real, pico.imag) #punto q hace el pico en el triangulo equilatero

    resultado = []
    resultado.extend(subdividir_segmentos(p_1, p_a, nivel - 1)[:-1])  # todos menos el último para no duplicar
    resultado.extend(subdividir_segmentos(p_a, pic, nivel - 1)[:-1])
    resultado.extend(subdividir_segmentos(pic, p_b, nivel - 1)[:-1])
    resultado.extend(subdividir_segmentos(p_b, p_2, nivel - 1))
    
    return resultado

def copo_de_nieve(
    centro_x: float, 
    centro_y: float, 
    radio: float, 
    nivel: int
) -> list[tuple[float, float]]:

    vertices = calcular_vertices(centro_x, centro_y, radio)

    if nivel == 0:
        return vertices + [vertices[0]]
    
    puntos_finales = []
    
    # Procesar los 3 lados del triángulo
    for i in range(3):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % 3]  # el siguiente vértice, el último conecta con el primero
        
        if i == 0:
            # Primer segmento: incluir todos los puntos
            puntos_finales.extend(subdividir_segmentos(p1, p2, nivel))
        else:
            # Siguientes segmentos: excluir el primer punto para no duplicar
            puntos_finales.extend(subdividir_segmentos(p1, p2, nivel)[1:])
    
    return puntos_finales

def dibujar_copo(centro_x, centro_y, radio, nivel):
    puntos = copo_de_nieve(centro_x, centro_y, radio, nivel)
    
    # Separar coordenadas x e y
    x = [p[0] for p in puntos]
    y = [p[1] for p in puntos]
    
    plt.figure(figsize=(8, 8))
    plt.plot(x, y, 'b-')
    plt.axis('equal')
    plt.title(f'Copo de nieve de Koch - Nivel {nivel}')
    plt.grid(False)
    plt.show()

# Ejemplo de uso
# if __name__ == "__main__":
#     dibujar_copo(0, 0, 1, 4) 