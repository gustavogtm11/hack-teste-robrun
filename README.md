# ROB RUN Research Labs

Aplicativos desktop independentes para pesquisa visual e testes locais de autorização de inventário.

> **Limites técnicos:** os programas não se conectam ao ROB RUN, não leem capturas de tela, memória, processos ou arquivos do jogo, não enviam comandos a servidores e não interagem com o Easy Anti-Cheat. O Overlay Lab desenha entidades sintéticas em uma janela transparente/sempre no topo. Ele não é um ESP funcional para partidas reais.

## Aplicativos

### 1. ROB RUN Overlay Lab

- Janela de overlay separada, sempre no topo e com transparência ajustável.
- Demonstração de rótulos de jogadores, skeleton, distância, veículos, equipamentos e mira.
- Cada elemento pode ser ativado/desativado no painel.
- Janela de overlay pode ser movida pela faixa superior.
- Usa exclusivamente dados fictícios gerados pelo próprio aplicativo.

Executar pelo código-fonte:

```powershell
py -3 overlay_lab.py
```

### 2. Inventory Security Lab

- Interface gráfica Windows usando Python/Tkinter.
- Banco local SQLite, salvo em `Documentos/RobRunInventoryLab/`.
- Catálogo ilustrativo de equipamentos.
- Simulação de solicitações com validação de propriedade.
- Teste de alegação adulterada do cliente, registro de auditoria e exportação CSV.

Executar pelo código-fonte:

```powershell
py -3 app.py
```

## Gerar os executáveis Windows

No Windows 10/11 com Python 3.10 ou superior, dê duplo clique em `build_windows.bat`. Serão criados:

- `dist/RobRunOverlayLab.exe`
- `dist/RobRunInventoryLab.exe`

A compilação também é executada automaticamente pelo GitHub Actions a cada alteração relevante na `main`. O pacote de saída chama-se `ROB-RUN-Labs-Windows`.

## Testar o Overlay Lab

1. Abra `RobRunOverlayLab.exe`.
2. O painel de controle e a janela de demonstração serão abertos.
3. Ative/desative Player labels, Skeleton, Distance, Vehicles, Equipment labels e Crosshair.
4. Ajuste a transparência.
5. Arraste a faixa superior do overlay para reposicioná-lo.
6. Use Mostrar/ocultar para esconder ou exibir a janela.

**Importante:** os nomes, distâncias, bonecos e veículos são exemplos sintéticos. O aplicativo não detecta entidades reais no ROB RUN.

## Testar o Inventory Security Lab

1. Abra `RobRunInventoryLab.exe`.
2. Selecione um item marcado como **Bloqueado**.
3. Clique em **Simular requisição adulterada**.
4. Resultado esperado: **REJECTED**, pois a alegação do cliente não substitui a autorização armazenada no simulador.
5. Selecione um item marcado como **Possuído** e clique em **Solicitar item**.
6. Exporte a auditoria CSV.

## Estrutura

- `overlay_lab.py`: overlay visual com entidades sintéticas.
- `app.py`: interface do laboratório de inventário.
- `lab/catalog.py`: catálogo fictício de demonstração.
- `lab/store.py`: persistência SQLite, regras de autorização e auditoria.
- `build_windows.bat`: compilação dos dois executáveis.
- `.github/workflows/build-windows.yml`: build automatizado para Windows.

## Pesquisa responsável

Podemos ampliar o catálogo usando recursos públicos e autorizados, documentar observações visuais e desenvolver cenários de teste em ambiente próprio. Não use os aplicativos para obter vantagem em partidas públicas ou contornar mecanismos de proteção.
