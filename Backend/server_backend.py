from flask import Flask, render_template
from flask import request
from flask import jsonify
from flask import Response
from flask_restful import Api
import re
from Usuario import *
from Estadistica import *

import xml.etree.ElementTree as ET
import base64
import xmltodict

app = Flask(__name__)

@app.route('/prueba')
def index():
    return 'Server_Backend Funcionado con Flask expuesto en el puerto: {}'



@app.route('/oxml', methods=['GET'])
def obtener_xml():
    # print(request.data)
    # LEE EL ARCHIVO XML
    tree = ET.parse('country_data_backend.xml')
    root = tree.getroot()
    # MODIFICA ELEMENTO EN EL XML
    print(root[0][0].text)
    root[0][0].text = '5'
    print(root[0][0].text)
    # print (root)
    # ESCRIBE EL XML MODIFICADO
    tree.write('country_data_backend.xml')
    # LEE EL ARCHIVO XML MODIFICADO
    archivo_xml = open("country_data_backend.xml", "r")
    lectura_xml = archivo_xml.read()
    # RETORNA EL ARCHIVO XML MODIFICADO EN FORMATO XML
    # print(lectura_xml)
    return Response(lectura_xml, mimetype='text/xml')


@app.route("/exml", methods=['GET', 'POST'])
def parse_xml():
    # RECIBE EL PARAMETRO XML
    xml_data = request.data
    # ESCRIBE EL XML RECIBIDO
    archivo_xml = open("Desdefrontend.xml", "wb")
    archivo_xml.write(xml_data)

    #content_dict = xmltodict.parse(xml_data)
    #print(jsonify(content_dict))
    #return jsonify(content_dict)
    #return ('exito')

    return Response(xml_data, mimetype='text/xml')

@app.route("/nxml", methods=['GET'])
def nombre_xml():
    global nom
    nom = request.data
    return nom


