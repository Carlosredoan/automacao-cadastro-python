# =============================================================================
# PROJETO: Automação de Cadastro de Produtos (RPA)
# DESENVOLVEDOR: Carlos Redoan
# IDE: Visual Studio Code (VS Code)
# AMBIENTE DE EXECUÇÃO: Arch Linux
# SISTEMA ALVO: ERP Web (Interface de Treinamento)
# =============================================================================
# 📍 FERRAMENTAS DE DESENVOLVIMENTO:
# - Mapeamento de Tela: Script auxiliar 'pegar_posicao.py' (incluso no projeto).
# - Método: Captura dinâmica de coordenadas X e Y via PyAutoGUI.
# - Auditoria: Sistema de logs nativo com registro de timestamps.
# =============================================================================
# 💡 APLICAÇÕES DESTE CÓDIGO NO MERCADO:
# 1. FINANCEIRO: Lançamento massivo de notas fiscais ou boletos.
# 2. LOGÍSTICA: Cadastro de fretes e rastreio em sites de transportadoras.
# 3. E-COMMERCE: Atualização de estoque e preços em Marketplaces.
# =============================================================================

import pandas as pd
import pyautogui
import time
import pyperclip

# --- CONFIGURAÇÕES INICIAIS ---
# Definimos o endereço do sistema que será automatizado
link = "https://dlp.hashtagtreinamentos.com/python/intensivao/login"

# Define um tempo de espera padrão entre cada comando do PyAutoGUI (Segurança)
pyautogui.PAUSE = 1.0 

# --- PASSO 1: ACESSAR O SISTEMA ---
# No Arch Linux, usamos Alt+F2 para abrir o executor de comandos do sistema
pyautogui.hotkey("alt", "f2")
time.sleep(5) # Tempo para a barra de pesquisa aparecer

# Digita o nome do executável do navegador e confirma
pyautogui.write("chromium")
pyautogui.press("enter")
time.sleep(3) # Tempo para o navegador carregar a janela

# Foca na barra de endereços (Ctrl+L), copia e cola o link para evitar erros
pyautogui.hotkey("ctrl", "l")
pyperclip.copy(link)
pyautogui.hotkey("ctrl", "v")
pyautogui.press("enter")
time.sleep(3) # Aguarda o carregamento da página de login

# --- PASSO 2: AUTENTICAÇÃO (LOGIN) ---
# Clica no campo de e-mail usando a coordenada mapeada na tela
pyautogui.click(x=676, y=388)
pyautogui.write("seu_email@gmail.com")

# Navega para o campo de senha usando a tecla TAB (Mais seguro que clique)
pyautogui.press("tab")
pyautogui.write("sua_senha_aqui")

# Confirma o formulário enviando o comando Enter
pyautogui.press("tab")
pyautogui.press("enter")
time.sleep(3) # Aguarda o carregamento do painel principal

# --- PASSO 3: MANIPULAÇÃO DE DADOS ---
# Carrega a base de dados CSV para a memória usando a biblioteca Pandas
tabela = pd.read_csv("produtos.csv")

# --- PASSO 4: AUDITORIA E LOGS ---
# Cria o arquivo de log no modo 'w' (write) para iniciar um novo registro
with open("log_execucao.txt", "w") as log:
    log.write(f"Iniciando automação: {time.strftime('%d/%m/%Y %H:%M:%S')}\n")
    log.write("-" * 35 + "\n")

# --- PASSO 5: LOOP DE CADASTRO MASSIVO ---
# Aumentamos a velocidade para o preenchimento dos campos
pyautogui.PAUSE = 0.1 

for linha in tabela.index:
    # 1. Inicia o cadastro clicando no primeiro campo do formulário
    pyautogui.click(x=670, y=273)

    # 2. Preenche os dados da tabela, convertendo para String para o PyAutoGUI
    pyautogui.write(str(tabela.loc[linha, "codigo"]))
    pyautogui.press("tab")

    pyautogui.write(str(tabela.loc[linha, "marca"]))
    pyautogui.press("tab")

    pyautogui.write(str(tabela.loc[linha, "tipo"]))
    pyautogui.press("tab")

    pyautogui.write(str(tabela.loc[linha, "categoria"]))
    pyautogui.press("tab")

    pyautogui.write(str(tabela.loc[linha, "preco_unitario"]))
    pyautogui.press("tab")

    pyautogui.write(str(tabela.loc[linha, "custo"]))
    pyautogui.press("tab")

    # 3. Lógica para o campo de Observação (Tratamento de valores vazios/NaN)
    obs = str(tabela.loc[linha, "obs"])
    if obs != "nan":
        pyautogui.write(obs)
    
    # 4. Envia o produto cadastrado
    pyautogui.press("tab")
    pyautogui.press("enter")

    # 5. Retorna o scroll para o topo para garantir que o próximo clique seja no campo certo
    pyautogui.scroll(5000)

    # 6. Registra o evento no log de auditoria (Modo 'a' para acrescentar)
    msg = f"Sucesso: Produto {tabela.loc[linha, 'codigo']} às {time.strftime('%H:%M:%S')}"
    with open("log_execucao.txt", "a") as log:
        log.write(msg + "\n")
    
    print(msg) # Feedback visual no terminal para o desenvolvedor

# --- FINALIZAÇÃO ---
# Dispara um alerta nativo do SO informando o fim da tarefa
pyautogui.alert("Finalizado com sucesso! Todos os produtos estão no sistema, Carlos.")

# Fecha a aba do navegador para limpar o ambiente
pyautogui.hotkey("ctrl", "w")

print("Automação concluída com sucesso! Verifique 'log_execucao.txt'.")