import os
import pwd
import threading
import time
import json

def aquisicao_hostname():
    with open('/proc/sys/kernel/hostname', 'r') as arquivo:
        hostname = arquivo.read().strip()
    
    return {"Hostname": hostname}

def aquisicao_dados_cpu():
    
    with open('/proc/cpuinfo', 'r') as arquivo:
        info_CPU = arquivo.readlines()

        #Carrega as informacoes gerais sobre o processador
        modelo = info_CPU[4].split('\t')[1].split(' ',1)[1].strip()
        cores = info_CPU[12].split('\t')[1].split(' ')[1].strip()
        threads = info_CPU[10].split('\t')[1].split(' ')[1].strip()

        cpu = {"Modelo": modelo,
               "Nucleos Fisicos": cores,
               "Nucleos Virtuais" : threads }
        dados_CPU = { "CPU" : cpu}
       
 
    CPU_stat = []
    i=0
    t_cpu = []
    #Carrega as informacoes sobre o tempo do processador
    with open('/proc/stat', 'r') as arquivo:
        while i < int(threads) + 1 :
            CPU_stat.append(arquivo.readline())
            j=0
            if i == 0:
                j=1 
            tempos = []
            k = 1
            while k < 11:
                tempos.append(CPU_stat[i].split(' ')[k+j].strip())
                k += 1

            t_cpu.append({"t_user1":int(tempos[0]),
                          "t_user2":int(tempos[1]),
                          "t_system":int(tempos[2]),
                          "t_ocioso":int(tempos[3]),
                          "t_i/o_wait":int(tempos[4]),
                          "t_inthard":int(tempos[5]),
                          "t_intsoft":int(tempos[6]),
                          "t_virt":int(tempos[7]),
                          "t_virt1cpu":int(tempos[8]),
                          "t_energ":int(tempos[9])})
            i += 1

    dados_CPU = { "info_CPU" : cpu,
                 "times_CPU": t_cpu}
    return dados_CPU 
 

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
        proc.append ({"PID": pid,
                      "PPID": ppid,
                      "Nome": name,
                      "Ususario": user, 
                      "Memoria": memo,
                      "Quantidade de Threads": trd})

    return proc

def grava_dados():
    while True: 
        Dados = {"Hostname": aquisicao_hostname(),
                 "CPU":aquisicao_dados_cpu(),
                 "Processos":aquisicao_dados_processos()}
        # Mostra as informações na tela
        #print(aquisicao_dados_processos())
        #print(aquisicao_dados_cpu())
        
        with open("Dados.json","w") as arquivo:
            json.dump(Dados,arquivo,indent= 4)
        time.sleep(5)

thr_aq_dados = threading.Thread(target= grava_dados)


thr_aq_dados.start()


