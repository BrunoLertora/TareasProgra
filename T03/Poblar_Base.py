# class Usuario:
#     def __init__(self, user, password):
#         self.user = user
#         self.password = password
#
#
# class Reproduccion:
#     contador = 0
#     def __init__(self, user, song, date):
#         self.user = user
#         self.song = song
#         self.date = date
#         self.id_reproduccion = Reproduccion.contador
#         Reproduccion.contador += 1

import csv
# [usuario_id, usuario,contraseña]
usuario1 = [1,'elzambon','enzozambon']
usuario2 = [2,'lzambon','lucianozambon']
usuario3 = [3,'balertora','brunogay']
usuario4 = [4,'jionate','onatetraves']
usuario5 = [5,'eezh','eduardo123']

#canciones usuario1 [id_reproduccion, usuario_id, cancion, fecha]
reprod1_1 = [1,1,'Young Folks','15-07-1995-15:00']
reprod1_2 = [2,1,'Sol a Sol','15-07-1995-15:05']
reprod1_3 = [3,1,'We Are Never Ever Getting Back Together','15-07-1995-15:10']
reprod1_4 = [4,1,'Havana','15-07-1995-15:20']

reprod2_1 = [5,2,'Young Folks','14-07-1995-15:00']
reprod2_2 = [6,2,'Uneasy','14-07-1995-12:00']
reprod2_3 = [7,2,'Sed de Mal','14-07-1995-13:00']
reprod2_4 = [8,2,'Look What You Made Me Do','14-07-1995-14:00']

reprod3_1 = [9,3,'Break Free','10-07-1995-19:00']
reprod3_2 = [10,3,'Since U Been Gone','10-07-1995-12:00']
reprod3_3 = [11,3,'Albion Intro','10-07-1995-9:00']
reprod3_4 = [12,3,'Young Folks','10-07-1995-23:00']

reprod4_1 = [13,4,'Break Free','10-07-1995-19:00']
reprod4_2 = [14,4,'Por Favor','12-07-1995-19:00']
reprod4_3 = [15,4,'Gran Santiago','13-07-1995-19:00']
reprod4_4 = [16,4,'Sed de Mal','14-07-1995-19:00']

reprod5_1 = [17,5,'Sol a Sol','11-07-1995-19:00']
reprod5_2 = [18,5,'Gran Santiago','10-06-1995-19:00']
reprod5_3 = [19,5,'Break Free','10-05-1995-19:00']
reprod5_4 = [20,5,'Since U Been Gone','10-02-1995-19:00']



#Creacion archivo usuarios

with open('usuarios.csv', "w", encoding='utf8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames = ['usuario_id', 'usuario', 'contraseña'])
        writer.writeheader()
        writer = csv.writer(csv_file, delimiter=',')
        for line in [usuario1, usuario2,usuario3,usuario4,usuario5]:
            writer.writerow(line)
#Creacion archivo reproduccion
reproducciones1 = [reprod1_1,reprod1_2,reprod1_3,reprod1_4]
reproducciones2 = [reprod2_1,reprod2_2,reprod2_3,reprod2_4]
reproducciones3 = [reprod3_1,reprod3_2,reprod3_3,reprod3_4]
reproducciones4 = [reprod4_1,reprod4_2,reprod4_3,reprod4_4]
reproducciones5 = [reprod5_1,reprod5_2,reprod5_3,reprod5_4]
reproducciones = reproducciones1 + reproducciones2 + reproducciones3 + reproducciones4 + reproducciones5
with open('reproduccion.csv', "w", encoding='utf8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames = ['id_reproduccion', 'usuario_id', 'cancion', 'fecha'])
        writer.writeheader()
        writer = csv.writer(csv_file, delimiter=',')
        for line in reproducciones:
            writer.writerow(line)









