import tkinter as tk
import time

"""
Contenido:
1. Inicialización de la clase
    1.1. Atributos de la mascota
    1.2. Elemento seleccionado en el menú
    1.3. Menú de acciones
    1.4. Interfaz Gráfica
2. Funciones para los botones de la interfaz
    2.1. show_icon
    2.2. b_next
    2.3. b_select
    2.4. b_cancel
3. Funciones automáticas de TAMA
    3.1. reset_menu
    3.2. reset_gui
    3.3. add_hunger
    3.4. subs_energy
    3.5. subs_happiness
    3.6. goes_to_the_loo
4. Funciones del Menú
    4.1. feed
    4.2. play
    4.3. health
    4.4. clean
    4.5. sleep
    4.6. lights
    4.7. discipline
    4.8. show_status
5. Atributos de Tiempo
    5.1. update_times
    5.2. time_hunger
    5.3. time_poop
    5.4. time_energy
    5.5. time_happiness
"""


class Tama:
    def __init__(self, name):
        """
        Inicia una instancia de la clase Tama (Tamagotchi).

        Parámetros:
        - name (str): Nombre de la mascota.
        """
        # Atributos de la mascota
        self.name = name
        self.status = {
            'sick': False,
            'poop': 0,
            'hygiene': 100,
            'lights': True,
            'hunger': 0,
            'happiness': 100,
            'energy': 100
        }

        # Elemento seleccionado en el menú
        self.selected_menu_item = None

        # Menú de acciones
        self.MENU = {
            'none': {
                'funct': None,
                'image': None,
                'place': None
            },
            'feed': {
                'funct': self.activate_feed,
                'image': 'imgs/icons/food.png',
                'place': (137, 142),
                'submenu': {
                    'cake': {
                        'funct': [self.feed,'cake'],
                        'image': 'imgs/icons/cake.png',
                        'place': None,
                    },
                    'burger': {
                        'funct': [self.feed,'burger'],
                        'image': 'imgs/icons/burger.png',
                        'place': None,
                    },
                }
            },
            'play': {
                'funct': self.play,
                'image': 'imgs/icons/toys.png',
                'place': (218, 142)
            },
            'health': {
                'funct': self.health,
                'image': 'imgs/icons/jab.png',
                'place': (304, 142)
            },
            'clean': {
                'funct': self.clean,
                'image': 'imgs/icons/bath.png',
                'place': (405, 142)
            },
            'sleep': {
                'funct': self.sleep,
                'image': 'imgs/icons/sleep.png',
                'place': (125, 485)
            },
            'lights': {
                'funct': self.lights,
                'image': 'imgs/icons/lights.png',
                'place': (223, 485)
            },
            'discipline': {
                'funct': self.discipline,
                'image': 'imgs/icons/discipline.png',
                'place': (315, 485)
            },
            'status': {
                'funct': self.show_status,
                'image': 'imgs/icons/status.png',
                'place': (420, 485)
            },
        }
        self.ITERMENU = iter(self.MENU)
        self.menu_value = next(self.ITERMENU)
        self.ITERSUBMENU = None
        self.submenu_value = None
        self.main_menu = True
        self.sub_menu = False

        ## INTERFAZ GRÁFICA ##
        ######################

        # Crear la ventana principal
        self.window = tk.Tk()
        self.window.title("Xemigotchi")


        # Canvas para mostrar la imagen de la mascota
        self.canvas = tk.Canvas(width=576, height=648)
        self.background_img = tk.PhotoImage(file="imgs/TamaFront.png")
        self.canvas.create_image(288, 324, image=self.background_img)
        self.canvas.grid(row=0, column=0)

        # Botones de navegación
        self.button_img = tk.PhotoImage(file='imgs/icons/button_small.png')
        self.button_A = tk.Button(text="A", command=self.b_next,
                                  image=self.button_img, bg='indigo', highlightthickness=0)
        self.button_A.place(x=153, y=550)
        self.button_B = tk.Button(text="B", command=self.b_select,
                                  image=self.button_img, bg='indigo', highlightthickness=0)
        self.button_B.place(x=255, y=580)
        self.button_C = tk.Button(self.window, text="C", command=self.b_cancel,
                                  image=self.button_img, bg='indigo', highlightthickness=0)
        self.button_C.place(x=363, y=550)

        
        # Etiqueta FEDDBACK
        self.fbtext = ''
        self.feedback_label = tk.Label(text=f"{self.fbtext}")
        self.feedback_label.place(x=280, y=333)

    ## Funciones para los botones de la interfaz ##
    ##############################################

    def show_icon(self, menu):
        """
        Muestra el icono correspondiente en la interfaz gráfica.

        Parámetros:
        - menu (dict): Información del elemento del menú.
        """
        global reset
        try:
            self.label.after_cancel(reset)
        except Exception:
            pass

        if hasattr(self, 'label') and isinstance(self.label, tk.Label):
            self.label.place_forget()

        self.img = tk.PhotoImage(file=menu['image'])
        self.label = tk.Label(image=self.img)
        self.label.config(width=32, height=32)
        self.label.place(x=menu['place'][0], y=menu['place'][1])

        reset = self.label.after(5000, self.reset_gui)

    def b_next(self):
        """
        Función que se ejecuta al presionar el botón A.
        """
        # Lógica para avanzar
        if self.main_menu == True and self.sub_menu == False:
            try:
                self.menu_value = next(self.ITERMENU)
            except Exception:
                self.ITERMENU = iter(self.MENU)
                self.menu_value = next(self.ITERMENU)
                if self.menu_value == 'none':
                    self.menu_value = next(self.ITERMENU)
            
            if len(self.MENU[self.menu_value]) >3:
                self.SUBMENU= self.MENU[self.menu_value]['submenu']
                self.ITERSUBMENU = iter(self.SUBMENU)
            
            # Cambia icono e imprime        
            self.show_icon(self.MENU[self.menu_value])
            self.fbtext = str(self.menu_value)
            self.feedback_label.config(text=self.fbtext)

        elif self.main_menu == False and self.sub_menu == True:
            # pasa a seleccionar la lista del SUB MENU
            
            try:
                self.submenu_value = next(self.ITERSUBMENU)
            except Exception:
                self.ITERSUBMENU = iter(self.SUBMENU)
                self.submenu_value = next(self.ITERSUBMENU)
                if self.submenu_value == 'none':
                    self.submenu_value = next(self.ITERSUBMENU)
            # Imprime 
            self.fbtext = str(self.submenu_value)
            self.feedback_label.config(text=self.fbtext)

    def b_select(self):
        """
        Función que se ejecuta al presionar el botón B.
        """
        if self.main_menu == True and self.sub_menu == False:

            if self.menu_value != 'none':
                try:
                    self.MENU[self.menu_value]['funct']()
                except Exception:
                    pass

        elif self.main_menu == False and self.sub_menu == True:

            if self.submenu_value != 'none':
                try:
                    self.SUBMENU[self.submenu_value]['funct'][0](self.SUBMENU[self.submenu_value]['funct'][1])
                except Exception:
                    pass
            

    def b_cancel(self):
        """
        Función que se ejecuta al presionar el botón C.
        """
        # Lógica para retroceder
        if self.main_menu == True and self.sub_menu == False:
            if self.menu_value != 'none':
                self.ITERMENU = iter(self.MENU)
                self.menu_value = next(self.ITERMENU)

            if hasattr(self, 'label') and isinstance(self.label, tk.Label):
                self.label.place_forget()

        elif self.main_menu == False and self.sub_menu == True:
            # pasa a seleccionar la lista del MAIN MENU
            # cambia al MAIN MENU
            self.main_menu = True
            self.sub_menu = False

    ## Funciones automáticas de TAMA ##
    #################################

    def reset_menu(self):
        """
        Reinicia el menú principal.
        """
        self.ITERMENU = iter(self.MENU)
        self.menu_value = next(self.ITERMENU)

    def reset_gui(self):
        """
        Reinicia la interfaz gráfica.
        """
        self.label.place_forget()
        self.reset_menu()
        self.main_menu = True
        self.sub_menu = False

    def add_hunger(self):
        """
        Aumenta el nivel de hambre de Tamagotchi en 10 puntos.
        """
        self.status['hunger'] += 10

    def subs_energy(self):
        """
        Reduce el nivel de energía de Tamagotchi en 5 puntos.
        """
        self.status['energy'] -= 5

    def subs_happiness(self):
        """
        Reduce el nivel de felicidad de Tamagotchi en 5 puntos.
        """
        self.status['happiness'] -= 5

    def goes_to_the_loo(self):
        """
        Verifica si Tamagotchi necesita ir al baño según su nivel de hambre.

        Añade +1 al self.status['poop']
        """
        if self.status['hunger'] > 30:
            self.status['poop'] += 1

    ## FUNCIONES DEL MENÚ ##
    #########################

    def activate_feed(self):
        """
        Activa el SUBMENU de feed.
        """
        self.label.after_cancel(reset)

        self.main_menu = False
        self.sub_menu = True

    def feed(self, item_type):
        """
        Aumenta el nivel de hambre de Tamagotchi.
        """
        

        self.main_menu = False
        self.sub_menu = True

        if item_type == 'burger':
            self.status['hunger'] += 15
            self.fbtext = str(self.status['hunger'])
            self.feedback_label.config(text=self.fbtext)

        elif item_type == 'cake':
            self.status['hunger'] += 5
            self.fbtext = str(self.status['hunger'])
            self.feedback_label.config(text=self.fbtext)

    def play(self):
        """
        Aumenta el nivel de felicidad de Tamagotchi.
        """
        self.status['happiness'] += 1

    def health(self):
        """
        Mejora la salud de Tamagotchi si está enfermo.
        """
        if self.status['sick']:
            self.status['sick'] = False
        else:
            # Hará algo si está sano
            pass

    def clean(self):
        """
        Reduce la cantidad de desechos de Tamagotchi si hay.
        """
        if self.status['poop'] > 0:
            self.subs_cleanliness()
            self.fbtext = str('Una caca limpia')
            self.feedback_label.config(text=self.fbtext)
        else:
            # Hará algo si no hay desechos
            self.fbtext = str('NO hay cacas')
            self.feedback_label.config(text=self.fbtext)
            pass

    def sleep(self):
        """
        Pone a Tamagotchi a dormir si tiene poca energía.
        """
        if self.status['energy'] < 15:
            # Tamagotchi se va a dormir
            self.fbtext = str('buenas noches')
            self.feedback_label.config(text=self.fbtext)
            pass
        self.fbtext = str('No tengo sueño')
        self.feedback_label.config(text=self.fbtext)

    def lights(self):
        """
        Controla el estado de las luces.
        """
        if self.status['lights'] == True:
            self.status['lights'] = False
        elif self.status['lights'] == False:
            self.status['lights'] = True
        self.fbtext = str(self.status['lights'])
        self.feedback_label.config(text=self.fbtext)

    def discipline(self):
        """
        Reduce la felicidad de Tamagotchi como disciplina.
        """
        self.status['happiness'] -= 1
        self.fbtext = str(self.status['happiness'])
        self.feedback_label.config(text=self.fbtext)

    def show_status(self):
        """
        Muestra el estado de Tamagotchi.
        """
        self.label.after_cancel(reset)
        # Cambiamos a SUB_MENU
        self.main_menu = False
        self.sub_menu = True

        # Mostrar:
        self.tiempo_actual = time.localtime()  # Time
        self.fbtext = str(time.strftime("%H:%M:%S", self.tiempo_actual))
        self.feedback_label.config(text=self.fbtext)  # Attributes
        for key, value in self.status.items():
            self.fbtext = str(key, ' = ', value)
            self.feedback_label.config(text=self.fbtext)

        self.label.after(10000, self.reset_gui)

    update_times = 20
    time_hunger = 1
    time_poop = 1
    time_energy = 6
    time_happiness = 12