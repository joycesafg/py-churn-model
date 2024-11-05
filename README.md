# Objetivo do Projeto

**Este projeto representa o processo de desenvolvimento de um modelo de machine learning para identificar clientes insatisfeitos e evitar churn. Ele inclui a preparação dos dados, a definição de funções de apoio, a configuração do MLflow para tracking e versionamento, treinamento, avaliação do modelo e deploy do modelo. O modelo foi treinado utilizando um conjunto de dados de clientes e implementado em uma API FastAPI, hospedada no Heroku.**

**O objetivo do modelo é maximizar o lucro em ações de retenção a partir da identificação de clientes que possam vir a se disvincular da marca. A correta classificação dos clientes churn e a atuação em cima desses clientes implica num lucro de R$90.00, enquanto a classificação indevida implica no prejuízo de R$10.00.**

Por facilidade mantive todo o código de desenvolvimento do modelo, ingestão dos dados no mongo e aplicativo na branch **develop**. Na branch main tem apenas a aplicação final utilizando o modelo. Na **develop** tem tudo.

**Abaixo está a estrutura de pastas do projeto e uma breve explicação de cada uma:**



# Aplicação: 
https://py-churn-app-model-75dda4af3bc2.herokuapp.com/

OBS: O ID do cliente deve ser um Inteiro [0..inf]
Retornos: 0, 1, Not found (Acontece quando o modelo não se aplica ao cliente).

# Estrutura do projeto: 
```
DataMaster_Case/
├───.github
│   └───workflows
├───app
│   ├───Model
│   └───templates
├───features_treatment_ingestion
├───model_training
│   └───data
└───tests
```



## Descrição das Pastas
- **workflows**: Contém o pipeline de execução incluindo testes

- **app/**: Contém o artefato do modelo (.pkl), as configurações de acesso para consulta da API e a aplicação em si. 
    - **Model/**: Contém os artefatos do modelo
    - **Templates/**: Contém o arquivo HTML de front

- **features_treatment_ingestion/**: Etapa de configuração de banco nosql, criação da collection, tratamento e ingesta dos dados usados na aplicação.

- **model_training/**: Código fonte dos modelos disponíveis no mlflow .
    - **data/**: Dados usados para desenvolimento do modelo de ML.

    Para tracking dos experimentos e versionamento dos modelos utilizei o dagshub, você pode consultar os experimentos em:
    https://dagshub.com/joycesafg/DataMaster_Case/experiments

    DagsHub é uma plataforma colaborativa para gerenciamento de projetos de machine learning, construída sobre ferramentas de código aberto, como DVC (Data Version Control) e MLflow.  

- **tests/**: Scripts de teste para garantir a qualidade e a funcionalidade do código.


# Arquitetura utilizada

![Architecture Diagram](bronzesilvergold.png)

# Overview das ferramentas utilizadas

1.  Jupyter Notebook + Mlflow hospedado no dagshub para treinamento, rastreio, avaliação e versionamento dos modelos.
2.  Docker + Github para empacotamento, teste e deploy automático da aplicação no Heroku.
3. MongoDB para feature table que alimenta o modelo e para salvar os dados de saída da aplicação.
4. OpenMetaData para governança da feature table
4. Elastic Search + Kibana + arize para monitoramento, tanto para acompanhamento da saúde da aplicação como para avaliação da estabilidade e desempenho do modelo.
5. Airflow para orquestração do ELT que vai alimentar a feature table
6. Heorku como Plataforma para deploy de aplicação
7. MongoCharts para acompanhamento analítico da aplicação : O dashboard pode ser acessado através de https://charts.mongodb.com/charts-project-0-ycudizl/public/dashboards/6702fe80-5b8a-4f70-8cb0-2e16355874c0 

# Instruções de reproducibilidade

## Pre-requisitos

1. **Install Python**: Certifique-se de que o Python está instalado. Você pode baixá-lo em [python.org](https://www.python.org/).

2. **Clone o repositório**:
    ```sh
    git clone https://github.com/joycesafg/py-churn-model.git
    cd py-churn-model
    ```

## Configuração do ambiente

1. **Crie um Virtual Environment**:
    ```sh
    python -m venv venv
    ```

2. **Ative o Virtual Environment**:
    - On Windows:
        ```sh
        .\venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```sh
        source venv/bin/activate
        ```

3. **Instale as dependencias**:
    ```sh
    pip install -r requirements.txt
    ```

4. **COnfiguração das variáeveis de ambiente**:
    
    - Crie um arquivo .env no diretório raiz do projeto.
    - Adicione suas credenciais do MongoDB ao arquivo .env:
      ```env
      MONGO_URI=mongodb+srv://username:password@cluster0.mongodb.net/mydatabase?retryWrites=true&w=majority
      ```

## Executando a API

1. **Execute API**:
    ```sh
    uvircorn --reload main:app
    ```

## Informações Adicionais
- **Documentaão da API**: https://py-churn-app-model-75dda4af3bc2.herokuapp.com/docs#/

- **Dados**: Certifique-se de que os dados necessários para o projeto estão colocados no diretório apropriado, conforme especificado na estrutura do projeto.
- **Configuração**: Modifique os arquivos de configuração conforme necessário para corresponder ao seu ambiente.

