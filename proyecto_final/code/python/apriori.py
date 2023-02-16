import pandas as pd
import numpy as np

def apriori(T : pd.DataFrame) -> pd.DataFrame:
    """
    Parameters
    ---
    T :pd.DataFrame Transaction set for association rule mining.
    Variable Names
    ----
    L : Set of k-itemsets.Has two fields: 1-itemset;2-support count  
    Ck :
    Ct :
    """
    L: pd.DataFrame = getOneItemSet(T);
    k: int = 2;
    while(len(L) == 0):
        Ck = apriori_gen(L)#new candidate
        for t in T:
            Ct = subset(Ck,t)#Candidates contained in t
            for c in Ct:
                c.count+=1;
        k+=1;
    return Lk;

def apriori_gen(L : pd.DataFrame)-> pd.DataFrame:
    #1 join L with L
    Ck: pd.DataFrame = pd.DataFrame();
    Lp: pd.DataFrame = L;
    Lq :pd.DataFrame = L.copy();
    Ck = union(Lp,Lq);
    #2 delete all itemsets c on Ck talque algunos k-1 subset of c is not in lk-1
    for c in Ck:
        for s in subSets(c):
            if(elementOf(s,Ck)):
                deleteOf(s,Ck)
    return 

def subSets(c)-> list:
    return [];

def deleteOf(a,A) -> None:
    return None;

def elementOf(a,A) -> bool:
    return True;

def union(A :pd.DataFrame, B : pd.DataFrame) -> pd.DataFrame:
    C : pd.DataFrame = pd.DataFrame();
    return C;

def getOneItemSet(T: pd.DataFrame) -> pd.DataFrame:
    S : pd.DataFrame = T.columns.to_frame();
    S["supp"] = supp(S,T)
    return 

def supp(S: pd.DataFrame | list, D: pd.DataFrame) -> np.:
    """
    Pameters:
    ---
    S :pd.Series A Itemset
    D :pd.DataFrame 
    """
    return card(setFromItemSet(S[1],D)) / card(D);

def setFromItemSet(S:, D:):

def card(A: pd.DataFrame):
    return A.count();

def confidence()