@app.route("/txml", methods=['GET'])
def modificarXML():
    global nom
    global fechas
    global cErrores
    global festadistica
    global na
    global ne
    linea=[]
    eventos=[]
    event = []
    cErrores=[]
    afec=""
    canti = []
    eventosM=[] #Eventos modificados

    # Expresiones regulares
    expfecha = re.compile(r'^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$')
    expemail = re.compile(r'([\w\.]+)@([\w\.]+)(\.[\w\.]+)')
    experror=re.compile(r'([0-9]{5,5})')

    with open("Desdefrontend.xml", 'r') as archivo:
        lineas = archivo.read().splitlines()
        for l in lineas:  # Con este for leo el archivo
            n = l.replace("\t", "").replace("Guatemala,","")
            linea.append(n)
            if l == "\t</EVENTO>":
                eventos.append(linea)
                linea = []
            elif l == "<EVENTOS>":
                linea.pop()


        for x in range(len(eventos)):
            for y in range(len(eventos[x])):
                if y == 3:                                          #Con este for entro a la casilla donde estan los correos de los afectados
                    c = eventos[x][y].split(",")                    #Espliteo los afectados cuando son mas de 1
                    for co in c:                                    #Con este for entro a la nueva lista de afectados y los recorro
                        corr = re.search(expemail, co.strip())      #Corroboro con la expresion regular
                        if corr:
                            afec = afec + "," + corr.group(0)      #Si son iguales, concateno los correos
                    afec=afec[1:]
                    event.append(afec)                              #Envio los correos a mi lista
                    afec=""
                else:
                    correo = re.search(expemail, eventos[x][y].strip())
                    fecha = re.search(expfecha, eventos[x][y].strip())
                    error = re.search(experror, eventos[x][y].strip())
                    if fecha:
                        event.append(fecha.group(0))
                    if correo:
                        event.append(correo.group(0))
                    if error:
                        event.append(error.group(0))
            eventosM.append(event)
            event=[]

        final=[]
        for a in range(len(eventosM)):
            final.append(Usuario(eventosM[a][0],eventosM[a][1],eventosM[a][2].split(","),eventosM[a][3]))
            #print(str(final[a].fecha) + str(final[a].afectados))

        fechas=[]
        for fe in range(len(final)):
            fechas.append(final[fe].fecha)
        fechas=sorted(list(set(fechas)))


        esta=[]
        testa=[]
        tempfinal=final
        cfechas=""
        cafect=""
        cerror=""

        for n in range(len(fechas)):
            esta.append(tempfinal[n].fecha)
            for m in range(len(final)):
                if tempfinal[m].fecha == fechas[n]:
                    cfechas = (cfechas + "," + tempfinal[m].correo).strip()
                    for a in tempfinal[m].afectados:
                        cafect = (cafect + "," + a).strip()
                    cerror = (cerror + "," + tempfinal[m].error).strip()
            cfechas = cfechas[1:]
            cafect = cafect[1:]
            cerror=cerror[1:]
            esta.append(cfechas)
            esta.append(cafect)
            esta.append(cerror)
            cfechas=""
            cafect=""
            cerror=""
            testa.append(esta)
            esta=[]

        festadistica = []
        for a in range(len(testa)):
            festadistica.append(Estadistica(testa[a][0].strip(), testa[a][1].strip().split(","), testa[a][2].strip().split(","), testa[a][3].strip().split(",")))

        errores=[]


        cont=0
        f = open("estadisticas.xml", 'w')
        f.write('<ESTADISTICAS>\n')
        for k in range(len(festadistica)):
            f.write('\t<ESTADISTICA>\n')
            f.write('\t\t<FECHA>' + festadistica[k].fecha + '</FECHA>\n')
            f.write('\t\t<CANTIDAD_MENSAJES>' + str(len(festadistica[k].usuarios)) + '</CANTIDAD_MENSAJES>\n')
            f.write('\t\t<REPORTADO POR>\n')

            for u in festadistica[k].usuarios:
                f.write('\t\t\t<USUARIO>\n')
                f.write('\t\t\t\t<EMAIL>' + u+ '</EMAIL>\n')
                f.write('\t\t\t\t<CANTIDAD_MENSAJES>' + '1' + '</CANTIDAD_MENSAJES>\n')
                f.write('\t\t\t</USUARIO>\n')

            f.write('\t\t</REPORTADO POR>\n')
            f.write('\t\t<AFECTADOS>\n')

            for aff in festadistica[k].afectados:
                f.write('\t\t\t<AFECTADO>' + aff + '</AFECTADO>\n')

            f.write('\t\t</AFECTADOS>\n')
            f.write('\t\t<ERRORES>\n')
            f.write('\t\t\t<ERROR>\n')

            errores = sorted(list(set(festadistica[k].error)))
            for ax in range(len(errores)):
                for ay in range(len(festadistica[k].error)):
                    if errores[ax] == festadistica[k].error[ay]:
                        cont = cont + 1
                canti.append(str(cont))
                cErrores.append(errores[ax])
                f.write('\t\t\t\t<CODIGO>' + errores[ax] + '</CODIGO>\n')
                f.write('\t\t\t\t<CANTIDAD_MENSAJES>' + str(cont) + '</CANTIDAD_MENSAJES>\n')
                cont=0

            f.write('\t\t\t</ERROR>\n')
            f.write('\t\t</ERRORES>\n')

            f.write('\t</ESTADISTICA>\n')
        f.write('</ESTADISTICAS>\n')
        f=open('estadisticas.xml','r')

        na = open("gra1.txt", 'w')
        for a in cErrores:
            na.write(str(a) + "\n")

        ne = open("gra11.txt", 'w')
        for a in canti:
            ne.write(str(a) + "\n")



    return Response(response=f.readlines(),mimetype='text/plain',content_type='text/plain')

@app.route("/egraph", methods=['GET'])
def graficauno():
    global fechas
    global cErrores
    global festadistica
    global na
    global ne
    festadistica=[]
    cErrores=[]
    canti=[]
    cont=0
    na = open('gra1.txt', 'r')
    ne = open('gra11.txt', 'r')
    return Response(response=na.readlines(),mimetype='text/plain',content_type='text/plain')
    return Response(response=ne.readlines(),mimetype='text/plain',content_type='text/plain')

if __name__ == '__main__':
    app.run(debug=True)