class Token:
    def __init__(self, lexema, simbolo, linha):
        self.lexema = lexema
        self.simbolo = simbolo
        self.linha = linha

# Função para obter o próximo token da lista
def proximo_token(tokens, i):
    return tokens[i] if i < len(tokens) else None

# Função para verificar se o token atual corresponde ao esperado
def verifica_token(token, simbolo_esperado):
    return token and token.simbolo == simbolo_esperado

# Função para analisar o programa
def analisa_programa(tokens, i, output_text):
    token = proximo_token(tokens, i)
    if verifica_token(token, 'sprograma'):
        i += 1
        token = proximo_token(tokens, i)
        if verifica_token(token, 'sidentificador'):
            i += 1
            token = proximo_token(tokens, i)
            if verifica_token(token, 'sponto_virgula'):
                i += 1
                i = analisa_bloco(tokens, i, output_text)
                if i == -1:
                    return "ERRO"
                token = proximo_token(tokens, i)
                if verifica_token(token, 'sponto'):
                    i += 1
                    if i == len(tokens):
                        return "Sucesso"
                    else:
                        output_text.insert("end", f"Erro: Token inesperado na linha {token.linha}\n")
                        return "ERRO"
                else:
                    output_text.insert("end", f"Erro: Token esperado '.' na linha {token.linha}\n")
                    return "ERRO"
            else:
                output_text.insert("end", f"Erro: Token esperado ';' na linha {token.linha}\n")
                return "ERRO"
        else:
            output_text.insert("end", f"Erro: Token esperado 'identificador' na linha {token.linha}\n")
            return "ERRO"
    else:
        output_text.insert("end", f"Erro: Token esperado 'programa' na linha {token.linha}\n")
        return "ERRO"

def analisa_bloco(tokens, i, output_text):
    # token = proximo_token(tokens, i)  # Remova essa linha
    # if verifica_token(token, 'sinicio'):  # Remova essa linha
        # i += 1  # Remova essa linha
        i = analisa_et_variaveis(tokens, i, output_text)
        if i == -1:
            return -1
        i = analisa_subrotinas(tokens, i, output_text)
        if i == -1:
            return -1
        i = analisa_comandos(tokens, i, output_text)
        if i == -1:
            return -1
        return i
    # else:
        # output_text.insert("end", f"Erro: Token esperado 'inicio' na linha {token.linha}\n")
        # return "ERRO" 

def analisa_et_variaveis(tokens, i, output_text):
    token = proximo_token(tokens, i)
    if verifica_token(token, 'svar'):
        i += 1
        token = proximo_token(tokens, i)
        if verifica_token(token, 'sidentificador'):
            while verifica_token(token, 'sidentificador'):
                i = analisa_variaveis(tokens, i, output_text)
                if i == -1:
                    return -1
                token = proximo_token(tokens, i)
                if verifica_token(token, 'sponto_virgula'):
                    i += 1
                    token = proximo_token(tokens, i)
                else:
                    output_text.insert("end", f"Erro: Token esperado ';' na linha {token.linha}\n")
                    return "ERRO"
            return i
        else:
            output_text.insert("end", f"Erro: Token esperado 'identificador' na linha {token.linha}\n")
            return "ERRO"
    return i  # Se não encontrar 'svar', continua a análise

def analisa_variaveis(tokens, i, output_text):
    token = proximo_token(tokens, i)
    if verifica_token(token, 'sidentificador'):
        i += 1
        while verifica_token(token, 'svírgula') or verifica_token(token, 'sdoispontos'):
            if verifica_token(token, 'svírgula'):
                i += 1
                token = proximo_token(tokens, i)
                if verifica_token(token, 'sdoispontos'):
                    output_text.insert("end", f"Erro: Token inesperado ':' na linha {token.linha}\n")
                    return "ERRO"
                elif verifica_token(token, 'svírgula'):  # Verificação para duas vírgulas seguidas
                    output_text.insert("end", f"Erro: Duas vírgulas seguidas na linha {token.linha}\n")
                    return "ERRO"
            else:
                i += 1
                token = proximo_token(tokens, i)
                if verifica_token(token, 'sdoispontos'):
                    i += 1
                    token = proximo_token(tokens, i)
                    i = analisa_tipo(tokens, i, output_text)
                    if i == -1:
                        return -1
                    return i
                else:
                    output_text.insert("end", f"Erro: Token esperado ':' na linha {token.linha}\n")
                    return "ERRO"
        return i
    else:
        output_text.insert("end", f"Erro: Token esperado 'identificador' na linha {token.linha}\n")
        return "ERRO"

def analisa_tipo(tokens, i, output_text):
    token = proximo_token(tokens, i)
    if verifica_token(token, 'sinteiro') or verifica_token(token, 'sbooleano'):
        i += 1
        return i
    else:
        output_text.insert("end", f"Erro: Tipo inválido na linha {token.linha}\n")
        return "ERRO"

def analisa_comandos(tokens, i, output_text):
    # token = proximo_token(tokens, i)  # Remova essa linha
    # if verifica_token(token, 'sinicio'):  # Remova essa linha
        # i += 1  # Remova essa linha
        i = analisa_comando_simples(tokens, i, output_text)
        if i == -1:
            return -1
        while not verifica_token(token, 'sfim'):
            token = proximo_token(tokens, i)
            if verifica_token(token, 'sponto_virgula'):
                i += 1
                token = proximo_token(tokens, i)
                if not verifica_token(token, 'sfim'):
                    i = analisa_comando_simples(tokens, i, output_text)
                    if i == -1:
                        return -1
            else:
                output_text.insert("end", f"Erro: Token esperado ';' na linha {token.linha}\n")
                return "ERRO"
        i += 1
        return i
    # else:
        # output_text.insert("end", f"Erro: Token esperado 'inicio' na linha {token.linha}\n")
        # return "ERRO"

