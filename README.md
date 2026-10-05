# Estudo RAG (Retrieval-Augmented Generation)

Este documento foi criado para registrar o progresso e o aprendizado durante o desenvolvimento deste projeto. Ele serve tanto para revisão dos conceitos quanto para contextuzalizar a IA sobre de onde paramos.

---

## 🚀 O que aprendemos até agora

### 1. Arquitetura Básica do Projeto
- **`bd.py`**: Nosso script responsável pela "ingestão de dados". Ele lê os arquivos, divide o texto e os converte em formato matemático (vetores) em um banco de dados.
- **Pasta `base/`**: Diretório onde colocamos nossos arquivos em PDF para servirem de base de conhecimento.
- **Pasta `db/`**: Diretório criado automaticamente pelo script onde o **Chroma** (nosso banco de dados vetorial) salva as informações localmente.
- **Arquivo `.env`**: Arquivo de ambiente para armazenar chaves secretas (como `GOOGLE_API_KEY`). Ele garante que a chave não fique exposta diretamente no código fonte.
- **`main.py`**: Nosso script de consulta. Ele recebe a pergunta do usuário, busca no banco de dados os trechos mais relevantes e pede para a IA formular uma resposta.
### 2. O Pipeline de Dados (O que o `bd.py` faz)

O nosso script divide o trabalho em 3 grandes etapas:

1. **Carregamento (Loading)**
   - **Ferramenta:** `PyPDFDirectoryLoader`
   - Lemos de forma automatizada todos os arquivos PDF presentes na pasta definida (`pasta_base = "base"`).

2. **Divisão de Textos (Splitting / Chunks)**
   - **Ferramenta:** `RecursiveCharacterTextSplitter`
   - Modelos de IA têm um limite do quanto conseguem ler de uma vez. Por isso, "quebramos" as páginas do PDF em blocos (chunks).
   - **Tamanho (`chunk_size=2000`)**: Cada bloco terá no máximo 2000 caracteres.
   - **Sobreposição (`chunk_overlap=500`)**: Pegamos 500 caracteres do bloco anterior para iniciar o novo. Isso evita que uma frase ou contexto seja cortado no meio.

3. **Vetorização e Armazenamento (Embedding e Vector Store)**
   - **Ferramentas:** `GoogleGenerativeAIEmbeddings` e `Chroma`
   - O texto não é salvo como texto normal. Usamos os modelos do Google Gemini (como o `gemini-embedding-2`) para transformar esses chunks em **Embeddings** (representações matemáticas baseadas no significado do texto).
   - O **Chroma** recebe esses embeddings e os armazena na pasta `db`. Futuramente, quando fizermos uma pergunta, o sistema buscará os vetores mais similares matematicamente à nossa pergunta.

### 3. Bibliotecas e Dependências Importantes
Durante esse processo instalamos bibliotecas chaves:
- `langchain-community`, `langchain-chroma`, `langchain-google-genai`: O ecossistema **LangChain** que facilita a união de diferentes IAs e ferramentas (fizemos a transição de OpenAI para Google Gemini).
- `pypdf`: Essencial para ler PDFs (sem ele, o Loader falharia).
- `chromadb`: O motor do banco de dados vetorial local.
- `python-dotenv`: Usado na função `load_dotenv()` para ler o arquivo `.env`.

### 4. Boas Práticas e Aprendizados de Código
- **Sintaxe de blocos e loops Python:** Toda função (`def`) requer `:` no final da sua definição.
- **Atenção aos nomes em arquivos `.env`**: As bibliotecas procuram exatamente por nomes específicos (como `GOOGLE_API_KEY`). Outros nomes não são reconhecidos e causam erros.
- **Bloco de Execução Segura**: Usar `if __name__ == "__main__":` na hora de chamar as funções principais no final do arquivo previne que o banco de dados seja processado inteiramente por acidente.
- **Atenção às versões dos modelos**: Modelos de IA são atualizados e descontinuados constantemente (ex: `gemini-2.5-flash` descontinuado em favor do `gemini-3.8-flash`). É preciso estar atento aos erros de `NOT_FOUND` e usar versões suportadas na API.
- **Extração da resposta**: Ao usar o Langchain com ChatModels, a resposta vem encapsulada num objeto. É necessário utilizar `.content` para extrair apenas o texto gerado pela IA.

---

## 📌 Status Atual
- ✅ Script de população do banco de dados criado com sucesso (`bd.py`).
- ✅ Transição de provedor da OpenAI para a API do Google Gemini.
- ✅ Script de consulta e Chat criado com sucesso (`main.py`).
- ✅ Sistema de RAG funcional e respondendo perguntas baseadas no PDF!
- ⏳ **Próximo passo provável:** Refinar os prompts, adicionar suporte a histórico de conversas (para o bot ter memória das perguntas anteriores) ou criar uma interface gráfica para facilitar o uso.
