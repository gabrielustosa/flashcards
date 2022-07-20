# Flashcards

Flashcards é uma plataforma de criação de cartões para memorização de palavras em inglês

## Tecnologias usadas

Abaixo está a lista de todas as tecnologias usadas para a construção desse projeto.

* [Django](https://docs.djangoproject.com/en/4.0/)
* [PostgreSQL](https://www.jetbrains.com/datagrip/features/?source=google&medium=cpc&campaign=15034928143&term=postgresql&gclid=CjwKCAjwzeqVBhAoEiwAOrEmzXvmumNvZqv3cvPSzs16PuethLHO7dukXPMc3g6XyhQkcsiHkCnHKRoCNt4QAvD_BwE)
* [Tailwind](https://tailwindcss.com/)
* [HTMX](https://htmx.org/)
* [Hyperscript](https://hyperscript.org/)

## Iniciando projecto

Siga os passos abaixo para iniciar o projeto localmente em sua máquina.

### Instalação

Primeiro passo é clonar o projeto dentro do seu editor de código dessa maneira.

```
git clone https://github.com/gabrielustosa/flashcards.git
```

Agora, dentro da pasta que você baixou inicie um ambiente virtual.

```
python3 -m venv venv
source venv/bin/activate
```

Instale todos os pacotes necessários

```
pip install -r requirements/_base.txt
```

Ajuste o .env

```
cp .env-example .env
nano .env
```

Faça as migrações 

```
python manage.py migrate
```

### Observação

Você precisa de uma chave para API de traduções da microst, saiba mais [aqui](https://docs.microsoft.com/pt-br/azure/cognitive-services/Translator/translator-text-apis?tabs=python#translate-text)


## Contato

Gabriel Lustosa Queiroz - [@gabrielustosa](https://www.linkedin.com/in/gabrielustosa) -  me@gabrielustosa.com.br
