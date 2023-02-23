# Minería de reglas de asociación espacial sobre Minecraft

## El Proyecto
Este proyecto tiene como objetivo la aplicación de algoritmos de Inteligencia Artificial. La idea inicial consistió en buscar una solución a un problema particular que se puede explicar de la siguiente manera:

Dentro de la industria de creación de videojuegos existe un area grande e importante que consiste en la generación procedural.
Se le llama generación procedural de contenido, o **PCG** (*Procedural Content Generation*) por sus siglas en ingles, a la creación algorítmica de contenido para videojuegos con entradas del usuario limitadas o indirectas. [*Procedural Content
Generation in Games_ Noor Shaker,Julian Togelius,Mark J. Nelson*].  

Dentro de este area existen varios algoritmos que permiten la generación de contenido a partir de el establecimiento de parámetros de entrada que permiten al Diseñador orientar el funcionamiento del algoritmo. Teniendo en cuenta esta característica surge la pregunta: 
- ¿Sería posible mediante un algoritmo de inteligencia artificial y un entorno no generado artificialmente, poder *inferir* parámetros para que el algoritmo genere entornos similares?  

O de otra manera:
- ¿Puedo ***inferir las relaciones*** que existen entre los objetos de un entorno dado y, a partir de ellos, establecer parámetros para un algoritmo de generación procedural?

Debido a la extension que conllevaría realizar un proyecto para contestar estas preguntas, se decidió que el enfoque del proyecto estará en la búsqueda y comparación de algoritmos de inteligencia artificial que permitan la descripción, aprendizaje o inferencia de las relaciones que existen entre objetos en un espacio físico o virtual.

Con la exploración bibliográfica se puede entender que existe un area de investigación dentro de la ciencia en minería de datos que enfocada en como realizar las tareas de minería de datos sobre bases de datos espaciales o geográficas. La **Minería de Datos Espaciales** o **SDM** es un proceso de descubrimiento y extracción de conocimiento generalizado sobre gran cantidad de datos espaciales. [Spatial Data Mining_ Theory and Application_Deren L., Shuliang W., Deyi L]

El proyecto entonces consistirá en la aplicación de algunas técnicas y algoritmos utilizados en el area de *SDM* para realizar la inferencia de relaciones entre objetos espaciales en un entorno. Concretamente, los aplicaremos sobre un conjunto de datos extraídos del Videojuego *Minecraft*.

