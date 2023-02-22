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
    #1-itemSet
    L: pd.DataFrame = __getOneItemSet(T);
    L = L[__supp(L,T) >= min_supp];
    
    Llist :list[pd.DataFrame] = [];
    while(len(L) != 0):
        Ck = __apriori_gen(L,T)#new candidate
        L = Ck[__supp(Ck,T) >= min_supp]
        if(len(L)>0):
            Llist.append(L);
    
    #union de todos los L
    itemSets = pd.concat(Llist);
     
    #Create all the non-void subsets s (s ⊆ l) for each frequent itemsets l.
    columns=["antecedants","=>","consequents","support","confidence","lift"];
    rows=[];
    for itemset in itemSets["itemset"].tolist():
        subitemsets = __subitemset(itemset,k=len(itemset)-1);
        for sub in subitemsets:
            A = sub;
            B = __restaSet(itemset,sub);
            con = __conf(A,B,T);
            if(con >= min_conf):
                sup = __support(A,B,T);
                li = con/sup;
                rows.append([str(A),"=>",str(B),sup,con,li]);
    res = pd.DataFrame(data=rows,columns=columns);
    return res;

def __getOneItemSet(T: pd.DataFrame) -> pd.DataFrame:
    """Generate the 1-itemset."""
    S : pd.DataFrame = T.columns[2:len(T.columns)].to_frame(name="itemset");
    #pd.concat([S,pd.Series(map(lambda x: [x],list(S.iloc[:,0])))]);
    S.iloc[:,0] = list(map(lambda x: [x],list(S.iloc[:,0])));
    return S;

def __apriori_gen(L : pd.DataFrame,T: pd.DataFrame)-> pd.DataFrame:
    #1 join L with L
    Ck: pd.DataFrame = pd.DataFrame();
    Lp: pd.DataFrame = L;
    Lq :pd.DataFrame = L.copy();
    Ck = __union(Lp,Lq);
    #2 delete all itemsets c on Ck tal que algunos k-1 subset of c is not in lk-1
    for c in Ck["itemset"]:
        for s in __subitemset(c,k=len(c)-1):
            if(not __elementOf(s,L)):
                Ck = __deleteOf(c,Ck);
    return Ck

def __union(A :pd.DataFrame, B : pd.DataFrame) -> pd.DataFrame:
    """Creates a new dataframe that is result of union of each itemset of A with B """
    C  = pd.DataFrame(columns=["itemset"]);
    allSet = set();
    for i in range(0,len(A)):
        for j in range(0,len(B)):
            if(i!=j):
                currSet = set(A.iat[i,0]).union(set(B.iat[j,0]));
                if(len(currSet) == len(A.iat[i,0])+1):
                    allSet.add(frozenset(currSet)); 
    C.loc[:,"itemset"] = list(map(lambda x: list(x),list(allSet)));
    #pd.concat([C,pd.Series(map(lambda x: [x],list(allSet)))]);
    return C;

def __deleteOf(a :list,A:pd.DataFrame) -> pd.DataFrame:
    """Delete itemset form column itemSet"""
    A = A.drop(A[A.itemset.isin([a])].index);
    return A;

def __elementOf(a : list,A :pd.DataFrame) -> bool:
    """Return True if itemset a in in A itemset column"""
    result = pd.Series([a]).isin(A["itemset"]);
    return result[0];

def __subitemset(c: list,k : int) -> list:
    """Resturn the powerset of an itemset without the void set and the hole set"""
    return __subitemsetRecursive(c,[],k);

def __subitemsetRecursive(c: list,A :list, k: int) -> list:
    if(len(c) == k):
        A.append(c);
    else:
        for i in range(0,len(c)):
            newSub = c.copy();
            newSub.remove(c[i]);
            __subitemsetRecursive(newSub,A,k);
        return A;

# unir, es nesesario?
def __unirSet(A:list,B:list)->list:
    return list(set(A).union(set(B)));

#resta de listas
def __restaSet(A:list,B:list):
    return list(set(A).difference(set(B)))

def __conf(A: list,B: list, D: pd.DataFrame):
    S = __unirSet(A,B)
    C = pd.DataFrame(data=[[S]],columns = ["itemset"]);
    C = __freq(C,D);
    dfA = pd.DataFrame(data=[[A]],columns = ["itemset"]);
    dfA = __freq(dfA,D);
    return (C["freq"]/dfA["freq"])[0];

def __freq(S: pd.DataFrame, T: pd.DataFrame)->pd.DataFrame:
    """
    Returns the S dataframe with a new column "freq" that contains the frequency for each itemset.
    """
    f: list = [];
    for itemset in S.iloc[:,0]:
        A = T.copy();
        for att in itemset:
            A = A[A[att] == True];
        f.append(len(A));
    S["freq"] = f;
    return S;

def __supp(S: pd.DataFrame, D: pd.DataFrame) -> pd.Series:
    """
    Calculates the support for each itemset from given transaction datarse.
    Retorna una serie con el sopporte de cada elemento.
    """
    S = __freq(S, D);
    return S["freq"]/len(D);

def __support(A:list,B:list,D: pd.DataFrame):
    S = __unirSet(A,B)
    C = pd.DataFrame(data=[[S]],columns = ["itemset"]);
    return __supp(C,D)[0];

def plot(rules):
    import networkx as nx
    import matplotlib.pyplot as plt 
    G1 = nx.DiGraph()

    color_map=[]
    N = 50
    colors = np.random.rand(len(rules))    
    names=[]

    for i in range(len(rules)):
        names.append("R" + str(i));      
        G1.add_nodes_from(["R" + str(i)],subset= (i % 1)+1)
        
        ant = rules.iloc[i]['antecedants'];
        G1.add_nodes_from([ant],subset=0)
        G1.add_edge(ant, "R"+str(i), color=colors[i] , weight = 2)
    
        con = rules.iloc[i]['consequents'];
        G1.add_nodes_from([con],subset=11)
        G1.add_edge("R"+str(i), con, color=colors[i],  weight=2)

    for node in G1:
        found_a_string = False
        for item in names: 
            if node==item:
                    found_a_string = True
        if found_a_string:
                color_map.append('yellow')
        else:
                color_map.append('green')       

    edges = G1.edges()
    colors = [G1[u][v]['color'] for u,v in edges]
    weights = [G1[u][v]['weight'] for u,v in edges]


    #pos = nx.random_layout(G1);
    pos = nx.arf_layout(G1);
    #pos = nx.spring_layout(G1)
    nx.draw(G1, pos,node_color = color_map, edge_color=colors, width=weights, font_size=16, with_labels=False)
    #, edges=edges, )            

    for p in pos:  # raise text positions
            pos[p][1] += 0.07
    nx.draw_networkx_labels(G1, pos)
    plt.show()