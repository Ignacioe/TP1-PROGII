#lenGt: (Any List, Int, Int) - > Boolean
def lenGt(lista, largo, contador = 0):                      #Definimos una funcion lenGt (length greater than), que es mas eficiente que len
    if (contador > largo):                                  #en los chequeos que tenemos que hacer. Esto se debe a que debemos chequear si 
        return True                                         #listas muy largas tienen mas de 0/1 elementos.
    elif (lista == []):
        return False
    else:
        return lenGt(lista[1:], largo, contador + 1)

#La funcion ingreso es la que debe llamarse desde el Shell. Se encarga de leer el archivo de entrada, y genera una lista de Diccionarios
#Cada Dict hace referencia a una persona y las keys seran Nombre, Apellido, Edad, Ciudad, Genero e Interes.
#Los values serán los datos de cada persona.
#ingreso: (String, String, String) -> None
def ingreso(nombreEntrada, nombreSalidaParejas, nombreSalidaSinParejas):
    archivo = open(nombreEntrada,"r", encoding = "latin1")
    texto = archivo.read()
    archivo.close()
    renglon = texto.split("\n")                             #Separa en renglones
    personas = []
    for elem in renglon:
        datos = elem.split(", ")                            #Separa por comas, en los distintos datos
        dictPersona = {"nombre" : datos[0], "apellido" : datos[1], 
                       "ciudad" : datos[2], "edad" : int(datos[3]), 
                       "genero" : datos[4], "interes" : datos[5]}
        personas.append(dictPersona)
    filtrado(personas, nombreSalidaParejas, nombreSalidaSinParejas)

#La funcion filtrado abre los archivos que se escribirán, y llama a filterEdad y filterCiudad, las cuales se encargan de
#encapsular a las personas en subgrupos determinados por su ciudad de residencia y su grupo de edades (jovenes, adolescentes, adultos).
#Luego, envia esta nueva lista de Diccionarios a matching, que se encargará de generar las posibles parejas.
#filtrado:(Dict List, String, String) -> None
def filtrado(personas, nombreConParejas, nombreSinParejas):
    sinPareja = open(nombreSinParejas,"w")                  #Abre el archivo donde escribiremos las parejas
    conPareja = open(nombreConParejas,"w")                  #Abre el archivo donde escribiremos la gente que queda sin pareja
    edades = filterEdad(personas, sinPareja)
    edadesCiudades = filterCiudad(edades)
    matching(edadesCiudades, conPareja, sinPareja)

#La función filterEdad toma la lista de personas y genera una lista de tres listas de personas, y cada una corresponde a un grupo de edades.
#Ademas, filtra las personas menores y asexuales, llamando a una funcion que las agrega al archivo de gente sin pareja.
#filterEdad: (Dict List, File) -> (Dict List) List
def filterEdad(personas, sinPareja):
    edades = [[], [], []]                                       #Edades es una lista de tres lista donde el primer elemento son los:
    for persona in personas:                                    #jovenes(11/14), adolescentes(15,18) y mayores(18+)
        if(persona["interes"] == "N"):                          #Si su interes es "N", lo agregamos al archivo con la gente sin pareja
            aggSinPareja(persona, "Asexual", sinPareja)         #con el motivo "Asexual"
        elif(persona["edad"] < 11):                             #Si su edad es menor de 10, lo agregamos al archivo con la gente sin pareja
            aggSinPareja(persona, "Menor", sinPareja)           #con el motivo "Menor"
        elif(persona["edad"] < 15):                             #Si es menor de 15, lo agrego al primer elemento
            edades[0].append(persona)
        elif(persona["edad"] < 18):                             #Sino, si es menor a 18, lo agrego al segundo elemento
            edades[1].append(persona)
        else:                                                   #Sino, lo agrego al tercer elemento
            edades[2].append(persona)
    return edades

