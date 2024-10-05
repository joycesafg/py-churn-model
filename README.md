

**Este projeto representa o processo de desenvolvimento de um modelo de machine learning para identificar clientes insatisfeitos e evitar churn. Ele inclui a preparação dos dados, a definição de funções de apoio, a configuração do MLflow para tracking e versionamento, treinamento, avaliação do modelo e deploy do modelo.**

**O objetivo do modelo é maximizar o lucro em ações de retenção a partir da identificação de clientes que possam vir a se disvincular da marca. A correta classificação dos clientes churn e a atuação em cima desses clientes implica num lucro de R$90.00, enquanto a classificação indevida implica no prejuízo de R$10.00.**

Por facilidade mantive todo o código de desenvolvimento do modelo, ingestão dos dados no mongo e aplicativo na branch **develop**. Na branch main tem apenas a aplicação final utilizando o modelo. Na **develop** tem tudo.

**Abaixo está a estrutura de pastas do projeto e uma breve explicação de cada uma:**



A aplicação para teste encontra-se em: 
https://py-churn-app-model-75dda4af3bc2.herokuapp.com/predict

OBS: O ID do cliente deve ser um Inteiro [0..inf]

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

