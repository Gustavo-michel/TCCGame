## Para executar o projeto no seu computador, siga os passos abaixo:

1. Clone o repositório do GitHub(caso não tenha).

2. Instale as dependências necessárias:
```bash
pip install -r requirements.txt
```
3. Execute o django para a aplicação web:
```bash
python manage.py runserver
```

## Usando container docker

1. puxar container:
```bash
docker pull gustavomichelads/tccgamesapp
```

2. rodar container:
```bash
docker run -p 8000:8000 gustavomichelads/tccgamesapp
```