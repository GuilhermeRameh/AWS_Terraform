import os
from rich.console import Console, Group
from rich.text import Text
from rich.prompt import Confirm
from rich.panel import Panel
from rich.align import Align
from rich.pretty import pprint
import json
import boto3

console = Console()
console.clear()

global region
global username
global dict_variables
global dict_users
username = console.input("Digite seu [green]usuário[/]: ")
region_sel = console.input("Selecione sua [cyan]região[/]: \n1. us-east-1\n2. us-west-1\n")

if region_sel=='2':
    region = "us-west-1"
else:
    region = "us-east-1"

if region=="us-east-1":
    vpc_cidr_block = "10.0.0.0/16"
    ubuntu_2004 = "ami-0149b2da6ceec4bb0"
    ubuntu_2204 = "ami-08c40ec9ead489470"
else:
    vpc_cidr_block = "10.1.0.0/16"
    ubuntu_2004 = "ami-0149b2da6ceec4bb0"
    ubuntu_2204 = "ami-08c40ec9ead489470"


session = boto3.Session(profile_name=username, region_name=region)
ec2client = session.client('ec2')
ec2iam = session.client('iam')
ec2re = session.resource('ec2')

with open("terraform/variables.json", "r") as jsonfile:
    dict_variables = json.load(jsonfile)

dict_variables["aws_region"] = region
dict_variables["vpc_cidr_block"] = vpc_cidr_block

# with open("terraform/users.json", "r") as jsonfile:
#     dict_users = json.load(jsonfile)

START = True
console.clear()

