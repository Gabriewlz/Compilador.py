import tkinter as tk
from tkinter import scrolledtext, filedialog
from analisador_lexico import analisar_lexico
from analisador_sintatico import analisar_sintaticamente

# Função para compilar o código
def compilar():
    codigo = codigo_text.get("1.0", "end-1c")
    lexemas, simbolos, linhas, erros_lexicos = analisar_lexico(codigo)

    output_text.config(state='normal')
    output_text.delete("1.0", "end")

    if erros_lexicos:
        output_text.insert("end", "Erros léxicos encontrados:\n")
        for erro, linha, descricao in erros_lexicos:
            output_text.insert("end", f"Linha {linha}: {descricao} - '{erro}'\n")
    else:
        resultado_sintatico = analisar_sintaticamente(lexemas, simbolos, linhas, output_text)
        if resultado_sintatico == "ERRO":
            output_text.insert("end", f"Erro sintático: {resultado_sintatico}\n")
        else:
            # Mensagem de sucesso
            output_text.insert("end", "Compilado com sucesso!\n")

    output_text.config(state='disabled')

# Função para limpar o código
def limpar():
    codigo_text.delete("1.0", "end")
    output_text.config(state='normal')  # Habilita a área de saída
    output_text.delete("1.0", "end")  # Limpa a saída
    output_text.config(state='disabled')  # Desabilita a área de saída

# Função para abrir um arquivo
def abrir_arquivo():
    arquivo = filedialog.askopenfilename(
        defaultextension=".txt",
        filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os arquivos", "*.*")]
    )
    if arquivo:
        with open(arquivo, "r") as f:
            codigo_text.delete("1.0", tk.END)
            codigo_text.insert(tk.END, f.read())

# Função para atualizar os números de linha
def atualizar_numeros_linha(event=None):
    codigo_linhas = codigo_text.get("1.0", "end-1c").split('\n')
    numeros_linha_text.config(state='normal')
    numeros_linha_text.delete('1.0', 'end')
    for i, _ in enumerate(codigo_linhas, 1):
        numeros_linha_text.insert(f'{i}.0', f'{i}\n')
    numeros_linha_text.config(state='disabled')

# Função para sincronizar a rolagem
def sincronizar_rolagem(event=None):
    numeros_linha_text.yview_moveto(codigo_text.yview()[0])

# Cria a janela principal
janela = tk.Tk()
janela.title("Compilador")

# Frame para botões
frame_botoes = tk.Frame(janela)
frame_botoes.pack(side=tk.TOP, fill=tk.X)

# Botão de compilar
btn_compilar = tk.Button(frame_botoes, text="Compilar", command=compilar)
btn_compilar.pack(side=tk.LEFT)

# Botão de limpar
btn_limpar = tk.Button(frame_botoes, text="Limpar", command=limpar)
btn_limpar.pack(side=tk.LEFT)

# Botão de abrir arquivo
btn_abrir_arquivo = tk.Button(frame_botoes, text="Abrir Arquivo", command=abrir_arquivo)
btn_abrir_arquivo.pack(side=tk.LEFT)

# Frame para código e números de linha
frame_codigo = tk.Frame(janela)
frame_codigo.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Campo de texto para o código
codigo_text = scrolledtext.ScrolledText(frame_codigo, wrap=tk.WORD)
codigo_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Área de números de linha
numeros_linha_text = tk.Text(frame_codigo, width=4, state='disabled', highlightthickness=0)
numeros_linha_text.pack(side=tk.LEFT, fill=tk.Y)

# Saída
output_text = scrolledtext.ScrolledText(janela, wrap=tk.WORD, state='disabled')
output_text.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

# Sincronizar rolagem
codigo_text.bind("<KeyRelease>", atualizar_numeros_linha)
codigo_text.bind("<MouseWheel>", sincronizar_rolagem)

# Inicializa a interface
atualizar_numeros_linha()
janela.mainloop()