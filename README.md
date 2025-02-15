# Projeto API - Processo Seletivo Stract 2025

Este projeto é uma API simples desenvolvida em Python com Flask que interage com a API externa fornecida pela Stract.

## Dependências

1. Python 3.x
2. Flask (instalado automaticamente via `requirements.txt`)

   ## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/Fernanda-Dantas/Processo-Seletivo-Stract-2025
   cd projeto-api

   
####  **Repositório GitHub**:
   - Crie um repositório público no GitHub.
   - Adicione seu código (o arquivo `app.py` e o `README.md`) no repositório.
   - Use os seguintes comandos para subir seu código no GitHub:
     ```bash
     git init
     git add .
     git commit -m "Primeiro commit"
     git remote add origin https://github.com/seu-usuario/projeto-api.git
     git push -u origin master
     ```
 ## Endpoints utilizados:
- Endpoint Raiz ("/"): http://127.0.0.1:5000/
- Endpoint "/platforms": http://127.0.0.1:5000/platforms
- Endpoint "/report/<platform>": http://127.0.0.1:5000/report/meta_ads
- Endpoint "/<platform>/resumo":  http://127.0.0.1:5000/meta_ads/resumo
- Endpoint "/geral": http://127.0.0.1:5000/geral
- Endpoint "/geral/resumo": http://127.0.0.1:5000/geral/resumo
  
##  **Testando a API**:
   Após rodar a aplicação localmente com `python app.py`, você pode testar os endpoints em `http://localhost:5000/` usando um navegador.

##  **Publicação do Repositório**:
   Após concluir os passos acima, você terá um repositório público no GitHub contendo o código.

---


### Resumo
1. **Instale as dependências**: Apenas Flask.
2. **Crie os endpoints**: Seguindo a documentação fornecida.
3. **Implemente o código em Flask**: Organize seu projeto em um arquivo `app.py`.
4. **Crie o `README.md`** com instruções de uso.
5. **Publique o código no GitHub**.
