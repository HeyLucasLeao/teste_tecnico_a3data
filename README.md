# Visão Geral
Teste técnico com objetivo de desenvolver um assistente conversacional baseado em GenAI para processar e interpretar relatórios epidemiológicos da União Europeia (2021). A solução espera-se receber questionamentos perantes aos dados processados a fim de trazer insights através de linguagem natural, facilitando a tomada de decisão para profissionais de saúde.

# Utilizar via Python (Ambiente Local)
## 1. Pré-requisitos:
- Python versão 3.11 a 3.15
- Poetry para gerenciamento de dependências
## 2. Instalação e execução:
```bash 
# Instalar as dependências com Poetry
poetry install

# Executar a aplicação
just run
```
## 3. Interface:
- Será iniciada uma interface Streamlit
- Faça upload dos PDFs desejados para processamento
- Utilize o chat para interagir com o assistente

# Utilizar via Docker
- just docker-compose
- docker-compose up
- basta acessar localmente `localhost:8501`, e trocar no `config.toml` para `0.0.0.0` no endereço!
- Vale ressaltar que devido a limitaçâo nativa de capacidade do Docker, é capaz dele gargalar
- Provavelmente deve demorar por conta da dependência com a biblioteca da nvidia!