#filterCiudad recibe la lista que devuelve filterEdad, y genera una lista de tres elementos; donde cada elemento es
#un diccionario corespondiente a cada grupo de edades.
#Las keys del diccionario serán las ciudades, y los values serán las listas de personas que residen alli
#(siempre que esten en su correspondiente grupo de edades)
#filterCiudad: Dict List -> Dict List
def filterCiudad(edades):
    edadesCiudades = []                                         #Nueva lista para guardar los tres diccionarios
    for elem in edades:
        edadCiudad = dict()                                     #Nuevo diccionario, uno para cada grupo de edades
        for persona in elem:
            ciudad = persona["ciudad"]
            if(ciudad in edadCiudad):                           #Si la existe la key, agrega la persona al value
                edadCiudad[ciudad]+=[persona]
            else:
                edadCiudad[ciudad] = [persona]                  #Sino inicializa la key e iguala el value a una lista con la persona
        edadesCiudades.append(edadCiudad)
    return edadesCiudades

#Esta funcion es la principal que se encarga de generar las parejas. Recibe las listas de personas encapsuladas en la lista de diccionarios,
#llama a la funcion que separa por sexualidad y llama a las distintas funciones que matchean a las personas,
#dandoles como parametro los diferentes grupos de sexualidad que deben ser juntados
#Recordar que: 1 - HombresHomo, 2 - HombresHetero, 3 - HombresBi, 4 - MujeresHomo, 5 - MujeresHetero, 6 - MujeresBi
#matching: (Dict List, File, File) -> None
def matching(edadesCiudades, conPareja, sinPareja):
    for edad in edadesCiudades:
        for ciudad in edad:
            personas = edad[ciudad]                                 #Ingresa al diccionario Edad en la Key ciudad, es decir, a cada lista de personas
            sexualidad = separarSexo(personas)                      #Separa la lista de personas en las diferentes sexualidades
            sexualidad[0] = parejasHomo(sexualidad[0], conPareja)   #Genera las parejas HombreHomo - HombreHomo
            sexualidad[3] = parejasHomo(sexualidad[3], conPareja)   #Genera las parejas MujerHomo - MujerHomo
            (sexualidad[1], sexualidad[4]) = parejasHetero(sexualidad[1], sexualidad[4], conPareja) #Genera las parejas HombreHetero - MujerHetero
            sexualidad[1] += sexualidad[3]                          #Junta las listas de HombresHetero y MujeresHomo, ya que ambas formaran parejas
            sexualidad[3] = []                                      #con HombresBisexuales
            sexualidad[4] += sexualidad[0]                          #De la misma forma, junta las MujeresHetero con los HombresHomo
            sexualidad[0] = []
            (sexualidad[4], sexualidad[2]) = parejasHetero(sexualidad[4] ,sexualidad[2] ,conPareja) #Arma parejas HombresHomo/MujerHetero con HombresBi
            (sexualidad[1], sexualidad[5]) = parejasHetero(sexualidad[1], sexualidad[5], conPareja) #Arma parejas MujeresHomo/HombresHetero con MujeresBi
            sexualidad[5] = parejasHomo(sexualidad[2] + sexualidad[5], conPareja)   #Arma parejas entre los bisexuales(mujeres u hombres)
            sexualidad[2] =  []
            sobrantes(sexualidad, sinPareja)                        #Escribo en el archivo que personas quedaron sin pareja

