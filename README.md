# Consumindo dados da API de Brandwatch com AWS Lambda

![](src/brandwatch-logo.png)

## Introdução

**O que é Brandwatch?**

Brandwatch é uma ferramenta de inteligência artificial para monitoramento de mídias sociais que busca interpretar e classificar menções dos usuários em diversos portais como Twitter, Instagram, Facebook, Blogs, portais de Notícias e etc.

**Sobre a API**

A API de Brandwatch é uma API páginada podendo trazer até cinco mil menções por requisição, permitindo 30 requisições a cada 10 minutos.

Nesse projeto utilizaremos a API do Brandwatch para extrair dados de menções sobre a marca, armazenando esses dados em ambiente de Data Lake onde será possível, por exemplo, disponibilizar serviços de monitoramento e gerenciamento de risco para os clientes sobre as menções da marca e entre outros estudos interessantes.

## O que utilizaremos?

**AWS CDK**

O AWS CDK é um framework que utiliza linguagem de programação para definir os recursos na nuvem que queremos utilizar usando CloudFormation ou também Terraform. Visando torna os projetos mais dinâmicos a medida que é possível implementar lógica. A longo prazo conforme os projetos vão se tornando maiores, fica mais fácil dar manutenção, replicar modelos de infraestrutura e acelerar o ínicio de novos projetos.

Nesse projeto, utilizaremos o AWS CDK para provisionar o recurso de Lambda na AWS.

Todo o processo de preparação do ambiente do CDK pode ser encontrado nessa documentação da AWS:

[Get Started with AWS CDK](https://aws.amazon.com/getting-started/guides/setup-cdk/?nc1=h_ls)

## Iniciando o projeto de CDK

Primeiramente criaremos uma pasta vazia necessária para iniciar o projeto de CDK. Em seguida executaremos o comando:

```
cdk init app --language python
```

Como no exemplo abaixo:

![](src/init-project-cdk.png)

O projeto vem com um ambiente virtual e com uma lista de dependências a ser instalada, então executaremos o comando para entrar no ambiente virtual:

```
source .venv/bin/activate
```

E em seguida instalaremos as dependencias utilizando o comando:

```
python -m pip install -r requirements.txt
```

Por final teremos essa estrutura do projeto:

![](src/structure-project-1.png)
