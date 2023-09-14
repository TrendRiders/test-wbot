from django.shortcuts import render
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from pymongo import MongoClient
import time
import csv
import requests
import os
admin_sid = "AC7bf48046af90d69f4ab9c554d4cc17fc"
admin_auth = "8f99941000cb99f38c43be1531989673"
client = Client(admin_sid, admin_auth)


MONGO_URI = 'mongodb://localhost'
mongo_client = MongoClient(MONGO_URI)

@csrf_exempt
def bot(request):

    message = request.POST["Body"]
    sender_name = request.POST["ProfileName"]
    sender_number = request.POST["From"]
    
    

    user_id = sender_number

    if message == "/reset123":
        msg_response = ""
        db_codes = mongo_client['test_codes']
        codes = db_codes['codes']
        code_track = db_codes['track']
        track = code_track.find_one({"_id": "counter"})           
        if track is None:
            code_track.insert_one({"_id": "counter", "count":-1})
        else:
            code_track.update_one({"_id": "counter"}, {"$set": { "count":-1}})
            print("counter reseted to 0")

        track1 = code_track.find_one({"_id": "counter"})

        msg_response += "*Counter reseteado a :* " + str(track1["count"]+1) + "\n"

        with open("./codes.csv", 'r') as file:
            csvreader = csv.reader(file)
            counter = 0
            for row in csvreader:
                cd = row[0]
                code = codes.find_one({"_id": counter})
                if code is not None:
                    #print(code)
                    codes.update_one({"_id": counter}, {"$set": { "used_by": ""}})
                if code is None:
                    codes.insert_one({"_id": counter, "used_by": "", "code_id" : cd})
                counter += 1

        msg_response += "*Codigos disponibles:* 1000"
        client.messages.create(from_= "whatsapp:+14155238886",
                                body = msg_response,
                                to = user_id) 
    
    
    elif message in ['m', 'M']:
        db_codes = mongo_client['test_codes']
        codes = db_codes['codes']
        code_track = db_codes['track']
        filtro = {"_id": "counter"}
        actualizaciones = {"$inc": {"count": 1}}
        track = code_track.find_one_and_update(filtro, actualizaciones, return_document=True)

        filtro = {"_id": track['count']}
        actualizaciones = {"$set": {"used_by": sender_name}}
        codigo_encontrado = codes.find_one_and_update(filtro, actualizaciones, return_document=True)
        
        client.messages.create(from_= "whatsapp:+14155238886",
                                body = codigo_encontrado['code_id'],
                                to = user_id)


    elif message == '/show':
        db_codes = mongo_client['test_codes']
        codes = db_codes['codes']
        code_track = db_codes['track']
        filtro = {"_id": "counter"}
        track = code_track.find_one(filtro)

        msg_response = "Codigos usados: " + str(track['count']+1) + "\n"

        for i in range(0,track['count']+1):
            filtro = {"_id": i}
            code_doc = codes.find_one(filtro)
            msg_response += code_doc['code_id'] + " : " + code_doc['used_by'] + "\n"
        
        print(msg_response)

        # client.messages.create(from_= "whatsapp:+14155238886",
        #                         body = msg_response,
        #                         to = user_id)
    
    else:
        client.messages.create(from_= "whatsapp:+14155238886",
                                body = "*COMANDOS:*\n/show : muestra los codigos usados y usuarios asignados\n/reset : reinicia el sistema\nm : pedir codigo",
                                to = user_id)
        


    return HttpResponse("hello")

# @csrf_exempt
# def bot(request):

#     message = request.POST["Body"]
#     sender_name = request.POST["ProfileName"]
#     sender_number = request.POST["From"]

#     user = users.find_one({"_id": sender_number})
    
#     if user is None:
#         users.insert_one({"_id": sender_number, "name": sender_name , "complete_name":"-", "ID":"-", "bday": "-", 'complete_data':0,"stage": 1})
#         user = users.find_one({"_id": sender_number})
#         client.messages.create(from_= "whatsapp:+14155238886",
#                                 body="*Hola!*\nBienvenido a *La Molipromo 2023*\nPara participar ten a la mano tu empaque ABIERTO de Fideos *MOLITALIA* el cual lleva el sticker Amarillo de la Molipromo.\nQué deseas hacer? Escribe \n1) Participar\n2) Consultas",
#                                 to = sender_number)
         
#         return HttpResponse("hello")
    

#     stage = user['stage']
#     user_id = user['_id']

