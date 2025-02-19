# Automação Whatsapp com IA

## Descrição

- Este projeto automatiza o envio e recebimento de mensagens no WhatsApp para coletar avaliações. As mensagens são processadas por uma IA e os resultados são atualizados em uma planilha Excel.

## Funcionalidades

- **Envio de Mensagens:** Permite enviar mensagem carregadas `<code>`.txt `</code>` para números na planilha carregada `<code>`.xlsx `</code>.`
- **Reconhecimento de Mensagens:** Reconhece imagens no Navegador `<code>`Chrome for Testing `</code>` e envia para IA.
- **Processamento com IA:** Envia mensagens para IA avaliar sentimentos (star rating).
- **Atualização da Planilha:** Preenche as colunas da planilha com base nas respostas processadas.

## Tecnologias Usadas

- Python: Linguagem de programação usada para desenvolver o script.
- Json: Linguagem de programação usada para se comunicar com IA.
- Requests: Bilioteca Usada para chamadas com IA.
- Selenium: Biblioteca usada para automação no navegador.
- Tkinter: Biblioteca usada para interface gráfica simples no Python.
- Pandas: Biblioteca usada para ler planilhas e modificá-las.
- Openpyxl: Biblioteca para abrir documentos e usá-los na aplicação.
- Criptography: Biblioteca para criptografar API-Keys no Computador.
- Threading: Tecnologia usada para manter interface gráfica com eficiência.

---

- Docker: Para Containerização da Aplicação (Distribuição).
- PyInstaller: Para gerar Executável do Aplicativo (Distribuição).

## Requisitos

- Python 3.9 ou superior.
- Chrome for Testing `<code>`CfT `</code>` (para o Selenium).
- API-Keys para IA.
- Planilhas .xlsx (Modelos na pasta Docs).

## Instalação

1. ### Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/automacao-whatsapp.git
   cd automacao-whatsapp
   ```
2. ### Instale as dependências:

   ```pip
   pip install -r requirements.txt
   ```
3. ### Baixe o Chrome for Testing:

   - Baixe e instale a versão Stable mais Recente do Chrome for Testing (CfT) `<code>`https://googlechromelabs.github.io/chrome-for-testing/`</code>.`
   - Mova o `<code>`chrome.exe `</code>` para a mesma pasta onde está o executável.
4. ### Criptografe sua API Key:

   ```bash
   python -c "from utils.security import criptografar_credencial; criptografar_credencial('SUA_API_KEY')"
   ```
5. ### Prepara planilhas para dados:

   - Selecionar um Exemplo da pasta `<code>`docs `</code>.`

## Como Usar

1. Crie um Executável

   - No terminal na pasta do projeto execute:

   ```bash
   pyinstaller --onefile --windowed app/main.py
   ```
   - O argumento `<code>`--windowed `</code>` evita que o terminal apareça ao executar o aplicativo.
2. Organize os arquivos

   - O executável será gerado na pasta `<code>`dist/`</code>`. Mova o executável para a pasta de origem do projeto.
   - Certifique-se de que as pastas `<code>`data/`</code>` e `<code>`app/`</code>` estejam na mesma pasta que o executável.
3. Execute o Programa

   - Clique no executável que está na pasta raíz do projeto.
   - Abrirá o `<code>`CfT `</code>` já aberto na página `<code>`https://web.whatsapp.com `</code>.`
   - Escaneie o QR Code.
   - Volte ao Aplicativo e *aproveite!*
4. Distribua o Aplicativo:

   - Compacte a pasta `<code>`AUTOMACAO-WHATSAPP `</code>` e envie para outra máquina.
   - Na outra máquina, basta descompactar e clicar no main.exe.
