import numpy as np

def Mandelbrot(xmin, xmax, ymin, ymax, width, height, max_iter): # limites del plano, ancho y largo de la imagen en pixeles
    """
    Del fractal de Mandelbrot

    Devuelve una matriz con el número de iteraciones
    que tardó cada punto en escapar
    """
    # crea numeros igualmente distanciados para luego representar los pixeles
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    
    # construir la matriz del plano complejo, es como multiplicar un vector mx1 por uno 1xn
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis] # x[np.newaxis,:] convierte a x en una fila, y al contrario convierte por ejemplo a y en una columna, 1j es i en py
    Z = np.zeros_like(C, dtype= np.complex128) # matriz de ceros, como la ecuacion de Mandelbrot empieza en cero para verificar si pertenece o no el punto luego
    
    output = np.zeros(C.shape, dtype= np.int32) # empezar a crear la salida, que es basicamente cuanto demora en escapar cada punto
    mask = np.ones(C.shape, dtype= bool) # una mascara de bits para ver que puntos siguen o no activos
    
    # el bucle principal de la funcion, ver cuantas veces se iterara
    for i in range(max_iter):
        # ecuacion de Mandelbroot, para verficar los puntos que siguen activos
        Z[mask] = Z[mask]**2 + C[mask] # evaluar en una matriz (Z) una mascara de bits (mask) hace que solo trabaje con los trues
        escaped = np.abs(Z) > 2 # evalua la condicion booleana de > 2 en cada elemento de Z y crea una matriz booleana
        
        # mask me dice True si el punto esta activo y escaped si se escapo en esta iteracion o no
        newly_escaped = escaped & mask # hace un and a cada elemento de ambas matrices, devuelve los que se escaparon
        output[newly_escaped] = i + 1 # guarda en que iteracion se escapo cada punto 
        mask &= ~escaped # quitar de mask los que escaparon
        
        # condicion para parar el bucle, si ya todos escaparon
        if not mask.any():
            break
        
    output[mask] = max_iter # los puntos que siguen activos despues de todas las operaciones se les asigna la ultima iteracion
    return output
         
def Julia(xmin, xmax, ymin, ymax, width, height, c, max_iter): # aqui c es constante, lo que cambia es el empezar de z
    """
    Del fractal de Julia para un valor fijo c

    Devuelve una matriz con el número de iteraciones
    que tardó cada punto en escapar
    """
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    Z = x[np.newaxis, :] + 1j * y[:, np.newaxis] # cada punto empieza con su propio valor complejo ahora
    
    output = np.zeros (Z.shape, dtype= np.int32) # igual para saber en cuantas iteraciones han escapado
    mask = np.ones(Z.shape, dtype= bool) # igual empiezan todos activos
    
    for i in range(max_iter):
        Z[mask] = Z[mask]**2 + c # aqui c es constante
        escaped = np.abs(Z) > 2
        newly_escaped = mask & escaped
        
        # misma idea
        output[newly_escaped] = i + 1 
        mask &= ~escaped
        
        if not mask.any():
            break
        
    output[mask] = max_iter
    return output
        
def generate_complex_fractal(fractal_type, params):
    """
    Generador unificado para fractales complejos

    Los tipos de fractales son:
        - "mandelbrot"
        - "julia"

    Y los parametros que se pasan:
        xmin, xmax, ymin, ymax, width, height, max_iter
        y para Julia además: c
    """
    # definir parametros que se pasan en params
    xmin = params.get("xmin", -2.5)
    xmax = params.get("xmax", 1.5)
    ymin = params.get("ymin", -2.0)
    ymax = params.get("ymax", 2.0)
    width = params.get("width", 800)
    height = params.get("height", 600)
    max_iter = params.get("max_iter", 200)
    
    if fractal_type == "mandelbrot":
        return Mandelbrot(xmin, xmax, ymin, ymax, width, height, max_iter)
    elif fractal_type == "julia":
        c = params.get("c", complex(-0.8, 0.156))
        return Julia(xmin, xmax, ymin, ymax, width, height, c, max_iter)
    else:
        raise ValueError("Tipo de fractal no válido.")
    