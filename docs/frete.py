import re

def validar_cep(cep: str) -> str:
    """
    Valida e normaliza o CEP. Retorna apenas os dígitos se for válido.
    Caso contrário, lança ValueError("CEP inválido").
    """
    if not isinstance(cep, str):
        raise ValueError("CEP inválido")
    
    # Remove hífens e espaços
    cep_limpo = re.sub(r'[\s-]', '', cep)
    
    # Verifica se tem exatamente 8 dígitos numéricos
    if not cep_limpo.isdigit() or len(cep_limpo) != 8:
        raise ValueError("CEP inválido")
        
    return cep_limpo

def obter_regiao_e_valor_base(cep_limpo: str) -> tuple[str, float]:
    """
    Retorna a região correspondente ao CEP e o valor base do frete.
    """
    primeiro_digito = cep_limpo[0]
    
    # Mapeamento do primeiro dígito do CEP para Região e Valor Base do Frete
    mapeamento = {
        '0': ('Sudeste', 20.0),
        '1': ('Sudeste', 20.0),
        '2': ('Sudeste', 20.0),
        '3': ('Sudeste', 20.0),
        '4': ('Nordeste', 30.0),
        '5': ('Nordeste', 30.0),
        '6': ('Norte', 40.0),
        '7': ('Centro-Oeste', 35.0),
        '8': ('Sul', 25.0),
        '9': ('Sul', 25.0)
    }
    
    if primeiro_digito not in mapeamento:
        raise ValueError("CEP inválido")
        
    return mapeamento[primeiro_digito]

def calcular_frete(cep: str, valor_carrinho: float) -> dict:
    """
    Calcula o valor do frete com base no CEP e no valor do carrinho.
    
    RF-01: Quando o limite regional for atingido, o frete é zerado.
    RF-04: Frete baseado na região obtida do CEP.
    RB-02: Se a região for Norte, limite é R$ 300,00. Demais: R$ 200,00.
    RB-03: Se valor_carrinho <= 0, lança ValueError("Valor de Carringo inválido").
    RB-05: Se CEP for inválido, lança ValueError("CEP inválido").
    """
    # RB-03: Validar valor do carrinho
    try:
        valor_carrinho_float = float(valor_carrinho)
    except (TypeError, ValueError):
        raise ValueError("Valor de Carringo inválido")
        
    if valor_carrinho_float <= 0:
        raise ValueError("Valor de Carringo inválido")
        
    # RB-05: Validar CEP
    cep_limpo = validar_cep(cep)
    
    # RF-04: Obter região e frete base
    regiao, frete_base = obter_regiao_e_valor_base(cep_limpo)
    
    # RB-02: Verificar limite regional de frete grátis
    limite_frete_gratis = 300.0 if regiao == 'Norte' else 200.0
    
    # RF-01: Zera o frete se atingir o limite
    if valor_carrinho_float >= limite_frete_gratis:
        frete_final = 0.0
    else:
        frete_final = frete_base
        
    return {
        "cep": cep,
        "valor_carrinho": valor_carrinho_float,
        "regiao": regiao,
        "frete_original": frete_base,
        "frete": frete_final,
        "limite_frete_gratis": limite_frete_gratis
    }
