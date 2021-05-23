# Programação Distribuida - Communcations
> Autor: Ariel Rossetto Ril
> Matrícula: 15105050
> Email: ariel.ril@edu.pucrs.br
> Repositório: https://github.com/arielril/distrprog-node-comms


## Introdução
Neste trabalho é apresentado uma implementação de um sistema P2P (peer-to-peer) básico, o qual possui um conjunto de nodos e supernodos. Os nodos são componentes que possuem uma lista de recursos, neste caso uma lista de arquivos, disponibilizado para consumo do cliente do sistema. Os supernodos são responsáveis por manter um tipo de "repositório" centralizado da informação de onde os recursos estão armazendos.

Cada nodo dentro do ecossistema executa um registro em um supernodo para que seja possível que outros nodos no sistema possam descobrir onde esta algum recurso solicitado pelo cliente do sistema, sem ter a necessidade de ter que solicitar para todos os nodos dentro do ecossistema. Dessa maneira, ao nodo solicitar ao seu supernodo um recurso, o supernodo executa uma pesquisa local em busca do recurso e caso o supernodo não tenha a resposta local o supernodo executa a pesquisa do recurso dentro de um grupo multicast, onde todos os supernodos estão registrados para responder as solicitações de seus parceiros.

## Desenvolvimento
Para realizar o desenvolvimento deste trabalho foi utilizado a linguagem de programação Python, utilizando o framework **Flask** para as comunicações que utilizam o protocolo HTTP em uma API Restful e foi utilizado o pacote *socket* para realizar a comunicação multicast (UDP) entre os supernodos.

### Organização
A organização do código para este trabalho esta dividido em:

1. Model
	1. Node
	2. Supernode
	3. UDP
2. Api
	1. Node
	2. Supernode
3. Background
	1. Supernode Check Liveness
4. Config
5. Resources

#### Model - Node
Esta classe possui a lógica referente ao funcionamento de um Nodo no sistema. Utilizando esta classe é possível:
- Listar os recursos de um nodo
- Buscar as informações sobre um recurso pelo seu identificador
- Buscar as informações sobre um recurso pelo seu identificador no Supernodo em que o Nodo esta registrado

Ao inicializar uma instância de `Node` é executado o registro do Nodo em um Supernodo, o Supernodo é definido através de uma variável de ambiente. Durante o processo de inicialização, o Nodo executa a busca dos seus recursos e registro em uma "base" local.

Durante o processo de inicialização o Nodo executa uma listagem e leitura dos recursos pertencentes ao Nodo. Para definir um identificador único entre os recursos em todos os Nodos, foi utilizado uma abordagem de ler o conteúdo dos recursos e a partir do conteúdo gerar um hash SHA 256 do conteúdo, tendo assim um identificador único para o recurso.

![[Pasted image 20210523153156.png]]

#### Model - Supernode
Esta classe possui a lógica referente ao funcionamento de um Supernodo no sistema. Utilizando esta classe é possivel:
- Registrar um Nodo
- Buscar as informações sobre um recurso pelo seu identificador
- Buscar os Nodos vivos
- Realizar um processo de identificação dos Nodos que estão registrados e estão vivos

Ao inicializar uma instância de `Supernode` é inicializado uma nova thread para responder às solicitações de recursos de outros Supernodos e é inicializado um *job* (processo que executa de 5-5 segundos) para inicializar o processo de identificação de Nodos vivos. Durante o processo de identificação de Nodos registrados que estão vivos é verificado se o Nodo não responde a 2 verificações seguidas (10 segundos), este Nodo é considerado morto e removido da listagem de nodos e removido o registro de seus recursos.

![[Pasted image 20210523153830.png]]


#### Model - UDP
Esta classe é responsável pelo funcionamento da comunicação multicast UDP entre os Supernodos. Utilizando esta classe é possível:
- Enviar mensagens de pesquisa de recurso. Essas mensagens são no formato `<supernode_name>;20;<hash_id>`
- Enviar mensagens de resposta sobre uma pesquisa de recurso. Nesse caso é utilizado dois códigos de mensagem: `21` e `22`. No caso do código `21` é uma resposta OK, ou seja, o Supernodo que respondeu tem um registro do recurso e enviou a localização do recurso (`<supernode_name>;21;<file_location>`). No caso do código `22` é uma resposta NOK, ou seja, o Supernodo respondeu que não possui conhecimento sobre o recurso solicitado (`<supernode_name>;22;<hash_id>`).
- Escutar ao grupo multicast esperando solicitações de pesquisa de recursos

![[Pasted image 20210523155116.png]]

