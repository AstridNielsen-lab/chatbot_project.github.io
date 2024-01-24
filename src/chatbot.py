import sqlite3
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import numpy as np
from keras.models import load_model  # Corrigindo a importação

import os

# Certifique-se de baixar o recurso necessário para a tokenização
nltk.download('punkt')

# Obter o diretório atual do script
script_dir = os.path.dirname(__file__)

# EU ACHO QUE ISSO VAI AQUI , PELA MINHA LOGICA ESTOU CERTO , VOCE MANDOU ISSO SOLTO NA TELA TENTEI ENCAIXAR ONDE ACHEI QUE ERA CERTO 
confidencial = {}

# Carregar o modelo treinado (usando caminho relativo)
model_path = os.path.join(script_dir, 'models', 'chatbot_model_v1.h5')
model = load_model(model_path)  # Corrigindo o uso de load_model

# Constrói caminhos relativos para o modelo e o banco de dados
model_path = os.path.join(script_dir, 'models', 'chatbot_model_v1.h5')
db_path = os.path.join(script_dir, 'data', 'base_de_dados.db')

# Inicializar o lematizador
lemmatizer = WordNetLemmatizer()

# Carregar o banco de dados SQLite (usando caminho relativo)
conn = sqlite3.connect(db_path)

# Função para pré-processar a entrada do usuário
def preprocess(sentence):

    # Tokenização da sentença
    tokens = word_tokenize(sentence)

    # Outras etapas de pré-processamento, como lematização, remoção de pontuações, etc., podem ser adicionadas aqui

    return tokens

# Função para obter a resposta do modelo
def get_response(user_input):
    # Vetorizar a entrada do usuário usando o modelo de lematização
    input_tokens = preprocess(user_input)

    # Converter os tokens em vetores usando o modelo de lematização
    input_vector = [lemmatizer.lemmatize(token.lower()) for token in input_tokens]

    # Realizar a predição usando o modelo treinado
    input_vector = np.array(input_vector).reshape(1, -1)  # Formatar o vetor para corresponder à entrada do modelo
    predicted_class = int(np.argmax(model.predict(input_vector), axis=-1)[0])

    # Aqui, você precisará de uma lógica para mapear a classe prevista de volta para uma resposta adequada
    # Isso depende do seu conjunto de dados e como você mapeou as classes durante o treinamento.

    # Exemplo simples: suponha que você tenha uma lista de respostas correspondentes às classes
    # response_mapping = {0: "Resposta para classe 0", 1: "Resposta para classe 1", ...}
    # response = response_mapping.get(predicted_class, "Resposta padrão se classe não mapeada")

    # Obtém a resposta com base na classe prevista
    response_mapping = {
        0: "Resposta para classe 0",
        1: "Resposta para classe 1",
        # Adicione mais mapeamentos conforme necessário
    }

    # Obtém a resposta com base na classe prevista
    response = response_mapping.get(predicted_class, "Resposta padrão se classe não mapeada")

    # Retorna a resposta
    return response

# Loop principal de conversação
while True:
    user_input = input("Você: ")
    if user_input.lower() == 'sair':
        break
    
    preprocessed_input = preprocess(user_input)
        
    print("IA: " + response)

    # Adicionamos uma condição para verificar se o usuário está compartilhando um segredo
    if user_input.lower().startswith('segredo:'):
        # Extrair o nome da pessoa e o segredo
        _, nome, *segredo = user_input.split()
        nome = ' '.join(nome)
        segredo = ' '.join(segredo)

        # Armazenar o segredo no dicionário confidencial
        if nome in confidencial:
            confidencial[nome].append(segredo)
        else:
            confidencial[nome] = [segredo]

        print(f"IA: Ooh, um segredo! Você pode compartilhar mais detalhes se quiser uma resposta apropriada.a {nome}!")
        continue  # Continuar para a próxima iteração do loop

    preprocessed_input = preprocess(user_input)
    response = get_response(preprocessed_input)
    
    print("IA: " + response)