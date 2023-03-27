from model import Model
from ingestion_simulator import Ingestion
from notification import Notification
import pandas as pd
import numpy as np
import datetime
import logging 


logger = logging.getLogger(__name__)

### O modelo não necessita ser rodado sempre, ele pode ser rodado em um período adequado de tempo
# -- semanal, quinzenal, mensal -- de acordo com a regra de negócio adotada. 
## Irei usar logger.warning e não logger.info, pois dependendo do sistema operacional(Já que rodamos local), logger.info
## não é exibido, mas logger.warn sim.

logger.warning('Rodando o modelo, geraremos os centroides.') 

model = Model()

centroids = model.get_centroids()

logger.warning("\nCentroides: \n" + str(centroids))

logger.warning('\nSimulando ingestão dos dados (Consulta de latência via request): \n')

latency, time = Ingestion().ingestion()

logger.warning("\nLatência: " + str(latency))
logger.warning("\nTime: "+ str(time))

## Agora vamos encontrar em qual grupo nosso datapoint (latency x time) melhor se encaixa:

logger.warning('\nEncaixando nosso ponto no melhor grupo, mais próximo:')

cluster = model.get_cluster(latency, time)

logger.warning('\nA latência encontra-se: ' + str(cluster))

## Agora, vamos notificar via email usando Courier caso a latência não esteja boa:

Notification().send_email(cluster)

logger.warning('Notificação enviada caso latência não esteja boa.')