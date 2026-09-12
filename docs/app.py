from flask import Flask, render_template, request, jsonify
from frete import calcular_frete

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    data = {}
    if request.is_json:
        data = request.get_json() or {}
    else:
        # Suporta também dados enviados por formulário normal
        data = request.form or {}

    cep = data.get('cep')
    # Suporta tanto 'valor_carrinho' quanto 'valor'
    valor_carrinho = data.get('valor_carrinho')
    if valor_carrinho is None:
        valor_carrinho = data.get('valor')

    try:
        if valor_carrinho is None:
            raise ValueError("Valor de Carringo inválido")
            
        resultado = calcular_frete(cep, valor_carrinho)
        return jsonify(resultado), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": f"Erro inesperado: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
