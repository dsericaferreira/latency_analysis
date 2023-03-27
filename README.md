<img width="600" src="https://user-images.githubusercontent.com/101155921/227826492-4a2c1119-7fe4-47f6-b22b-23c4a0e0f589.gif">

<h4> Para rodar o projeto: </h4>
<h4>1. Primeiro, tenha o python (usei o python:3.8.8) instalado e em suas variáveis de ambiente.</h4>
<h4>2. Clone o projeto.</h4>
<h4>3. Na pasta do projeto vá no diretório /app.</h4>
<h4>4. Abra um temrinal nessa pasta e rode o comando: pip install -r requirements.txt<br>
       Esse comando deve instalar todas as dependências e módulos usados no projeto.</h4>
<h4>5. Agora que está com tudo instalado, rode no mesmo terminal: python run.py</h4>
<h4>6. Pronto, agora você viu o comportamento do projeto.</h4>
<h4>7. Fora do diretório /app deixei o notebook que foi utilizado para estudo e para
       chegar à lógica final do projeto. </h4>
   
<h4>Qualquer dúvido e/ou sugestão: dsericaferreira@gmail.com </h4>

<h4> Explicando o código: 


1. Inicialmente, com a análise do problema, nos questionamos, o que seria uma boa latência?
   Como grande fã de técnicas de clustering no reconhecimento de padrÕes e perfis, 
   observei que os dados fornecidos encontram-se, em média, muito próximos, porém com alguns pontos 
   mais dispersos no dataset, devido a essa proximidade, adotei o algoritmo de clustering hierárquico 
   como método escolhido. 
   
2. A partir do comportamento dos dados resolvi analisar a latência em relação ao horário do dia 
   no qual a mesma foi consultada. Outras features, porém, podem trazer mais benefícios, eu particularmente
   gosto de analisar status da aplicação, dia da semana e localização geográfica como features de impacto na latência.
   Alguma outra sugestão? Pode me contatar em dsericaferreira@gmail.com
   
3. Após limpar e trabalhar os dados - e os tipos de dados, pois ao lidarmos com tempo em Horas:Minutos:Segundos é preferível
   que possamos converter o tempo em segundos, assim temos um tipo float/int e conseguimos trabalhar com os dados
   nas dimensões corretas. Agora temos latência e tempo (em segundos), chega o momento de dividir os dados 
   em clusters e interpretarmos as labels de cada cluster. No caso, analisamos em ordem crescente de média de 
   latência as labels e chegamos aos seguintes clusters: Boa, Ruim, Péssima. 
   
4. Considerei a latência como ruim e péssima já que alguns pontos encontravam-se muito mais dispersos, mas que já que esses
   não foram considerados outliers, decidi que, na ausência do status do produto, considerar essas latências seria mais 
   interessante e para pontos muito mais afastados, considerei a latência como péssima.

5. Analisar centroides: Calculei os centroides de cada grupo - centros geométricos - e gerei um dataset de 
   centroides, latências, time e labels. A ideia é que ao termos novos valores de latência, possamos calcular 
   a distância desse novo ponto em relação aos centroides e inserimos esse novo ponto no cluster cujo centroide 
   estiver mais próximo, ou seja, trabalhamos com similaridade. 

6. Após a lógica de geração de centroides, salvamos o arquivo com os dados dos centroides e dos grupos: Boa, Ruim e Péssima. 
   E agora precisamos treinar sempre o modelo e gerar novos cetroides? Essa lógica depende da regra de negócio escolhida, 
   esse treino pode ocorrer semanal, quinzenal ou mensalmente, por exemplo, e a automação deve apenas reter os valores
   de centroides e calcular a distância da latência a esses pontos para que possamos classificá-la e então seguimos para o 
   próximo passo, notficar latências ruins.

7. Para notificação, optei pelo módulo TryCourier - python. Nele podemos enviar notificações via email, sms, slack, discord, etc.
   Optei nesse caso por email e a lógica ficou para que - ao termos uma latência com uma classificação diferente de 'Boa', 
   seja enviada uma notificação. 
   Deixei o layout da mensagem com essa formatação:
   <img width="650" alt="Courier Template" src="https://user-images.githubusercontent.com/101155921/227825215-f41d3fe1-2a1e-42ac-a90c-950f2f77d599.png">

       
   <h4>Caso queira testar o módulo de notificação, no código, é necessário um cadastro em: https://app.courier.com
   E a geração de uma token de autenticação. No caso, por segurança, a token não foi compartilhada no código.  </h4>
   
8. Ao rodar o código, aparecerá em sua tela os centroides, os clusters, a latência simulada naquele momento 
   e em qual classificação ela se encontra. 
   
9. A ideia é que esse app rode em um docker container e que possa estar instanciado em um projeto aws/gcp ou ainda 
   em alguma outra configuração preferida. 
   
   Espero que tenham gostado e que possa contribuir um pouco com seus estudos!! 
   
   Tudo de bom, 
   Érica Ferreira. </h4>
   
   
    
