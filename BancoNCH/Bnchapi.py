from flask import Flask, request, jsonify,Blueprint
import requests

app = Flask(__name__)

main = Blueprint('Bnchapi', __name__)


def obtener_tipo_de_cambio():
    try:
        url = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=nicon607@gmail.com&pass=Elnicox1&firstdate=2024-05-20&timeseries= &function=GetSeries"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            series = data.get('Series')
            if series:
                obs = series.get('Obs')
                if obs:
                    tipo_de_cambio = float(obs[0].get('value')) 
                    return tipo_de_cambio
            return None
        else:
            return None
    except Exception as ex:
        print("Error al obtener el tipo de cambio:", ex)
        return None

def convertir_a_dolares(json_input):
    try:
        valor_producto = json_input.get('valor')
        tipo_de_cambio = obtener_tipo_de_cambio()
        if tipo_de_cambio is not None:
            valor_en_dolares = float(valor_producto) / tipo_de_cambio
            valor_en_dolares_redondeado = round(valor_en_dolares, 1)
            return valor_en_dolares_redondeado
        else:
            print("No se pudo obtener el tipo de cambio.")
            return None
    except Exception as ex:
        print("Error al convertir a dólares:", ex)
        return None


@main.route('/convertir_a_dolares', methods=['POST'])
def convertir_a_dolares_Postman():
    try:
        data = request.json
        if data is None:
            return jsonify({"error": "Se requiere un JSON válido en el cuerpo de la solicitud"}), 400
        valor_en_dolares = convertir_a_dolares(data)
        if valor_en_dolares is not None:
            return jsonify({"valor_en_dolares": valor_en_dolares})
        else:
            return jsonify({"error": "No se pudo obtener el valor en dólares del producto."}), 500
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500
