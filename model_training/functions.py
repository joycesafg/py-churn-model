import datetime
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report, make_scorer, roc_auc_score


def removeUnvariable(X, cols, threshold):

    """
    Identifica colunas em um DataFrame que não atendem a um limite de variância especificado.
    Args:
    X (pd.DataFrame): O DataFrame de entrada contendo os dados.
    cols (list): Uma lista de nomes de colunas para verificar a variância.
    threshold (float): O limite mínimo de variância que uma coluna deve atender para ser considerada variável.
    Returns:
    list: Uma lista de nomes de colunas que não atendem ao limite de variância especificado.
    """
   
    colsVariance = []
    
    for i in cols:
      if i != 'TARGET':
        if X[i].var() >= threshold:
          pass
        else:
            colsVariance.append(i)
    return colsVariance


def timer(start_time=None):
    """
    Função para medir o tempo decorrido.
    Args:
        start_time (datetime, opcional): O tempo inicial. Se não fornecido, a função retorna o tempo atual.
    Returns:
        datetime: Se start_time não for fornecido, retorna o tempo atual.
    Exibe:
        str: Se start_time for fornecido, exibe o tempo decorrido no formato de horas, minutos e segundos.
    """
    
    if not start_time:
        start_time = datetime.now()
        return start_time
    elif start_time:
        thour, temp_sec = divmod((datetime.now() - start_time).total_seconds(), 3600)
        tmin, tsec = divmod(temp_sec, 60)
        print('\n Time taken: %i hours %i minutes and %s seconds.' % (thour, tmin, round(tsec, 2)))

#funcao que aplica o ponto de corte ideal para calcular o lucro
def ponto_de_corte(lista, pto_corte): 
    """
    Classifica os elementos de uma lista com base em um ponto de corte.
    Esta função recebe uma lista de tuplas e um ponto de corte. Para cada tupla na lista,
    verifica se o segundo elemento da tupla é menor ou igual ao ponto de corte. Se for,
    adiciona 0 a uma nova lista; caso contrário, adiciona 1. A função retorna a nova lista
    como um array numpy.
    Args:
        lista (list of tuples): Lista de tuplas onde o segundo elemento de cada tupla é um valor numérico.
        pto_corte (float): O ponto de corte usado para classificar os elementos da lista.
    Returns:
        numpy.ndarray: Um array numpy contendo 0s e 1s, onde 0 indica que o segundo elemento da tupla
                    é menor ou igual ao ponto de corte e 1 indica que é maior.
    """
    new_df = []
    for x in lista:
        if x[1] <= pto_corte:
            new_df.append(0)
        else:
            new_df.append(1)

    return np.array(new_df)


def lucro_maximo(target_real, valor_predito):
    """
    Calcula o lucro máximo com base na matriz de confusão entre os valores reais e os valores preditos.
    Args:
    target_real (array-like): Valores reais dos alvos.
    valor_predito (array-like): Valores preditos pelo modelo.
    Returns:
    int: O lucro calculado com base nos verdadeiros positivos (TP) e falsos positivos (FP).
    A fórmula do lucro é dada por:
    lucro = 90 * TP - 10 * FP
    onde:
    - TP (True Positives) são os verdadeiros positivos.
    - FP (False Positives) são os falsos positivos.
    """

    conf_matrix = confusion_matrix(target_real, valor_predito)
    
    FP = conf_matrix[0][1] # Falsos positivos
    TP = conf_matrix[1][1] # Verdadeiros positivos
    
    lucro = 90*TP - 10*FP # lucro da acao de retencao 
    
    return lucro


def evaluate_pto_corte(model, X_train, X_test, y_train, y_test, pto_corte):
    """
    Avalia o desempenho de um modelo de classificação com base em um ponto de corte específico.
    Args:
    -----------
    model : object
        O modelo de classificação treinado que possui o método `predict_proba`.
    X_train : array-like
        Conjunto de características de treinamento.
    X_test : array-like
        Conjunto de características de teste.
    y_train : array-like
        Rótulos verdadeiros para o conjunto de treinamento.
    y_test : array-like
        Rótulos verdadeiros para o conjunto de teste.
    pto_corte : float
        Ponto de corte para converter probabilidades em previsões binárias.
    Returns:
    --------
    tuple
        Uma tupla contendo:
        - auc_score_train (float): AUC do conjunto de treinamento.
        - auc_score (float): AUC do conjunto de teste.
        - lucro_treino (float): Lucro obtido no conjunto de treinamento.
        - lucro_maximo_treino (float): Lucro máximo possível no conjunto de treinamento.
        - lucro_test (float): Lucro obtido no conjunto de teste.
        - lucro_maximo_test (float): Lucro máximo possível no conjunto de teste.
        - confusion_matrix_train (ndarray): Matriz de confusão do conjunto de treinamento.
        - confusion_matrix_test (ndarray): Matriz de confusão do conjunto de teste.
        - pto_corte (float): O ponto de corte utilizado.
    Note:
    ------
    - A função imprime os resultados de avaliação, incluindo lucro, matriz de confusão, AUC e relatório de classificação para os conjuntos de treinamento e teste.
    - A função assume que as funções `ponto_de_corte`, `lucro_maximo`, `roc_auc_score`, `classification_report`, `confusion_matrix` e `pd.DataFrame` estão definidas/importadas no escopo.
    """



    pred_train = ponto_de_corte(model.predict_proba(X_train), pto_corte)
    pred_test= ponto_de_corte(model.predict_proba(X_test), pto_corte)

    auc_score_train = roc_auc_score(y_train,model.predict_proba(X_train)[:,1])
    auc_score = roc_auc_score(y_test,model.predict_proba(X_test)[:,1])
    
    lucro_treino = lucro_maximo(y_train, pred_train)
    lucro_maximo_treino = sum([x for x in y_train if x == 1])*90

    lucro_test = lucro_maximo(y_test, pred_test)
    lucro_maximo_test = sum([x for x in y_test if x == 1])*90

    print("TRAINIG RESULTS: \n===============================")
    print("lucro no treino:",lucro_maximo(y_train, pred_train))
    print("perncetual do lucro total no treino obtido: ", round((lucro_treino/lucro_maximo_treino)*100, 2))


    clf_report = pd.DataFrame(classification_report(y_train, pred_train, output_dict=True))
    print(f"CONFUSION MATRIX:\n{confusion_matrix(y_train, pred_train)}")
    print(f"AUC:\n{auc_score_train:.4f}")
    print(f"CLASSIFICATION REPORT:\n{clf_report}")

    print("TESTING RESULTS: \n===============================")
    print("lucro no teste:",lucro_maximo(y_test, pred_test))
    print("perncetual do lucro total no test obtido: ", round((lucro_test/lucro_maximo_test)*100, 2))

    clf_report = pd.DataFrame(classification_report(y_test, pred_test, output_dict=True))
    print(f"CONFUSION MATRIX:\n{confusion_matrix(y_test, pred_test)}")
    print(f"AUC:\n{auc_score:.4f}")
    print(f"CLASSIFICATION REPORT:\n{clf_report}")

    return auc_score_train, auc_score, lucro_treino, lucro_maximo_treino, lucro_test, lucro_maximo_test, confusion_matrix(y_train, pred_train), confusion_matrix(y_test, pred_test), pto_corte