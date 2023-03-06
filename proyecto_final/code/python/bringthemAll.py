#Path del CSV
csvPath = "..\\..\\Data\\chunks.csv"
#Lectura del CSV
import pandas as pd
df = pd.read_csv(csvPath,delimiter=";",lineterminator="\n")
df = df.rename(columns={"ChunkX": "CX","ChunkZ\r": "CZ"}, errors="raise")
from preprocess import Preprocess
atts  = df.Tag.unique().tolist();
#intratable Arboles y hojas
Preprocess.referenceFeatureModel(atts,df,atts,"..\\..\\Data\\AlltransactionsCruz.csv");