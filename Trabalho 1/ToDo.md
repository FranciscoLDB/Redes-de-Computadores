# To-Do List: Implementação de Aplicação UDP

## Procurar Código de Exemplo
- [ ] Encontrar um código "Hello World" usando servidor UDP e cliente.

## Configuração do Servidor UDP
- [ ] Escolher uma porta para comunicação (maior que 1024).
- [ ] Implementar a recepção de dados no servidor.
- [ ] Tratar os dados recebidos (propor um protocolo próprio, ex.: GET /arquivo).
- [ ] Implementar a transmissão do arquivo requisitado pelo cliente (arquivo > 1 MB).
- [ ] Dividir o arquivo em pedaços (considerar tamanho do buffer e MTU).
- [ ] Definir e implementar o tamanho do buffer.
- [ ] Implementar checksums para verificação de integridade.
- [ ] Numerar os pedaços do arquivo.
- [ ] Implementar resposta para arquivo não encontrado.

## Configuração do Cliente UDP
- [ ] Configurar o endereço da máquina e porta do servidor.
- [ ] Implementar a requisição de um arquivo.
- [ ] Dar opção ao usuário para descartar parte do arquivo (simular perda de dados).
- [ ] Receber, montar e conferir o arquivo recebido (checksums).
- [ ] Apresentar o arquivo requisitado se estiver OK.
- [ ] Verificar e solicitar reenvio de pedaços faltantes se o arquivo não estiver OK.
- [ ] Interpretar e tratar erros (ex.: arquivo não encontrado).

## Testes e Validações
- [ ] Testar o que acontece se o servidor for desligado durante a transmissão e religado depois.
- [ ] Testar com dois clientes simultâneos requisitando arquivos diferentes.

## Defesa do Trabalho
- [ ] Preparar a defesa do trabalho para o professor nas aulas definidas.

## Considerações Importantes
- [ ] Usar Socket UDP diretamente, sem bibliotecas que mascarem o trabalho.
- [ ] Implementar somas de verificação (checksums) ou resumos criptográficos (MD5, SHA) para verificação de integridade.
