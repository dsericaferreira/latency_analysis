import pandas as pd
import random
import datetime
import json
from trycourier import Courier
from notification import Notification

class Ingestion():

    def __init__(self):
        self.note = Notification()


    def ingestion(self):
        self.centroids = pd.read_excel('centroids.xlsx')

        ## Vamos simular ingestão de dados, gerando uma latência aleatória nesses critérios,
        ## apenas para simularmos o que poderia ser uma chamada a api do produto
        ## e guardaríamos a latência e o horário da chamada. 

        self.df = pd.read_excel('data.xlsx')
        self.lat = random.randint(min(self.df['latencies']), max(self.df['latencies']/3))
        self.date = datetime.datetime.now()
        self.mid = datetime.datetime.combine(self.date.date(), datetime.time.min)
        self.seconds = (self.date - self.mid).total_seconds()

        return self.lat, self.seconds
