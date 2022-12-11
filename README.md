# Bem vindo ao AWS Terminal

## 1. Pacotes necessários:
Para funcionamento da aplicação, é preciso que o usuáro tenha os seguintes pacotes baixados:

```
terraform -> version 0.10.1
boto3 -> version 1.26.16
rich -> version 12.6.0
aws-cli
```

### 1.1 Instalando pacotes:

Siga o tutorial de como instalar terraform no [site oficial da Hashicorp](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli).

Para os outros pacotes, use os códigos abaixo:
```
pip install boto3==1.26.16
pip install rich==12.6.0
sudo apt-get install awscli
```

## 2. Iniciando o programa
Antes de rodar sua aplicação, é necessário ter um usuário da AWS com suas credenciais salvas (access key e secret key), além de setar esse usuário para a utilização do *boto3* (que apenas serve para listar os recursos, que é uma das funcionalidades do programa) e setar suas chaves como variáveis de ambiente para o terraform usá-las sem riscos de vazamentos.

**Lembre-se, cuidado com as suas credenciais, não as deixe expostas em nenhum lugar onde possam ser vazadas!**

Primeiro, vamos setar suas variáveis de ambiente:
- Abra o arquivo *.bashrc*, que define as variáveis de ambiente padrão do seu console (toda vez que o console inicia, esse arquivo define as variáveis , entre outras coisas):
```
nano ~/.bashrc
```
- Dentro da interface do terminal, deça até o final do arquivo e copie essas linhas de código, mudando os Xs para respectivamente sua Access Key e Secret Key:
```
# Setting my enviroment variables

export AWS_ACCESS_KEY_ID="XXXXXXXXXXX"   # Essa é sua Access Key
export AWS_SECRET_ACCESS_KEY="XXXXXXXXXXXXXXX"  # Essaé sua Secret Key
```

Após definidas as variáveis de ambiente, vamos setar seu usuário no boto3:
```
aws configure --profile "your username"
```

**IMPORTANTE**: Esse será o usuário que você irá usar dentro da aplicação.

Agora você está pronto para usar a aplicação. Ela funciona na base do terminal, e a interface varia na digitação dos números das opções listadas!

## 3. Usando a aplicação

Uma vez dentro da aplicação, você será requisitado primeiro a digitar seu usuário (o mesmo que foi configurado no boto3 na etapa anterior) e selecionar sua região. Assim que fizer isso, poderá explorar as seguintes opções:

1. Instâncias
- 1.1 Criar
- 1.2 Deletar
- 1.3 Listar

2. Usuários
- 2.1 Criar
- 2.2 Deletar
- 2.3 Listar

3. Security Groups
- 3.1 Criar
- 3.2 Deletar
- 3.3 Listar

**Todas mudanças realizadas à esses itens são aplicadas automaticamente usando o terraform**

4. Update Cloud from Local
- Opção criada com a intenção de, se há discrepâncias entre nuvem e local, e deseja subir a infraestrutura sem realizar nenhuma mudança.

5. Quit 
- Opção de sair da aplicação

As instruções mais específicas estão dentro da aplicação, e conforme o usuário explora a aplicaão, a experiência deve ser bem intuitíva.
  

