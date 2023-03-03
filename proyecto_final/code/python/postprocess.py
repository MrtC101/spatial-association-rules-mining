import pandas as pd;
import numpy as np;
import math 

def changeFrameToString(A :pd.DataFrame):
    for name in A.columns:
        if(A[name].dtype == np.dtype('O')):
            col : pd.Series = A[name];
            A[name] = coltostr(col);
    return A

def coltostr(l : pd.Series) -> pd.Series:
    return pd.Series(map(lambda x : str(x),l));  

def changeFrame(A :pd.DataFrame):
    for name in A.columns:
        if(A[name].dtype == np.dtype('O')):
            col : pd.Series = A[name];
            A[name] = coltolist(col);
    return A;

def coltolist(l : pd.Series) -> pd.Series:
    return pd.Series(map(lambda x : tolist(x),l));  

def tolist(l : str) -> list:
    n = l.replace("'","").strip('][').strip(' ').strip("'").split(',');
    for e in n:
        e = e.strip(" ");
    return n


def chi_square_test(r : pd.Series,R :pd.Series) -> float:
    #   fr   |   xfr-fr   |xfr
    # yfr-fr |n-yfr+fr-frx|n-xfr
    #   yfr  |    n-yfr   |n = fr/supp
    #busco a partir de la regla y su ancestro construir la tabla de contingencia
    m = [[0,0,0],[0,0,0],[0,0,0]];
    m[2][2]= r["frequency"]/r["support"]
    m[0][0]= r["support"]*m[2][2];
    #Susede que esta definicion es correcta cuando "->y" pero en otro caso no
    #surje la pregunta entonces Como esta planteado la prueba para que se involucre r y R.
    m[2][0]= R["support"]*m[2][2];
    m[0][2]= (r["support"]/r["confidence"]) * m[2][2];
    m[0][1]= m[0][2]-m[0][0];
    m[1][0]= m[2][0]-m[0][0];
    m[1][2]= m[2][2]-m[0][2];
    m[2][1]= m[2][2]-m[2][0];
    m[1][1]= m[2][2]-m[2][0]+m[0][0]-m[0][2];
    es = [[0,0],[0,0]]
    for i in range(2):
        for j in range(2):
            es[i][j] = (m[i][2]*m[2][j])/m[2][2];
    res = 0;
    for i in range(0,2):
        for j in range(0,2):
            res+= math.pow(m[i][j] - es[i][j],2) / es[i][j];
    return res;

def evalPrune(r : pd.Series,r_rest : pd.Series,s):
    """ Evalúa si la regla r es podada por:
        - regla que podo a r_rest
        - la regla r_rest
        - si no existe correlación positiva entre r y r_rest
    """
    if type(r_rest.pruned)==pd.Series:
        r_rest = r_rest.pruned;
    if r.dir != 1:
        r.loc["pruned"] = tuple(r_rest); 
    elif(compDir(r,r_rest,s)!= 1):
        r.loc["pruned"] = tuple(r_rest); 

def compDir(r : pd.Series,R : pd.Series, s : float)->int:
    """
    Uses chi-square test to compute direction of rule r respect rule R.    
    
    Parameters
    ---------
    r : `pd.Series` a rule.
    R : `pd.Series` an ancestor rule of r.(same consequent but bigger antecedent)
    chi : `float` a chi-squeare value at a `s` significance level
    """

    import scipy,scipy.stats
    chi = scipy.stats.chi2.ppf(q=(1-s), df=1);
    if chi_square_test(r,R) > chi:
        #cover = supp(X)
        rcover = (r["support"]/r["confidence"]);
        Rcover = (R["support"]/R["confidence"]);
        if(r["support"] > rcover*(R["support"]/Rcover)):
            return 1;
        else:
            return -1;
    return 0;

def mostGeneralRule(r : pd.Series)->pd.Series:
    ry = r.copy();
    ry.antecedants = [];
    ry.support = r.Yfrequency / (r.frequency / r.support);
    ry.confidence = r.support;
    ry.frequency = r.Yfrequency
    ry.Xfrequency = None;
    ry.lift = 1;
    ry.efrequency = None;
    return ry;

