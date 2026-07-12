from PIL import Image

def text_to_bin(text):
    """Converte texto para uma sequência binária."""
    return ''.join(format(ord(i), '08b') for i in text)

def encode_image(image_path, secret_text, output_path):
    """Esconde o texto nos bits menos significativos (LSB) da imagem."""
    img = Image.open(image_path)
    binary_secret = text_to_bin(secret_text) + '1111111111111110' # Delimitador de fim
    
    pixels = list(img.getdata())
    new_pixels = []
    bit_idx = 0

    for pixel in pixels:
        if bit_idx < len(binary_secret):
            # Modifica o bit menos significativo do canal Vermelho (R)
            new_r = (pixel[0] & ~1) | int(binary_secret[bit_idx])
            new_pixels.append((new_r, pixel[1], pixel[2]))
            bit_idx += 1
        else:
            new_pixels.append(pixel)

    img.putdata(new_pixels)
    img.save(output_path, "PNG")
    print(f"Mensagem escondida com sucesso em: {output_path}")

def decode_image(image_path):
    """Extrai a mensagem escondida de uma imagem PNG."""
    img = Image.open(image_path)
    pixels = list(img.getdata())
    
    binary_data = ""
    for pixel in pixels:
        binary_data += str(pixel[0] & 1)

    # Divide em bytes e converte para caracteres até encontrar o delimitador
    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    decoded_text = ""
    for byte in all_bytes:
        char = chr(int(byte, 2))
        decoded_text += char
        if decoded_text.endswith('þ'): # Nosso delimitador simplificado
            break
            
    return decoded_text[:-1]

if __name__ == "__main__":
    # Exemplo de uso:
    # encode_image("input.png", "Minha mensagem ultra secreta!", "secret.png")
    # print(decode_image("secret.png"))
    print("Use as funções encode_image e decode_image para testar!")
