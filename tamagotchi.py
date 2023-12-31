import tkinter as tk
import time
import datetime
import random

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
    3.1. movimiento_basico
    3.2. show_pet
    3.3. hide_pet
    3.4. reset_menu
    3.5. reset_gui
    3.6. add_hunger
    3.7. subs_energy
    3.8. subs_happiness
    3.9. goes_to_the_loo
4. Funciones del Menú
    4.1. activate_submenu
    4.2. feed
    4.3. play
    4.4. health
    4.5. clean
    4.6. sleep
    4.7. lights
    4.8. discipline
    4.9. show_status
5. Atributos de Tiempo
    5.1. update_times
    5.2. time_hunger
    5.3. time_poop
    5.4. time_energy
    5.5. time_happiness
    5.6. tiempo_actual
    5.7. UPDATETIME

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
                'funct': self.activate_submenu,
                'image': 'imgs/icons/food.png',
                'place': (137, 142),
                'submenu': {
                    'cake': {
                        'funct': [self.feed, 'cake'],
                        'image': 'imgs/icons/cake.png',
                        'place': None,
                    },
                    'burger': {
                        'funct': [self.feed, 'burger'],
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
                'funct': self.activate_submenu,
                'image': 'imgs/icons/status.png',
                'place': (420, 485),
                'submenu': {
                    'pagina1': {
                        'funct': [self.show_status, 'pagina1'],
                        'image': 'imgs/icons/cake.png',
                        'place': None,
                    },
                    'pagina2': {
                        'funct': [self.show_status, 'pagina2'],
                        'image': 'imgs/icons/burger.png',
                        'place': None,
                    },
                }
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

        # Canvas para mostrar la imagen del BACKGROUND
        self.canvas = tk.Canvas(width=576, height=648)
        self.background_img = tk.PhotoImage(file="imgs/TamaFront.png")
        self.canvas.create_image(288, 324, image=self.background_img)
        self.canvas.grid(row=0, column=0)

        # Crea un canvas para contener la imagen de la mascota
        self.pet = tk.Canvas(width=387, height=287)
        self.pet_img = tk.PhotoImage(file="imgs/monkey.png")
        # Genera el movimiento en la siguiente linea
        self.posx = 72
        self.posy = 200
        #### ------------------------------------####
        self.canvas_pet = self.pet.create_image(self.posx, self.posy, image=self.pet_img)
        self.pet.config(bg='white', highlightthickness=0)
        self.show_pet()

        #########################

        # Botones de navegación CONFIG
        self.button_img = tk.PhotoImage(file='imgs/icons/button_small.png')
        # Boton A
        self.button_A = tk.Button(text="A", command=self.b_next,
                                  image=self.button_img, bg='indigo', highlightthickness=0)
        self.button_A.place(x=153, y=550)
        # Boton B
        self.button_B = tk.Button(text="B", command=self.b_select,
                                  image=self.button_img, bg='indigo', highlightthickness=0)
        self.button_B.place(x=255, y=580)
        # Boton C
        self.button_C = tk.Button(self.window, text="C", command=self.b_cancel,
                                  image=self.button_img, bg='indigo', highlightthickness=0)
        self.button_C.place(x=363, y=550)

        # Etiqueta FEDDBACK
        self.fbtext = ''
        self.feedback_label = tk.Label(text=f"{self.fbtext}")
        self.feedback_label.place(x=280, y=333)

        # Timing!
        self.UPDATETIME = {
            "time_hunger": [1, self.add_hunger],
            "time_poop": [1, self.goes_to_the_loo],
            "time_energy": [6, self.subs_energy],
            "time_happiness": [12, self.subs_happiness],
        }

    def check_times(self):
        time_now_min = int(datetime.datetime.now().strftime('%M'))
        for value in self.UPDATETIME:
            if self.UPDATETIME[value][0] % time_now_min == 0:
                self.UPDATETIME[value][1]()
    

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

            if len(self.MENU[self.menu_value]) > 3:
                self.SUBMENU = self.MENU[self.menu_value]['submenu']
                self.ITERSUBMENU = iter(self.SUBMENU)
            else:
                self.SUBMENU = None
                self.ITERSUBMENU = None

            # Cambia icono e imprime
            self.show_icon(self.MENU[self.menu_value])
            self.fbtext = str(self.menu_value)
            self.feedback_label.config(text=self.fbtext)

            # return self.SUBMENU , self.ITERSUBMENU

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
        # Si estamos en MENU 
        if self.main_menu == True and self.sub_menu == False:
            # Si el MENU_VALUE no esta vacio
            if self.menu_value != 'none':
                # Ejecutara la funcion correspondiente a MENU_VALUE
                try:
                    self.MENU[self.menu_value]['funct']()
                # Si existe algun problema no hará nada he imprimira el problema
                except Exception as e:
                    print(e)
                    pass
        # Si estamos en el SUB MENU            
        elif self.main_menu == False and self.sub_menu == True:
            # Si SUBMENU_VALUE no esta vacio
            if self.submenu_value != 'none':
                # Ejecutara la funcion correspondiente a SUBMENU_VALUE
                try:
                    self.SUBMENU[self.submenu_value]['funct'][0](
                        self.SUBMENU[self.submenu_value]['funct'][1]
                    )
                # Si existe algun problema no hará nada he imprimira el problema
                except Exception as e:
                    print(e)
                    pass
            # Si SUBMENU_VALUE esta vacio selecciona el primero de la lista 
            elif self.submenu_value == 'none':
                self.submenu_value = next(self.ITERSUBMENU)
                pass

    def b_cancel(self):
        """
        Función que se ejecuta al presionar el botón C.
        """
        global reset
        # Lógica para retroceder
        if self.main_menu == True and self.sub_menu == False:
            if self.menu_value != 'none':
                self.ITERMENU = iter(self.MENU)
                self.menu_value = next(self.ITERMENU)

            if hasattr(self, 'label') and isinstance(self.label, tk.Label):
                self.label.place_forget()
                self.feedback_label.config(text="")

        elif self.main_menu == False and self.sub_menu == True:
            # pasa a seleccionar la lista del MAIN MENU
            # cambia al MAIN MENU
            self.main_menu = True
            self.sub_menu = False
            self.feedback_label.config(text=self.menu_value)
            self.show_pet()
            reset = self.label.after(5000, self.reset_gui)
        self.SUBMENU = None
        self.submenu_value = None

    ## Funciones automáticas de TAMA ##
    #################################

    def movimiento_basico(self):
        """
        Realiza un movimiento básico de la mascota Tamagotchi.

        Genera nuevas coordenadas aleatorias dentro de un rango predefinido
        y actualiza la posición de la mascota en la interfaz gráfica.

        """
        new_posx = random.randint(72, 315)
        new_posy = random.randint(119, 168)

        self.posx = new_posx
        self.posy = new_posy

        self.pet.coords(self.canvas_pet, self.posx, self.posy)
        self.pet.update()
        self.pet.after(3000, self.movimiento_basico)

    def show_pet(self):
        """
        Muestra la mascota Tamagotchi en la interfaz gráfica.

        """
        self.pet.place(x=93, y=186)

    def hide_pet(self):
        """
        Oculta la mascota Tamagotchi de la interfaz gráfica.

        """
        self.pet.place_forget()

    def reset_menu(self):
        """
        Reinicia el menú principal.
        """
        self.ITERMENU = iter(self.MENU)
        self.menu_value = next(self.ITERMENU)

    #######################################
    #### funcion para organizr submenu?? ##
    #######################################

    def reset_gui(self):
        """
        Reinicia la interfaz gráfica.
        """
        self.label.place_forget()
        self.reset_menu()
        self.main_menu = True
        self.sub_menu = False
        self.feedback_label.config(text='')
        self.show_pet()

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

    def activate_submenu(self):
        """
        Activa el SUBMENU de feed.
        """
        # Cancela RESET
        self.label.after_cancel(reset)
        # Cambia del MENU A SUB_MENU
        self.main_menu = False
        self.sub_menu = True
        # Esconde la MASCOTA
        self.hide_pet()

        # muestra las opciones
        if self.SUBMENU[self.submenu_value]['funct'][0] == 'show_status':
            self.SUBMENU[self.submenu_value]['funct'][0](
                        self.SUBMENU[self.submenu_value]['funct'][1]
                    )

        else:
            submenu_options = ', \n'.join(self.SUBMENU.keys())
            self.fbtext = f"Selecciona una opción:\n {submenu_options}"
            self.feedback_label.config(text=self.fbtext)

    def feed(self, item_type):
        """
        Aumenta el nivel de hambre de Tamagotchi.
        """

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

    def show_status(self, page):
        """
        Muestra el estado de Tamagotchi.
        """
        self.label.after_cancel(reset)

        if self.submenu_value == None:
            self.submenu_value = (next(self.ITERSUBMENU))

        if page == 'pagina1':
            # Mostrar:
            self.tiempo_actual = time.localtime()  # Time
            self.fbtext = str(
                f"""{time.strftime('%H:%M:%S', self.tiempo_actual)}
                HAPPINESS : {self.status['happiness']}
                HUNGER : {self.status['hunger']}%
                ENERGY : {self.status['energy']}%

                """
            )
            self.feedback_label.config(text=self.fbtext)

        elif page == 'pagina2':
            # Mostrar:
            self.tiempo_actual = time.localtime()  # Time
            self.fbtext = str(
                f"""{time.strftime('%H:%M:%S', self.tiempo_actual)}
                HYGENE : {self.status['hygiene']}%
                SICK : {self.status['sick']}
                POOP : {self.status['poop']}

                """
            )
            self.feedback_label.config(text=self.fbtext)

        reset = self.label.after(10000, self.reset_gui)
