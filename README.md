# Consumindo dados da API de Brandwatch com AWS Lambda

![](src/brandwatch.png)

## Introdução

**O que é Brandwatch?**

Brandwatch é uma ferramenta de inteligência artificial para monitoramento de mídias sociais que busca interpretar e classificar menções dos usuários em diversos portais como Twitter, Instagram, Facebook, Blogs, portais de Notícias e etc.

**Sobre a API**

A API de Brandwatch é uma API páginada podendo trazer até cinco mil menções por requisição, permitindo 30 requisições a cada 10 minutos.

Nesse projeto utilizaremos a API do Brandwatch para extrair dados de menções sobre a marca, armazenando esses dados em ambiente de Data Lake onde será possível, por exemplo, disponibilizar serviços de monitoramento e gerenciamento de risco para os clientes sobre as menções da marca e entre outros estudos interessantes.

## O que utilizaremos?

**AWS CDK**

O AWS CDK é um framework que utiliza linguagem de programação para definir os recursos na nuvem que queremos utilizar. O que a longo prazo conforme os projetos vão se tornando maiores, fica mais fácil dar manutenção, replicar modelos de infraestrutura e acelerar o ínicio de novos projetos.

Nesse projeto, utilizaremos o AWS CDK para provisionar o recurso de Lambda na AWS.