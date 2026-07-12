import PIL.Image

# Caracteres usados para representar diferentes níveis de cinza (do mais escuro ao mais claro)
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio * 0.5)  # Ajuste de proporção para o caractere
    return image.resize((new_width, new_height))

def grayify(image):
    return image.convert("L")

def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
    return characters

def main(new_width=100):
    path = input("Insira o caminho da imagem (ex: foto.jpg): ")
    try:
        image = PIL.Image.open(path)
    except Exception as e:
        print(f"Erro ao abrir imagem: {e}")
        return

    # Processamento
    new_image_data = pixels_to_ascii(grayify(resize_image(image, new_width)))
    
    # Formatação do output
    pixel_count = len(new_image_data)
    ascii_image = "\n".join([new_image_data[index:(index + new_width)] for index in range(0, pixel_count, new_width)])
    
    print(ascii_image)

    # Salva o resultado em um arquivo de texto
    with open("ascii_art.txt", "w") as f:
        f.write(ascii_image)

if __name__ == "__main__":
    main()
