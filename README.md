# Bem vindo ao AWS Terminal

## 1. Pacotes necessários:
Para funcionamento da aplicação, é preciso que o usuáro tenha os seguintes pacotes baixados:

```
terraform -> version 0.10.1
boto3 -> version 1.26.16
rich -> version 12.6.0
```

### 1.1 Instalando pacotes:

Siga o tutorial de como instalar terraform no [site oficial da Hashicorp](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli).

Para os outros pacotes, use os códigos abaixo:
```
pip install boto3==1.26.16
pip install rich==12.6.0
```

## Iniciando o programa
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
