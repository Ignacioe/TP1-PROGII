from TP1 import *

def test_lenGt():
    assert lenGt([1, 2, 3, 4], 2) == True
    assert lenGt([], 1) == False
    assert lenGt([1, 2, 3, 4], 5) == False

def test_filterEdad():
    sinParejaTest = open("sinParejaEdadTesting.txt","w") 
    texto = open("edadciudadsexoTesting.txt")
    persona = eval(texto.read())

    assert filterEdad([persona[0], persona[1], persona[2], persona[3], persona[4], persona[5], persona[6]], sinParejaTest) == [[persona[2]], [persona[4], persona[5]], [persona[0], persona[1], persona[6]]]

def test_filterCiudad():
    sinParejaTest = open("sinParejaEdadTesting.txt","w") 
    texto = open("edadciudadsexoTesting.txt")
    persona = eval(texto.read())

    assert filterCiudad([[persona[2], persona[3]],
                         [persona[4], persona[5]],
                         [persona[0], persona[1], persona[6]]]) == [{"SANTA ANA": [persona[2]], "SAN PABLO": [persona[3]]},
                                                                    {"SAN PABLO": [persona[4]], "SANTA ANA": [persona[5]]},
                                                                    {"SANTA ANA": [persona[0]], "GOICOECHEA": [persona[1], persona[6]]}]

def test_separarSexo():
    sinParejaTest = open("sinParejaEdadTesting.txt","w") 
    texto = open("edadciudadsexoTesting.txt")
    persona = eval(texto.read())

    assert separarSexo([persona[2]]) == [[], [], [], [persona[2]], [], []]
    assert separarSexo([persona[3]]) == [[], [], [persona[3]], [], [], []]
    assert separarSexo([persona[4]]) == [[persona[4]], [], [], [], [], []]
    assert separarSexo([persona[5]]) == [[], [persona[5]], [], [], [], []]
    assert separarSexo([persona[0]]) == [[], [], [persona[0]], [], [], []]
    assert separarSexo([persona[1], persona[6]]) == [[], [], [], [], [persona[1], persona[6]], []]
    assert separarSexo([persona[0], persona[1], persona[2], persona[3], persona[4], persona[5], persona[6]]) == [[persona[4]],
                                                                                                                 [persona[5]],
                                                                                                                 [persona[0], persona[3]],
                                                                                                                 [persona[2]],
                                                                                                                 [persona[1], persona[6]],
                                                                                                                 []]

def test_parejasHomo():
    conParejaTest = open("conParejasTest.txt","w") 
    persona1 = {
        "nombre": "JOSE",
        "apellido": "DELGADO",
        "ciudad": "SANTA ANA",
        "edad": 52,
        "genero": "M",
        "interes": "M"
    }
    persona2 = {
        "nombre": "JOSE FRANCISCO",
        "apellido": "DUARTE",
        "ciudad": "SANTA ANA",
        "edad": 70,
        "genero": "M",
        "interes": "M"
    }
    persona3 = {
        "nombre": "RECAREDO",
        "apellido": "MURILLO",
        "ciudad": "SANTA ANA",
        "edad": 40,
        "genero": "M",
        "interes": "M"
    }
    persona4 = {
        "nombre": "ELIAS",
        "apellido": "ROJAS",
        "ciudad": "SANTA ANA",
        "edad": 20,
        "genero": "M",
        "interes": "M"
    }
    
    assert parejasHomo([persona1, persona2, persona3, persona4], conParejaTest) == []
    assert parejasHomo ([persona1, persona2, persona3], conParejaTest) == [persona3]

def test_parejasHetero():
    conParejaTest = open("conParejasTest.txt","w")
    persona1 = {
        "nombre": "JOSE",
        "apellido": "DELGADO",
        "ciudad": "SANTA ANA",
        "edad": 52,
        "genero": "M",
        "interes": "F"
    }
    persona2 = {
        "nombre": "CARMEN",
        "apellido": "CORRALES",
        "ciudad": "SANTA ANA",
        "edad": 32,
        "genero": "F",
        "interes": "M"
    }
    persona3 = {
        "nombre": "ALEJANDRO",
        "apellido": "ARAYA",
        "ciudad": "SANTA ANA",
        "edad": 42,
        "genero": "M",
        "interes": "F"
    }
    persona4 = {
        "nombre": "OFELIA",
        "apellido": "AVALOS",
        "ciudad": "SANTA ANA",
        "edad": 47,
        "genero": "F",
        "interes": "M"
    }
    persona5 = {
        "nombre": "VIDAL",
        "apellido": "POAS",
        "ciudad": "SANTA ANA",
        "edad": 19,
        "genero": "M",
        "interes": "F"
    }
    persona6 = {
        "nombre": "FLORA",
        "apellido": "ESTRADA",
        "ciudad": "SANTA ANA",
        "edad": 32,
        "genero": "F",
        "interes": "M"
    }

    assert parejasHetero([persona1, persona3, persona5], [persona2, persona4, persona6], conParejaTest) == ([], [])
    assert parejasHetero([persona1, persona3], [persona2, persona4, persona6], conParejaTest) == ([], [persona6])
    assert parejasHetero([persona1, persona3, persona5], [], conParejaTest) == ([persona1, persona3, persona5], [])

def test_ingreso():
    ingreso("ingresoTesting.txt", "conParejaIngresoTesting.txt", "sinParejaIngresoTesting.txt")
    conParejaTesting = open("conParejaIngresoTesting.txt", "r")
    sinParejaTesting = open("sinParejaIngresoTesting.txt", "r")
    assert (conParejaTesting.read() == "")
    assert (sinParejaTesting.read() == """Pablo, Antuna, Rosario, 20, M, F - No hay parejas compatibles disponibles
Lucas, Bachur, Rosario, 20, M, F - No hay parejas compatibles disponibles
Nahuel, Blando, Rosario, 20, M, F - No hay parejas compatibles disponibles
Tomas, Castro, Rosario, 20, M, F - No hay parejas compatibles disponibles
Blas, Barbagelata, Rosario, 20, M, F - No hay parejas compatibles disponibles
Lautaro, Garavano, Rosario, 20, M, F - No hay parejas compatibles disponibles
Lautaro, Cerruti, Rosario, 20, M, F - No hay parejas compatibles disponibles
Giuliano, Regolo, Rosario, 20, M, F - No hay parejas compatibles disponibles
Alesandro, Regolo, Rosario, 20, M, F - No hay parejas compatibles disponibles
Tomas, Scalbi, Rosario, 20, M, F - No hay parejas compatibles disponibles
""")
    conParejaTesting.close()
    nParejaTesting.close()
