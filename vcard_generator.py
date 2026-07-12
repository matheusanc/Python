pip install qrcode[pil]

import qrcode

def generate_vcard_qr(data, filename="meu_contato.png"):
    """
    Gera um QR Code contendo um vCard (formato padrão de contatos).
    """
    # Formatação do padrão vCard 3.0
    vcard = (
        f"BEGIN:VCARD\n"
        f"VERSION:3.0\n"
        f"FN:{data['nome']}\n"
        f"ORG:{data['empresa']}\n"
        f"TEL;TYPE=CELL:{data['telefone']}\n"
        f"EMAIL:{data['email']}\n"
        f"URL:{data['github']}\n"
        f"URL;TYPE=LinkedIn:{data['linkedin']}\n"
        f"END:VCARD"
    )

    # Configuração do QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(vcard)
    qr.make(fit=True)

    # Criação da imagem
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print(f"✅ QR Code gerado com sucesso: {filename}")

if __name__ == "__main__":
    print("--- Gerador de Cartão de Visita Digital ---")
    
    meus_dados = {
        "nome": "Seu Nome Completo",
        "empresa": "Desenvolvedor Full Stack",
        "telefone": "+5561999999999", # Exemplo com DDD de Brasília
        "email": "seuemail@exemplo.com",
        "github": "https://github.com/seuusuario",
        "linkedin": "https://linkedin.com/in/seuusuario"
    }

    generate_vcard_qr(meus_dados)
