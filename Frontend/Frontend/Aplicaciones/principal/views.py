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
        xmlinicio = open(nom, "r")
        for linea in xmlinicio:
            enxml=str(enxml)+str(linea)
        context['todoxml'] = enxml

        #------------- PARA ENVIAR EL XML DESDE FRONT A BACK-----------------

        archivo_xml = open(nom, "r")
        lectura_xml = archivo_xml.read()
        # HACE LA CONSULTA ENVIANDO EL ARCHIVO XML
        r = requests.get('http://127.0.0.1:5000/exml',data=lectura_xml)
        n = requests.get('http://127.0.0.1:5000/nxml', data=nom)


    return render(request,'index.html',context)



def obtenerXML(request):
    global nom
    enxml = ""
    enxmli = ""
    l = ""
    cont = 0
    context = {}
    context2 = {}
    if request.method == 'GET':
        archivo_xmls=open("estadisticas.xml","w")
        r = requests.get('http://127.0.0.1:5000/txml')
        archivo_xmls.write(r.text)
        archivo_xmls.close()

        xmlfinal = open("estadisticas.xml","r")

        for linea in xmlfinal:
            enxml = str(enxml) + str(linea)
        context2['todoxml2'] = enxml

        xmlinicio = open(nom, "r")
        for line in xmlinicio:
            enxmli = str(enxmli) + str(line)
        context['todoxml'] = enxmli

    return render(request, 'index.html', context2)

def graficauno(request):
    context={}
    erros=[]
    if request.method == 'GET':
        archivo_xmls = open("gra11.txt", "w")
        r = requests.get('http://127.0.0.1:5000/egraph')
        archivo_xmls.write(r.text)
        archivo_xmls.close()

        xmlfinal = open("gra11.txt", "r")

        for linea in xmlfinal:
            erros.append(int(linea))
        context['errores']=erros
    return render(request, 'grafica1.html',context)


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
