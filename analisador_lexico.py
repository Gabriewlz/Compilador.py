import re

# Função para analisar se é um número
def analisa_numero(codigo):
    padrao = r'^\d+(\.\d+)?'
    match = re.match(padrao, codigo)
    if match:
        return match.group(0), 'snúmero'
    return None, None

# Função para analisar se é um identificador
def analisa_identificador(codigo):
    padrao = r'^[a-zA-Z_][a-zA-Z0-9_]*'
    match = re.match(padrao, codigo)
    if match:
        return match.group(0), 'sidentificador'
    return None, None

# Função para analisar operadores relacionais
def analisa_operador_relacional(codigo):
    operadores = {
        '>': 'smaior',
        '>=': 'smaiorig',
        '=': 'sig',
        '<': 'smenor',
        '<=': 'smenorig',
        '!=': 'sdif'
    }
    for op, simbolo in operadores.items():
        if codigo.startswith(op):
            return op, simbolo
    return None, None

# Função para analisar operadores aritméticos
def analisa_operador_aritmetico(codigo):
    operadores = {
        '+': 'smais',
        '-': 'smenos',
        '*': 'smult',
        '/': 'sdiv'  # Corrigido: 'div' para '/'
    }
    for op, simbolo in operadores.items():
        if codigo.startswith(op):
            return op, simbolo
    return None, None

# Função para analisar palavras reservadas
def analisa_palavra_reservada(codigo):
    palavras_reservadas = {
        'programa': 'sprograma',
        'inicio': 'sinício',
        'fim': 'sfim',
        'procedimento': 'sprocedimento',
        'funcao': 'sfuncao',
        'se': 'sse',
        'entao': 'sentao',
        'senao': 'ssenao',
        'enquanto': 'senquanto',
        'faca': 'sfaca',
        'escreva': 'sescreva',
        'leia': 'sleia',
        'var': 'svar',
        'inteiro': 'sinteiro',
        'booleano': 'sbooleano',
        'verdadeiro': 'sverdadeiro',
        'falso': 'sfalso'
    }
    for palavra, simbolo in palavras_reservadas.items():
        if codigo.startswith(palavra):
            return palavra, simbolo
    return None, None

# Função para analisar delimitadores e atribuição corretamente
def analisa_delimitador(codigo):
    if codigo.startswith(':='):
        return ':=', 'satribuição'

    delimitadores = {
        '.': 'sponto',
        ';': 'sponto_virgula',
        ',': 'svírgula',
        '(': 'sabre_parênteses',
        ')': 'sfecha_parênteses',
        ':': 'sdoispontos'
    }
    for delim, simbolo in delimitadores.items():
        if codigo.startswith(delim):
            return delim, simbolo
    return None, None

# Função para analisar operadores lógicos
def analisa_operador_logico(codigo):
    operadores = {
        'e': 'se',
        'ou': 'sou',
        'nao': 'snao'
    }
    for op, simbolo in operadores.items():
        if codigo.startswith(op):
            return op, simbolo
    return None, None

# Função para ignorar comentários
def analisa_comentario(codigo):
    if codigo.startswith('{'):
        comentario_fechado = codigo.find('}')
        if comentario_fechado != -1:
            return codigo[:comentario_fechado + 1], 'scomentario'
        else:
            return codigo, 'erro_comentario_nao_fechado'
    elif codigo.startswith('}'):
        return codigo[0], 'erro_comentario_nao_iniciado'
    return None, None

# Função para análise léxica do código
def analisar_lexico(codigo):
    # Listas de lexemas e símbolos identificados
    lexemas = []
    simbolos = []
    linhas = []
    erros = []

    codigo_linhas = codigo.split("\n")

    for numero_linha, linha in enumerate(codigo_linhas, start=1):
        linha = linha.strip()

        while linha:
            lexema, simbolo = None, None

            # Tenta analisar comentários primeiro
            lexema, simbolo = analisa_comentario(linha)
            if lexema and 'erro' in simbolo:
                erros.append((lexema, numero_linha, "Comentário não fechado" if simbolo == 'erro_comentario_nao_fechado' else "Comentário não iniciado"))
                linha = linha[len(lexema):].strip()
                continue
            elif lexema:
                linha = linha[len(lexema):].strip()
                continue

            # Tenta analisar cada tipo de símbolo
            for analise_funcao in [analisa_palavra_reservada, analisa_numero, analisa_identificador,
                                   analisa_operador_relacional, analisa_operador_aritmetico,
                                   analisa_delimitador, analisa_operador_logico]:
                lexema, simbolo = analise_funcao(linha)
                if lexema:
                    lexemas.append(lexema)
                    simbolos.append(simbolo)
                    linhas.append(numero_linha)
                    linha = linha[len(lexema):].strip()
                    break

            if not lexema:
                erros.append((linha[0], numero_linha, f"Caractere inválido '{linha[0]}'"))
                linha = linha[1:].strip()

    return lexemas, simbolos, linhas, erros