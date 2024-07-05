# Importar os módulos necessários
from super_image import EdsrModel, ImageLoader
from PIL import Image
import os
import shutil
import glob


# Criar um objeto da classe EdsrModel
model = EdsrModel.from_pretrained('eugenesiow/edsr-base', scale=2)

# Definir as pastas de origem e destino das imagens
origem = os.path.abspath("imagens")
destino = "imagens_upscaled"

shutil.rmtree("imagens_upscaled")
# Copiar toda a estrutura de pastas e arquivos da pasta de origem para a pasta de destino
shutil.copytree(origem, destino)

caminhos = []

def converter_para_webp(caminho_da_imagem, caminho_da_copia_webp):
    try:
        # Abrir a imagem original
        imagem_original = Image.open(caminho_da_imagem)

        # Salvar uma cópia em formato WebP
        imagem_original.save(caminho_da_copia_webp, 'webp')

        print(f"Cópia da imagem salva com sucesso em {caminho_da_copia_webp}")
    except Exception as e:
        print(f"Erro ao criar cópia da imagem: {e}")



# Definir uma função que converta as imagens de uma pasta e suas subpastas
def converter_imagens(pasta,caminhos):


# Usar a função os.walk para percorrer todos os arquivos e pastas da pasta atual
    for raiz, diretorios, arquivos in os.walk(pasta):
# Para cada arquivo na pasta atual
        for arquivo in arquivos:
# Obter o caminho completo do arquivo
            caminho = os.path.join(raiz, arquivo)
# Verificar se é uma imagem
            if arquivo.endswith((".jpg", ".png", ".bmp")):
# Usar um bloco try-except para capturar e tratar os possíveis erros ou exceções
                try:
# Abrir a imagem com o Pillow
                    imagem = Image.open(caminho)
# Converter a imagem para um array numpy
                    inputs = ImageLoader.load_image(imagem)
# Fazer o upscaling da imagem usando o modelo
                    preds = model(inputs)
# Salvar a imagem aumentada no mesmo caminho

                    ImageLoader.save_image(preds, caminho)
# Fechar a imagem original
                    imagem.close()


                    nome, ext = os.path.splitext(arquivo)

                    nome_arquivo=nome+ext

                    diretorio=caminho.replace(nome_arquivo,"")


# Padrão de busca para arquivos de imagem (pode ser ajustado conforme necessário)
                    padrao_busca = os.path.join(diretorio, '*.jpg')  # Substitua '.jpg' pela extensão desejada

# Lista de arquivos que correspondem ao padrão de busca
                    arquivos_de_imagem = glob.glob(padrao_busca)


                    for arquivo in arquivos_de_imagem:

                        print(arquivo)

                        if arquivo not in caminhos:

                            caminhos.append(caminho)
                            os.rename(arquivo, caminho)

                            converter_para_webp(caminho, diretorio+nome+".webp")


                except Exception as e:
# Imprimir o erro ou exceção que ocorreu
                    print(f"Erro ao converter a imagem {caminho}: {e}")

# Chamar a função para a pasta de destino
converter_imagens(destino,caminhos)



