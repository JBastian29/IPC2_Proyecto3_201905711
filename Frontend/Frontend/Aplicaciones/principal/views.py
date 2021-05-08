from django.shortcuts import render, HttpResponse
import xml.etree.ElementTree as ET
import requests
import xmltodict

# Create your views here.

def inicio(request):
    global nom
    enxml = ""
    l=""
    cont=0
    context={}
    if request.method == 'POST':
        archivo_subido= request.FILES['Cargar_archivo']
        nom=archivo_subido.name
        for linea in archivo_subido:
            if cont==0:
                l=str(linea[:len(linea)-2])
                cont=cont+1
            else:
                l = str(linea[1:])
                l = str(l[:len(linea) - 1])
            enxml=str(enxml)+str(l)+"\n"
        context['todoxml'] = enxml
        #------------- PARA ENVIAR EL XML DESDE FRONT A BACK-----------------

        archivo_xml = open(nom, "r")
        lectura_xml = archivo_xml.read()
        # HACE LA CONSULTA ENVIANDO EL ARCHIVO XML
        r = requests.get('http://127.0.0.1:5000/exml',data=lectura_xml)
        n = requests.get('http://127.0.0.1:5000/nxml', data=nom)

        # string_xml = r.content
        # tree = ET.fromstring(string_xml)
        # a = str(ET.dump(tree))

        # dict_data = xmltodict.parse(r.content)
        # tree = ET.fromstring(r.content)

    return render(request,'index.html',context)


def ejemplo1(request):
    global nom
    # LEE EL ARCHIVO XML
    archivo_xml = open("country_data_frontend.xml", "r")
    lectura_xml = archivo_xml.read()
    # HACE LA CONSULTA ENVIANDO EL ARCHIVO XML
    r = requests.get('http://127.0.0.1:5000/exml', data=lectura_xml)

    # string_xml = r.content
    # tree = ET.fromstring(string_xml)
    # a = str(ET.dump(tree))

    # dict_data = xmltodict.parse(r.content)
    # tree = ET.fromstring(r.content)
    print(r.text)

    return render(request,'index.html')

def obtenerXML(request):
    pass
