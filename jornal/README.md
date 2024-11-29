# Jornal

**Jornal** é uma aplicação em Python com uma interface gráfica (GUI) desenvolvida com `wxPython` para extração de texto de páginas da web. Este programa utiliza `requests` para obter o HTML das páginas e `BeautifulSoup` para fazer o scraping do conteúdo principal, exibindo-o de forma legível e sem anúncios.

## Funcionalidades

- Permite inserir um link de uma página de notícia e extrair todo o conteúdo de texto relevante.
- Exibe o conteúdo extraído em uma área de texto na interface.
- Inclui botões para processar e limpar a entrada e saída de dados.
- Inclui menu de contexto para operações de copiar, colar, desfazer e recortar na área de exibição do conteúdo.

## Pré-requisitos

Certifique-se de que as bibliotecas abaixo estão instaladas:

- `wxPython`: Para criar a interface gráfica.
- `requests`: Para fazer requisições HTTP e buscar o HTML das páginas.
- `BeautifulSoup4`: Para analisar o HTML e extrair o conteúdo.

Para instalar as dependências, execute:
```bash
pip install wxPython requests beautifulsoup4
```

## Uso

1. Insira o link de uma página de notícia na caixa de texto de URL.
2. Clique em **Processar** para extrair o conteúdo textual da página.
3. O texto extraído será exibido na área de resultado.
4. Use o botão **Limpar** para limpar os campos de entrada e saída.

## Código do Programa

O código principal está em `jornal.py`. Aqui está uma visão geral das principais funções:

- `OnProcess`: Obtém o link da entrada, realiza uma requisição HTTP para a URL inserida e usa o BeautifulSoup para encontrar o conteúdo de texto. Caso o conteúdo seja encontrado, ele é exibido na área de resultado.
- `OnClear`: Limpa os campos de URL e a área de resultado.

## Exemplo de Execução

- Após inserir uma URL válida e clicar em **Processar**, o programa exibe o conteúdo textual do artigo.
- Caso o URL esteja incorreto ou o site bloqueie o acesso, uma mensagem de erro será exibida.

## Licença

Este projeto está licenciado sob a licença MIT - consulte o arquivo LICENSE para mais detalhes.
