import os

"""Diccionario que la llave sera la estacion y el contenido rutas y distance a las estaciones"""
stops = {} #contiene nombres de las rutas y distancias de cada una
routesS = {} #contiene rutas con sus respectivos numeros

def openDB():
    """Try y except   sirven para detectar la base de datos, si no existe manda un mensaje
    y se cierra el programa, sin la base de datos el programa no funciona"""
    try:
        file = open('BD.txt', 'r')
    except:
        print ('No se encontro la base de datos')
        exit()

    """Este for sirve para recorrer cada una de la lineas de el archivo"""
    for line in file:
        """Se va almacenar la parada"""
        stop = []

        """Se va almacenar las rutas en las que se encuentra la estacion"""
        routes = []

        """Se va a contener la lista 'distance'"""
        next = {}

        """Contiene las siguientes paradas y la distance"""
        distance = []

        """Este auxiliar contendra la cadena"""
        aux = ""

        """Este auxiliar contendra el numero de columna"""
        auxNum = 0

        """Este for sirve para recorrer letra por letra"""
        for x in range(0, len(line)):
            """Al momento de encotrar ':' se cortara y almacenara"""
            if line[x] == ':':
                x += 1
                """"Dependiendo de la posicion lo almacenara en cierta lista"""
                if auxNum == 0:
                    stop.append(aux.upper())
                elif auxNum < 10:
                    if aux != '':
                        routes.append(aux)
                else:
                    if auxNum % 2 == 1:
                        distance.append(int(aux))
                        next[distance[0]] = distance[1]
                        distance = []
                        aux = ""
                        auxNum += 1
                        continue
                    distance.append(aux.upper())
                aux = ""
                auxNum += 1
                continue
            aux += line[x]

        """Ya teniendo las listas completas de la estacion, se añaden al diccionario"""
        stops[stop[0]] = next
        routesS[stop[0]] = routes

def MetodoDijkstra(stops,f,t):
    visit, distance, dad = {}, {}, {}
    ordenada = []
    for aux in stops:
        visit[aux] = False
        distance[aux] = float('inf')
        dad[aux] = ''
    distance[f] = 0
    aux = f
    while aux != t and visit[aux] is False:
        visit[aux] = True
        ady = stops[aux]
        for q, peso in ady.items():
            if distance[q] > distance[aux]+peso:
                distance[q] = distance[aux]+peso
                dad[q] = aux
        aux = min((a for a in stops if visit[a] is False), key=lambda a:distance[a])
        ordenada = distance.items()
        ordenada = [(a,b) for b,a in ordenada]
        ordenada.sort()
        ordenada = [(a,b) for b,a in ordenada]

    if dad[t]:
        camino = [t]
        aux = t
        while aux != f:
            camino.append(dad[aux])
            aux = dad[aux]
        extraido = camino[0]
        for a,b in ordenada:
            if extraido == a:
                peso = b
        return camino
    else:
        return None

def printR(g):
    printString = ""
    printRoute = ""
    for j in routesS[g[0]]:
        if j in routesS[g[len(g)-1]]:
            printRoute += j +','
    print('\n=============================')
    if printRoute == "":
        trans = checkRoute(g).keys()
        for x in trans:
            print('USAR RUTA ', checkRoute(g)[x], 'HASTA LA ESTACION ', x, 'TRANSBORDAR')
    else:
        print(' LA RUTA MAS CORTA:' + printRoute)
    print('=============================\n')
    for i in reversed(g):
        printString = i
        printString += ':'
        for j in routesS[i]:
            printString += '  Ruta '
            printString += j
        print(printString)

def checkRoute(g):
    same = []
    notSame = []
    trans = {}
    for x in routesS[g[len(g)-1]]:
        same.append(x)

    for i in range(len(g)-1, -1, -1):
        for j in same:
            if j not in routesS[g[i-1]]:
                notSame.append(j)
        for k in notSame:
            same.remove(k)
        if len(same) == 0:
            for j in routesS[g[i]]:
                if j in routesS[g[i-1]]:
                    same.append(j)
            trans[g[i]] = notSame
        notSame = []
    return trans

def start():
    openDB()
    f = input('Ingresa la parada donde estas: ').upper()
    while f not in stops:
        print('ERROR: Esta estacion no existe')
        f = input('Ingresa la parada donde estas: ').upper()

    t = input('Ingresa la parada de destino: ').upper()
    if f == t:
        t = ''
    while t.upper() not in stops:
        print('ERROR: Ingresa nuevamente la estacion')
        t = input('Ingresa la parada de destino: ').upper()
        if f == t:
            y = ''

    g = MetodoDijkstra(stops,f, t)
    printR(g)

x = ''
while x != 'E':
    os.system("PUMABUS.jpeg")
    os.system("cls")
    print('================================================================')
    start()
    x = input('Ingresa la letra "E" para salir o enter para reiniciar: ').upper()
