class Fichier:
    def __init__(self,nom,compilation_time,replicate_time):
        self.nom=nom
        self.compilation_time=compilation_time
        self.replicate_time=replicate_time
        self.num_dep=0
        self.list_dep=[]
    
    def __str__(self):
        return "Ficher : {}".format(self.nom)
        
class Target:
    def __init__(self,nom,dead_line,goal_point):
        self.nom=nom
        self.dead_line=dead_line
        self.goal_point=goal_point
        
    def __str__(self):
        return "Target : {} ".format(self.nom)
        
class Input_file:
    def __init__(self,chemin_file):
        self.input_fichier = open(chemin_file,"r")
        
        line = self.input_fichier.readline()
        line = line.split()
        
        self.num_files=int(line[0])
        self.num_target=int(line[1])
        self.num_server=int(line[2])
        
        #Structurer la liste de Fichier
        # we will start a loop to go over the files 
        files=[]
        for i in range(0,self.num_files):
            #On traite les lignes deux à deux 
            line = self.input_fichier.readline()
            
            line=line.split()
            nv_fichier = Fichier(line[0],int(line[1]),int(line[2]))
            
            line = self.input_fichier.readline()
           
            line=line.split()
            
            #On traite les dépendances 
            if(int(line[0])>0):
                # on a une liste de dependance qu'on doit stoker
                dep_list=[]
                for j in range(1,int(line[0])+1):
                    dep_list.append(line[j])
                
                nv_fichier.list_dep=dep_list
                nv_fichier.num_dep=int(line[0])
            files.append(nv_fichier)
        self.fileL = files
        
        #Structurer la liste de Target
        target_list=[]
        for i in range(0,self.num_target):
            line=self.input_fichier.readline()
            #print(line)
            line=line.split()
            nv_target = Target(line[0],int(line[1]),int(line[2]))
            target_list.append(nv_target)
            
        self.targetL = target_list
    ##Fin de la méthode constructeur
    
    def getFile(self):
        return self.fileL

    def getTarget(self):    
        return self.targetL
    
    #méthode d'affichage
    def __str__(self):
        tab_Target = "[ "
        for el in self.targetL:
            tab_Target = tab_Target + str(el) + ","
        tab_Target = tab_Target + "]"
        
        tab_File = "[ "
        for el in self.fileL:
            tab_File = tab_File + str(el) + ","
        tab_File = tab_File + "]"
        
        result = "Sur ce document, il y a : \n{} Fichiers\n{} Serveurs\n{} Targets\n".format(self.num_files,self.num_server,self.num_target)
        result = result + "Et les Fichiers sont:\n{}\nAvec les targets :\n{}".format(tab_File,tab_Target)
        return result
        
if __name__=='__main__':
    #permet d'ouvrir un fichier en lecture 
    input_fichier = Input_file("text.txt")
    print(input_fichier)