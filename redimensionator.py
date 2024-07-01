import logging
from PIL import Image, ImageOps
import os

# Configuração de logging
logging.basicConfig(filename='image_processing.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def resize_and_center_image(input_path, output_path, new_size=(1200, 1200), product_ratio=0.65):
    try:
        # Verificar se o arquivo é uma imagem
        if not input_path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            logging.warning(f'Arquivo ignorado (extensão não suportada): {input_path}')
            return
        
        # Abra a imagem original
        original_image = Image.open(input_path)
        original_width, original_height = original_image.size

        # Calcule o novo tamanho da imagem do produto
        new_product_width = int(new_size[0] * product_ratio)
        new_product_height = int((new_product_width / original_width) * original_height)

        # Redimensione a imagem do produto mantendo a proporção
        resized_image = original_image.resize((new_product_width, new_product_height), Image.LANCZOS)

        # Crie uma nova imagem branca com o tamanho especificado
        new_image = Image.new("RGB", new_size, (255, 255, 255))

        # Calcule as coordenadas para centralizar a imagem do produto
        x_offset = (new_size[0] - new_product_width) // 2
        y_offset = (new_size[1] - new_product_height) // 2

        # Cole a imagem do produto no fundo branco
        new_image.paste(resized_image, (x_offset, y_offset))

        # Salve a nova imagem
        new_image.save(output_path)
        logging.info(f'Imagem processada com sucesso: {output_path}')

    except Exception as e:
        logging.error(f'Erro ao processar o arquivo {input_path}: {e}')

def resize_image(input_path, output_path, new_size=(1200, 1200)):
    try:
        # Verificar se o arquivo é uma imagem
        if not input_path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            logging.warning(f'Arquivo ignorado (extensão não suportada): {input_path}')
            return
        
        # Abra a imagem original
        original_image = Image.open(input_path)

        # Redimensione a imagem mantendo a proporção
        resized_image = original_image.resize(new_size, Image.LANCZOS)

        # Salve a nova imagem redimensionada
        resized_image.save(output_path)
        logging.info(f'Imagem redimensionada com sucesso: {output_path}')

    except Exception as e:
        logging.error(f'Erro ao redimensionar o arquivo {input_path}: {e}')

def smart_resize_image(input_path, output_path, new_size=(1200, 1200), product_ratio=0.65):
    try:
        # Verificar se o arquivo é uma imagem
        if not input_path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            logging.warning(f'Arquivo ignorado (extensão não suportada): {input_path}')
            return
        
        # Abra a imagem original
        original_image = Image.open(input_path)
        original_width, original_height = original_image.size

        # Decidir qual função usar com base no tamanho da imagem
        if original_width < new_size[0] and original_height < new_size[1]:
            logging.info(f'Usando resize_and_center_image para: {input_path}')
            resize_and_center_image(input_path, output_path, new_size, product_ratio)
        else:
            logging.info(f'Usando resize_image para: {input_path}')
            resize_image(input_path, output_path, new_size)
    except Exception as e:
        logging.error(f'Erro ao processar o arquivo {input_path} na smart_resize_image: {e}')

# Crie a pasta de saída principal se não existir
output_base_folder = "resized-images"
if not os.path.exists(output_base_folder):
    os.makedirs(output_base_folder)

# 
main_folder = "images"
if not os.path.exists(main_folder):
    os.makedirs(main_folder)

while True:
    option = input(
    """
    [1] Adicionar fundo branco 1200x1200
    [2] Redimensionar imagens 1200x1200
    [3] Smart Resize
    [Q] Sair
    Escolha uma opção: """
    ).strip().upper()

    if option == '1':
        logging.info('Opção selecionada: Adicionar fundo branco 1200x1200')
        for folder in os.listdir("images"):
            subfolder_path = os.path.join("images", folder)

            # Verificar se é uma pasta
            if os.path.isdir(subfolder_path):
                logging.info(f'Entrando na pasta: {subfolder_path}')
                
                # Loop pela subpasta
                for file in os.listdir(subfolder_path):
                    file_path = os.path.join(subfolder_path, file)
                    
                    # Verificar se é um arquivo
                    if os.path.isfile(file_path):
                        logging.info(f'Arquivo encontrado: {file_path}')
                        # Crie a pasta de saída para a subpasta se não existir
                        resized_folder = os.path.join(output_base_folder, os.path.basename(subfolder_path))
                        if not os.path.exists(resized_folder):
                            os.makedirs(resized_folder)
                        
                        # Gerar o caminho completo para o arquivo de saída
                        output_path = os.path.join(resized_folder, file)
                        
                        resize_and_center_image(file_path, output_path)

    elif option == '2':
        logging.info('Opção selecionada: Redimensionar imagens 1200x1200')
        for folder in os.listdir("images"):
            subfolder_path = os.path.join("images", folder)

            # Verificar se é uma pasta
            if os.path.isdir(subfolder_path):
                logging.info(f'Entrando na pasta: {subfolder_path}')
                
                # Loop pela subpasta
                for file in os.listdir(subfolder_path):
                    file_path = os.path.join(subfolder_path, file)
                    
                    # Verificar se é um arquivo
                    if os.path.isfile(file_path):
                        logging.info(f'Arquivo encontrado: {file_path}')
                        # Crie a pasta de saída para a subpasta se não existir
                        resized_folder = os.path.join(output_base_folder, os.path.basename(subfolder_path))
                        if not os.path.exists(resized_folder):
                            os.makedirs(resized_folder)
                        
                        # Gerar o caminho completo para o arquivo de saída
                        output_path = os.path.join(resized_folder, file)
                        
                        resize_image(file_path, output_path)

    elif option == '3':
        logging.info('Opção selecionada: Smart Resize')
        for folder in os.listdir("images"):
            subfolder_path = os.path.join("images", folder)

            # Verificar se é uma pasta
            if os.path.isdir(subfolder_path):
                logging.info(f'Entrando na pasta: {subfolder_path}')
                
                # Loop pela subpasta
                for file in os.listdir(subfolder_path):
                    file_path = os.path.join(subfolder_path, file)
                    
                    # Verificar se é um arquivo
                    if os.path.isfile(file_path):
                        logging.info(f'Arquivo encontrado: {file_path}')
                        # Crie a pasta de saída para a subpasta se não existir
                        resized_folder = os.path.join(output_base_folder, os.path.basename(subfolder_path))
                        if not os.path.exists(resized_folder):
                            os.makedirs(resized_folder)
                        
                        # Gerar o caminho completo para o arquivo de saída
                        output_path = os.path.join(resized_folder, file)
                        
                        smart_resize_image(file_path, output_path)

    elif option == 'Q':
        logging.info('Saindo do programa')
        break

    else:
        print("Opção inválida. Escolha novamente.")
