# Consumindo dados da API de Brandwatch com AWS Lambda

![](src/brandwatch-logo.png)

## Introdução

**O que é Brandwatch?**

Brandwatch é uma ferramenta de inteligência artificial para monitoramento de mídias sociais que busca interpretar e classificar menções dos usuários em diversos portais como Twitter, Instagram, Facebook, Blogs, portais de Notícias e etc.

**Sobre a API**

A API de Brandwatch é uma API páginada podendo trazer até cinco mil menções por requisição, permitindo 30 requisições a cada 10 minutos.

Nesse projeto utilizaremos a API do Brandwatch para extrair dados de menções sobre a marca, armazenando esses dados em ambiente de Data Lake onde será possível, por exemplo, disponibilizar serviços de monitoramento e gerenciamento de risco para os clientes sobre as menções da marca e entre outros estudos interessantes.

## O que utilizaremos?

**AWS CLI**

<img src="src/aws-cli.png" width="12%">

Utilizaremos o AWS CLI para gerenciar os serviços da AWS por linha de comando.

A instalação do pode ser feita seguindo a documentação da AWS: [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

**AWS CDK + CloudFormation**

<p float="left">
<img src="src/cdk-logo.png" width="20%">
<img src="src/cloud-formation.png" width="7%">
</p>

O AWS CDK é um framework que utiliza linguagem de programação para definir os recursos na nuvem que queremos utilizar usando CloudFormation ou também Terraform. Visando torna os projetos mais dinâmicos a medida que é possível implementar lógica. A longo prazo conforme os projetos vão se tornando maiores, fica mais fácil dar manutenção, replicar modelos de infraestrutura e acelerar o ínicio de novos projetos.

Nesse projeto, utilizaremos o AWS CDK para provisionar o recurso de Lambda na AWS.

Todo o processo de preparação do ambiente do CDK pode ser encontrado nessa documentação da AWS:

[Get Started with AWS CDK](https://aws.amazon.com/getting-started/guides/setup-cdk/?nc1=h_ls)

**AWS LAMBDA**

<img src="src/lambda-logo.png" width="10%">

A AWS Lambda é um serviço serveless (sem necessidade de provisionar servidores) com a vantagem de pagar somente pelo tempo que a função permeneceu rodando (no máximo 15 minutos) e os recursos utilizados para otimizar o desempenho.

Utilizaremos a AWS Lambda para executar nosso módulo que faz as requisições para a API de Brandwatch usando a biblioteca requests do Python.

**AWS S3**

<img src="src/s3-logo.png" width="10%">

AWS S3 é um serviço de armazenamento de objetos divido em buckets. Onde será dada a carga dos dados que vem da API na camada de Landing Zone do nosso Data Lake.

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

Então o CDK gerou um módulo **brandwatch_cdk_stack.py** que possuí a classe **BrandwatchCdkStack**. Quando instanciamos essa classe estamos construindo uma Stack de recursos com o CloudFormation. Stacks são conjuntos de recursos que decidimos provisionar através um template do CloudFormation que nesse caso será construído através do CDK.

Pra provisionarmos o recurso de Lambda Function, precisamos antes importar o módulo de aws_lambda do CDK. Iremos instalar o módulo passando **aws_cdk.aws_lambda** para o **requirements.txt** e dentro da virtualenv executar o comando:

```
python -m pip install -r requirements.txt
```

Importando o módulo, iremos inserir no método **__init__** da classe **BrandwatchCdkStack** uma variavel que daremos o nome de **lambda_bw_api** que vai instanciar a classe **Function** do módulo **aws_lambda** passando os seguintes argumentos para os respectivos parametros:

- scope: parametro que recebe o Stack onde iremos fazer o deploy da Lambda Function, no caso a própria BrandwatchCdkStack, então passaremos como argumento somente: self;

- id: recebe uma string com o nome que daremos para o recurso dentro do CloudFormation onde passaremos: BrandwatchAPIExtract;

- runtime: passaremos o runtime do Python 3.8 que vem do módulo aws_lambda dessa forma: 

    lambda_bw.Runtime.PYTHON_3_9

- timeout: recebe um objeto do tipo Duration. Usaremos o método minutes para definir o tempo máximo para timeout da função que será de 15 minutos - tempo máximo que uma Lambda pode rodar.

    Como na documentação de Runtime do módulo aws_lambda: [Runtime](
https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_lambda/Runtime.html#aws_cdk.aws_lambda.Runtime);

- code: recebe um objeto do tipo Code onde vamos usar o método from_asset pra apontar a pasta onde está código da nossa função Lambda. Então criamos uma pasta code no nível do módulo **brandwatch_cdk_stack.py** e dentro da pasta teremos o modulo com o código que faz as requisições para a API de Brandwatch e guarda os objetos JSON das requisições no Data Lake. Passaremos dessa forma:

    lambda_bw.Code.from_asset('brandwatch_cdk/code')

    Então tudo o que estiver dentro da pasta code vai ser usado para construção da Lambda.

- handler: passaremos o módulo **lambda_handler** que criamos e a função **handler** que será executada dessa forma:

    lambda_handler.handler

- inicial_policy: Aqui declaramos as politicas inicias da função, passando como argumento um array de políticas que vai pode fazer inserção de objetos no S3 com uma lista de ações, no caso aqui somente a s3:PutObject e uma lista de ARNs (Amazon Recurse Names) do S3 com o nome do Bucket e acesso recursivo em todas as pastas do Bucket. Dessa forma:

    [bw_iam.PolicyStatement(actions = "s3:PutObject", ['arn:aws:s3:::data-lake-brandtest/*'])]

- memory_size: iremos atribuir 512, pois somente 128 a função acaba incorrendo em timeout por conta da quantidade de dados.

No final o objeto instanciado na lambda_bw_api ficará dessa forma:

![](src/object-function.png)

Mais propriedades da Function podem ser encontradas aqui na documentação do módulo **aws_lambda**: [Function](https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_lambda/Function.html)

## Provisionando um Bucket S3 para Data Lake

Também iremos criar um Bucket S3 que terá uma camada de landing zone para a ingestão dos dados brutos da API.

Precisaremos importar o módulo **aws_s3** usando a classe **Bucket** que atribuiremos a variável **bucket_data_lake** usaremos os seguintes parametros:

- scope, id: com as mesma finalidades da Function;

- bucket_name: onde passaremos uma string com o nome do bucket: brandwatch-mentions-test;

- block_public_access: vamos usar o objeto BlockPublicAccess restringindo o acesso público usando o parametro restrict_public_buckets como True;

Ficando dessa forma:

![](src/object-bucket.png)

Feito isso, podemos executar o comando:

```
cdk synth
```

E teremos a saída de um arquivo YAML que faremos o deploy para a CloudFormation 

Imagem de parte do arquivo para exemplo:

![](src/yaml-cdk.png)

Para fazer o deploy, temos que ter um perfil de usuário configurado com as credenciais utilizando **AWS CLI** e exportar o perfil de usuário para a variável de ambiente **AWS_PROFILE** como na imagem:

![](src/export-profile.png)

Em seguida, para isolarmos o que é recurso para CloudFormation do que não faz parte do CloudFormation - por exemplo o módulo das requisições para a API - precisaremos executar o comando comando:

```
cdk bootstrap
```

![](src/cdk-bootstrap.png)

Feito isso, para relizar o deploy da Lambda, executamos o comando:

```
cdk deploy
```

![](src/cdk-deploy.png)

No console do CloudFormation podemos então olhar a Stack de recursos que criamos e ver todos os recursos provisionados com o AWS CDK:

![](src/cloud-formation-resources.png)

Em seguida, testando a função Lambda podemos ver que os dados de menções foram carregados na camada de landing zone do Data Lake no S3:

![](src/log-lambda.png)
![](src/json-objects-s3.png)

Link do módulo que faz as requisições pra API: [bw_requests.py](https://github.com/macielf1994/brandwatch-api-extract/blob/master/brandwatch-cdk/brandwatch_cdk/code/bw_requests.py)