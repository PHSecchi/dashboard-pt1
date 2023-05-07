import os
import pwd
import threading
import time


def aquisicao_dados_cpu():
    dados_CPU = ""
    with open('/proc/cpuinfo', 'r') as arquivo:
        info_CPU = arquivo.readlines()

        #Carrega as informacoes gerais sobre o processador
        modelo = info_CPU[4].split('\t')[1].split(' ',1)[1].strip()
        cores = info_CPU[12].split('\t')[1].split(' ')[1].strip()
        threads = info_CPU[10].split('\t')[1].split(' ')[1].strip()

        cpu = f"Modelo: {modelo} Nucleos Fisicos: {cores} Nucleos Virtuais: {threads}\n"

        dados_CPU += cpu
 
    CPU_stat = []
    i=0

    #Carrega as informacoes sobre o tempo do processador
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

            dados_CPU += CPU_stat[i]
            i += 1
    
    return dados_CPU
 

def aquisicao_dados_processos():
    # Carrega todos os diretorios que tem como nome um numero inteiro, ou seja, sao diretorios de processos
    processos = []
    for p in os.listdir('/proc'):
        if p.isdigit():
            processos.append(p)

    dados_processos = ""

    #Abre o arquivo "status" de todos os processos e retira as informacoes necessaria 
    for id_proc in processos:
        with open(f"/proc/{id_proc}/status", 'r') as arquivo:
            status = arquivo.readlines()
            memo = 0
        for s in status:
            if (s.split('\t')[0].strip()) == 'Pid:':
                pid = s.split('\t')[1].strip() 
            if (s.split('\t')[0].strip()) == 'PPid:':
                ppid = s.split('\t')[1].strip() 
            if (s.split('\t')[0].strip()) == 'Name:':
                name = s.split('\t')[1].strip() 
            if (s.split('\t')[0].strip()) == 'VmSize:':
                memo = s.split('\t')[1].strip() 
            if (s.split('\t')[0].strip()) == 'Threads:':
                trd = s.split('\t')[1].strip() 
            if (s.split('\t')[0].strip()) == 'Uid:':
                uid = s.split('\t')[1].strip() 

        user = pwd.getpwuid(int(uid)).pw_name

        #Monta uma string e concatena com as informacoes dos demais processos
        proc = f"PID: {pid} PPID: {ppid} Nome: {name} Ususario: {user} Uso de memória: {memo} Quantidade de Threads: {trd}\n"
        dados_processos += proc

    return dados_processos
def printa_dados():
    while True: 
        # Mostra as informações na tela
        print(aquisicao_dados_cpu())
        print(aquisicao_dados_processos())
        time.sleep(5)

thr_aq_dados = threading.Thread(target= printa_dados)


thr_aq_dados.start()