tela_inicial = Group(
    Panel(f"Bem Vindo ao terminal AWS!\nDigite qual ação gostaria de fazer:\nRegião: [cyan]{region}[/]", title="AWS TERMINAL", title_align="left"),
    "(1.) [green]Instâncias[/]\n(2.) [yellow]Usuários[/]\n(3.) [purple]Security Group[/]\n('u') [magenta]Update Cloud from Local[/]\n('q') [red]Quit[/]",
)
console.print(Panel(tela_inicial))
var = console.input()
while START:
    console.clear()
    if var=="1":
        instancia_dict={}
        tela_instancias = Group(
            Panel("O que quer fazer?", title="INSTÂNCIAS", title_align="left"),
            "(1.) [green]Criar[/]\n(2.) [red]Deletar[/]\n(3.) [yellow]Listar[/]\n('q') Voltar",
        )
        console.print(Panel(tela_instancias), "")
        instancia_act = console.input()
        if instancia_act=="1":
            # criar
            console.clear()
            console.print(Panel("Escolha a imagem da sua instância:\n(1.) Ubuntu 20.04\n(2.) Ubuntu 22.04"))
            id_imagem_sel = console.input()
            if id_imagem_sel=="1":
                id_imagem = ubuntu_2004
            else:
                id_imagem = ubuntu_2204

            console.print(f"Id da Imagem Escolhida: [cyan]{id_imagem}[/]")
            console.print(Panel("Agora escolha o tipo da instância que deseja criar:\n(1.) t2.nano\n(2.) t2.micro\n(3.) t2.small"))
            inst_type_sel = console.input()
            if inst_type_sel=="1":
                inst_type = "t2.nano"
            elif inst_type_sel=="2":
                inst_type = "t2.micro"
            else:
                inst_type = "t2.small"

            console.print(f"Tipo de instância escolhida: [cyan]{inst_type}[/]")
            console.print(Panel(f"Gostaria de adicionar um [i]Security Group[/] à sua instância? Caso não, usará o sec group 'default'."))
            if Confirm.ask():
                console.print("Digite o nome do Security Group que gostaria de adicionar:")
                sec_gp_name = console.input()

                if sec_gp_name not in dict_variables["sec_groups"].keys():
                    console.print("[b red]Nenhum Security Group com esse nome. Vá para a aba de SGs e crie um com esse nome, ou use outro SG.")
                    console.print("Aperte [i red]'Enter'[/] para sair")
                    input()
                    break

            else:
                sec_gp_name = "default"
                
            console.print(Panel("Por fim, nomeie sua máquina:"))
            inst_name = console.input()
            
            dict_variables["instances"][inst_name] = {"image_id": id_imagem, "instance_type":inst_type, "sec_group":sec_gp_name}
            with open("terraform/variables.json", "w") as jsonfile:
                jsonfile.write(json.dumps(dict_variables, indent=4))

            with console.status("Aplicando Nova Instância...", spinner="aesthetic"):
                os.system("cd terraform && terraform init && terraform apply -var-file=variables.json -auto-approve")
        
        elif instancia_act=="2":
            # deletar
            console.clear()
            console.print(Panel("Digite o nome da instância que deseja [red]apagar[/]: "))
            inst_del = console.input()
            if inst_del not in dict_variables["instances"]:
                console.print("[b red]Instância não encontrada, você pode checar as instâncias válidas com a opção 'Listar'.")
                console.input("Aperte [red]'Enter'[/] para continuar")
            else:
                instancia = dict_variables["instances"][inst_del]
                confirmation = Confirm.ask(f"[b red]Você vai deletar a instância {instancia}, tem certeza?")
                if confirmation:
                    dict_variables["instances"].pop(str(inst_del))
                    with open("terraform/variables.json", "w") as jsonfile:
                        jsonfile.write(json.dumps(dict_variables, indent=4))

                    with console.status("Aplicando Delete...", spinner="aesthetic"):
                        os.system("cd terraform && terraform init && terraform apply -var-file=variables.json -auto-approve")

        elif instancia_act=="3":
            console.clear()
            with console.status("Listando Instâncias ...", spinner="aesthetic"):
                for each in ec2re.instances.all():
                    console.print(f"[green]Id:[/] " + each.id + "; [green]Nome:[/] " + each.tags[0]["Value"] + "; [green]Estado:[/] " + each.state["Name"] + "; [green]Tipo:[/] " 
                    + each.instance_type +  "; [cyan]Região:[/] "+  each.placement['AvailabilityZone'])
            
            console.print("Aperte [i red]'Enter'[/] para sair")
            input()

        # elif instancia_act=='4':
        #     console.clear()
        #     console.print(Panel("Digite o nome da instância que deseja [green]ligar (start)[/] ou [red]desligar (stop)[/]: "))
        #     inst_name_sel = console.input()
        #     if inst_name_sel not in dict_variables["instances"].keys():
        #         console.print("[b red]Instância não encontrada, você pode checar as instâncias válidas com a opção 'Listar'.")
        #         console.input("Aperte [red]'Enter'[/] para continuar")
        #     else:
        #         with console.status("Fetching Id...", spinner="aesthetic"):
        #             for instance in ec2re.instances.all():
        #                 if instance.tags[0]["Value"] == inst_name_sel:
        #                     status_inst = instance.state

        #         console.print(f'O estado da instância é: {status_inst["Name"]}')
        #         input()

        elif instancia_act=='q':
            var=0
        
    elif var=="2":
        tela_usuarios = Group(
            Panel("O que quer fazer", title="USUÁRIOS", title_align="left"),
            "(1.) [green]Criar[/]\n(2.) [red]Deletar[/]\n(3.) [yellow]Listar[/]\n('q') Voltar",
        )
        console.print(Panel(tela_usuarios))
        usuarios_act = console.input()

        if usuarios_act=="1":
            # criar
            console.clear()
            console.print(Panel("Digite o nome do usuário que deseja [green]Criar[/]: "))
            console.print("[i](ele será criado com as permissões padrões de usuário aws)[/]")
            new_user_name = console.input()
            if new_user_name not in dict_variables["users"].keys():
                dict_variables["users"][new_user_name]={"username":new_user_name}
                with open("terraform/variables.json", "w") as jsonfile:
                    jsonfile.write(json.dumps(dict_variables, indent=4))

                with console.status("Criando Usuário...", spinner="aesthetic"):
                    os.system("cd terraform && terraform init && terraform apply -var-file=variables.json -auto-approve")
                console.print("[b red]ATENÇÃO! Procure pela chave de acesso gerada, e copie para um local seguro!\nPara acessar este usuário criado, vá para o site da AWS, e faça login com o nome que você escolheu e a senha gerada.\n Você será pedido para trocar a senha imediatamente.")
                console.print("Quando estiver pronto, aperte [i red]'Enter'[/] para sair")
                input()
            else:
                console.print("[b red]Este usuário já existe, crie com outro nome.")
                console.input("Aperte [red]'Enter'[/] para continuar")
                input()              
        
        elif usuarios_act=="2":
            # deletar
            console.clear()
            console.print(Panel("Digite o nome do usuário que deseja [r]apagar[/]: "))
            user_del = console.input()
            if user_del not in dict_variables["users"]:
                console.print("[b red]Instância não encontrada, você pode checar as instâncias válidas com a opção 'Listar'.")
                console.input("Aperte [red]'Enter'[/] para continuar")
            else:
                if Confirm.ask(f"[b red]Você está prestes a deletar o usuário {user_del} e suas credenciais, tem certeza?[/]"):
                    dict_variables["users"].pop(user_del)
                    with open("terraform/variables.json", "w") as jsonfile:
                        jsonfile.write(json.dumps(dict_variables, indent=4))

                    with console.status("Deletando usuário...", spinner="aesthetic"):
                        os.system("cd terraform && terraform init && terraform apply -var-file=variables.json -auto-approve")
                    

        elif usuarios_act=="3":
            console.clear()
            with console.status("Listando Usuários ...", spinner="aesthetic"):
                for user in ec2iam.list_users()['Users']:
                    console.print(f'[green]Username:[/] {user["UserName"]}')
            
            console.print("Aperte [i red]'Enter'[/] para sair")
            input()
        
        elif usuarios_act=='q':
            var=0

    elif var=="3":
        tela_secgroup = Group(
            Panel("O que quer fazer?", title="SECURITY GROUP", title_align="left"),
            "(1.) [green]Criar Security Group[/]\n(2.) [red]Deletar Security Group[/]\n(3.) [yellow]Listar SGs[/]\n('q') Voltar"
        )
        console.print(Panel(tela_secgroup))
        sec_act = console.input()

        if sec_act=="1":
            # criar
            console.clear()
            console.print(Panel("Digite o nome do Security Group que gostaria de adicionar:"))
            sec_gp_name = console.input()

            if sec_gp_name not in dict_variables["sec_groups"].keys():
                console.print("Nenhum Security Group com esse nome. Criando um novo:\n")

                aws_from_port = console.input(f"Digite a porta de origem (from port):")
                aws_to_port = console.input(f"Digite a porta de destino (to port):")
                aws_protocol = console.input(f"Digite o protocolo (ex: 'tcp'):")
                aws_cidr_blocks = console.input(f"Digite o bloco CIDR (ex: '0.0.0.0/0'):")

                dict_sg = {"ingress" : {"description" : str("custom sec group"), \
                                            "from_port" : str(aws_from_port), 
                                            "to_port" : str(aws_to_port),
                                            "protocol" : str(aws_protocol), 
                                            "ipv6_cidr_blocks" : None,
                                            "prefix_list_ids" : None,
                                            "self" : None,
                                            "security_groups" : None,
                                            "cidr_blocks" : [str(aws_cidr_blocks)]}}

                dict_variables["sec_groups"][sec_gp_name] = {"name": sec_gp_name, "ingress": [dict_sg]}

                with open("terraform/variables.json", "w") as jsonfile:
                    jsonfile.write(json.dumps(dict_variables, indent=4))

                os.system("cd terraform && terraform init && terraform apply -var-file=variables.json -auto-approve")

            else:
                console.print("[b red]Esse grupo de segurança já existe. Crie com outro nome, ou delete o existente.[/]")
                console.print("Aperte [i red]'Enter'[/] para sair")
                input()
        
        elif sec_act=="2":
            # deletar
            console.print("Digite o nome do Security Group que gostaria de [red]deletar[/]:")
            sec_gp_name = console.input()
            if sec_gp_name not in dict_variables["sec_groups"].keys():
                console.print("[b red]Security Group não encontrado, você pode checar os grupos válidos com a opção 'Listar'.")
                console.input("Aperte [red]'Enter'[/] para continuar")
            else:
                if Confirm.ask(f"[b red]Você está prestes a apagar o Security Group {sec_gp_name}. Tem certeza?[/]"):
                    dict_variables["sec_groups"].pop(sec_gp_name)

                    with open("terraform/variables.json", "w") as jsonfile:
                        jsonfile.write(json.dumps(dict_variables, indent=4))
                    
                    os.system("cd terraform && terraform init && terraform apply -var-file=variables.json -auto-approve")
        
        elif sec_act=="3":
            console.clear()
            with console.status("Listando Security Groups ...", spinner="aesthetic"):
                for secgroup in ec2re.security_groups.all():
                    console.print(f'[green]Security Group:[/] {secgroup.group_name}')
                    for rule in secgroup.ip_permissions:
                        console.print(f'    [white]Regra:[/] {rule}\n')
            
            console.print("Aperte [i red]'Enter'[/] para sair")
            input()
        
        elif sec_act=='q':
            var=0

    elif var=='u' or var=="U":
        with console.status("Updating Infrastructure ...", spinner="bouncingBar"):
            os.system("cd terraform && terraform init && terraform apply -var-file=variables.json -auto-approve")
        var=0

    elif var=="q" or var=="Q":
        START=False
        break 

    else:
        tela_inicial = Group(
            Panel(f"Bem Vindo ao terminal AWS!\nDigite qual ação gostaria de fazer:\nRegião: [cyan]{region}[/]", title="AWS TERMINAL", title_align="left"),
            "(1.) [green]Instâncias[/]\n(2.) [yellow]Usuários[/]\n(3.) [purple]Security Group[/]\n('u') [magenta]Update Cloud from Local[/]\n('q') [red]Quit[/]",
        )
        console.print(Panel(tela_inicial))
        var = console.input()

# with console.status("Initializing ...", spinner="aesthetic"):
#     stream = os.popen('terraform init')
#     output = stream.read()
#     print(output)


# with console.status("Applying ...", spinner="aesthetic"):
#     stream = os.popen('terraform apply -var-file=variables.json -auto-approve')
#     output = stream.read()
#     print(output)