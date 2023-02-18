import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import math
import random

class outilerDetection:

    @staticmethod
    def countBlocks(i :int ,j: int ,k: int,D: pd.DataFrame,atts : list):
        if(i>0 and i<=16 and j>0 and j<=16 and k>0 and k<=256):
            if((math.log2(i)%2==0 or i == 1) and (math.log2(j)%2==0 or j==1) and (math.log2(k)%2==0 or k==1)):
                #Contar bloque spor sección
                blockCount = pd.DataFrame(columns= ["Section","X","Y","Z"] + atts);
                width = math.trunc(16/i);
                length = math.trunc(16/j);
                height = math.trunc(256/k);
                for cx in list(D.CX.sort_values().unique()):
                    for cz in list(D.CZ.sort_values().unique()):
                        for x in range(0,16,width):
                            for z in range(0,16,length):
                                for y in range(0,256,height):
                                    subsection :pd.Series = D[(D.CX == cx) & (D.CZ == cz) & (D.X <= x+width) & (D.X >= x) & (D.Z <= z+length) & (D.Z >= z) & (D.Y <= y+height) & (D.Y >= y)].Tag.value_counts();
                                    row = ["("+str(cx)+","+str(cz)+")",x,y,z] + outilerDetection.count(atts,subsection);
                                    blockCount.loc[len(blockCount)] = row;
                return blockCount;
            else:
                raise Exception("Arguments must satisfy math.log2(arg)%2==0 or arg==1")
        else:
            raise Exception("Arguments must satisfy i,j in (1,16) and k in (1,256)")
    
    @staticmethod
    def count(atts,subsection):
        """
        Toma la serie que indica la cantidad de tipos de bloques que hay en una sección y 
        devuelve una lista con la cantidad correspondiente a un atributo o 0.    
        """
        L = [];
        boolList:list = pd.Series(atts).isin(subsection.index).tolist();
        j = 0;
        for i in range(0,len(boolList)):
            if(boolList[i]==True):
                L.append(subsection[j]);
                j += 1;
            else:
                L.append(0);
        return L;

    @staticmethod
    def variogramCloud(blockCount: pd.DataFrame,atts: list):
        #plot
        colors = ["b","c","g","m","r","y","k"];
        ncols = 7
        nrows = 7
        fig, ax = plt.subplots(ncols,nrows, sharex='none',sharey='none')
        fig.dpi = 120;
        fig.set_size_inches(30,30);
        for i in range(0,len(blockCount)):
            tuple = list(blockCount.Section.unique())[i];
            blockCount.iat[i,1] += int(tuple[1])*16
            blockCount.iat[i,3] += int(tuple[3])*16
        #Generar puntos (A,B) donde A,B = "(cx,cz),(x,y,z)"
        i = 0;
        j = 0;
        for attribute in atts:
            if(j == ncols):
                j = 0;
                i+=1;
            points = outilerDetection.getpoints(attribute,blockCount);
            ax[i][j].scatter(points.eucD, points.absD, c=random.choice(colors),alpha=0.3, edgecolors='none')
            ax[i][j].set_xlabel("Distancia Euclidiana");
            ax[i][j].set_ylabel("Diferencia absoluta de atributo " + attribute);
            ax[i][j].grid(True);
            j+=1;
        return fig, ax;

    @staticmethod
    def getpoints(attribute: str,blockCount: pd.DataFrame)->pd.DataFrame:
        points = pd.DataFrame(columns=["point","absD","eucD"]);
        for i in range(0,len(blockCount)):
            for j in range(0,len(blockCount)):
                if(i!=j):
                    point = str(blockCount.iat[i,0])+":("+str(blockCount.iat[i,1])+","+str(blockCount.iat[i,2])+","+str(blockCount.iat[i,3])+")"+"|"+str(blockCount.iat[j,0])+":("+str(blockCount.iat[j,1])+","+str(blockCount.iat[j,2])+","+str(blockCount.iat[j,3])+")";
                    absD = math.sqrt(abs(int((blockCount.at[i,attribute]) - int(blockCount.at[j,attribute]))));
                    eucD = math.sqrt(
                        math.pow(int((blockCount.iat[i,1])) - int((blockCount.iat[j,1])),2) +
                        math.pow(int((blockCount.iat[i,2])) - int((blockCount.iat[j,2])),2) +
                        math.pow(int((blockCount.iat[i,3])) - int((blockCount.iat[j,3])),2) 
                    );
                    points.loc[len(points)] = [point,absD,eucD];
        return points;