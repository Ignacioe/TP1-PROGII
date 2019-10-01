def aggSinPareja(persona, motivo,sinPareja):
    sinPareja.write(persona["nombre"] + ", " +
                    persona["apellido"] +", " +
                    str(persona["edad"]) + ", " +
                    persona["ciudad"] + ", " +
                    persona["genero"] + ", " +
                    persona["interes"] + " - " +
                    motivo + "\n")

def aggPareja(persona1, persona2, conPareja):
    conPareja.write(persona1["nombre"] + ", " +
                    persona1["apellido"] +" - " +
                    persona2["nombre"] + ", " +
                    persona2["apellido"] + " - " +
                    persona1["ciudad"] + "\n")

def separarSexo(personas):
    mascHom = []
    mascHet = []
    mascBi = []
    femHom = []
    femHet = []
    femBi = []
    for persona in personas:
        if(persona["genero"] == "F"):
            if(persona["interes"] == "F"):
                femHom.append(persona)
            elif(persona["interes"] == "M"):
                femHet.append(persona)
            else:
                femBi.append(persona)
        else:
            if(persona["interes"] == "F"):
                mascHet.append(persona)
            elif(persona["interes"] == "M"):
                mascHom.append(persona)
            else:
                mascBi.append(persona)
    return [mascHom, mascHet, mascBi, femHom, femHet, femBi]

def parejasHomo(personas,conPareja):
    if(len(personas) > 1):
        aggPareja(personas[0],personas[1],conPareja)
        personas = personas[2:]
        return parejasHomo(personas,conPareja)
    else:
        return personas


def parejasHetero(personas1,personas2,conPareja):
    if((len(personas1) > 0) and (len(personas2) > 0)):
        aggPareja(personas1[0],personas2[0],conPareja)
        personas1=personas1[1:]
        personas2=personas2[1:]
        return parejasHetero(personas1,personas2,conPareja)
    else:
        return (personas1,personas2)

def homoConBi(hom,bi,conPareja):
    if((len(hom) == 1) and (len(bi)>0)):
        aggPareja(hom[0],bi[0],conPareja)
        hom=[]
        bi=bi[1:]
    return (hom,bi)

def sobrantes(sexualidad, sinPareja):
    for elem in sexualidad:
        for persona in elem:
            aggSinPareja(persona, "No hay parejas compatibles disponibles", sinPareja)

def matching(edadesCiudades, conPareja, sinPareja):
    i = 0
    for edad in edadesCiudades:
        for ciudad in edad:
            personas = edad[ciudad]
            sexualidad = separarSexo(personas)
            sexualidad[0] = parejasHomo(sexualidad[0], conPareja)
            sexualidad[3] = parejasHomo(sexualidad[3], conPareja)
            (sexualidad[1], sexualidad[4]) = parejasHetero(sexualidad[1], sexualidad[4], conPareja)
            (sexualidad[0], sexualidad[2]) = homoConBi(sexualidad[0], sexualidad[2], conPareja)
            (sexualidad[3], sexualidad[5]) = homoConBi(sexualidad[3], sexualidad[5], conPareja)
            if(len(sexualidad[1]) == 0):
                (sexualidad[4], sexualidad[2]) = parejasHetero(sexualidad[4] ,sexualidad[2] ,conPareja)
            else:
                (sexualidad[1], sexualidad[5]) = parejasHetero(sexualidad[1], sexualidad[5], conPareja)
            sexualidad[5] = parejasHomo(sexualidad[2] +sexualidad[5], conPareja)
            sexualidad[2] =  []
            sobrantes(sexualidad, sinPareja)
            print (i,ciudad, sexualidad)
            
        i+=1

def ingreso(nombreEntrada, nombreSalidaParejas, nombreSalidaSinParejas):
    archivo = open(nombreEntrada,"r")
    texto = archivo.read()
    archivo.close()
    renglon = texto.split("\n")
    personas = []
    for elem in renglon:
        datos = elem.split(", ")
        dictPersona = {"nombre" : datos[0], "apellido" : datos[1], "ciudad" : datos[2],
                       "edad" : int(datos[3]), "genero" : datos[4], "interes" : datos[5]}
        personas.append(dictPersona)
    filtrado(personas,nombreSalidaParejas, nombreSalidaSinParejas)

def filtrado(personas, nombreConParejas, nombreSinParejas):
    sinPareja = open(nombreSinParejas,"w")
    conPareja = open(nombreConParejas,"w")
    edades = [[],[],[]]
    for persona in personas:
        if(persona["interes"] == "N"):
            aggSinPareja(persona,"Asexual",sinPareja)
        elif(persona["edad"] < 11):
            aggSinPareja(persona,"Menor",sinPareja)
        elif(persona["edad"] < 15):
            edades[0].append(persona)
        elif(persona["edad"] < 18):
            edades[1].append(persona)
        else:
            edades[2].append(persona)
    edadesCiudades = []
    for elem in edades:
        edadCiudad = dict()
        for persona in elem:
            ciudad = persona["ciudad"]
            if(ciudad in edadCiudad):
                edadCiudad[ciudad]+=[persona]
            else:
                edadCiudad[ciudad] = [persona]
        edadesCiudades.append(edadCiudad)
    matching(edadesCiudades, conPareja, sinPareja)
