# Trabalho com conexão TCP.

### O Protocolo de Controle de Transmissão - TCP
Neste trabalho iremos explorar a implementação de uma aplicação rodando sobre TCP através da programação com sockets. Este trabalho tem a finalidade de trazer o conhecimento de programação e funcionamento básico do protocolo TCP, principalmente demonstrando os serviços que o TCP fornece para a camada de aplicação.

#### **Fluxo do trabalho**:
1. Procurar um código “Hello word” usando servidor TCP multi thread e seu cliente.
    - Este trabalho pode ser realizado em qualquer linguagem de programação, a escolha do aluno, mas lembre-se: não pode ser usado bibliotecas que manipulem o TCP, e sim usar o TCP diretamente através da criação e manipulação dos sockets.
2. **No servidor TCP** (deve executar antes do cliente)
    - Escolher um porta para comunicação (maior que 1024)
    - Aceitar a conexão do cliente
    - Criar uma thread com a conexão do cliente (para cada cliente). Na thread:
        - Receber **requisições** enviadas pelo cliente:
            - **“Sair”**
                - se sim: fechar a conexão.
                - Finalizar a thread.
            - **“Arquivo”** + NOME.EXT (Deve poder tratar arquivo maior que 10M ):
                - Abrir o arquivo solicitado.
                - Calcular o (Hash) do arquivo com SHA (Procure um exemplo de uso do SHA), que serve como verificador de integridade.
                - Escolher a ordem/como enviar (Atenção! Este será o seu protocolo, você define.)
                    - Nome do arquivo
                    - Tamanho
                    - Hash
                    - Dados
                    - Status (ok, nok, etc…)
                        - Ex.: arquivo inexistente.
            - **“Chat”**
                - Imprimir os dados recebidos na tela do servidor.
                - Tudo digitado no servidor será enviado para o Cliente como “Chat”
3. **No Cliente TCP** (deve executar depois do servidor)
    - Fazer a conexão para o endereço da máquina e porta escolhida para o servidor
        - Abrir socket
    - Enviar uma das opções tratadas no servidor (**requisições**), escolhida pelo usuário.
    - Receber os dados do servidor: (**Resposta**)
        - **“Sair”**
            - se sim: fechar a conexão.
            - Finalizar a thread.
        - **“Arquivo”**:
            - Receber os dados de acordo com a ordem escolhida. (Acabou de criar um protocolo!)
            - Abrir o arquivo.
            - Verificar o Hash
            - Gravar o arquivo no cliente.
        - **“Chat”**:
            - Imprimir os dados recebidos na tela do cliente.

#### **O trabalho deve**:

1. Usar Sockets TCP Multi-thread
    - Cliente e Servidor
2. **No cliente**:
    - O usuário escolher a requisição para se comunicar com o servidor.
    - Enviar as requisições para o servidor.
    - Receber as respostas do servidor e fazer o esperado.
    - Fazer verificação de integridade do arquivo recebido (Verificar se Hash é igual).
    - Deve poder tratar arquivo maior que 10M
3. **No Servidor**
    - Receber requisições de 2 Clientes simultâneos.
    - Tratar corretamente as requisições e fazer o esperado.


> [!WARNING]
> Este trabalho deverá ser defendido para o professor nas aulas definidas para este propósito para validar a nota.

> [!WARNING]
> O aluno deve usar as chamadas TCP e não pode usar bibliotecas que mascarem o trabalho.

> [!TIP]
> Para agilizar a verificação de integridade são utilizadas somas de verificação (checksums) ou resumos criptográficos como o MD5 e SHA.