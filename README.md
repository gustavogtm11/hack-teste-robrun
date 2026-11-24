# ROB RUN Inventory Security Lab

Aplicativo desktop local para estudar conceitos de autorização de inventário e registrar testes reproduzíveis.

> **Escopo:** este projeto é um laboratório independente. Ele não se conecta ao ROB RUN, não lê nem modifica processos/arquivos do jogo, não envia comandos a servidores e não interage com o Easy Anti-Cheat. O catálogo inicial contém apenas itens ilustrativos, não nomes ou IDs verificados do jogo.

## Recursos da primeira versão

- Interface gráfica para Windows usando Python/Tkinter.
- Banco local SQLite, salvo em `Documentos/RobRunInventoryLab/`.
- Catálogo de equipamentos ilustrativos.
- Simulação de solicitação de item com validação de propriedade no lado autoritativo.
- Teste de alegação adulterada do cliente, que deve ser rejeitada quando não há autorização.
- Registro de auditoria e exportação CSV.

## Executar pelo código-fonte

Requisitos: Windows 10/11 e Python 3.10+.

```powershell
py -3 app.py
```

## Gerar o instalável/executável

Dê duplo clique em `build_windows.bat`. O script cria um ambiente virtual, instala PyInstaller e gera:

```
dist/RobRunInventoryLab.exe
```

O executável é portátil e cria o banco SQLite no primeiro uso. A compilação deve ser feita no Windows para gerar um binário Windows.

## Como testar

1. Abra o aplicativo.
2. Selecione um item marcado como **Bloqueado**.
3. Clique em **Simular requisição adulterada**.
4. O resultado esperado é **REJECTED**, pois a alegação enviada pelo cliente não substitui a autorização armazenada no servidor simulado.
5. Selecione um item marcado como **Possuído** e clique em **Solicitar item**. O simulador deve confirmar a propriedade.
6. Exporte a auditoria CSV para guardar os resultados.

## Estrutura

- `app.py`: interface gráfica.
- `lab/catalog.py`: catálogo fictício de demonstração.
- `lab/store.py`: persistência SQLite, regras de autorização e auditoria.
- `build_windows.bat`: geração do executável.

## Próximas etapas de pesquisa

- Adicionar importação de catálogos obtidos de fontes públicas e autorizadas.
- Criar cenários de teste de autorização (propriedade, desbloqueio, consistência e persistência).
- Gerar relatórios técnicos com passos de reprodução, impacto e evidências.
- Analisar apenas interfaces, arquivos e comportamentos que possam ser examinados sem contornar controles ou afetar partidas públicas.

## Divulgação responsável

Qualquer possível falha real deve ser validada somente com autorização explícita do responsável pelo serviço e reportada pelo canal oficial de suporte/segurança do desenvolvedor. Não use este laboratório para obter vantagem em partidas públicas.
