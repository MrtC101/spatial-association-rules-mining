import pandas as pd
import numpy as np

def apriori(T : pd.DataFrame,min_supp : float,min_conf: float) -> pd.DataFrame:
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
    Llist = [];
    L: pd.DataFrame = getOneItemSet(T);
    L = L[supp(L,T) >= min_supp];
    while(len(L) != 0):
        Ck = apriori_gen(L,T)#new candidate
        #support
        L = Ck[supp(Ck,T) >= min_supp]
        Llist.append(L);
    #union de todos los L y generacion de reglas
    result = pd.DataFrame(columns={"itemset","freq"});
    for L in Llist:
        for i in range(0,len(L)):
            result.loc[len(result)] = L.iloc[i,0:len(L.columns)]; 
    #Create all the non-void subsets s (s ⊆ l) for each frequent itemsets l.
    itemsets = result["itemset"].tolist();
    res= pd.DataFrame(columns=["rule","support","confidence","lift"]);
    for itemset in itemsets:
        subitemsets = allSubsets(itemset);
        for sub in subitemsets:
            A = sub;
            B = restaSet(itemset,sub);
            con = conf(A,B,T);
            if(con >= min_conf):
                rule =str(A)+"=>"+str(B);
                sup = support(A,B,T);
                li = con/sup;
                res.loc[len(res)] = [rule,sup,con,li];
    return res;

# unir, es nesesario?
def unirSet(A:list,B:list)->list:
    C = A.copy();
    for i in A:
        for j in B:
            if(i!=j):
                C.append(j);
    return C;
#resta de listas
def restaSet(A:list,B:list):
    C = [];
    for a in A:
        for b in B:
            isin = False;
            if(a == b):
                isin = True;
                break;
        if(not isin):
            C.append(a)
    return C

def apriori_gen(L : pd.DataFrame,T: pd.DataFrame)-> pd.DataFrame:
    #1 join L with L
    Ck: pd.DataFrame = pd.DataFrame();
    Lp: pd.DataFrame = L;
    Lq :pd.DataFrame = L.copy();
    Ck = union(Lp,Lq);
    #2 delete all itemsets c on Ck tal que algunos k-1 subset of c is not in lk-1
    for c in Ck["itemset"]:
        for s in subSets(c):
            if(not elementOf(s,L)):
                Ck = deleteOf(c,Ck);
    return Ck

def freq(S: pd.DataFrame, T: pd.DataFrame)->pd.DataFrame:
    f: list = [];
    for itemset in S.iloc[:,0]:
        A = T.copy();
        for att in itemset:
            A = A[A[att] == True];
        f.append(len(A));
    S["freq"] = f;
    return S;

def subSets(c : list)-> list:
    power = [];    
    for i in range(0,len(c)):
        newSub = c.copy();
        newSub.remove(c[i])
        power.append(newSub);
    return power;


def allSubsets(c: list) -> list:# un itemset
    power=[[]];
    for s in range(1,len(c)):
        for j in range(len(power)):
            sub = power[j];
            currC = c.copy();
            for el in sub:
                currC.remove(el);
            for el in currC:
                newSub = sub.copy();
                newSub.append(el);
                power.append(newSub);
    power.remove([]);
    return power

def deleteOf(a,A:pd.DataFrame) -> pd.DataFrame:
    A = A.drop(A[A.itemset.isin([a])].index);
    return A;

def elementOf(a : list,A :pd.DataFrame) -> bool:
    result = pd.Series([a]).isin(A["itemset"]);
    return result[0];

#arreglar
def union(A :pd.DataFrame, B : pd.DataFrame) -> pd.DataFrame:
    C  = pd.DataFrame(columns={"itemset"});
    for i in range(0,len(A)):
        for j in range(0,len(B)):
            if(i!=j):
                new = A.iat[i,0].copy();
                for e in B.iat[j,0]:
                    if sum(list(map(lambda x: x == e,new))) == 0:
                        new.append(e);
                if(len(new) == len(A.iat[i,0])+1):
                    if(isinSet(C.iloc[:,0],new) == False):
                        C.loc[len(C)] = [new];
    return C;

#ineficiente n^3
def isinSet(s: pd.Series,newset: list)->bool:
    for set in s:
        for j in range(len(newset)):
            if(isin(set,newset[j]) == False):
                break;
            elif(j == len(newset)-1):
                return True;
    return False;

def isin(l :list, e) -> bool:
    for item in l:
        if(e == item):
            return True;
    return False;

def getOneItemSet(T: pd.DataFrame) -> pd.DataFrame:
    S : pd.DataFrame = T.columns[2:len(T.columns)].to_frame(name="itemset");
    for i in range(0,len(S)):
        new = list();
        new.append(S.iat[i,0]);
        S.iat[i,0] = new;
    return S;


def conf(A: list,B: list, D: pd.DataFrame):
    S = unirSet(A,B)
    C = pd.DataFrame(columns = ["itemset"]);
    C.loc[len(C)] = [S];
    C = freq(C,D);
    dfA = pd.DataFrame(columns = ["itemset"]);
    dfA.loc[len(dfA)] = [A]
    dfA = freq(dfA,D);
    return (C["freq"]/dfA["freq"])[0];


def support(A:list,B:list,D: pd.DataFrame):
    S = unirSet(A,B)
    C = pd.DataFrame(columns = ["itemset"]);
    C.loc[len(C)] = [S];
    return supp(C,D)[0];

def supp(S: pd.DataFrame, D: pd.DataFrame) -> pd.Series | list:
    S = freq(S, D);
    return (S["freq"]/len(D));