#Quitar reglas no importantes
def pruneRules(rules : pd.DataFrame,s : float)-> pd.DataFrame:
    rules = changeFrame(rules);
    """
    Params
    ------
    rules : `pd.DataFrame` conjunto de reglas de asociación
    s : `float` significance for chi_square_test.
    """
    newrules = rules.copy();
    newrules["dir"] = None;
    newrules["pruned"] = None;
    newrules["justify"] = None;
    
    DSR = pd.DataFrame(columns=newrules.columns); #Directed Setting Rules set
    
    n = max(list(map(len,rules["antecedants"])));
    previousRules = pd.DataFrame(columns=newrules.columns); 
    for k in range(1,n):

        klevelrules = newrules[pd.Series(map(len,newrules["antecedants"])) == k];
        for i in range(len(klevelrules)):
            
            r :pd.Series = klevelrules.iloc[i].copy();

            ry = mostGeneralRule(r);
            #"X->y"," ->y"
            r.loc["dir"] = compDir(r,ry,s);
            if(k == 1):
                if(r.dir == 1):
                    r.justify = "positive correlated 1-level rule";
                    DSR.loc[len(DSR)] = r;
                else:
                    r.loc["pruned"] = tuple(ry);
            else:
                currAnt :list = list(r["antecedants"]).copy();
                rulesUntilk = pd.concat([previousRules,klevelrules]);
                sameConRules : pd.DataFrame = rulesUntilk[rulesUntilk["consequents"].isin(r.take([2]))]#Esto tambien 
                
                for el in currAnt:
                    if type(r.pruned)==tuple:
                            break; #r is already pruned
                    
                    rest = currAnt.copy();
                    rest.remove(el);
                    r_restCandidates = sameConRules[sameConRules["antecedants"].isin(pd.Series([rest]))];
                    if(len(r_restCandidates) > 0): # If There is a rule with antecendant like rest
                        r_rest = r_restCandidates.iloc[0].copy();  

                        evalPrune(r,r_rest,s) #verificar
                        
                        if(type(r.pruned) != tuple): # If still not pruned
                            
                            r_1Candidates = sameConRules[sameConRules["antecedants"].isin(pd.Series([[el.strip(" ")]]))];
                            if(len(r_1Candidates) > 0): # If There is a rule with antecendant like [el]
                                r_1 = r_1Candidates.iloc[0].copy();
                                
                                if(r_1.dir == 1 and r_rest.dir == 1):
                                    if(r.dir == 1):#Expected direction
                                        r.loc["justify"] = [];
                                    else:
                                        r.loc["dir"] = None;
                                elif((r_1.dir==1 and r_rest.dir==0)or(r_1.dir==0 and r_rest.dir==1)):
                                    if(r.dir==1):#Expected direction
                                        r.loc["justify"] = [];
                                    else:
                                        r.loc["dir"] = None;
                                elif(r_1.dir==0 and r_rest.dir==0):
                                    if(r.dir==0):#Expected direction
                                        r.loc["justify"]=[];
                                    elif(r.dir == 1):
                                        if(type(r.justify)!=list):
                                            r.loc["justify"]=[];
                                        r.loc["justify"] = r.justify.extend((r_1,r_rest))
                                    else:
                                        r.loc["dir"] = None;
                                else:
                                    if(r.dir == 1):
                                        if(type(r.justify)!=list):
                                            r.loc["justify"]=[];
                                        r.loc["justify"] = r.justify.extend((r_1,r_rest))
                                    else:
                                        r.loc["dir"] = None;
                if(r["justify"] != None):
                    if(len(r["justify"])>0):
                        if(r["pruned"] != None):
                            r["dir"] = None;
                        else:
                            DSR.loc[len(DSR)] = r;
            klevelrules.iloc[i] = r;
        previousRules = pd.concat([previousRules,klevelrules]);
    previousRules = changeFrameToString(previousRules);
    DSR = changeFrameToString(DSR);
    non_DS = previousRules[~previousRules.antecedants.isin(DSR.antecedants) & (previousRules.pruned == "None")];
    #return DS,non-DS;
    return DSR,non_DS;

#rules = pd.read_csv("proyecto_final\Data\chunk00rules5x00.csv",sep=";");
#rules = rules.drop(rules.columns[0],axis=1);
#pruneRules(rules,s=0.2);

# Export a neo No fue util --------------------------------------------------------------------------------
def clean(tx):
      tx.run("MATCH ()-[r]->() "
             "MATCH (a) "
             "DELETE r "
             "DELETE a");

def make_relations(tx,path):
    result=tx.run("LOAD CSV WITH HEADERS FROM \"file:///"+path+"\" AS row FIELDTERMINATOR ';' "
        "MATCH (e:item {name: row.antecedants}) "
        "MATCH (c:item {name: row.consequents}) "
        "MERGE (e)-[:RULE {supp:row.support,conf:row.confidence,lift:row.lift}]->(c) "
        "RETURN *")

def load_csv(tx,path):
    result=tx.run("LOAD CSV WITH HEADERS FROM \"file:///"+path+"\" AS row FIELDTERMINATOR ';' "
        "MERGE (anti:item {name:row.antecedants}) "
        "MERGE (coni:item {name:row.consequents})")

