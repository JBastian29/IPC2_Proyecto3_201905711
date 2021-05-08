from flask import Flask, render_template
from flask import request
from flask import jsonify
from flask import Response
from flask_restful import Api

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
    archivo_xml = open("prueba_Desdefrontend.xml", "wb")
    archivo_xml.write(xml_data)

    #content_dict = xmltodict.parse(xml_data)
    #print(jsonify(content_dict))
    #return jsonify(content_dict)
    #return ('exito')

    return Response(xml_data, mimetype='text/xml')

@app.route("/nxml", methods=['GET'])
def nombre_xml():
    nom = request.data
    print(str(nom))
    print("jale bien todo paps")
    return nom


if __name__ == '__main__':
    app.run(debug=True)