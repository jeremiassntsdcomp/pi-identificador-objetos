from operator import concat
import sys

# aumenta limite para recursão
sys.setrecursionlimit(100000)


def getFile():
    image = ''
    print("\nInsira o arquivo para realizar a análise:")
    image = input()
    # abre arquivo da imagem
    file = open("examples/" + image, "r")
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

    return {"img": img, "lines": lines_size, "columns": columns_size}


def printImage(img):
    color = "\033[94m"
    end = "\033[0m"
    for line in img:
        # cor em valores maiores que 0
        newLine = list(map(lambda x: color + str(x) + end if x > 0 else str(x), line))
        print("".join(newLine))


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
        x -= 1
    elif case == 1:
        x -= 1
        y += 1
    elif case == 2:
        y += 1
    elif case == 3:
        x += 1
        y += 1
    elif case == 4:
        x += 1
    elif case == 5:
        x += 1
        y -= 1
    elif case == 6:
        y -= 1
    else:
        x -= 1
        y -= 1

    return (x, y)


def isValidPosition(img, ref_img, x, y, l, c):
    result = (
        x >= 0 and x < l and y >= 0 and y < c and img[x][y] > 0 and ref_img[x][y] == 0
    )
    return result


def growRegion(img, ref_img, x, y, l, c, id_object, cases):
    for case in cases:
        positions = getNextPosition(case, x, y)
        new_x = positions[0]
        new_y = positions[1]

        if isValidPosition(img, ref_img, new_x, new_y, l, c):
            ref_img[new_x][new_y] = id_object
            growRegion(img, ref_img, new_x, new_y, l, c, id_object, cases)


def generateComplement(comp_img, ref_img, id_object):
    for line in ref_img:
        columns = []
        for column in line:
            new_pixel = 1 if column != id_object else 0
            columns.append(new_pixel)
        comp_img.append(columns)


def sumImgs(img1, img2):
    img_result = []
    for i, line in enumerate(img1):
        columns = []
        for j, column in enumerate(line):
            result = 1 if column + img2[i][j] >= 1 else 0
            columns.append(result)
        img_result.append(columns)

    return img_result


def checkValueIsOnImage(img, value):
    for line in img:
        for column in line:
            if column == value:
                return True
    return False


def main():
    img_info = getImage()

    img = img_info["img"]
    l = img_info["lines"]
    c = img_info["columns"]
    # print("--------------- Imagem original ---------------")
    # printImage(img)

    n_bjects_with_hole = 0

    # preenche imagem de referência
    ref_img = createImage(l, c, 0)
    # define identificador do objeto
    id_object = 0
    # busca sementes
    for i, line in enumerate(img):
        for j, column in enumerate(line):
            if column > 0 and ref_img[i][j] == 0:
                id_object += 1
                # achou semente, inicia crescimento por região
                # utiliza objeto estruturante quadrado 3 x 3
                cases = [0, 1, 2, 3, 4, 5, 6, 7]
                ref_img[i][j] = id_object
                growRegion(img, ref_img, i, j, l, c, id_object, cases)
                # define complemento apenas do objeto criado
                comp_img = []
                generateComplement(comp_img, ref_img, id_object)
                # aplica segmentação por crescimento de região para mapear a parte externa do objeto
                # utiliza objeto estruturante cruz 3 x 3
                cases = [0, 2, 4, 6]
                comp_ref_img = createImage(l, c, 0)
                growRegion(comp_img, comp_ref_img, 0, 0, l, c, 1, cases)
                # obtém imagem original apenas com objeto analisado
                obj_img = []
                generateComplement(obj_img, comp_img, 1)
                # soma imagem de objeto original com imagem com exterior segmentado sobrando apenas buracos
                only_holes_img = sumImgs(obj_img, comp_ref_img)
                # verifica se na imagem resultante restou algum 0, que será buraco
                has_hole = checkValueIsOnImage(only_holes_img, 0)
                if has_hole:
                    n_bjects_with_hole += 1

    # print("--------------- Imagem com objetos mapeados ---------------")
    # printImage(ref_img)
    print("Objetos encontrados: " + str(id_object))
    print("Objetos encontrados com buracos: " + str(n_bjects_with_hole))
    print("Objetos encontrados sem buracos: " + str(id_object - n_bjects_with_hole))


main()