#     if stage == 0:
#         client.messages.create(from_= "whatsapp:+14155238886",
#                                 body="*Hola!*\nBienvenido a *La Molipromo 2023*\nPara participar ten a la mano tu empaque ABIERTO de Fideos *MOLITALIA* el cual lleva el sticker Amarillo de la Molipromo.\nQué deseas hacer? Escribe \n1) Participar\n2) Consultas",
#                                 to = sender_number)
#         users.update_one({"_id": user_id}, {"$set": { "stage":1 }})     

#     if stage == 1:
#         if message in ["1","participar"]:
#             client.messages.create(from_= "whatsapp:+14155238886",
#                                 body = "Puedes participar desde el: \n*1 de junio hasta el 31 de agosto del 2023*\nLee los términos y condiciones en el siguiente link:\ntyc.com\n*Aceptas los términos y condiciones?*\n1) Si\n2) No" ,
#                                 to = user_id)
#             users.update_one({"_id": user_id}, {"$set": { "stage":2 }})

#         elif message in ["2","consultas"]:
#             client.messages.create(from_= "whatsapp:+14155238886",
#                                 body = "Mensaje de consulta",
#                                 to = user_id)
#             users.update_one({"_id": user_id}, {"$set": { "stage":0 }})
        
#         else: 
#             client.messages.create(from_= "whatsapp:+14155238886",
#                                 body = "Por favor, ingresa una respuesta válida.",
#                                 to = user_id)


#     if stage == 2:
#         if user['complete_data'] == 1:
#             if message in ['si']:
#                 stage = 5
#             elif message in ['no']:
#                 client.messages.create(from_= "whatsapp:+14155238886",
#                                         body = "Gracias por participar!",
#                                         to = user_id) 
#                 users.update_one({"_id": user_id}, {"$set": { "stage":0 }})
            
#         else:
#             if message in ['si']:
#                 client.messages.create(from_= "whatsapp:+14155238886",
#                                         body = "Por favor, escribe tus:\n*Nombres y apellidos completos.*",
#                                         to = user_id) 
#                 users.update_one({"_id": user_id}, {"$set": { "stage":3 }})
#             elif message in ['no']:
#                 client.messages.create(from_= "whatsapp:+14155238886",
#                                         body = "Gracias por participar!",
#                                         to = user_id) 
#                 users.update_one({"_id": user_id}, {"$set": { "stage":0 }})
#             else:
#                 client.messages.create(from_= "whatsapp:+14155238886",
#                                         body = "Por favor, ingresa una respuesta válida.",
#                                         to = user_id) 

#     if stage == 3:
#         users.update_one({"_id": user_id}, {"$set": { "complete_name": message }})
#         client.messages.create(from_= "whatsapp:+14155238886",
#                                 body = "Por favor, escribe tu:\n*DNI o Carnet de Extranjería*",
#                                 to = user_id) 
#         users.update_one({"_id": user_id}, {"$set": { "stage":4 }})

#     if stage == 4:
#         users.update_one({"_id": user_id}, {"$set": { "ID": message }})
#         client.messages.create(from_= "whatsapp:+14155238886",
#                                 body = "Por favor, escribe tu:\n*Fecha de nacimiento en formato DD/MM/AAAA*\nEjemplo: 31/05/1998",
#                                 to = user_id) 
#         users.update_one({"_id": user_id}, {"$set": { "stage":5 }})

#     if stage == 5:
#         print(message)
#         users.update_one({"_id": user_id}, {"$set": { "bday": message }})

#         client.messages.create(from_= "whatsapp:+14155238886",
#                                 body = "*Muy bien*\nTus participaciones estarán asociadas con estos datos. No será necesario reingresarlos.\n*Tus datos son:*\nNombre: {}\nIdentificación: {}\nFecha de nacimiento: {}\nEn caso seas un ganador, nos comunicaremos a este número.\nEstás de acuerdo con los datos?\n1) Si\n2) Modificar".format(user["complete_name"],user["ID"],message),
#                                 to = user_id) 
#         users.update_one({"_id": user_id}, {"$set": { "stage":6 }})
    
#     if stage == 6:
#         if message in ["1", "si"]:
#             users.update_one({"_id": user_id}, {"$set": { "complete_data":1 }})
#             client.messages.create(from_= "whatsapp:+14155238886",
#                                 body = "Excelente {}, empecemos.\nUbica el código en el *reverso de tu empaque* de fideos *Molitalia*\n*Si ya ubicaste el codigo*\nEscribe:\n*Listo*\n*Si tu producto no tiene un código*\nEscribe\n*Sin código*\n*Si quieres hacer consultas*\nEscribe\n*Consultas*".format(user['complete_name']),
#                                 media_url = "https://lh3.googleusercontent.com/pw/AIL4fc8V5y1m2kJJBZtnxjPqGkHxOKTCrscSnRWTBvlcqj43XBm8Yb0GgDpZgZN19SJVMIlMt0oRfHfUXJQbSeXTT7nbiX-VqiUXbN7lzgA7k6ZYIwlL1H9XD2cRVnbcVxDQWOZuQ7-j6hLia7YWjbRrnMU=w1030-h1032-s-no?authuser=0",
#                                 to = user_id) 

