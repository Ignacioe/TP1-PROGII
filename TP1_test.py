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
    texto = open("parejasHomoTesting.txt")
    persona = eval(texto.read())

    assert parejasHomo([persona[0], persona[1], persona[2], persona[3]], conParejaTest) == []
    assert parejasHomo ([persona[0], persona[1], persona[2]], conParejaTest) == [persona[2]]

def test_parejasHetero():
    conParejaTest = open("conParejasTest.txt","w")
    texto = open("parejasHeteroTesting.txt")
    persona = eval(texto.read())

    assert parejasHetero([persona[0], persona[2], persona[4]], [persona[1], persona[3], persona[5]], conParejaTest) == ([], [])
    assert parejasHetero([persona[0], persona[2]], [persona[1], persona[3], persona[5]], conParejaTest) == ([], [persona[5]])
    assert parejasHetero([persona[0], persona[2], persona[4]], [], conParejaTest) == ([persona[0], persona[2], persona[4]], [])

def test_ingreso():
    ingreso("ingresoTesting.txt", "conParejaIngresoTesting.txt", "sinParejaIngresoTesting.txt")
    conParejaTesting = open("conParejaIngresoTesting.txt", "r")
    sinParejaTesting = open("sinParejaIngresoTesting.txt", "r")
    sinParejaTestingExpected = open("sinParejaTestingExpected.txt", "r")
    assert (conParejaTesting.read() == "")
    assert (sinParejaTesting.read() == sinParejaTestingExpected.read())
    conParejaTesting.close()
    sinParejaTesting.close()
