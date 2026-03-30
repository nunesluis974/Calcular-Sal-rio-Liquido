from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "API rodando"

@app.route("/calcular", methods=["POST"])
def calcular():
    dados = request.json

    salario = dados["salario"]
    descontos = dados["descontos"]
    adicionais = dados["adicionais"]

    # INSS
    if salario <= 1621:
        inss = salario * 0.075
    elif salario <= 2902.84:
        inss = (1621 * 0.075) + ((salario - 1621) * 0.09)
    elif salario <= 4354.27:
        inss = (1621 * 0.075) + ((2902.84 - 1621) * 0.09) + ((salario - 2902.84) * 0.12)
    elif salario <= 8475.55:
        inss = (1621 * 0.075) + ((2902.84 - 1621) * 0.09) + ((4354.27 - 2902.84) * 0.12) + ((salario - 4354.27) * 0.14)
    else:
        inss = (1621 * 0.075) + ((2902.84 - 1621) * 0.09) + ((4354.27 - 2902.84) * 0.12) + ((8475.55 - 4354.27) * 0.14)

    # IRRF
    base = salario + adicionais - inss - descontos

    if base <= 2259.20:
        irrf = 0
    elif base <= 2826.65:
        irrf = (base * 0.075) - 169.44
    elif base <= 3751.05:
        irrf = (base * 0.15) - 381.44
    elif base <= 4664.68:
        irrf = (base * 0.225) - 662.77
    else:
        irrf = (base * 0.275) - 896.00

    if irrf < 0:
        irrf = 0

    liquido = salario + adicionais - inss - irrf - descontos

    return jsonify({
        "inss": inss,
        "irrf": irrf,
        "liquido": liquido
    })

app.run(host="0.0.0.0", port=5000, debug=True)