def analisa_comando_simples(tokens, i, output_text):
    token = proximo_token(tokens, i)
    if verifica_token(token, 'sidentificador'):
        i = analisa_atrib_chprocedimento(tokens, i, output_text)
        if i == -1:
            return -1
        return i
    elif verifica_token(token, 'sse'):
        i = analisa_se(tokens, i, output_text)
        if i == -1:
            return -1
        return i
    elif verifica_token(token, 'senquanto'):
        i = analisa_enquanto(tokens, i, output_text)
        if i == -1:
            return -1
        return i
    elif verifica_token(token, 'sleia'):
        i = analisa_leia(tokens, i, output_text)
        if i == -1:
            return -1
        return i
    elif verifica_token(token, 'sescreva'):
        i = analisa_escreva(tokens, i, output_text)
        if i == -1:
            return -1
        return i
    # elif verifica_token(token, 'sinicio'):  # Remova essa linha
        # i = analisa_comandos(tokens, i, output_text)  # Remova essa linha
        # if i == -1:  # Remova essa linha
            # return -1  # Remova essa linha
        # return i  # Remova essa linha
    else:
        output_text.insert("end", f"Erro: Comando inválido na linha {token.linha}\n")
        return "ERRO"

def analisa_atrib_chprocedimento(tokens, i, output_text):
    token = proximo_token(tokens, i)
    i += 1
    token = proximo_token(tokens, i)
    if verifica_token(token, 'satribuição'):
        i = analisa_atribuicao(tokens, i, output_text)
        if i == -1:
            return -1
        return i
    else:
        i = chamada_procedimento(tokens, i - 1, output_text)
        if i == -1:
            return -1
        return i

def analisa_leia(tokens, i, output_text):
    token = proximo_token(tokens, i)
    i += 1
    token = proximo_token(tokens, i)
    if verifica_token(token, 'sabre_parenteses'):
        i += 1
        token = proximo_token(tokens, i)
        if verifica_token(token, 'sidentificador'):
            i += 1
            token = proximo_token(tokens, i)
            if verifica_token(token, 'sfecha_parenteses'):
                i += 1
                return i
            else:
                output_text.insert("end", f"Erro: Token esperado ')' na linha {token.linha}\n")
                return "ERRO"
        else:
            output_text.insert("end", f"Erro: Token esperado 'identificador' na linha {token.linha}\n")
            return "ERRO"
    else:
        output_text.insert("end", f"Erro: Token esperado '(' na linha {token.linha}\n")
        return "ERRO"

def analisa_escreva(tokens, i, output_text):
    token = proximo_token(tokens, i)
    i += 1
    token = proximo_token(tokens, i)
    if verifica_token(token, 'sabre_parenteses'):
        i += 1
        token = proximo_token(tokens, i)
        if verifica_token(token, 'sidentificador'):
            i += 1
            token = proximo_token(tokens, i)
            if verifica_token(token, 'sfecha_parenteses'):
                i += 1
                return i
            else:
                output_text.insert("end", f"Erro: Token esperado ')' na linha {token.linha}\n")
                return "ERRO"
        else:
            output_text.insert("end", f"Erro: Token esperado 'identificador' na linha {token.linha}\n")
            return "ERRO"
    else:
        output_text.insert("end", f"Erro: Token esperado '(' na linha {token.linha}\n")
        return "ERRO"

def analisa_enquanto(tokens, i, output_text):
    token = proximo_token(tokens, i)
    i += 1
    i = analisa_expressao(tokens, i, output_text)
    if i == -1:
        return -1
    token = proximo_token(tokens, i)
    if verifica_token(token, 'sfaca'):
        i += 1
        i = analisa_comando_simples(tokens, i, output_text)
        if i == -1:
            return -1
        return i
    else:
        output_text.insert("end", f"Erro: Token esperado 'faca' na linha {token.linha}\n")
        return "ERRO"

def analisa_se(tokens, i, output_text):
    token = proximo_token(tokens, i)
    i += 1
    i = analisa_expressao(tokens, i, output_text)
    if i == -1:
        return -1
    token = proximo_token(tokens, i)
    if verifica_token(token, 'sentao'):
        i += 1
        i = analisa_comando_simples(tokens, i, output_text)
        if i == -1:
            return -1
        token = proximo_token(tokens, i)
        if verifica_token(token, 'ssenao'):
            i += 1
            i = analisa_comando_simples(tokens, i, output_text)
            if i == -1:
                return -1
            return i
        else:
            return i
    else:
        output_text.insert("end", f"Erro: Token esperado 'entao' na linha {token.linha}\n")
        return "ERRO"

def analisa_expressao(tokens, i, output_text):
    # Adicione regras para analisar expressões aqui
    return i  # Por enquanto, retorna o índice sem analisar a expressão

def analisa_subrotinas(tokens, i, output_text):
    # Adicione regras para analisar subrotinas aqui
    return i  # Por enquanto, retorna o índice sem analisar as subrotinas

def analisa_atribuicao(tokens, i, output_text):
    # Adicione regras para analisar atribuições aqui
    return i  # Por enquanto, retorna o índice sem analisar atribuições

def chamada_procedimento(tokens, i, output_text):
    # Adicione regras para analisar chamadas de procedimento aqui
    return i  # Por enquanto, retorna o índice sem analisar chamadas de procedimento

# Função para analisar o código sintaticamente
def analisar_sintaticamente(lexemas, simbolos, linhas, output_text):
    tokens = [Token(lexemas[i], simbolos[i], linhas[i]) for i in range(len(lexemas))]
    return analisa_programa(tokens, 0, output_text)