<table>
<tr>
<td>
<a href= "https://vtal.com"><img src="https://upload.wikimedia.org/wikipedia/commons/0/09/Vtal_logo_2022.png" alt="V.tal" border="0" width="60%"></a>
</td>
<td><a href= "https://www.inteli.edu.br/"><img src="./inteli-logo.png" alt="Inteli - Instituto de Tecnologia e Liderança" border="0" width="50%"></a>
</td>
</tr>
</table>

# Introdução

Este é um dos repositórios do projeto de alunos do Inteli em parceria com a V.tal no 2º semestre de 2023. Este projeto está sendo desenvolvido por alunos do Módulo 6 do curso de Ciência da Computação.

# Projeto: *Algoritmo de otimização para alocação e distribuição de equipes de técnicos*

# Grupo: *Vitalis*

# Integrantes:

* Guilherme Moura
* Guilherme Lima
* José Vitor
* Lucas Galvão
* Marcos Teixeira
* Vinícius Kumagai

# Descrição

O problema em questão está inserido no contexto da empresa de rede neutra V.TAL, onde a operação é dividida em várias áreas, cada uma com um número predefinido de técnicos responsáveis por atender aos pontos de atendimento. Dentro dessas áreas, encontram-se distribuídos clientes que demandam serviços técnicos. No entanto, a alocação atual de técnicos é uma tarefa extremamente trabalhosa e repetitiva, uma vez que o cenário deve ser recalculado toda vez que houver alguma alteração de demanda e oferta de serviço.

Neste estágio, A solução proposta simplifica a dinâmica ao considerar os setores como entidades fixas. Este enfoque inicial visa facilitar o desenvolvimento da solução.

O objetivo deste projeto é a criação um algoritmo de alto desempenho capaz de otimizar a distribuição de técnicos, por meio da configuração minimizada de deslocamentos entre os setores que acarretem em menores custos e que garantam o suprimento de todas as demandas de cada região. Isso resultará em uma gestão mais eficaz dos recursos disponíveis.


# Configuração de desenvolvimento

Procedimento para baixar e executar o código deste projeto:

## Backend

Em um terminal, execute os comandos a seguir a partir da pasta raiz do projeto (`...\grupo3`): 

`cd codigo`

 `python -m venv .venv`    

`pip install -r requirements.txt`

 `.\.venv\Scripts\activate`    

 `cd flask`          

`flask run`                      

## Frontend

Após rodar o backend localmente, em um outro terminal, execute os comandos a seguir (também na pasta raiz  `...\grupo3`):

`.\codigo\.venv\Scripts\activate`

`cd codigo\streamlit`

`streamlit run 1-home.py`


# Releases/Tags

* SPRINT1: estas duas semanas foram utilizadas para fazer uma análise primária do problema, entendendo o negócio da parceira V.Tal, a experiência do usuário por trás da nossa solução e a modelagem matemática. 
* SPRINT2: nesta segunda sprint desenvolvemos uma solução inicial para o algoritmo, assim como demos início a redação do artigo e fizemos alterações na modelagem matemática.
* SPRINT3: entrega do frontend e backend, assim como melhorias no algoritmo e pesquisas de trabalho para o artigo. 
* SPRINT4: finalizamos o algoritmo, realizamos uma complexidade e corretude dele e redação dos resultados obtidos para o artigo.
* SPRINT5: refinação e refatoração de código, com preparação para entrega final pro parceiro.

## 📋 Licença/License

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/">

<a property="dct:title" rel="cc:attributionURL">Grupo</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName">Inteli, Guilherme Moura, Guilherme Lima, José Vitor, Lucas Galvão, Marcos Teixeira, Vinícius Kumagai</a> is licensed under <a href="https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
