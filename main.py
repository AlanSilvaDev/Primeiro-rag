from langchain_chroma.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate



load_dotenv()


CAMINHO_DB ='db'

prompt_template = """ Responda a pergunta do usuário: {pergunta}, 
com base nessa informação: {base_conhecimento}, """


def perguntar():
  pergunta = input("Digite sua pergunta: ") 

#carregar a base de conhecimento do banco de dados
  funcao_embedding = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2")  
  db = Chroma(persist_directory=CAMINHO_DB, embedding_function=funcao_embedding)  

#comparar a pergunta do user com a base de conhecimento
  resultados = db.similarity_search_with_relevance_scores(pergunta, k=4)  # Retorna o documento mais similar
  if len(resultados) == 0 or resultados[0][1] < 0.5:
        print("Desculpe, não sei a resposta para essa pergunta.")   
        return

  textos_resultado = []
  for resultado in resultados:
      texto = resultado[0].page_content
      textos_resultado.append(texto)

  base_conhecimento = "\n\n----\n\n".join(textos_resultado)
  prompt = ChatPromptTemplate.from_template(prompt_template)
  prompt = prompt.invoke({"pergunta":pergunta, "base_conhecimento": base_conhecimento})
 # print(prompt)

  modelo = ChatGoogleGenerativeAI(model="gemini-3.8-flash")
  resposta = modelo.invoke(prompt)
  
  conteudo = resposta.content
  texto_limpo = ""
  
  if isinstance(conteudo, list):
      for bloco in conteudo:
          if isinstance(bloco, dict) and 'text' in bloco:
              texto_limpo += bloco['text']
          elif isinstance(bloco, str):
              texto_limpo += bloco
  else:
      texto_limpo = str(conteudo)
      
  print('\nResposta da AI:\n')
  print(texto_limpo)
  print('\n' + '-'*40 + '\n')

  
perguntar()