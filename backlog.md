## Backlog

O objetivo desse arquivo é simular um backlog ao listar pequenas tarefas que foram pensadas mas ainda não foram programadas.

Não fui criterioso quanto a categorização do que seria uma feature para o usuário final ou etapas do desenvolvimento.
Logo estarão como equivalente tarefas como alterar a interface para o usuário, mudanças no banco de dados, reestruturação do projeto, etc.
O importante aqui é saber o que foi feito recentemente e o que ainda pode ser feito que já foi pensado.

Além do registro do que está sendo feito, tarefas aqui lista serão progressivamente reorganizadas, agrupando algumas já feitas, adicionando novas, etc.

Um lembrete final: não me proponho a descrever extensivamente de forma prévia tudo. Parte do processo é descobrir o que deve ser feito

- Usuários Steam
  - Adicionar e manipular usuários Steam:
    - [ ] Cadastrar novo usuário Steam
    - [x] Selecionar qual usuário será usado para navegar 
  - Fazer login do usuário para acessar páginas privadas da Steam
    - [x] Adicionando cookies de login por meio de arquivo de texto
    - [ ] Adicionando cookies de login durante runtime
    - [ ] Simulando a página de login da Steam

- UI
  - Garantir que entradas do usuário não quebrem o programa
    - [x] Validar alguns tipos genéricos
    - [ ] Validar entradas baseado em dados já registrados no banco
  - Possibilitar mudança na lingua para o inglês
    - [x] (parcial) Isolar elementos da UI para facilitar traducao dos textos
    - [ ] Inserir textos em arquivos separados do código
    - [ ] Traduzir textos
    - [ ] Acessar comandos da UI por uma interface única que sabe qual lingua está configurada
  - GUI

- DB e data structures
  - Estabelecer o básico para persistir dados
    - [x] Criar banco localmente e conectá-lo com o programa
    - [x] (parcial) Usar pandas para todas as estruturas de dados (inventory ta mal feito)
    - [ ] DB remoto?
  - Avançar no DB
    - [x] Tabela de usuarios
    - [x] Tabela de jogos e eventos
    - [x] Tabelas de badges
    - [X] Tabelas de cartas
    - [ ] Tabela de items
    - [ ] Tabela de inventários

- Web crawlers
  - Geral
    - [x] Navegar pelas páginas por meio de requests
    - [ ] Navegar por meio do Selenium
    - [x] Desacoplar melhor usuários Steam dos web_crawlers
  - Steam Inventory
    - [x] (parcial) Fazer download e acessar itens do inventário
    - [x] Abrir pacotes de cartas da steam dado id do pacote
    - [ ] Abrir pacotes de cartas dado o nome do jogo
    - [ ] Capaz de extrair e persistir novas informações
  - Steam badges
    - [x] Capaz de extrair e persistir novas informações
    - [ ] Fazer transformação dos dados de forma assíncrona
    - [ ] Nova interação: construir badges
