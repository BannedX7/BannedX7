import telebot
import os
import time
from tqdm import tqdm
import urllib.parse
from colorama import Fore, Style

# Chave de API do seu bot
CHAVE_API = "7159521536:AAGSgaiU_RImJmcKGT14g5I1qkE9FltV5YI"

# Lista de IDs de usuários autorizados
USUARIOS_AUTORIZADOS = [6026313462, 5443240670, 6251183795]

bot = telebot.TeleBot(CHAVE_API)

def limpar_nome_arquivo(nome_arquivo):
    caracteres_invalidos = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in caracteres_invalidos:
        nome_arquivo = nome_arquivo.replace(char, '_')
    return nome_arquivo

def buscar_e_escrever_linhas_com_palavra_chave(nome_arquivo, palavra_chave):
    linhas_relevantes = []
    erros_decodificacao = 0
    with open(nome_arquivo, 'rb') as arquivo:
        for linha_bytes in arquivo:
            try:
                linha = linha_bytes.decode('utf-8')
                if palavra_chave in linha:
                    linhas_relevantes.append(linha.strip())
            except UnicodeDecodeError:
                erros_decodificacao += 1
    return linhas_relevantes, erros_decodificacao

def main(palavra_chave, chat_id, message_id):
    pasta_db = "db"

    palavra_chave_encoded = urllib.parse.quote(palavra_chave)

    nome_arquivo_saida = f"{limpar_nome_arquivo(palavra_chave_encoded)}.txt"

    arquivos_txt = [arquivo for arquivo in os.listdir(pasta_db) if arquivo.endswith('.txt')]

    with tqdm(total=len(arquivos_txt), desc="Progresso da pesquisa") as progresso_barra:
        total_linhas_encontradas = 0
        total_erros_decodificacao = 0
        with open(nome_arquivo_saida, 'w') as arquivo_saida:
            for arquivo_txt in arquivos_txt:
                caminho_arquivo = os.path.join(pasta_db, arquivo_txt)
                linhas_relevantes, erros_decodificacao = buscar_e_escrever_linhas_com_palavra_chave(caminho_arquivo, palavra_chave)
                total_linhas_encontradas += len(linhas_relevantes)
                total_erros_decodificacao += erros_decodificacao
                if linhas_relevantes:
                    arquivo_saida.write(f"Resultados:\n")
                    arquivo_saida.writelines("\n".join(linhas_relevantes))
                    arquivo_saida.write("\n\n")
                progresso_barra.update(1)
                time.sleep(0.1)

    if total_linhas_encontradas == 0:
        mensagem = "Nenhuma linha relevante encontrada."
    else:
        mensagem = ""

    if total_erros_decodificacao > 0:
        mensagem += f" Total de erros de decodificação: {total_erros_decodificacao}"

    if mensagem:
        bot.send_message(chat_id, mensagem)
    with open(nome_arquivo_saida, 'rb') as documento:
        bot.send_document(chat_id, documento)
    bot.delete_message(chat_id, message_id)  # Apaga a mensagem de "Buscando URL nas databases..."

@bot.message_handler(commands=["search"])
def handle_search(message):
    chat_id = message.chat.id  # Obtém o ID do chat da mensagem
    user_id = message.from_user.id  # Obtém o ID do remetente da mensagem
    if user_id in USUARIOS_AUTORIZADOS:
        texto = message.text.split(maxsplit=1)
        if len(texto) > 1:
            palavra_chave = texto[1]
            msg = bot.reply_to(message, "Buscando URL nas databases...")
            main(palavra_chave, chat_id, msg.message_id)
        else:
            bot.reply_to(message, "Por favor, inclua a palavra-chave após o comando /search.")
    else:
        bot.reply_to(message, "Desculpe, você não está autorizado a usar este bot.")

@bot.message_handler(commands=["id"])
def show_id(message):
    user_id = message.from_user.id
    bot.reply_to(message, f"Seu ID de usuário é: {user_id}")

# Aqui você pode adicionar outros comandos e funcionalidades do seu bot

@bot.message_handler(commands=["Dono"])
def dono(mensagem):
    bot.reply_to(mensagem, "humm, ok! Se você esta tendo problemas quer falar com o dono do bot, basta clicar no @ a seguir. @usufluiram")

@bot.message_handler(commands=["DONO"])
def dono(mensagem):
    bot.reply_to(mensagem, "humm, ok! Se você esta tendo problemas quer falar com o dono do bot, basta clicar no @ a seguir. @usufluiram")

@bot.message_handler(commands=["dono"])
def dono(mensagem):
    bot.reply_to(mensagem, "humm, ok! Se você esta tendo problemas e/ou quer falar com o dono do bot, basta clicar no @ a seguir. @usufluiram")


def verificar(mensagem):
    return True


@bot.message_handler(func=verificar)
def responder (mensagem):
    texto = """Olá! eu sou o bot Search Logs.
eu fui criado pelo @usufluiram.
minha função é procurar qualquer URL que voce quiser!

para procurar uma URL, digite /search

para conversar com o dono, digite /dono

digite /id para saber seu id

digite /planos para saber os planos"""
    bot.reply_to(mensagem, texto)

bot.polling()