def save_graphml(tx,path):
    tx.run("CALL apoc.export.graphml.all(\""+path+"\" ,{useTypes:True,readLabels:True,deafaultRelationshipType:'Rule',caption:['name','supp']})")

#Crear un plot de nodos con neo4j database
def toNeo( csvname: str):
    csvpath = r"C:/Users/MrtC101/Desktop/Ciencias_en_Computacion/Cursado/3.2Inteligencia%20Artificial%20I/repositorio-proyecto-final/proyecto_final/Data/"+csvname+".csv";
    graphPath = r"/Users/MrtC101/Desktop/Ciencias_en_Computacion/Cursado/3.2Inteligencia Artificial I/repositorio-proyecto-final/proyecto_final/Images/Graphs/"+csvname+"graph.graphml";
    from neo4j import GraphDatabase as GD
    with GD.driver("neo4j://localhost:7687",auth=("neo4j", "martinsuperpassword")) as driver:
        driver.verify_connectivity()
        with driver.session(database="neo4j") as session:
            session.execute_write(clean);
            session.execute_write(load_csv,csvpath);
            session.execute_write(make_relations,csvpath);
            #session.execute_write(save_graphml,graphPath);
    #plot2(graphPath);

def plot2(path : str):
    import networkx as nx
    import matplotlib.pyplot as plt 
    G1 = nx.read_graphml(path);
    #Mejorar el plot
    plt.figure(figsize=(15,12));
    pos = nx.kamada_kawai_layout(G1);
    node_options={};
    edge_options={};
    nx.draw_networkx_nodes(G1,pos,node_options);
    nx.draw_networkx_edges(G1,pos,edge_options);
    nx.draw_networkx_labels(G1,pos,font_size=16);  

#Un plot que anda muy mal ---------------------------------------------------------------------
def plot(rules):
    import networkx as nx
    import matplotlib.pyplot as plt 
    G1 = nx.DiGraph();
     
    node = dict();
    for j in range(len(rules)):
        ant = rules.iloc[j]['antecedants'];
        con = rules.iloc[j]['consequents'];
        if(node.get(ant)==None):
            node.update({ant:1});
        else:
            node[ant]+=1;
        if(node.get(con)==None):
            node.update({con:1});
        else:
            node[con]+=1;
    
    for i in range(len(rules)):
        ant = rules.iloc[i]['antecedants'];
        con = rules.iloc[i]['consequents'];
        G1.add_nodes_from([ant],subset=0)
        G1.add_nodes_from([con],subset=1)
        weight=( 2*max(node.values())+1 - min(node.get(ant),node.get(con)))
        #weight= max(node.get(ant),node.get(con));
        G1.add_edge(ant, con, color='tab:blue',  weight=weight)
    edges = G1.edges();
    weights = [G1[u][v]['weight'] for u,v in edges]
    
    plt.figure(figsize=(20,20),dpi=150);
    pos = nx.spring_layout(G1,weight="weight");
    #pos = nx.arf_layout(G1,scaling=1);
    nx.draw_networkx_nodes(G1,pos,node_color = 'tab:blue', node_size=1000);
    nx.draw_networkx_edges(G1,pos,edge_color = "tab:red", width=0.5);
    nx.draw_networkx_labels(G1,pos,font_size=5);
    plt.show();

# Intento de stream a genphi------------------------------------------------------------------------
def togenphi(rules):
    from gephistreamer import graph
    from gephistreamer import streamer
    #create a stream
    stream = streamer.Streamer(streamer.GephiWS(hostname="localhost", port=8080, workspace="workspace0"))

    nodes = [];
    edges = [];
    k = 0;
    prev = dict();

    for i in range(len(rules)):
            ant = rules.iloc[i]['antecedants'];
            if(prev.get(ant)==None):
                antNode = graph.Node(k,label=ant)
                prev.update({ant:k});
                k+=1;
                nodes.append(antNode);
            else:
                antNode = nodes[prev[ant]];
            con = rules.iloc[i]['consequents'];
            if(prev.get(con)==None):
                conNode = graph.Node(k,label=con)
                prev.update({con:k});
                k+=1;
                nodes.append(conNode);
            else:
                conNode = nodes[prev[con]];
            edge = graph.Edge(antNode,conNode,supp=rules.iloc[i]['support'],conf=rules.iloc[i]['confidence'],lift=rules.iloc[i]['lift']);
            edges.append(edge)
    
    #Send
    for node in nodes:
        stream.add_node(node);
    for edge in edges:
        stream.add_edge(edge);
    stream.commit();
    del stream