#             print("BDAY",user['bday'])
#             users.update_one({"_id": user_id}, {"$set": { "stage":7 }})
    
#         elif message in ['modificar']:
#             client.messages.create(from_= "whatsapp:+14155238886",
#                                 body = "Por favor. Escribe tus \n*nombres y apellidos completos*",
#                                 to = user_id) 
#             users.update_one({"_id": user_id}, {"$set": { "stage":3 }})

#         else:
#             client.messages.create(from_= "whatsapp:+14155238886",
#                                     body = "Por favor, ingresa una respuesta válida.",
#                                     to = user_id) 
#     if stage == 7:
#         if message in ['listo',"Listo"]:
#             client.messages.create(from_= "whatsapp:+14155238886",
#                                 body = "Escribe tu *código de 10 digitos* que contiene letras y números juntos y sin espacios.",
#                                 to = user_id) 
#             users.update_one({"_id": user_id}, {"$set": { "stage":8 }})

#         elif message in ["sin codigo", "Sin codigo"]:
#             client.messages.create(from_= "whatsapp:+14155238886",
#                                 body = "Para poder asignarte un código, tenemos que validar la fecha de vencimiento de tu producto. \nUbica la fecha de vencimiento en la parte posterior del empaque y escríbela en el chat.\n(ejemplo:130225)",
#                                 media_url = "https://lh3.googleusercontent.com/pw/AIL4fc_YeO1bdyKCSkOAAFa8nISKeZ0ks61PN8xDcJhDdTpDk8C29cMGzIvIdCVd8Y7uXh5PNWXHNQD0IhoRPEUHHJvgo3ovsoVOnbNS2RfoH4bGfDXy-CPVZFPybaSV3n-z58_8U23szG9dsS5vDK1XLzI=w1044-h1030-s-no?authuser=0",
#                                 to = user_id)
#             users.update_one({"_id": user_id}, {"$set": { "stage":13 }})

#         elif message in ["consultas"]:
#             client.messages.create(from_= "whatsapp:+14155238886",
#                                 body = "mensaje consultas",
#                                 to = user_id)
#             users.update_one({"_id": user_id}, {"$set": { "stage":0 }})
#         else:
#             client.messages.create(from_= "whatsapp:+14155238886",
#                                     body = "Por favor, ingresa una respuesta válida.",
#                                     to = user_id) 
    
#     if stage == 8:
#         if message in ['cancelar']:
#             client.messages.create(from_= "whatsapp:+14155238886",
#                                 body = "Gracias por participar",
#                                 to = user_id) 
#             users.update_one({"_id": user_id}, {"$set": { "stage":0 }})
#         else:
#             db_codes = mongo_client['molipromo_codes']
#             codes = db_codes['codes']
#             code = codes.find_one({"_id": message})

#             if code is None:
#                 client.messages.create(from_= "whatsapp:+14155238886",
#                                     body = "El código ingresado no es válido, vuelve a intentar o escribe\n*Cancelar*\npara terminar la operación.",
#                                     to = user_id) 
#             elif code['uses'] < 2:
#                 codes.update_one({"_id": message}, {"$set": { "uses": (code['uses']+1) }})
#                 client.messages.create(from_= "whatsapp:+14155238886",
#                                     body = "Codigo aceptado!",
#                                     to = user_id) 
#                 users.update_one({"_id": user_id}, {"$set": { "stage":9 }})
#                 stage = 9
#             else:
#                 client.messages.create(from_= "whatsapp:+14155238886",
#                                     body = "El código ha sido usado muchas veces, vuelve a intentar o escribe\n*Cancelar*\npara terminar la operación.",
#                                     to = user_id)
            
        

