import pandas as pd
import numpy as np
import math

class Preprocess:

    @staticmethod
    def windowModel(i : int,j : int, k : int,atts : list,D : pd.DataFrame,amount : bool,ubication : bool)->pd.DataFrame:
        """
        Parameters:
        ---
        Las "ventanas" en este caso cubos, respetan un tamaño 16/i*16/j*256/k
        i : `int` define el ancho de la ventana como  height = 16/i
        j : `int` define el largo de la ventana como  height = 16/j
        k : `int` define el alto de la ventana como  height = 256/k
        atts : `list` es una lista con los valores del atributo que se pasa a booleano.
        D : `pd.DataFrame` es el dataset de donde se crearan las ventanas
        amount : bool
        ubication : bool
        """
        if(i>0 and i<=16 and j>0 and j<=16 and k>0 and k<=256):
            if((math.log2(i)%2==0 or i == 1) and (math.log2(j)%2==0 or j==1) and (math.log2(k)%2==0 or k==1)):
                width = math.trunc(16/i);
                length = math.trunc(16/j);
                height = math.trunc(256/k);
                columns = ["Section","SubSection"] + atts
                if(amount):
                    amountClasses = Preprocess.__amountClass(atts);
                    atts += amountClasses;
                if(ubication):
                    ubicationClasses = Preprocess.__ubicationClass(atts);
                    atts += ubicationClasses;
                Transactions = pd.DataFrame(columns=columns);
                for cx in list(D.CX.sort_values().unique()):
                    for cz in list(D.CZ.sort_values().unique()):
                        for x in range(0,16,width):
                            for z in range(0,16,length):
                                for y in range(0,256,height):
                                    subsection :pd.Series = D[(D.CX == cx) & (D.CZ == cz) & (D.X <= x+width) & (D.X >= x) & (D.Z <= z+length) & (D.Z >= z) & (D.Y <= y+height) & (D.Y >= y)].Tag;
                                    transaction = ["("+str(cx)+","+str(cz)+")","("+str(x)+","+str(y)+","+str(z)+")"] + pd.Series(atts).isin(subsection).tolist();
                                    if(amount):
                                        transaction+= Preprocess.__amountCloud(amountClasses,subsection);
                                    if(ubication):
                                        transaction+= Preprocess.__amountCloud(ubicationClasses,subsection);
                                    Transactions.loc[len(Transactions)] = transaction;
                return Transactions;
            else:
                raise Exception("Arguments must satisfy math.log2(arg)%2==0 or arg==1")
        else:
            raise Exception("Arguments must satisfy i,j in (1,16) and k in (1,256)")

    #devuelve la lista de todas los atributtos y sus clases
    @staticmethod
    def __amountClass(atts)->list:
        return []
    
    #devuelve la lista de todas los atributtos y sus clases
    @staticmethod
    def __ubicationClass(atts)->list:
        return []

    #devuelve la lista de booleanos que indica pertenecia a una clase
    @staticmethod
    def __amountCloud(amountClasses,subsection)->list:
        return []
    
    #devuelve la lista de booleanos que indica pertenecia a una clase
    @staticmethod
    def __amountCloud(ubicationClasses,subsection)->list:
        return []

    @staticmethod
    def referenceFeatureModel(atts : list,D : pd.DataFrame,attList : list)->pd.DataFrame:
        """
        Parameters:
        ---
        Son ventanas que contiene por cada bloque el bloque de arriba,abajo,izquierda,derecha,adelante y atras.
        atts : `list` es una lista con los valores del atributo que se pasa a booleano.
        D : `pd.DataFrame` es el dataset de donde se crearan las ventanas
        """
        filteredD = pd.DataFrame();
        for i in range(len(attList)):
            if i==0:
                filteredD = D[D["Tag"]==attList[i]];
            else:
                filteredD = pd.concat([filteredD,D[D["Tag"] == attList[i]]]);
            
        location :list = ["es "," esta a la izquierda de ","esta a la derecha de ","arriba hay ","abajo hay ","delante tiene ","detrás tiene "];
        columns = ["Section","SubSection"];
        
        for loc in location:
            for att in atts:
                columns.append(loc + att);
        rows:list = list(); 
        Transactions=pd.DataFrame(columns=columns)
        for i in range(len(filteredD)):
            row = filteredD.iloc[i,:];
            cx = row.CX;
            cz = row.CZ;
            x = row.X;
            y = row.Y;
            z = row.Z;
            transaction = ["("+str(cx)+","+str(cz)+")","("+str(x)+","+str(y)+","+str(z)+")"] + Preprocess.getAttsRow(cx,cz,x,y,z,D,atts); 
            rows.append(transaction);
            Transactions.loc[len(Transactions)] = transaction;
            if(i%(math.ceil( len(filteredD)/10)) == 0):
                print(str(i) + "/" +str(len(filteredD)));
        return Transactions;
    
    @staticmethod 
    def getAttsRow(cx :int,cz:int,x:int,y:int,z:int,blocks:pd.DataFrame,atts:list)->list:
        row = [];
        dif = [(0,0,0),(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,-1),(0,0,1)];
        for du in dif:
            block = blocks[(blocks.CX == cx) & (blocks.CZ == cz) & (blocks.X == x+du[0]) & (blocks.Y == y+du[1]) & (blocks.Z == z+du[2])].Tag;
            row += list(pd.Series(atts).isin(block));
        return row;