*Minecraft* es un videojuego 3D que utiliza un complejo procedimiento de generación procedural para la creación de terrenos de juego utilizando bloques. Se toma este escenario para la realización del proyecto debido a que los datos correspondientes a un terreno generado en el videojuego son de fácil acceso y la extracción de es sencilla, además, la disposición de los objetos dentro del juego son bloques con coordenadas rectangulares. Se puede obtener mas información sobre el procedimiento de generación procedural en está pagina web: [The World Generation of Minecraft](https://www.alanzucconi.com/2022/06/05/minecraft-world-generation/).

## Apriori Y Metricas

### Definición formal del problema
Sea $I = \{i_1,...,i_n\}$ un conjunto de *items*.Al conjunto que contiene *k* items se le llama conjunto *k* de items. Si $A \subseteq I,B \subseteq I$ y $A \cap B = \empty$, entonces las regla de asociación es una implicación de la forma $A\ implies B$.
   
$D$ es el conjunto de datos transaccionales relevantes para la tarea de minería.Cada transacción $T$ con un identificador $TID$ es el conjunto permitiendo $T \subseteq I$.  
Un conjunto de items ***frecuente*** es uno donde la frecuencia de ocurrencia de los items no es menor que el **soporte mínimo** establecido y no menor que el numero de transaccionen de $D$.

El algoritmo *Apriori* utiliza información en conjuntos de items *frecuentes* para generar reglas de asociación.La idea básica es buscar en el conjunto de datos transaccionales varias veces para determinar los *conjuntos de items frecuentes*. Cada búsqueda después de la primera, tiene la prioridad de generar conjuntos de datos frecuentes candidato a partir del ultimo conjunto de datos frecuentes obtenido. La información a priori es utilizada para generar el primer conjunto frecuente.

### Métricas
+ Soporte: Mide la frecuencia con la que aparece en cada transacción. Se trata de la probabilidad de que aparezca X o Y en las transacciones.
$$
Support({X}\to{Y})  = \dfrac
{\text{Transaction containing X and Y}}
{\text{Total number of transactions}}
$$

+ Confianza: Mide la probabilidad de que aparezca el consecuente dado un antecedente.

$$
Confidence({X}\to{Y})  = \dfrac
{\text{Transaction containing X and Y}}
{\text{Transactions containing X}}
$$

+ Sustentación: El indicador lift expresa cuál es la proporción del soporte observado de un conjunto de productos respecto del soporte teórico de ese conjunto dado el supuesto de independencia..Un valor de lift = 1 indica que ese conjunto aparece una cantidad de veces acorde a lo esperado bajo condiciones de independencia. Un valor de lift > 1 indica que ese conjunto aparece una cantidad de veces superior a lo esperado bajo condiciones de independencia (por lo que se puede intuir que existe una relación que hace que los productos se encuentren en el conjunto más veces de lo normal). Un valor de lift < 1 indica que ese conjunto aparece una cantidad de veces inferior a lo esperado bajo condiciones de independencia (por lo que se puede intuir que existe una relación que hace que los productos no estén formando parte del mismo conjunto más veces de lo normal).

$$
Lift({X}\to{Y})  = \dfrac{Confidence({X}\to{Y})}{Support({X}\to{Y})}
$$

## Creación de transacciones a partir de datos espaciales

Muchos conjuntos de datos espaciales consisten en instancias de una colección de atributos espaciales booleano. Estos, pueden ser pensados como tipos de item, y puede que no exista un numero finito de transacciones debido a la continuidad del espacio.
En muchos problemas y ambientes existe un interés en variedad de patrones espacio-temporales incluyendo las *co-location rules* (reglas de co-localización).

Los *patrones de co-localización* representan co-ocurrencias frecuentes de subconjuntos de Atributos espaciales booleanos. 

Existen dos tipos de patrones de co-localización:  
1. **Local co-location patterns**:  Representan relaciones entre eventos en localizaciones comunes, ignorando los aspectos temporales de los datos. Estos patrones pueden encontrarse utilizando algoritmos para la clásica minería de reglas de association.
2. **Spatial co-location patterns**: Representan relaciones entre eventos sucediendo en diferentes y posibles localizaciones cercanas.

Los acercamientos a el descubrimientos de *co-location rules* en la literatura puede categorizarse en **Spatial statistics** y **association rules**. 
- Los métodos basados en **estadística espacial** utilizan medidas de correlación espacial para caracterizar las relaciones entre los diferentes tipos de atributos espaciales. Computar las medidas de correlación espacial para todo posible patron de co-localización puede ser computacionalmente caro debido al numero exponencial de candidatos dado una gran cantidad de atributos espaciales.
- El acercamiento basado en **reglas de association** se concentra en la creación de transacciones booleanas sobre el espacio de tal manera que se pueda usar el algoritmo ***apriori***.***(Estos son de nuestro interés para la resolución del problema)***

Los problemas de co-localización espacial se ven similares a los clásicos pero de hecho son diferentes debido a la ausencia de transacciones.En el problema de minería de reglas de co-localización espacial, las transacciones son implícitas y además son disjuntos en el sentido de que no comparten instancias de tipos de item. Las instancias de atributos espaciales booleanos están embebidos en el espacio y comparten una variedad de relaciones espaciales unas con otras.

### Modelos para transacciones booleanas de reglas de co-localización

Con el fin de tomar el conjunto de datos espaciales obtenidos compuesto por coordenadas rectangulares y modificarlos para que sirvan de entrada para el algoritmo **Apriori**. Se pretende utilizar algunos de los modelos siguientes.

Modelos:
1. **Reference feature centric model**  
Es relevante para aplicaciones enfocadas en un atributo espacial booleano. El modelo enumera los *vecindarios* para "materializar" un conjunto de transacciones al rededor de instancias del referenciado atributo espacial.
Al "materializar" transactions, el soporte y la confianza de la minería tradicional deberían ser usados como prevalencia y medidas de probabilidad condicionada.
2. **Window centric model**   
Es relevante para aplicaciones que se enfocan en land-parcels(raster). Un objetivo es predecir predecir conjuntos de atributos espaciales que es probable descubrir en una parcela dado que se han encontrado otros atributos en el.
Discretizando con un raster o grilla se generan particiones del terreno, y en este caso infinitas particiones pueden obtenerse con el solapamiento de ventanas. Nuevamente se utiliza el soporte y la confianza de la minería clásica.
3. **Event centric model**   
Es relevante para aplicaciones donde hay muchos tipos de atributos espaciales booleanos. Se utiliza cuando es de interés encontrar subconjuntos de atributos espaciales probables a ocurrir en el vecindario alrededor de instancias dado subconjuntos de tipos de eventos.
4. **Concept lattice**   
A lattice is a model for a gridded space in a spatial framework. Here the lattice refers to a countable collection of regular or irregular spatial sites related to each other via a neighborhood relationship. Several spatial statistical analyses, e.g., the spatial autoregressive model and Markov random fields, can be applied on lattice data. A Lattice Hasse diagram simply visualizes the generalization/characterization relationship between the intension and extension of a concept. Creating a Hasse diagram is similar to the process of concept classification and clustering. Compared with the Apriori algorithm, the concept lattice reduces the number of association rules by decreasing the quantity of the frequent itemsets and helps generate non-redundant rules by using a productive
subset of the frequent closed itemsets.
5. **Cloud model**   
In general, the frequent itemset association rules exist at a high conceptual level, and it is difficult to uncover them at a low conceptual level. In particular, when the attribute is numeric and the mining is on the original conceptual
level, strong association rules will not be generated if min_sup and the min_conf are larger, while many uninteresting rules will be produced if the thresholds are relatively smaller. In this case, the attribute needs to be elevated to a higher
conceptual level via attribute generalization, and then the association rules are extracted from the generalized data. The cloud model flexibly partitions the attribute space by simulating human language. Every attribute is treated as a linguistic variable that sometimes is represented with two or more attributes, which is
regarded as a multidimensional linguistic variable.
6. **Existen otros**

De todos los anteriores modelos, para este caso de aplicaciones solo 2 son de nuestro interés. El **Windows centric model** que nos resulta de muy fácil aplicación debido a que el mapa del videojuego ya se encuentra grillado en 3 dimensiones. Y (de manera tentativa), el **Cloud model** debido a que nos permite de alguna manera tomar el dominio de las coordinas rectangulares y generar expresarlo en lenguaje natural.

En principio como el mapa del juego esta grillado con coordenadas rectangulares y ademas esta subdividido en *chunks*,tranquilamente se podrían utilizar como ventanas y suponer que hay vecindad entre los bloques que los componen. Aún así estas ventanas serían muy grandes y nos darían una cantidad de transacciones pequeñas. Por lo tanto lo que podemos hacer es probar el algoritmo a priori con distintos tamaños de ventas y algún caso con superposición de ventanas.