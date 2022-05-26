from operator import concat

def getFile():
    # define o exemplo que será verificado
    option = 0
    exemplos = 3
    while option < 1 or option > exemplos:
        print("Opções disponíveis:")
        for i in range(0, exemplos):
            index = str(i + 1)
            print("Exemplo " + index)
        print("\nDigite o número do exemplo que deseja verificar: ")
        option = int(input())
    # abre arquivo da imagem
    file = open("examples/example" + str(option) + ".pbm", "r")
    return file

def getImage():
    # busca arquivo de imagem
    file = getFile()
    lines = file.readlines()
    # define tamanho da imagem
    line = lines[2]
    sizes = line.split(" ")
    columns_size = int(sizes[0])
    lines_size = int(sizes[1])
    # salva pixels
    pixels = []
    for i, line in enumerate(lines):
        if i > 2:
            filtered = list(filter(lambda x: x != " " and x != "\n", list(line)))
            mapped = list(map(lambda x: int(x), filtered))
            pixels = concat(pixels, mapped)
    # define imagem
    img = []
    for i in range(0, lines_size):
        start = i * columns_size
        end = start + columns_size
        columns = pixels[start:end]
        img.append(columns)
    
    return {
        "img": img,
        "lines": lines_size,
        "columns": columns_size
    }

def printImage(img):
    for line in img:
        newLine = list(map(lambda x: str(x), line))
        print(''.join(newLine))

def createImage(l, c, value):
    img = []
    for i in range(0, l):
        columns = []
        for j in range(0, c):
            columns.append(value)
        img.append(columns)
    
    return img

def getNextPosition(case, x, y):
    if case == 0:
        x-=1
    elif case == 1:
        y+=1
    elif case == 2:
        x+=1
    else:
        y-=1
    
    return (x, y)

def isValidPosition(img, ref_img, x, y, l, c):
    result = x >= 0 and x < l and y >= 0 and y < c and img[x][y] > 0 and ref_img[x][y] == 0
    return result

def growRegion(img, ref_img, x, y, l, c, id_object):
    cases = [0, 1, 2, 3]
    for case in cases:
        positions = getNextPosition(case, x, y)
        new_x = positions[0]
        new_y = positions[1]

        if isValidPosition(img, ref_img, new_x, new_y, l, c):
            ref_img[new_x][new_y] = id_object
            growRegion(img, ref_img, new_x, new_y, l, c, id_object)

def main():
    print("------ Sistema de verificação de produtos com defeito ------\n")
    img_info = getImage()

    img = img_info["img"]
    l = img_info["lines"]
    c = img_info["columns"]
    print("--------------- Imagem original ---------------")
    printImage(img)
    
    nObjectsWithHole = 0

    # preenche imagem de referência
    ref_img = createImage(l, c, 0)
    # define identificador do objeto
    id_object = 0
    # busca sementes
    for i, line in enumerate(img):
        for j, column in enumerate(line):
            if column > 0 and ref_img[i][j] == 0:
                id_object+=1
                # achou semente, inicia crescimento por região
                ref_img[i][j] = id_object
                growRegion(img, ref_img, i, j, l, c, id_object)
                # print("--------------- Objeto encontrado ---------------")
                # printImage(ref_img)

    print("--------------- Imagem com objetos mapeados ---------------")
    printImage(ref_img)
    print("Objetos encontrados: " + str(id_object))
    print("Objetos encontrados com buracos: " + str(nObjectsWithHole))

main()