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
    - [x] Conferir quais usuários Steam foram cadastrados
    - [x] Selecionar qual usuário será usado para navegar 
  - Fazer login do usuário para acessar páginas privadas da Steam
    - [x] Adicionando cookies de login por meio de arquivo de texto
    - [ ] Adicionando cookies de login durante runtime
    - [ ] Simulando a página de login da Steam

- UI
  - Garantir que entradas do usuário não quebrem o programa
    - [x] Conferir alguns tipos genéricos
    - [ ] Conferir baseado em dados já registrados do usuário
    - [ ] Integrar com web_crawlers para solicitar conferência no site da Steam
  - Possibilitar mudança na lingua para o inglês
    - [x] (parcial) Isolar elementos da UI para facilitar traducao dos textos
    - [ ] Inserir textos em arquivos separados do código
    - [ ] Traduzir textos
    - [ ] Acessar comandos da UI por uma interface única que sabe qual lingua está configurada
  - GUI

- DB e data structures
  - Estabelecer o básico para persistir dados
    - [x] Criar banco localmente e conectá-lo com o programa
    - [ ] POO para data structures (padronizar elas como as paginas web estão padronizadas)
    - [x] (parcial) Usar pandas como padrão para estrutura de dados
    - [ ] DB remoto?
  - Avançar no DB
    - [ ] Entender mais sobre quais e como esses dados estão sendo coletados
    - [x] Tabela de usuarios
    - [x] Tabela de jogos e eventos
    - [x] (parcial) Tabela de badges
    - [ ] Tabela de cartas
    - [ ] Tabela de inventário (é preciso persistir esse dado?)

- Web crawlers
  - Geral
    - [x] Navegar pelas páginas por meio de requests
    - [ ] Desacoplar melhor usuários Steam dos web_crawlers
    - [ ] Fazer transformação dos dados de forma assíncrona
    - [ ] Navegar por meio do Selenium 
  - Steam Inventory
    - [x] Fazer download e acessar itens do inventário
    - [x] Abrir pacotes de cartas da steam dado id do pacote
    - [ ] Abrir pacotes de cartas dado o nome do jogo
    - [ ] Capaz de extrair e persistir novas informações
  - Steam badges
    - [x] Acessar páginas de forma logada
    - [x] (parcial) Capaz de extrair e persistir novas informações
    - [ ] Nova interação: construir badges
