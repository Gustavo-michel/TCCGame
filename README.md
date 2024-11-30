# Projeto TCC - BrainQuest

Este é um projeto de um site educativo focado em programação desenvolvido como Trabalho de Conclusão de Curso (TCC). O objetivo do sistema é oferecer uma plataforma de aprendizado com jogos educativos e funcionalidades e sistema competitivo entre usuários. O site conta com um front-end rico em detalhes e utiliza Firebase como backend para autenticação e gerenciamento de dados.

## Funcionalidades

### **Gerenciamento de Usuários**
- **Cadastro:** Permite registrar novos usuários com email e senha.
- **Login:** Autentica usuários utilizando Firebase Authentication.
- **Recuperação de Senha:** Envia um email para redefinição de senha.
- **Logout:** Realiza o logout dos usuários e limpa a sessão.

### **Sistema de Pontuação**
- Atualiza a pontuação do usuário e calcula o nível com base nos pontos.
- Exibe a posição global do usuário e os 3 melhores jogadores em um ranking.

### **Jogos Educativos**
O site oferece diversos jogos para promover o aprendizado de forma interativa:
- Jogo da Forca (**Hangman**).
- Jogo da Memória (**Memory**).
- Jogo de Palavras estilo Termo (**Wordle**).
- Jogo de Linguagem (**Linguage**).

### **Outras Funcionalidades**
- Exibição dos dados do usuário, como pontuação e nível, na página inicial.
- Página de Política de Privacidade.

## Tecnologias Utilizadas

- **Backend:** Python e Django.
- **Frontend:** HTML e CSS.
- **Banco de Dados:** Firebase Realtime Database.
- **Autenticação:** Firebase Authentication.
- **API:** JSON e metodos HTTP para comunicações entre o frontend e o backend.

## Estrutura de Arquivos

### **`views.py`**
Contém as seguintes funcionalidades principais:
1. **Gerenciamento de Usuários**
   - `register`: Cadastro de usuários.
   - `login`: Autenticação e login.
   - `forgotPassword`: Recuperação de senha.
   - `logout`: Finaliza a sessão do usuário.
   - `account`: Página de conta do usuário.

2. **Jogos**
   - `gameHangman`: Página do jogo da forca.
   - `gameMemory`: Página do jogo da memória.
   - `gameWordle`: Página do jogo estilo Wordle.
   - `gameLinguage`: Página do jogo de linguagem.

3. **Pontuação e Rankings**
   - `update_score`: Atualiza a pontuação e nível do usuário.
   - `position_users`: Recupera a posição do usuário e os três melhores do ranking.
   - `user_data`: Obtém os dados do usuário para exibição na página inicial.

4. **Outros**
   - `privacy`: Página da política de privacidade.

### **Templates**
- **`index.html`**: Página inicial.
- **`userRegister.html`**: Página de registro de usuários.
- **`userLogin.html`**: Página de login.
- **`userForgot.html`**: Página de recuperação de senha.
- **`userAccount.html`**: Página da conta do usuário.
- **`gameHangman.html`**: Página do jogo da forca.
- **`gameMemory.html`**: Página do jogo da memória.
- **`gameWordle.html`**: Página do jogo Wordle.
- **`gameLinguage.html`**: Página do jogo de linguagem.
- **`privacy.html`**: Página da política de privacidade.

## Configuração e Instalação
### Para executar o projeto no seu computador, siga os passos abaixo:

1. Clone o repositório do GitHub.

2. pegue a chave de api(package-lock.json), variaveis de ambiente(.env).

3. build container(primeira vez executando ou após mudança no dockerfile):
```bash
docker-compose build
```
ou para contruir o container e subir ao mesmo tempo:
```bash
docker-compose up --build
```

4. subindo o container (toda vez que for executar o projeto):
```bash
docker-compose up
```

3. acessar localhost:8000 e verificar o funcionamento.

## Melhorias Futuras
- Adição mais jogos educativos.
- Criar funcionalidades para aprendizado colaborativo, como chats.
- Aumentar o volume de personalização de usuário.
