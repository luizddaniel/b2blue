
# **Projeto Django com Django Rest Framework**

## **Descrição**
Este projeto é uma API desenvolvida com Django e Django Rest Framework. O objetivo é fornecer uma estrutura para gerenciar e consumir dados por meio de endpoints RESTful.

---

## **Pré-requisitos**
Certifique-se de ter as ferramentas abaixo instaladas no seu sistema:

- Python 3.8 ou superior
- Pip (gerenciador de pacotes do Python)
- Virtualenv (opcional, mas recomendado)
- Banco de dados SQLite (configuração padrão)

---

## **Instalação**

1. **Clone o repositório**

   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. **Crie um ambiente virtual**
   (opcional, mas recomendado)

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**
   Crie um arquivo `.env` na raiz do projeto e adicione as seguintes configurações:

   ```
   DEBUG=True
   SECRET_KEY=sua_chave_secreta
   ```

---

## **Banco de Dados**

1. **Crie as migrações do banco de dados**

   ```bash
   python manage.py makemigrations
   ```

2. **Aplique as migrações**

   ```bash
   python manage.py migrate
   ```

---

## **Rodando o Servidor**

1. Execute o servidor Django no endereço `0.0.0.0:8000`:

   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

2. Acesse a API em:
   ```
   http://0.0.0.0:8000/
   ```

---

## **Rodando os testes**
1. Rodando o unit tests:
```bash
   python manage.py test
   ```

## **Endpoints**
### Exemplos de rotas configuradas:
- **Listar estação**: `GET /api/station/`
- **Criar estação**: `POST /api/station/`
- **Detalhes da estação**: `GET /api/rstation/<id>/`
- **Atualizar estação**: `PUT /api/station/<id>/`
- **Excluir estação**: `DELETE /api/station/<id>/`

---

## **Documentação da API**
Se você configurou o Swagger ou Redoc, acesse:

- **Swagger UI**: [http://0.0.0.0:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/)
- **Redoc**: [http://0.0.0.0:8000/api/schema/redoc/](http://127.0.0.1:8000/api/schema/redoc/)

---

## **Contribuindo**
Contribuições são bem-vindas! Por favor, envie suas sugestões ou abra um Pull Request.

1. **Crie um branch para sua feature**
   ```bash
   git checkout -b minha-feature
   ```

2. **Commit suas mudanças**
   ```bash
   git commit -m "Descrição da mudança"
   ```

3. **Envie suas alterações**
   ```bash
   git push origin minha-feature
   ```

4. **Abra um Pull Request**

---

## **Licença**
Este projeto é licenciado sob a [MIT License](LICENSE).