#### Api - Node
Este arquivo possui a declaração e a lógica por trás dos recursos disponibilizados pela API de Nodos. A API disponibiliza as funcionalidades:
- Buscar os recursos de um Nodo. `GET /node/resources`
- Buscar um recurso específico. `GET /node/resources/<hash_id>`
- Buscar uma lista de recursos. `GET /node/resources/find?hash_ids=1,2,3,4`
- Verificar a saúde do nodo. `GET /node/health`

![[Pasted image 20210523155809.png]]

#### Api - Supernode
Este arquivo possui a declaração e a lógica por trás dos recursos disponibilizados pela API de Supernodos. A API disponibiliza as funcionalidades:
- Registro de um Nodo. `POST /supernode/register`
- Buscar um recurso. `GET /supernode/search/<hash_id>`
- Buscar uma lista de recursos. `GET /supernode/search?hash_ids=1,2,3,4`
- Buscar os Nodos que estão vivos. `GET /supernode/alive` 
- Executar o processo de avaliação de Nodos vivos. `GET /supernode/xxx`

![[Pasted image 20210523160129.png]]


#### Background - Supernode Check Liveness
Este processo é responsável por solicitar ao Supernodo, através de sua API, para que seja executado o processo de verificação de vida dos Nodos. Esse processo consiste no Supernodo realizar uma request HTTP para todos os Nodos registrados no path `/node/health`. Caso um Nodo não responda a duas solicitações de saúde, o Nodo é removido da lista de Nodos registrados no Supernodo e todos seus recursos são removidos da listagem do Supernodo.

Este processo é inicializado ao criar um Supernodo e é executado em uma espécie de *cronjob*.

![[Pasted image 20210523160506.png]]


#### Config
Esta pasta possui os arquivos `.env` para servir de configuração tanto para os Nodos quanto os Supernodos. Cada instância de Nodo ou Supernodo possui um arquivo específico, para não misturar as configurações de cada instância. Entre as configurações de um Nodo é definido quem é seu Supernodo e o caminho para seus recursos.

![[Pasted image 20210523160729.png]]


#### Resources
Esta pasta possui um conjunto de pastas e arquivos que servem como sendo os recursos que cada Nodo possui a sua disposição.

![[Pasted image 20210523160944.png]]


## Demonstração

### Máquinas Virtuais
Para inicias as máquinas virtuais para a demonstração é necessário ter a ferramenta **vagrant**(https://www.vagrantup.com) instalada além de possuir VirtualBox instalado. Após instalar as ferramentas necessárias é preciso estar na pasta `machine`, a qual contém o arquivo `Vagrantfile` com as configurações necessárias para inciar 3 máquinas virtuais, para executar o comando `vagrant up`.

![[Pasted image 20210523161257.png]]

### Simulação
Para executar a simulação é possível iniciar a quantidade que quiser de conexões com as máquinas virtuais, para este trabalho foi utilizado 3 máquinas virtuais e 5 conexões. Durante a simulação foi utilizado 2 Supernodos e 3 Nodos.

![[Screen Shot 2021-05-23 at 1.03.50 PM.png]]

Na máquina 1 (**host-1**) foram executados os dois Supernodos, um disponibilizado no endereço *192.168.35.10:5000* e outro no endereço *192.168.35.10:5001*. Na máquina 2 (**host-2**) foi executado um Nodo (**node1**), o qual foi disponibilizado no endereço *192.168.35.11:8000*. Na máquina 3 (**host-3**) foram disponibilizados outros dois Nodos, o Nodo 2 disponibilizado no endereço *192.168.35.12:8000* e o Nodo 3 disponibilizado no endereço *192.168.35.12:8001*.

![[Screen Shot 2021-05-23 at 1.42.22 PM.png]]

Como todos os serviços foram disponibilizados através de uma API utilizando o protocolo HTTP, foi possível utilizar o programa *Postman* para realizar requisições HTTP e interagir com todos os serviços.

#### Listagem de recursos de um Nodo
Neste exemplo foi executado a listagem de recursos do Nodo 1.

![[Screen Shot 2021-05-23 at 1.19.00 PM.png]]

#### Busca de informações sobre um recurso
Neste exemplo foi executado a busca de informações de um recurso provido pelo Nodo 1. Neste caso, não foi necessário solicitar informações ao Supernodo sobre o recurso.

![[Screen Shot 2021-05-23 at 1.19.38 PM.png]]


#### Busca de informações sobre um recurso - Supernodo
Neste exemplo foi executado uma busca de informações de um recurso no Nodo 2 mas o recurso é provido pelo Nodo 3, o que, neste caso, fez com que fosse executado uma pesquisa de recursos no Supernodo do Nodo 2 juntamente da comunicação em multicast entre os Supernodos para a descoberta da localização do recurso.

![[resource3-search-node2-multi-req.png]]

Interação do Nodo 2 com o Supernodo 1 e a comunicação multicast entre os Supernodos.
![[resource3-search-node2-multi.png]]




