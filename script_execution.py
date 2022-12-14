#!/usr/bin/env python

from subprocess import run
from ast import Break
from datetime import datetime,timedelta
import subprocess
import os
import platform
import time
import math
import sys
import webbrowser

username = os.getlogin()

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
current_day = now.strftime("%d-%m-%y")

#set les variables d'environnement pour phoronix et input validation

while(True):
    ARGUMENT_LOG_NAME = input("Enter results and log name : ")
    if ARGUMENT_LOG_NAME != '':
        break
    else:
        print("string format required")

while(True):
    TOTAL_LOOP_TIME = input("Enter test duration (in minutes) : ")
    if TOTAL_LOOP_TIME != '' and TOTAL_LOOP_TIME.isdigit() == True:
        break
    else : 
        print("Only digits are allowed")

while(True):
    CONCURRENT_TEST_RUNS = input("Enter number of parallel tests to execute : ")
    if CONCURRENT_TEST_RUNS !='' and CONCURRENT_TEST_RUNS.isdigit() == True:
        break
    else :
        print("Only digits are allowed")

os.environ['PTS_CONCURRENT_TEST_RUNS']=CONCURRENT_TEST_RUNS
os.environ['TOTAL_LOOP_TIME']=TOTAL_LOOP_TIME
os.environ['TEST_RESULTS_NAME']=ARGUMENT_LOG_NAME
TOTAL_LOOP_TIME = int(TOTAL_LOOP_TIME)
ARGUMENT_LOG_EXECUTION_TIME = (TOTAL_LOOP_TIME * 60) - 20

#__________________________Récupération du fichier XML de "boucle"____________________________

Info_Test_def = open('/home/'+username+'/.phoronix-test-suite/test-profiles/local/boucle/test-definition.xml','r')
data = Info_Test_def.readlines()

data[22] = '<Arguments>'+str(ARGUMENT_LOG_EXECUTION_TIME)+' '+ARGUMENT_LOG_NAME+'</Arguments>\n'

#__________________________Modification du fichier XML de "boucle"____________________________

Info_Test_def = open('/home/'+username+'/.phoronix-test-suite/test-profiles/local/boucle/test-definition.xml','w')
Info_Test_def.writelines(data)
Info_Test_def.close()

result = datetime.now() + timedelta(minutes=TOTAL_LOOP_TIME+1) #Calcul de la durée estimé d'exécution 
#_________________________Installation des tests________________________________________________
run(["phoronix-test-suite","install","fio"])
run(["phoronix-test-suite","install","mbw"])
run(["phoronix-test-suite","install","libplacebo"])
run(["phoronix-test-suite","install","stress-ng"])
run(["phoronix-test-suite","install","boucle"])


#_________________________Exécution de la suite de test_________________________________________

print(str(current_time)+" : Benchmark in progress ... Estimated time of completion : "+result.strftime("%H:%M:%S"))
list_files = subprocess.run(["phoronix-test-suite", "stress-run", "testsmonitoring"],capture_output=True).stdout

#_________________________Sauvegarde des logs d'exécution________________________________________

directory = '/home/'+username+'/.phoronix-test-suite/test-results/log_phoronix_'+ARGUMENT_LOG_NAME+'_'+current_day+'_'+current_time+'.txt'
log_phoronix = open(directory, 'w')
log_phoronix.writelines(list_files.decode('UTF-8').replace('','').replace('[0m','').replace('[1m','').replace('[1;32m','').replace('[1;30m','').replace('[1;31m','').replace('[1;34m',''))

print('Tests Completed ...')
print('Results saved to /.phoronix-test-suite/test-results/')
print('CSV file generated at /.phoronix-test-suite/test-results/')
#_________________________Ouverture du fichier log________________________________________________
run(["geany",directory])
log_phoronix.close()

sys.exit()
