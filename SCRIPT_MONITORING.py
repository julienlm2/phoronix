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
import warnings
from multiprocessing import Process
import csv


def boucle(execution_time,log_name_temp):
    ARRAY_TIME = [] #Array pour export en .CSV
    ARRAY_CPU_USAGE = []

    username = os.getlogin()
    
    temps_voulu = execution_time #récupération des arguments 
    log_name= str(log_name_temp)

    temps_fin = time.time() + temps_voulu #calcul du temps d'exécution passé en paramètre

    temperature = 0.0
    ARRAY_TEMPERATURE = []


    now = datetime.now()
    today = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_day = now.strftime("%d-%m-%y")

    f = open('/home/'+username+'/.phoronix-test-suite/test-results/log_temp_'+log_name+'_'+current_day+'_'+current_time+'.txt', 'w') #création du fichier de log (cpu usage et température)

    count = 0
    while(time.time()<temps_fin):
        count = 0
        now = datetime.now()

        current_time = now.strftime("%H:%M:%S.%f")[:-3]

        Info_Sensors_Brut = run("sensors", capture_output=True).stdout #récupération des données thermiques
        Info_Usage_Brut = run(["mpstat","-P","ALL","2","1"], capture_output=True).stdout #récupération des données de charge CPU



        for line in Info_Sensors_Brut.splitlines():
            if "Core 0" in line.decode('utf-8'):

                        line_split = line.decode('utf-8').split("+") #découpage de la string pour garder uniquement les données voulues (thermiques)

                        temp = line_split[1]

                        temp_split = temp.split("°")
                        temperature = float(temp_split[0])

                        for line in Info_Usage_Brut.splitlines():
                            if "all" in line.decode('utf-8') and count == 0:
                                count = 1
                                line_split_usage = line.decode('utf-8').split("   ") #découpage de la string pour garder uniquement les données voulues (thermiques)
                                usage = line_split_usage[1]

                           
                                f.write("Cpu :"+str(usage)+"%  ") #écriture de la charge cpu dans les logs
                                #-----------CSV----------------
                                usage = usage.replace(".",",")
                                ARRAY_CPU_USAGE.append(usage)
                                #------------------------------
                        #-----------CSV----------------
                        ARRAY_TIME.append(current_time)
                        #------------------------------


                        if int(temperature) > 80 or int(temperature) < -40:
                            errors = open('/home/'+username+'/.phoronix-test-suite/test-results/ERRORS_'+log_name+'.txt', 'a') #création du fichier d'erreurs
                            errors.writelines(f"Error, time : {current_time} - Temperature too high : {temperature}°C\n")
                        

                        f.writelines(str(temperature)+"C") #écriture de la charge cpu dans les logs
                        f.writelines("  ["+str(current_time)+"]\n") #écriture du temps dans les logs

                        ARRAY_TEMPERATURE.append(math.trunc(temperature)) #modification du format de la température pour l'export en .CSV
                    
                        MAX = ARRAY_TEMPERATURE[0] #Calcul de la température Max
                        for i in range (len(ARRAY_TEMPERATURE)):
                           if (ARRAY_TEMPERATURE[i]>MAX):
                                MAX = ARRAY_TEMPERATURE[i]

                        MIN = ARRAY_TEMPERATURE[0] #Calcul de la température Min
                        for i in range (len(ARRAY_TEMPERATURE)):
                          if (ARRAY_TEMPERATURE[i]<MIN):
                                MIN = ARRAY_TEMPERATURE[i]

                        SOMME = 0        
                        for i in range (len(ARRAY_TEMPERATURE)):#Calcul de la moyenne de température
                           SOMME += ARRAY_TEMPERATURE[i]

                        MOYENNE = round(SOMME / len(ARRAY_TEMPERATURE),2)
                        time.sleep(0.001)

        


    #___________EXPORT CSV__________
    data = []
    Csv_File_Name = '/home/'+username+'/.phoronix-test-suite/test-results/'+log_name+'_'+current_day+'_'+current_time+'Monitoring_Data.csv'
    header = ['Cpu_Usage','Temperature','Time']
    with open(Csv_File_Name,'w',newline="") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(header)
        for i in range(len(ARRAY_TEMPERATURE)):
            data.append([ARRAY_CPU_USAGE[i],ARRAY_TEMPERATURE[i],ARRAY_TIME[i]])
        csvwriter.writerows(data)
    #__________________________________________
  

    #Ecriture des stats dans le fichier log 
    f.writelines("\nMAX TEMP = "+str(MAX)+"C\n")
    f.writelines("\nMIN TEMP = "+str(MIN)+"C\n")
    f.writelines("\nAVERAGE TEMP = "+str(MOYENNE)+"C\n")
    f.close()



#________________________________________________________________________________________________________________________________




username = os.getlogin()

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
current_day = now.strftime("%d-%m-%y")

Test_status = True

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

result = datetime.now() + timedelta(minutes=TOTAL_LOOP_TIME+1)

run(["phoronix-test-suite","install","fio"])
run(["phoronix-test-suite","install","mbw"])
run(["phoronix-test-suite","install","libplacebo"])
run(["phoronix-test-suite","install","stress-ng"])
run(["phoronix-test-suite","install","boucle"])
run(["phoronix-test-suite","install","pibench"])

p = Process(target=boucle, args=(ARGUMENT_LOG_EXECUTION_TIME,str(ARGUMENT_LOG_NAME)))
p.start()
#_________________________Exécution de la suite de test_________________________________________

current_time = now.strftime("%H:%M:%S")

print(str(current_time)+" : Benchmark in progress ... Estimated time of completion : "+result.strftime("%H:%M:%S"))

directory = '/home/'+username+'/.phoronix-test-suite/test-results/log_phoronix_'+ARGUMENT_LOG_NAME+'_'+current_day+'_'+current_time+'.txt'
log_phoronix = open(directory, 'w')

list_files = subprocess.Popen(["phoronix-test-suite", "stress-run", "testsmonitoring"],stdout=subprocess.PIPE,stdin=subprocess.PIPE,text=True)

for line in list_files.stdout:
    print(line)
    if "CPU Temperature" in line:
        temp = line.split('     ')
        tempint = int(temp[5].strip('.00').strip('    '))
        if tempint > 80 or tempint < -40:
            warnings.warn(f"{tempint}°C -> Température trop haute")
            Test_status = False
       
    #_________________________Sauvegarde des logs d'exécution________________________________________
    log_phoronix.writelines(line.replace('','').replace('[0m','').replace('[1m','').replace('[1;32m','').replace('[1;30m','').replace('[1;31m','').replace('[1;34m',''))

list_files.wait()
p.join()

now = datetime.now()
finish_time = now.strftime("%H:%M:%S")

print(f'{finish_time} - Tests Completed ...')
if Test_status == True:
    print("Test Passed !")
elif Test_status == False:
    print("Test Failed, ERROR LOGS SAVED TO /.phoronix-test-suite/test-results/ !")
print('Results saved to /.phoronix-test-suite/test-results/')
print('CSV file generated at /.phoronix-test-suite/test-results/')
#_________________________Ouverture du fichier log________________________________________________
run(["geany",directory])
log_phoronix.close()

sys.exit()