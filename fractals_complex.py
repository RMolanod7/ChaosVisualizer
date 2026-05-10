import numpy as np
from numba import njit as nj 

@nj(fastmath= True) # Convierte python en codigo maquina optimizado, lo de fastmath es para optimizaciones matematicas agresivas
def Mandelbrot(xmin, xmax, ymin, ymax, width, height, max_iter): # limites del plano, ancho y largo de la imagen en pixeles
    """
    Del fractal de Mandelbrot
    Devuelve una matriz con el número de iteraciones que tardó cada punto en escapar
    """
    image = np.zeros((height, width), dtype= np.uint16) # Crea una matriz de height x width que representan los pixeles de la pantalla y los tipos de datos son int de 16 bits sin signo
    
    # Para recorrer las filas
    for y in range(height):
        cy = ymin + (y / height) * (ymax - ymin) # Transforma coordenadas y de pantalla a coordenadas y matematicas
        
        # Para recorrer las columnas
        for x in range(width):
            cx = xmin + (x / width) * (xmax - xmin) # Transforma coordenadas x de pantalla a coordenadas x matematicas
            
            q = (cx - 0.25) ** 2 + cy ** 2 # Calcular una expresion geometrica para hacer la siguiente mas sencilla
            
            if q * (q + (cx - 0.25)) <= 0.25 * cy ** 2: # Verificar si el punto esta en el circulo grande principal del fractal gemetricamente
                image[y, x] = max_iter # los dibujo de amarillo
                continue
            
            if (cx + 1) ** 2 + cy ** 2 <= 0.0625: # Verificar si el punto esta en el cirulo pequeno izquierdo del fractal matematicamente
                image[y, x] = max_iter # los dibujo de amarillo
                continue
            
            # Ahora con el resto de puntos
            zx = 0.0
            zy = 0.0
            
            iteration = 0
            
            # Antes escapaba cuando |y|>2 pero ahora y=zx+zy*i entonces escapa cuando zx^2+zy^2>4
            while zx ** 2 + zy ** 2 <= 4.0 and iteration <= max_iter: # Trabajar con float es mucho mas eficiente que con complejos
                # La ecuacion de mandelbrot es z = z^2 + c, tomando z = zx+zy*i y despejando
                xtemp = zx ** 2 - zy ** 2 + cx # zx = zx^2 - zy^2 + cx
                zy = 2.0 * zx * zy + cy # zy*i = (2*zx*zy + cy)*i 
                zx = xtemp # Hay que hacer la variable xtemp para no modificar zx antes de tiempo
                
                iteration += 1 
            
            # Guarda en cuantas iteraciones logro escapar el punto para definir de que color se dibuja
            image[y, x] = iteration # Menos iteraciones mas negro (no pertenece al fractal), mas iteraciones mas amarillo (si lo hace)
        
    return image
                
@nj(fastmath= True)  # Muchos procesos analogos a MAndelbrot
def Julia(xmin, xmax, ymin, ymax, width, height, max_iter, creal, cimag): # aqui c es constante, lo que cambia es el empezar de z
    """
    Del fractal de Julia para un valor fijo c
    Devuelve una matriz con el número de iteracionesque tardó cada punto en escapar
    """
    image = np.zeros((height, width), dtype= np.uint16)
    
    for y in range(height):
        zy0 = ymin + (y / height) * (ymax - ymin)
        
        for x in range(width):
            zx0 = xmin + (x / width) * (xmax - xmin)
            
            zx = zx0
            zy = zy0
            
            iteration = 0
            
            # En Julia no existen pedazos obvios importantes que dibujar antes
            while zx ** 2 + zy ** 2 <= 4.0 and iteration <= max_iter: # Misma logica que Mandelbrot
                xtemp = zx ** 2 - zy ** 2 + creal
                zy = 2.0 * zx * zy + cimag
                zx = xtemp
                
                iteration += 1
                
            image[y, x] = iteration
            
    return image
        
def generate_complex_fractal(fractal_type, params):
    """
    Generador unificado para fractales complejos
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
        return Julia(xmin, xmax, ymin, ymax, width, height, max_iter, c.real, c.imag)
    else:
        raise ValueError("Tipo de fractal no válido.")
    