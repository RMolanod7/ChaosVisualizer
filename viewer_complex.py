import matplotlib.pyplot as plt # para dibujar cosas en pantalla
from matplotlib.widgets import * # para botones y barras
from fractals_complex import *

class FractalViewer:
    def __init__(self):
        # declarar medidas basicas del fractal y el llamado a funciones de la interfaz
        self.width = 900
        self.low_width = 350
        self.height = 700
        self.low_height = 250
        self.max_iter = 200
        self.c = complex(-0.8, 0.156)
        
        self.fractal_type = "mandelbrot" # al inicio el fractal sera mandelbrot
        
        # vistas por defecto de cada fractal
        self.views = { # estos fractales suelen verse mejor en estos rangos
            "mandelbrot" : [-2.5, 1.5, -2, 2],
            "julia" : [-2, 2, -2, 2]
        }
        
        # guardar vista actual
        self.xmin, self.xmax, self.ymin, self.ymax = self.views[self.fractal_type]
        
        # crear la figura en matplotlib
        self.fig = plt.figure(figsize= (13, 8)) # alto y ancho de la interfaz completa en pulgadas
        self.ax = self.fig.add_axes([0.08, 0.12, 0.72, 0.82]) # las dos primeras dan la posicion de la esquina inferior izquierda, y los dos restantes el alto y el ancho de la zona donde se vera el fractal
        self.image = None # para guardar la imagen
        
        self._dragging = False # para saber si el usuario esta arrastrando o no el mouse
        self._drag_start = None # guarda el ultimo punto del mouse en coordenadas del plano complejo
        self.last_render_pos = None ########################################################3
    
        self._build_controls() # crear los botones y los sliders de la interfaz
        self._connect_events() # conectar el evento del zoom del mouse
        ##############################################################3
        self.render(full_quality= True) # renderizar la figura para actualizarla y generarla
        
    def _build_controls(self):
        # boton para cambiar de fractal
        ax_radio = self.fig.add_axes([0.83, 0.72, 0.14, 0.16]) # zona donde iran los botones
        self.radio = RadioButtons(ax_radio, ["mandelbrot", "julia"]) # las dos opciones de los botones
        self.radio.on_clicked(self.change_fractal) # cuando se presione que llame a la funcion para cambiar el fractal
        
        # el slider para cambiar el numero de iteraciones
        ax_iter = self.fig.add_axes([0.83, 0.58, 0.14, 0.03])
        self.slider_iter = Slider(ax_iter, "Cantidad de iteraciones", 50, 1000, valinit= 200, valstep= 1) # el slider inicia en 200
        self.slider_iter.on_changed(self.change_iter) # cuando cambie el slider que llame a la funcion para cambiar las iteraciones
        
        # los sliders para cambiar la parte real y la parte imaginaria de c para el fractal de Julia
        ax_creal = self.fig.add_axes([0.83, 0.45, 0.14, 0.03])
        self.slider_creal = Slider(ax_creal, "Re(c)", -2, 2, valinit= 0.8, valstep= 0.001)
        self.slider_creal.on_changed(self.change_c)
        ax_cimag = self.fig.add_axes([0.83, 0.32, 0.14, 0.03])
        self.slider_cimag = Slider(ax_cimag, "Im(c)", -2, 2, valinit= 0.156, valstep= 0.001)
        self.slider_cimag.on_changed(self.change_c)
        
        # boton de reiniciar
        ax_reset = self.fig.add_axes([0.85, 0.18, 0.1, 0.05])
        self.button = Button(ax_reset, "Reiniciar")
        self.button.on_clicked(self.reset_view) # cuando se presione el boton que llame a la funcion para reiniciar
        
        # texto para informar
        self.info_text = self.fig.text(0.70,  0.88, "", fontsize= 10, va= "top") # ubicacion, tamano de letra, ver de forma vertical
        
    def _connect_events(self):
        # la funcion mpl_connect es para trabajar con las interacciones externas del mouse o del teclado
        self.cid_scroll = self.fig.canvas.mpl_connect("scroll_event", self._on_scroll) # cuando giras la rueda llama a la funcion
        self.cid_press = self.fig.canvas.mpl_connect("button_press_event", self._on_press) # cuando presionas el mouse llama a la funcion
        self.cid_release = self.fig.canvas.mpl_connect("button_release_event", self._on_release) # cuando sueltas el mouse llama a la funcion
        self.cid_motion = self.fig.canvas.mpl_connect("motion_notify_event", self._on_motion) # cuando mueves el mouse llama a la funcion
        
    def change_fractal(self, label):
        # cambiar el tipo de fractal y los ejes de inicio
        self.fractal_type = label
        self.xmin, self.xmax, self.ymin, self.ymax = self.views[label]
        self.render(full_quality= True) # se redibuja el fractal nuevo
        
    def change_iter(self, val): # las funciones on_change y on_clicked le pasan un parametro a la funcion que llaman (en este caso val)
        # cambiar el numero de iteraciones
        self.max_iter = int(val)
        self.render(full_quality= True)
        
    def change_c(self, val):
        self.c = complex(self.slider_creal.val, self.slider_cimag.val) # actualizar el nuevo valor de c
        if self.fractal_type == "julia": # renderizar solo si se esta viendo el fractal de julia
            self.render(full_quality= True)        
            
    def reset_view(self, event): # aunque no se usa el event se le paso un parametro
        # reiniciar los valores del inicio
        self.xmin, self.xmax, self.ymin, self.ymax = self.views[self.fractal_type]
        self.max_iter = 200
        self.slider_iter.set_val(self.max_iter)
        
        if self.fractal_type == "julia":
            self.slider_creal.set_val(-0.8)
            self.slider_cimag.set_val(0.156)
        
        self.render(full_quality= True)
        
    def render(self, full_quality= True):
        #########################################
        if full_quality:
            width = self.width
            height = self.height
        else:
            width = self.low_width
            height = self.low_height
        
        # parametros
        params = {
            "xmin" : self.xmin,
            "xmax" : self.xmax,
            "ymin" : self.ymin,
            "ymax" : self.ymax,
            "width" : width,
            "height" : height,
            "max_iter" : self.max_iter,
            "c" : self.c
        }
        
        # generar matriz del fractal
        data = generate_complex_fractal(self.fractal_type, params)
        
        # si todavia no existe la imagen, generarla
        if self.image is None:
            # convierte la matriz en una imagen visible
            self.image = self.ax.imshow(
                data, # matriz del fractal
                extent = [self.xmin, self.xmax, self.ymin, self.ymax], # region del plano donde se visualiza la imagen
                cmap = "inferno", # gama de colores
                origin =  "lower", # dibujar de abajp hacia arriba
                interpolation= "nearest" #####################################################33
            )
            # anadir etiquetas a los ejes coordenados
            self.ax.set_xlabel("Eje X")
            self.ax.set_ylabel("Eje Y")
        else:
            # si esta creada solo es actualizarla con la nueva matriz y las nuevas dimensiones
            self.image.set_data(data)
            self.image.set_extent([self.xmin, self.xmax, self.ymin, self.ymax])
            
        # anadir textos en la ventana
        self.ax.set_title(self._title_text())
        self.info_text.set_text(self._info_text())
        
        # limites de coordenadas mostradas
        self.ax.set_xlim(self.xmin, self.xmax)
        self.ax.set_ylim(self.ymin, self.ymax)
            
        # para actualizar la ventana en matplotlib
        self.fig.canvas.draw_idle()
        
    def _title_text(self):
        # titulo del fractal mostrado
        if self.fractal_type == "mandelbrot":
            return "Mandelbrot"
        else: 
            return f"Julia | c = {self.c.real:.2f} + {self.c.imag:.2f}i" # c mostrado con sus valores con 2 lugares despues de la coma
        
    def _info_text(self):
        # texto con informacion
        return (
            f"Fractal: {self.fractal_type}\n"
            f"Iteracions: {self.max_iter}\n"
            f"Zoom\n"
            f"   x = [{self.xmin:.3f}, {self.xmax:.3f}]\n"
            f"   y = [{self.ymin:.3f}, {self.ymax:.3f}]\n"
            f"Rodar el mouse: Zoom"
        )
        
    def _zoom(self, xmid, ymid, scale):
        # ver que tan grande sera la nueva ventana
        xrange = (self.xmax - self.xmin) * scale
        yrange = (self.ymax - self.ymin) * scale
        
        # hacer zoom centrado en donde esta el mouse
        self.xmin = xmid - xrange / 2
        self.xmax = xmid + xrange / 2
        self.ymin = ymid - yrange / 2
        self.ymax = ymid + yrange / 2
        
        self.render(full_quality= True)
        
    def _on_scroll(self, event):
        # verificar si el mouse esta dentro o no del dibujo
        if event.inaxes != self.ax:
            return
        
        # evitar que no haya coordenadas invalidas
        if event.xdata is None or event.ydata is None:
            return
        
        # si se hizo zoom se agranda la escala (x0.8) y sino se achica (x1.2)
        scale = 0.8 if event.button == "up" else 1.2 
        
        # el punto donde esta el mouse
        xmid = event.xdata
        ymid = event.ydata
        
        self._zoom(xmid, ymid, scale)
        
    def _on_press(self, event):
        if event.inaxes != self.ax:
            return
        
        if event.button == 1: # click izquierdo para centrar
            # verificar si son validas las coordenadas del mouse
            if event.xdata is not None and event.ydata is not None:
                # se mantiene el mismo largo y ancho lo que se cambia el centro dependiendo de donde este el raton
                width = self.xmax - self.xmin 
                height = self.ymax - self.ymin
                
                # imagen centrada en donde esta el mouse
                self.xmin = event.xdata - width / 2
                self.xmax = event.xdata + width / 2
                self.ymin = event.ydata - height / 2
                self.ymax = event.ydata + height / 2
                
                self.render(full_quality= True)
        elif event.button == 3: # click derecho para arrastrar
            self._dragging = True # comienza el arrastre
            self._drag_start = (event.xdata, event.ydata) # coordenadas donde inicia el arrastre
        
    def _on_release(self, event):
        ########################################
        if self._dragging:
            # Renderixar al final con calidad completa
            self.render(full_quality= True)
        
        self._dragging = False # termina el arrastre
        self._drag_start = None # no hay coordenada inicial
    
    def _on_motion(self, event):
        # verificar si se esta arrastrando
        if self._dragging == False:
            return
        
        # verificar si el mouse esta dentro de la ventana de la figura
        if event.inaxes != self.ax:
            return
        
        # verificar si hay coordenada inicial
        if self._drag_start is None:
            return
        
        # verificar si se asignan coordenadas validas
        if event.xdata is None or event.ydata is None:
            return
        
        x0, y0 = self._drag_start
        dx = x0 - event.xdata # ver cuanto se arrastra a la derecha/izquierda
        dy = y0 - event.ydata # ver cuanto se arrastra hacia abajo/arriba
        
        # actualizar bordes de la figura
        self.xmin += dx
        self.xmax += dx
        self.ymin += dy
        self.ymax += dy
        
        self._drag_start = (event.xdata, event.ydata) # actualizar punto inicial
        ############################################################33
        self.render(full_quality= False)
        
    def run(self):
        # mostrar todo el programa
        plt.show()