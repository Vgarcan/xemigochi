import random 
import time
from tamagotchi import Tama


# Iniciar la ventana
MiTama = Tama('caracaca')

MiTama.window.mainloop()
# while True:
#     if int(time.strftime("%M", time.localtime())) % MiTama.update_times :
#         # MiTama.time_hunger = random.randint(3,8)
#         MiTama.time_poop = random.randint(8,15)
#         # MiTama.time_energy = random.randint(1,4)
#         MiTama.time_happiness = random.randint(5,16)

     
#     elif int(time.strftime("%M", time.localtime())) % MiTama.time_hunger:
#         print ('rrr eee')
#         MiTama.add_hunger()
#     elif int(time.strftime("%M", time.localtime())) % MiTama.time_poop:
#         MiTama.goes_to_the_loo()
#     elif int(time.strftime("%M", time.localtime())) % MiTama.time_energy:
#         MiTama.subs_energy()
#         print ('rrr eee')
#     elif int(time.strftime("%M", time.localtime())) % MiTama.time_happiness:
#         MiTama.subs_happiness()








