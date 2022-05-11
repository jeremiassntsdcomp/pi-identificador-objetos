print("------ Sistema de verificação de produtos com defeito ------\n")
# define o exemplo que será verificado
option = 0
exemplos = 1
while option < 1 or option > exemplos:
    print("Opções disponíveis:")
    for i in range(0, exemplos):
        index = str(i + 1)
        print("Exemplo " + index)
    print("\nDigite o número do exemplo que deseja verificar: ")
    option = int(input())
# abre arquivo da imagem
file = open("examples/example" + str(option) + ".pbm", "r")
# define tamanho da imagem
for i in range(0, 3):
    line = file.readline()
    if i == 2:
        sizes = line.split(" ")
        n = int(sizes[0])
        m = int(sizes[1])
# define imagem
img = [[0 for _ in range(n)] for _ in range(m)]
for i in range(0, m):
    elements = file.readline().split(" ")
    columns = list(map(lambda x: int(x), elements))
    img[i] = columns