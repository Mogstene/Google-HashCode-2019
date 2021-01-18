# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 23:39:55 2019

@author: Omar
"""

class Fichier:
    def __init__(self,nom,compilation_time,replicate_time):
        self.nom=nom
        self.compilation_time=compilation_time
        self.replicate_time=replicate_time
        self.num_dep=0
        self.list_dep=[]
        
class Target:
    def __init__(self,nom,dead_line,goal_point):
        self.nom=nom
        self.dead_line=dead_line
        self.goal_point=goal_point
        
class input_file:
    def __init__(self,num_files,num_target,num_server,files,target_list):
        self.num_files=num_files
        self.num_target=num_target
        self.num_server=num_server
        self.files=files
        self.target_list=target_list
        
class Serveur:
    def __init__(self,list_files):
        self.list_files=list_files
        
        
input_fichier = open("e_intriguing.in","r")

#NOTRE FONCTION DE LECTURE

def lecture(input_fichier):
    
    # la premiere ligne contient files / target / servers
    
    line = input_fichier.readline()
    line=line.split()
    num_files=int(line[0])
    num_target=int(line[1])
    num_server=int(line[2])
    
    # On crée une boucle pour parcourir les fichiers
    
    files=[]
    for i in range(0,num_files):
        line=input_fichier.readline()
        #print(line)
        line=line.split()
        nv_fichier=Fichier(line[0],int(line[1]),int(line[2]))
        
        line=input_fichier.readline()
        line=line.split()
        if(int(line[0])>0):
            # Commençant par créer une liste qui contient les dépendances 
            # on a une liste de dependance qu'on doit stoker
            dep_list=[]
            for j in range(1,int(line[0])+1):
                # On veut trouver line[j] parmis les noms de fichier afin de recuperer son indice
                for c in range(0,len(files)):
                    if(files[c].nom==line[j]):
                        # Trouvé!! On récupère l'indice
                        dep_list.append(c)
                        break
                
            
            nv_fichier.list_dep=dep_list
            nv_fichier.num_dep=int(line[0])
        files.append(nv_fichier)
    # on doit stocker les targets maintenant 
    target_list=[]
    for i in range(0,num_target):
        line=input_fichier.readline()
        #print(line)
        line=line.split()
        target_list.append(Target(line[0],int(line[1]),int(line[2])))
        
    new_input=input_file(num_files,num_target,num_server,files,target_list)
    
    
    return new_input
        
            
        
input_f=lecture(input_fichier)

#print(input_f.num_files)



serveurs=[]
for i in range(0,input_f.num_server):
    serveurs.append(Serveur({input_f.files[0]:0})) # dictionnaire {clé : valeur} = {fichier, tmp}


def Affichage_dep(file):# fonction qui sert a calculer la profondeur d'un fichier dans l'arbre
    if(file.num_dep!=0):# si le nombre de dépendance du fichier n est pas nul on parcours ses dependances et si elles ne sont pas nul on les parcours aussi  
        return [x for x in ([Affichage_dep(input_f.files[int(i)])  for i in file.list_dep] + file.list_dep) if x!=[]] 
    else:
        return []
    

#                    ::::Les règles et principes::::
# Chaque serveur peut compiler un fichier à la fois 
# Chaque fichier à besoin d'un certaine durée pour etre compilé
# Une fois un fichier compilé on le réplique directement sur les autres serveurs 
# affichage dep , l'idee c'est d'appliquer la fonction sur toutes les dépendances
# list_parfaite=[1,3,5,7] correspondera aux fichiers a compiler par ordre


dic = {} #on crée un dictionnaire ou l on va stocker la longueur des dépendances de chaque fichier
for i in input_f.files:
    dic[i]=len(Affichage_dep(i))
      
sorted(dic.items(), key=lambda t: t[1]) #on tri notre dictionnaire selon le deuxième élément c-a-d la profondeur de l arbre
list_parfaite=[]# une fois trié on rajoute tout les fichiers dans l ordre dans notre liste parfaite 
for i in dic:
    list_parfaite.append(i)#la liste des fichier dans l ordre croissant des dépendances
## input : file , server_nmb   // le temps de replication sera toujours exprimé en négatif // on compile un fichier dans un serveur et on le repliquer dans les autres

def put_file_in_srv(file,srv_nmb):# cette fonction nous sert à déposer un fichier dans un serveur 
    # on doit poser un fichier dans ce serveur :serveurs[srv_nmb]
    max_n=0
    if(file.num_dep==0):
        if(max(serveurs[srv_nmb].list_files.values())<0):# dans le cas ou il n y a que des fichiers repliqué au début(cas très rare mais on ne sait jamais)
            max_n=0 
        else:
            # il faut vérifier quand est ce que les dependances vont finir leurs executions
            n=max(serveurs[srv_nmb].list_files.values())
            max_n=n 
    else:
        for num_dep in file.list_dep: 
            if(abs(serveurs[srv_nmb].list_files[input_f.files[num_dep]])>max_n):
                max_n=abs(serveurs[srv_nmb].list_files[input_f.files[num_dep]])
        ## je dois le comparer avec le max de la liste
        if(max(serveurs[srv_nmb].list_files.values())>max_n):
            max_n=max(serveurs[srv_nmb].list_files.values())
                
    
    serveurs[srv_nmb].list_files[file]=max_n+file.compilation_time
    
    
    for srv in  serveurs:
        if(srv!=serveurs[srv_nmb]):
            srv.list_files[file]=(max_n+file.compilation_time+file.replicate_time)*-1
        


# input: file
# Output: serveur parfait
# etape 1:  

def serveur_parfait(file):
    # On doit verifier les dependances du fichier
    best_server=0 
    best_time=1000000000000000000000000
    if(file.num_dep==0):
        # on peut le lancer direct sans voir leurs dependances
        #print("we have 0 dependencies : ")
        for i in range(0,len(serveurs)):
            if(max(serveurs[i].list_files.values())<best_time):
                # on garde ce serveur
                #print("new max : ",max(serveurs[i].list_files.values()) , "best time : ",best_time)
                best_time=max(serveurs[i].list_files.values())
                best_server=i
    else:
        # on doit parcourir les depandances car c'est ce qu'on va chequer dans les serveurs
        # on doit prendre le t max parmis ses dependances
        
        for i in range(0,len(serveurs)):
            max_t_depen=0
            tms=0
            for j in file.list_dep:
                if(abs(serveurs[i].list_files[input_f.files[j]])>max_t_depen):
                    
                    #print("t max in dependecies ",max_t_depen,"new max in dependencies : ",abs(serveurs[i].list_files[input_f.files[j]]))
                    max_t_depen=abs(serveurs[i].list_files[input_f.files[j]])
                    
            #print("max dependencies in new line ",max_t_depen)
            ## maintenant je dois le comparer avec le max t value 
            if(max_t_depen>max(serveurs[i].list_files.values())):
                tms=max_t_depen
                #print(" t max in dependencies is : ",max_t_depen,"t max in compiled files is ",max(serveurs[i].list_files.values()))
            else:
                tms=max(serveurs[i].list_files.values())
            if(tms<best_time):
                best_time=tms
                best_server=i
                #print("best time server is ",best_time,"and server num : ",best_server)
            
    return best_server

fo= open("e_intriguing.txt","w+")
fo.write("%d\n"%len(list_parfaite))

for k in list_parfaite:
    srv_p=serveur_parfait(k)
    put_file_in_srv(k,srv_p)
    
    #f.write(str(k.nom) , " ",str(srv_p))
    x=k.nom+" "+str(srv_p)+"\n"
    fo.write(x)
    
    
fo.close() 
#Fonction de scoring
score=0
tmp_excu=0
for f in input_f.target_list:
    for n in  input_f.files:
            if(f.nom==n.nom):
                fifi=n
            
    # c est le fichier que je cherche dans les serveurs je dois voir quand est ce qu il est dispo et ce qui est positive est ce qu on cherche 
    for srv in serveurs:
        if(srv.list_files[fifi]>0):
            # on recupere le temps
            tmp_excu=srv.list_files[fifi]
            if(f.dead_line>=tmp_excu):
                print((f.dead_line-tmp_excu)+f.goal_point)
                score=score+(f.dead_line-tmp_excu)+f.goal_point

print("le score est = ",score)
        