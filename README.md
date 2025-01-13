# Website Data API

Uma aplicação para realizar web scraping no site **VitiBrasil** e disponibilizar os dados extraídos por meio de uma API REST. Este projeto é dividido em três módulos principais:

- **scrape.py**: Responsável por realizar o scraping dos dados do site.
- **clean.py**: Contém funções para processar e limpar os dados extraídos.
- **app.py**: Implementa a API REST utilizando o FastAPI.

## Estrutura do Projeto

```plaintext
.
├── app.py          # Implementação da API REST.
├── Scripts/
│   ├── scrape.py   # Módulo para scraping de dados.
│   └── clean.py    # Módulo para limpeza e processamento de dados.
├── data/           # Pasta onde os dados processados são armazenados em formato Parquet.
├── requirements.txt # Dependências do projeto.
└── README.md       # Documentação do projeto.
```

## Uso
### Acesso

A API está disponível em: https://fiap-ml-techchallenge-fase1.vercel.app/docs

### Endpoints Disponíveis
`GET /vitibrasil/`

Obtém dados da aba e ano especificados, realizando o scraping ou carregando de um arquivo local caso a raspagem falhe.

#### Parâmetros:

- `aba` (Obrigatório): Aba a ser raspada. Opções:
    - `Produção`
    - `Processamento`
    - `Comercialização`
    - `Importação`
    - `Exportação`
- `ano` (Obrigatório): Ano dos dados a serem obtidos.
- `sub_aba` (Opcional): Subaba dentro da aba principal, se aplicável. Exemplo:
    - Para   `Processamento: Viníferas`, `Americanas e híbridas`, `Uvas de mesa`, `Sem classificação`.
    - Para `Importação` ou `Exportação`: `Vinhos de mesa`, `Espumantes`, `Uvas frescas`, `Uvas passas`, `Suco de uva`.

#### Exemplo de Uso:

```
http://127.0.0.1:8000/vitibrasil/?aba=Produção&ano=2023
```
Resposta: Retorna uma lista de dicionários representando os dados da tabela.

## Scripts Principais
`scrape.py`

Realiza o scraping de dados do site VitiBrasil com base nos parâmetros fornecidos.

- Função: `scrape_vitibrasil_data(aba, ano, sub_aba)`.
    - **Parâmetros:**
        - `aba`: Aba a ser raspada.
        - `ano`: Ano desejado.
        - `sub_aba`: Subaba, caso aplicável.

`clean.py`

Processa e limpa os dados extraídos para convertê-los em um formato estruturado.

- Função: `extract_table_from_html(html_table)`
    - **Parâmetros:**
        - `html_table`: Objeto BeautifulSoup representando a tabela extraída do site.

`app.py`
Define os endpoints da API e combina as funções de scraping e limpeza.

    - Principal endpoint:
    GET /vitibrasil/: Obtém os dados processados.

## Dependências
O projeto utiliza as seguintes bibliotecas:

- **FastAPI**: Framework para construção de APIs REST.
- **beautifulsoup4**: Para web scraping.
- **fake_useragent**: Simulação de cabeçalhos de requisições.
- **pandas**: Processamento e limpeza de dados.
- **requests**: Requisições HTTP.
- **uvicorn**: Servidor

As dependências completas estão listadas no arquivo requirements.txt
