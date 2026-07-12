import colorsys

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def generate_palettes(hex_base):
    # Converte HEX para RGB (escala 0-255) e depois para HLS (escala 0-1)
    rgb = hex_to_rgb(hex_base)
    h, l, s = colorsys.rgb_to_hls(rgb[0]/255, rgb[1]/255, rgb[2]/255)

    palettes = {
        "Monocromático": [(h, max(0, l-0.2), s), (h, l, s), (h, min(1, l+0.2), s)],
        "Análogo": [((h-0.05)%1, l, s), (h, l, s), ((h+0.05)%1, l, s)],
        "Complementar": [(h, l, s), ((h+0.5)%1, l, s)],
        "Triádico": [(h, l, s), ((h+1/3)%1, l, s), ((h+2/3)%1, l, s)]
    }

    print(f"--- Paletas para a cor base: {hex_base} ---")
    for name, colors in palettes.items():
        hex_colors = [rgb_to_hex([c*255 for c in colorsys.hls_to_rgb(*c)]) for c in colors]
        print(f"{name}: {' | '.join(hex_colors)}")

if __name__ == "__main__":
    cor_usuario = input("Digite uma cor HEX (ex: #3498db): ") or "#3498db"
    generate_palettes(cor_usuario)
