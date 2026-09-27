# Exemplo 1
def main():
    # Ler o conteúdo de um arquivo de texto
    # chamado plants.txt em uma lista.
    text_list = read_list("plants.txt")
    # Imprimir a lista inteira.
    print(text_list)

def read_list(filename):
    """Ler o conteúdo de um arquivo de texto em uma lista e
    retornar a lista. Cada elemento da lista conterá
    uma linha de texto do arquivo.
    Parâmetro filename: o nome do arquivo de texto a ser lido
    Retorno: uma lista de strings
    """
    # Criar uma lista vazia que armazenará
    # as linhas de texto do arquivo.
    text_list = []
    # Abrir o arquivo de texto para leitura e armazenar uma referência
    # ao arquivo aberto em uma variável chamada text_file.
    with open(filename, "rt") as text_file:
        # Ler o conteúdo do arquivo
        # uma linha por vez.
        for line in text_file:
            # Remover espaços em branco, se houver,
            # do início e do fim da linha.
            clean_line = line.strip()
            # Adicionar a linha limpa de texto
            # ao final da lista.
            text_list.append(clean_line)
    # Retornar a lista que contém as linhas de texto.
    return text_list

# Chamar main para iniciar este programa.
if __name__ == "__main__":
    main()
