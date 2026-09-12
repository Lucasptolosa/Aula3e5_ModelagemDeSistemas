import pytest
import json
from frete import calcular_frete
from app import app

# --- Testes Unitários de Domínio ---

def test_calcular_frete_sudeste_abaixo_limite():
    # Sudeste: CEP começa com 0, limite R$ 200,00, frete R$ 20,00
    resultado = calcular_frete("01000-000", 150.00)
    assert resultado["regiao"] == "Sudeste"
    assert resultado["frete"] == 20.0
    assert resultado["frete_original"] == 20.0
    assert resultado["limite_frete_gratis"] == 200.0

def test_calcular_frete_sudeste_no_limite():
    # Sudeste: atingiu limite de R$ 200,00 -> frete zerado
    resultado = calcular_frete("01000000", 200.00)
    assert resultado["regiao"] == "Sudeste"
    assert resultado["frete"] == 0.0

def test_calcular_frete_norte_abaixo_limite():
    # Norte: CEP começa com 6, limite R$ 300,00, frete R$ 40,00
    resultado = calcular_frete("68000-000", 250.00)
    assert resultado["regiao"] == "Norte"
    assert resultado["frete"] == 40.0
    assert resultado["limite_frete_gratis"] == 300.0

def test_calcular_frete_norte_no_limite():
    # Norte: atingiu limite de R$ 300,00 -> frete zerado
    resultado = calcular_frete("68000000", 300.00)
    assert resultado["regiao"] == "Norte"
    assert resultado["frete"] == 0.0

def test_calcular_frete_outras_regioes():
    # Nordeste: CEP começa com 4, limite R$ 200,00, frete R$ 30,00
    res_nordeste = calcular_frete("41000-000", 100.00)
    assert res_nordeste["regiao"] == "Nordeste"
    assert res_nordeste["frete"] == 30.0

    # Centro-Oeste: CEP começa com 7, limite R$ 200,00, frete R$ 35,00
    res_co = calcular_frete("70000-000", 100.00)
    assert res_co["regiao"] == "Centro-Oeste"
    assert res_co["frete"] == 35.0

    # Sul: CEP começa com 8, limite R$ 200,00, frete R$ 25,00
    res_sul = calcular_frete("80000-000", 100.00)
    assert res_sul["regiao"] == "Sul"
    assert res_sul["frete"] == 25.0

def test_valor_carrinho_invalido():
    with pytest.raises(ValueError, match="Valor de Carringo inválido"):
        calcular_frete("01000-000", 0.0)

    with pytest.raises(ValueError, match="Valor de Carringo inválido"):
        calcular_frete("01000-000", -50.0)

    with pytest.raises(ValueError, match="Valor de Carringo inválido"):
        calcular_frete("01000-000", "abc")  # tipo inválido

def test_cep_invalido():
    with pytest.raises(ValueError, match="CEP inválido"):
        calcular_frete("123", 100.0)

    with pytest.raises(ValueError, match="CEP inválido"):
        calcular_frete("123456789", 100.0)

    with pytest.raises(ValueError, match="CEP inválido"):
        calcular_frete("12345-67a", 100.0)

    with pytest.raises(ValueError, match="CEP inválido"):
        calcular_frete(None, 100.0)


# --- Testes de Integração da API (Flask) ---

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_flask_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Calculadora de Frete" in response.data

def test_flask_calcular_endpoint_sucesso(client):
    payload = {
        "cep": "01000-000",
        "valor_carrinho": 150.00
    }
    response = client.post('/calcular', 
                             data=json.dumps(payload), 
                             content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["regiao"] == "Sudeste"
    assert data["frete"] == 20.0

def test_flask_calcular_endpoint_frete_gratis(client):
    payload = {
        "cep": "01000-000",
        "valor_carrinho": 250.00
    }
    response = client.post('/calcular', 
                             data=json.dumps(payload), 
                             content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["regiao"] == "Sudeste"
    assert data["frete"] == 0.0

def test_flask_calcular_endpoint_erro_cep(client):
    payload = {
        "cep": "12345",
        "valor_carrinho": 150.00
    }
    response = client.post('/calcular', 
                             data=json.dumps(payload), 
                             content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["erro"] == "CEP inválido"

def test_flask_calcular_endpoint_erro_valor_carrinho(client):
    payload = {
        "cep": "01000-000",
        "valor_carrinho": -10.0
    }
    response = client.post('/calcular', 
                             data=json.dumps(payload), 
                             content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["erro"] == "Valor de Carringo inválido"
