###########################################
# Vamos utilizar um algoritmo de agrupamento hierárquico - Aglomerative clustering -
# Em Python utilizando scikit-learn. Vamos reconhecer 3 grupos:
#   Boa - Ruim - Péssima. O cenceito de péssima foi utilizado nesse caso teste,
#   pois nesse caso temos datas de consulta e temos valor de latência,
#   porém em um caso real o ideal seria incluirmos status da aplicação como um outro fator.
# Os grupos gerados terão centroids - centros geométricos de cada grupo - 
# Vamos exportar esses centroids, pois iremos utilizá-los para descobrir a qual grupo 
# pertence a latência no momento da consulta, ou seja, a latência vai pertencer 
# ao grupo de menor distância entre seu ponto e o ponto do respectivo centroide. 
# Por exemplo
#   Se a distância entre a latencia e os centroids for:
#       Cluster 'Boa' - distância = 234
#       Cluster 'Ruim' - distância = 600
#       Cluster 'Péssima' - distância = 1000
#  Por similaridade, essa latência pode ser considerada como uma boa latência. 
###########################################

#Imports:
import pandas as pd
from datetime import datetime
import datetime as dt 
import numpy as np
import logging

from sklearn.preprocessing import StandardScaler
import scipy.cluster.hierarchy as hcluster
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import linkage

class Model():

    def __init__(self):

        ## Aqui poderíamos medir a latência por alguns dias, documentar e utilizar como parâmetro. 
        pass

    def prepare_data(self, dataset):
        ## Data Cleansing:
        ## First, We manipulate date columns to become datetime in the right format.
        ## We will use the time from each created_at to simulate the realtime moment of latency extraction.

        date_columns = ['created_at', 'updated_at', 'day']
        for column in date_columns:
            dataset[column] = dataset[column].str.split('.')
            dataset[column] = [x[0] for x in dataset[column]]
            dataset[column] = pd.to_datetime(dataset[column])
        
            dataset['time'] = [str(x.time()) for x in dataset['created_at']]

            dataset['time'] = [datetime.strptime(c, '%H:%M:%S').time() for c in dataset['time']]

            # We're only gonna need the time of extraction so we convert it in seconds 
            # because only then we can manipulate them using clustering.

            dataset['time']  = [time.hour * 3600 + time.minute * 60 + time.second for \
                        time in dataset['time']]
            dataset['latencies'] = [str(x).split(',') for x in list(dataset['latencies'])]
            dataset = dataset.explode('latencies').reset_index()
            dataset = dataset.drop(['index'], axis=1)
            dataset['latencies'] = dataset['latencies'].astype('float')

        return dataset[['latencies', 'time']]

    def generate_centroids(self, dataset):
        linkage_data = linkage(dataset, method='average', metric='euclidean')
        hierarchical_cluster = AgglomerativeClustering(n_clusters=3, metric='euclidean', linkage='average')
        labels = list(hierarchical_cluster.fit_predict(dataset))
        dataset['labels'] = labels        
        aux = dataset.groupby('labels').describe()['latencies'].sort_values(by='min').reset_index()
        label = []
        for i in range(len(aux)):
            label.append(dataset[dataset['latencies'] == aux['min'][i]]['labels'].unique().astype('int'))
        
        dict = {label[0][0]:'Boa', label[1][0]:'Ruim', label[2][0]:'Péssima'}
        dataset.sort_values(by='latencies')
        centroids = pd.DataFrame(columns = dataset.columns)

        for i in range(0,3):
            s = pd.Series(np.mean(dataset[dataset['labels']==i], axis=0), index=centroids.columns)
            centroids.loc[len(centroids)] = s
        
        centroids['Cluster'] = centroids['labels'].replace(dict)

        return centroids

    def get_centroids(self):

        self.dataset = pd.read_excel('latencies by service.xlsx')

        self.prepared_data = pd.DataFrame()

        self.prepared_data = self.prepare_data(self.dataset)

        self.centroids = self.generate_centroids(self.prepared_data)

        self.centroids.to_excel('centroids.xlsx')

        return self.centroids
    
    def get_cluster(self, latency, time):
    
        self.centroids = pd.read_excel('centroids.xlsx')

        self.minima = float('inf')
        self.cluster = str()
        for i in range(len(self.centroids)):
            self.point2 = np.array([latency, time])
            self.point1 = np.array([self.centroids['latencies'][i], self.centroids['time'][i]])
            self.distance = np.sqrt(np.sum((self.point2 - self.point1)**2))
        
            if self.distance<self.minima:
                self.minima = self.distance
                self.cluster = self.centroids['Cluster'][i]
        
        return self.cluster