#Dashboard Parte 1
Este projeto foi desenvolvido na matéria de  Sistemas operacionais do curso de Sistemas de Informação, da Universidade Tecnológica Federarl do Paraná, campus Curitiba.

O projeto trata-se de um dashboard para verificação de alguns status do sistema Operacional Debian que é baseado em Linux

O software *Dashboard.py* acessa os arquivos da pasta /proc onde estão as informações dos sistemas e coleta e trata as informações de:
- Nome da máquina
- Dados de memória (uso e total)
- Processador (nome, cores, threads e uso)
- Informações de Processos (PID, PPID, usuário e memoria).

Após isso feito é criado um arquivo JSON com as respectivas chaves e valores.

Por fim o front end criado em IONIC verifica as informações e apresenta em tela. 