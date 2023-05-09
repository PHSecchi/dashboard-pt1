import os
import pwd
import threading
import time
import json

def aquisicao_hostname():
    with open('/proc/sys/kernel/hostname', 'r') as arquivo:
        hostname = arquivo.read().strip()
    
    return {"Hostname": hostname}

def aquisicao_dados_memo():
    with open('/proc/meminfo', 'r') as arquivo:
        info_memo = arquivo.readlines()

    for m in info_memo:
        if m.startswith('MemTotal:'):
                memo_total = int(m.split()[1])
        if m.startswith('MemFree:'):
                memo_free = int (m.split()[1])
    
    memo_uso = memo_total-memo_free

    return{"Total": memo_total,
           "Free" : memo_free,
           "emUso": memo_uso
            }

def aquisicao_dados_cpu():
    
    with open('/proc/cpuinfo', 'r') as arquivo:
        info_CPU = arquivo.readlines()

        #Carrega as informacoes gerais sobre o processador
        modelo = info_CPU[4].split('\t')[1].split(' ',1)[1].strip()
        cores = info_CPU[12].split('\t')[1].split(' ')[1].strip()
        threads = info_CPU[10].split('\t')[1].split(' ')[1].strip()
        
    #Carrega as informacoes sobre o tempo do processador
    with open('/proc/stat', 'r') as arquivo:
        stat_cpu1 = arquivo.readline()
        
    time.sleep(1)
        
    with open('/proc/stat', 'r') as arquivo:
        stat_cpu2 = arquivo.readline()
        
        t_cpu1 = []
        t_cpu2 = []
        k = 2
        while k < 12:
            t_cpu1.append(int(stat_cpu1.split(' ')[k].strip()))
            t_cpu2.append(int(stat_cpu2.split(' ')[k].strip()))
            k += 1

        t_cpu1total = sum(t_cpu1)
        t_cpu2total = sum(t_cpu2)

        percent = ((t_cpu2total - t_cpu2[3])-(t_cpu1total - t_cpu1[3])) / (t_cpu2total - t_cpu1total) * 100

    return {"Modelo": modelo,
            "Nucleos Fisicos": cores,
            "Nucleos Virtuais" : threads,
            "Porcentagem de Uso": percent }
 

def aquisicao_dados_processos():
    # Carrega todos os diretorios que tem como nome um numero inteiro, ou seja, sao diretorios de processos
    processos = []
    for p in os.listdir('/proc'):
        if p.isdigit():
            processos.append(p)

    proc = []
    #Abre o arquivo "status" de todos os processos e retira as informacoes necessaria 
    for id_proc in processos:
        with open(f"/proc/{id_proc}/status", 'r') as arquivo:
            status = arquivo.readlines()
            memo = 0
        for s in status:
            if s.startswith('Pid:'):
                pid = s.split('\t')[1].strip() 
            if s.startswith('PPid:'):
                ppid = s.split('\t')[1].strip() 
            if s.startswith('Name:'):
                name = s.split('\t')[1].strip() 
            if s.startswith('VmSize:'):
                memo = s.split('\t')[1].strip() 
            if s.startswith('Threads:'):
                trd = s.split('\t')[1].strip() 
            if s.startswith('Uid:'):
                uid = int(s.split('\t')[1].strip()) 

        with open('/proc/self/loginuid', 'r') as arquivo:
            loginuid = int(arquivo.read().strip())

        if loginuid == uid :
            user = pwd.getpwuid(uid).pw_name
            proc.append ({"PID": pid,
                          "PPID": ppid,
                          "Nome": name,
                          "Ususario": user, 
                          "Memoria": memo,
                          "Quantidade de Threads": trd})

    return proc

def grava_dados():
    while True:
        #aquisicao_dados_cpu() 
        Dados = {"Hostname": aquisicao_hostname(),
                 "CPU":aquisicao_dados_cpu(),
                 "Memoria": aquisicao_dados_memo(),
                 "Processos":aquisicao_dados_processos()}
        # Mostra as informações na tela
        #print(aquisicao_dados_processos())
        #print(aquisicao_dados_cpu())
        
        with open("Dados.json","w") as arquivo:
            json.dump(Dados,arquivo,indent= 4)
        time.sleep(5)

thr_aq_dados = threading.Thread(target= grava_dados)


thr_aq_dados.start()


