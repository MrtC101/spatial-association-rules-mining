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
    def customWindowModel(atts : list,D : pd.DataFrame)->pd.DataFrame:
        """
        Parameters:
        ---
        Son ventanas que contiene por cada bloque el bloque de arriba,abajo,izquierda,derecha,adelante y atras.
        atts : `list` es una lista con los valores del atributo que se pasa a booleano.
        D : `pd.DataFrame` es el dataset de donde se crearan las ventanas
        """
        location :list = ["es ","izquierda de ","derecha de ","sobre ","debajo ","delante de ","detrás de "];
        columns = ["Section","SubSection"];
        for loc in location:
            for att in atts:
                columns.append(loc + att);
        Transactions = pd.DataFrame(columns=columns);
        for cx in list(D.CX.sort_values().unique()):
            for cz in list(D.CZ.sort_values().unique()):
                for x in range(0,16):
                    for z in range(0,16):
                        for y in range(0,256):
                            transaction = ["("+str(cx)+","+str(cz)+")","("+str(x)+","+str(y)+","+str(z)+")"] + Preprocess.getAttsRow(cx,cz,x,y,z,D,atts); 
                            Transactions.loc[len(Transactions)] = transaction;
        return Transactions;
    
    @staticmethod 
    def getAttsRow(cx,cz,x,y,z,blocks,atts):
        row = [];
        attsS =pd.Series(atts);
        center =blocks[(blocks.CX == cx) & (blocks.CZ == cz) & (blocks.X == x) & (blocks.Y == y) & (blocks.Z == z)].Tag
        right = blocks[(blocks.CX == cx) & (blocks.CZ == cz) &(blocks.X == x+1) & (blocks.Y == y) & (blocks.Z == z)].Tag
        left = blocks[(blocks.CX == cx) & (blocks.CZ == cz) &(blocks.X == x-1) & (blocks.Y == y) & (blocks.Z == z)].Tag
        up=blocks[(blocks.CX == cx) & (blocks.CZ == cz) &(blocks.X == x) & (blocks.Y == y+1) & (blocks.Z == z)].Tag
        down=blocks[(blocks.CX == cx) & (blocks.CZ == cz) &(blocks.X == x) & (blocks.Y == y-1) & (blocks.Z == z)].Tag
        front=blocks[(blocks.CX == cx) & (blocks.CZ == cz) &(blocks.X == x) & (blocks.Y == y) & (blocks.Z == z+1)].Tag
        behind=blocks[(blocks.CX == cx) & (blocks.CZ == cz) &(blocks.X == x) & (blocks.Y == y) & (blocks.Z == z-1)].Tag
        row = list(attsS.isin(center)) + list(attsS.isin(right)) + list(attsS.isin(left)) + list(attsS.isin(up)) + list(attsS.isin(down)) + list(attsS.isin(front)) + list(attsS.isin(behind)); 
        return row;