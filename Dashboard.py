import os

dados_CPU = ""
with open('/proc/cpuinfo', 'r') as arquivo:
    info_CPU = arquivo.readlines()

    #print(info_CPU)

    modelo = info_CPU[4].split('\t')[1].split(' ',1)[1].strip()
    cores = info_CPU[12].split('\t')[1].split(' ')[1].strip()
    threads = info_CPU[10].split('\t')[1].split(' ')[1].strip()

    cpu = f"Modelo: {modelo} Nucleos Fisicos: {cores} Nucleos Virtuais: {threads}\n"

    dados_CPU += cpu

    print(dados_CPU)
 
CPU_stat = []
i=0
with open('/proc/stat', 'r') as arquivo:
    while i < int(threads) + 1 :
        CPU_stat.append(arquivo.readline())
        j=0
        if i == 0:
            j=1 
        t_cpu = []
        k = 1
        while k < 10:
            t_cpu.append(CPU_stat[i].split(' ')[k+j])
            k += 1
        
        print(t_cpu)
        print(CPU_stat[i])
        i += 1

    print(CPU_stat[0])

# Carrega todos os diretorios que tem como nome um numero inteiro, ou seja, sao diretorios de processos
processos = []
for p in os.listdir('/proc'):
    if p.isdigit():
        processos.append(p)

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
    trd = status[35].split('\t')[1].strip() 

    #Monta uma string e concatena com as informacoes dos demais processos
    proc = f"PID: {pid} PPID: {ppid} Nome: {name} Uso de memória: {mem} Quantidade de Threads: {trd}\n"

    dados_processos += proc

# Mostra as informações dos processos na tela
print(dados_processos)