#Esta funcion recibe una lista de personas (ya filtradas por Edad y Ciudad), y las separa en 6 listas de personas
#dependiendo de su Genero y Genero de Interes, devolviendo en este orden:
#Hombres Homosexuales, Hombres heterosexuales, Hombres Bisexuales, Mujeres Homosexuales, Mujeres Heterosexuales, Mujeres Bisexuales.
#separarSexo: Dict List -> (Dict List) List
def separarSexo(personas):
    mascHom = []
    mascHet = []
    mascBi = []
    femHom = []
    femHet = []
    femBi = []
    for persona in personas:
        if(persona["genero"] == "F"):
            if(persona["interes"] == "F"):                          #Genero: F + Interes: F = MujerHomo
                femHom.append(persona)                              #Genero: F + Interes: M = MujerHetero
            elif(persona["interes"] == "M"):                        #Genero: F + Interes: A = MujerBi
                femHet.append(persona)                              #Genero: M + Interes: M = HombreHomo
            else:                                                   #Genero: M + Interes: F = HombreHetero
                femBi.append(persona)                               #Genero: M + Interes: A = HombreBi
        else:
            if(persona["interes"] == "F"):
                mascHet.append(persona)
            elif(persona["interes"] == "M"):
                mascHom.append(persona)
            else:
                mascBi.append(persona)
    return [mascHom, mascHet, mascBi, femHom, femHet, femBi]

#Esta funcion toma un conjunto de personas que pueden ser pareja entre ellas, y genera la maxima cantidad posible.
#Luego, devuelve la lista con las personas que sobraron.
#Si se tiene una cantidad par de personas al inicio, no sobrarán personas. Si era impar, sobra una sola persona.
#parejasHomo: (Dict List, File) -> Dict List
def parejasHomo(personas,conPareja):
    if(lenGt(personas, 1)):                             #Si tiene al menos dos personas:
        aggPareja(personas[0],personas[1],conPareja)    #Las junta
        personas = personas[2:]                         #Las borra de la lista
        return parejasHomo(personas,conPareja)          #Llama a la funcion con la nueva lista
    else:
        return personas                                 #Devuelve las personas que quedan sin pareja (a lo sumo, una)

#Recibe dos listas de personas donde se pueden formar parejas tomando una persona de cada grupo, y maximiza las parejas.
#Luego, devuelve las dos listas con las personas que sobraron.
#Si se tienen n personas mas en la primera lista que en la segunda, sobran n personas en la primera lista y 0 en la segunda, y viceversa.
#parejasHetero: (Dict List, Dict List, File) -> (Dict List, Dict List)
def parejasHetero(personas1,personas2,conPareja):
    if((lenGt(personas1, 0)) and (lenGt(personas2,0))): #Si hay al menos una persona en cada lista
        aggPareja(personas1[0],personas2[0],conPareja)  #Las junta
        personas1=personas1[1:]                         #Las borra
        personas2=personas2[1:]
        return parejasHetero(personas1,personas2,conPareja) #Llama a la funcion con las nuevas listas
    else:
        return (personas1,personas2)

#Esta funcion toma la lista de personas separadas por sexo que no hallan encontrado pareja compatible disponible,
#y las agrega al archivo de personas sin pareja, con el motivo "No hay parejas compatibles disponibles".
#sobrantes: ((Dict List) List), File) -> None
def sobrantes(sexualidad, sinPareja):
    for elem in sexualidad:
        for persona in elem:
            aggSinPareja(persona, "No hay parejas compatibles disponibles", sinPareja)

#aggSinPareja simplemente escribe en el archivo siguiendo los estandares de salida brindados en el enunciado.
#aggSinPareja:(Dict, String, File) -> None
def aggSinPareja(persona, motivo, sinPareja):
    sinPareja.write(persona["nombre"] + ", " +
                    persona["apellido"] +", " +
                    str(persona["edad"]) + ", " +
                    persona["ciudad"] + ", " +
                    persona["genero"] + ", " +
                    persona["interes"] + " - " +
                    motivo + "\n")
    
#aggSinPareja simplemente escribe en el archivo siguiendo los estandares de salida brindados en el enunciado.
#aggPareja:(Dict, Dict, File) -> None
def aggPareja(persona1, persona2, conPareja):
    conPareja.write(persona1["nombre"] + ", " +
                    persona1["apellido"] +" - " +
                    persona2["nombre"] + ", " +
                    persona2["apellido"] + " - " +
                    persona1["ciudad"] + "\n")