#     if stage == 9:
#         client.messages.create(from_= "whatsapp:+14155238886",
#                                 body = "Para finalizar, mándanos una foto del *empaque abierto* donde se pueda ver claramente el paquete y el código.",
#                                 to = user_id) 
#         client.messages.create(from_= "whatsapp:+14155238886",
#                                 body = "Aquí tienes una foto de referencia",
#                                 media_url = "https://lh3.googleusercontent.com/pw/AIL4fc_qeOwhFxpIP4-oG4B7x5sr2aho4xtIOegAZTScsC_EiVdaOX5oyNuncwxjZ9tmsQaPFSRYiOjSpAkAVkzZzyqPkgv8cc7m3vFIy5F-5glpa11dE4PNd1SplJ-lVRglDkQwYx0MBgGUxvA0FQrUtUQ=w1044-h1028-s-no?authuser=0",
#                                 to = user_id) 
#         users.update_one({"_id": user_id}, {"$set": { "stage":10 }})
    
#     if stage == 10:
#         print(request.POST)
#         if request.POST['NumMedia'] == '0':
#             client.messages.create(from_= "whatsapp:+14155238886",
#                                     body = "Por favor, envía una foto.",
#                                     to = user_id)
#         else:
#             media_url = request.POST['MediaUrl0']
#             username = user_id
#             msg = request.POST['MessageSid']
#             if media_url:
#                 r = requests.get(media_url)
#                 content_type = r.headers['Content-Type']
#                 username = user_id.split(':')[1]  # remove the whatsapp: prefix from the number
#                 if content_type == 'image/jpeg':
#                     filename = f'uploads/{username}/{msg}.jpg'
#                 elif content_type == 'image/png':
#                     filename = f'uploads/{username}/{msg}.png'
#                 elif content_type == 'image/gif':
#                     filename = f'uploads/{username}/{msg}.gif'
#                 else:
#                     filename = None
#                     client.messages.create(from_= "whatsapp:+14155238886",
#                                     body = "Por favor, envía una foto válida.",
#                                     to = user_id) 
#                 if filename:
#                     client.messages.create(from_= "whatsapp:+14155238886",
#                                     body = "Tu participación ha sido registrada con éxito",
#                                     to = user_id) 
#                     users.update_one({"_id": user_id}, {"$set": { "stage":0 }})

#                     if not os.path.exists(f'uploads/{username}'):
#                         os.mkdir(f'uploads/{username}')
#                     with open(filename, 'wb') as f:
#                         f.write(r.content)
                

#     if stage == 11:
        
#         if message in ['si']:
#             client.messages.create(from_= "whatsapp:+14155238886",
#                                 body = "Escribe tu *código de 10 digitos* que contiene letras y números juntos y sin espacios.",
#                                 to = user_id) 
#             users.update_one({"_id": user_id}, {"$set": { "stage":8 }})

#         elif message in ['no']:
#             client.messages.create(from_= "whatsapp:+14155238886",
#                                 body = "Gracias por participar!",
#                                 to = user_id)

#             users.update_one({"_id": user_id}, {"$set": { "stage":0 }})
#         else:
#             client.messages.create(from_= "whatsapp:+14155238886",
#                                         body = "Por favor, ingresa una respuesta válida.",
#                                         to = user_id) 

#     if stage == 13:
#         if message.isdigit():
#             if int(message) > 100000:
#                 client.messages.create(from_= "whatsapp:+14155238886",
#                                     body = "Fecha ingresada correcta. Ahora, escriba el código *HL61* con plumón indeleble en el empaque como se muestra en la imagen.\nA continuación, mande una *única* foto del producto abierto en donde se muestre la fecha de vencimiento y el código escrito. Guíese de la imagen de referencia.",
#                                     media_url = "https://lh3.googleusercontent.com/pw/AIL4fc_qeOwhFxpIP4-oG4B7x5sr2aho4xtIOegAZTScsC_EiVdaOX5oyNuncwxjZ9tmsQaPFSRYiOjSpAkAVkzZzyqPkgv8cc7m3vFIy5F-5glpa11dE4PNd1SplJ-lVRglDkQwYx0MBgGUxvA0FQrUtUQ=w1044-h1028-s-no?authuser=0",
#                                     to = user_id) 
#                 users.update_one({"_id": user_id}, {"$set": { "stage":10 }})
#             else:
#                 client.messages.create(from_= "whatsapp:+14155238886",
#                                     body = "La fecha que ingresaste no es correcta.\nIntenta participar con otro producto.\n*Asegurate de que tenga el sticker amarillo de la promoción.*",
#                                     to = user_id) 

#                 users.update_one({"_id": user_id}, {"$set": { "stage":0 }})
#         else:
#             client.messages.create(from_= "whatsapp:+14155238886",
#                                     body = "Por favor, ingresa una respuesta válida.",
#                                     to = user_id) 
    
#     return HttpResponse("hello")