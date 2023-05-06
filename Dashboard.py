import os

# Carrega todos os diretorios que tem como nome um numero inteiro, ou seja, sao diretorios de processos
processos = []
for d in os.listdir('/proc'):
    if d.isdigit():
        processos.append(d)

print(processos)

dados_processos = ""

#Abre o arquivo "status" de todos os processos e retira as informacoes necessaria 
for id_proc in processos:
    with open(f"/proc/{id_proc}/status", 'r') as arquivo:
        status = arquivo.readlines()

    pid = status[5].split('\t')[1].strip()
    ppid = status[6].split('\t')[1].strip()
    name = status[0].split('\t')[1].strip()
    mem = status[18].split('\t')[1].strip() #VmSIZE

    #Monta uma string e concatena com as informacoes dos demais processos
    proc = f"PID: {pid} PPID: {ppid} Nome: {name} Uso de memória: {mem}\n"

    dados_processos += proc

# Mostra as informações dos processos na tela
print(dados_processos)