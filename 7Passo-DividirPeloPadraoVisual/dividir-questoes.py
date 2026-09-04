from PIL import Image
import os

def encontrar_padrao_preto(imagem, cor_alvo=(0, 0, 0), tolerancia_cor=15, altura_alvo=41, margem_erro=5):
    """
    Encontra posições onde há uma sequência vertical contínua da cor preta
    nos dois primeiros pixels da esquerda (x=0 ou x=1), com altura entre 36 e 46 pixels.
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    
    posicoes_corte = []
    altura_minima = altura_alvo - margem_erro  # 36 pixels
    altura_maxima = altura_alvo + margem_erro  # 46 pixels
    
    y = 0
    while y < altura:
        # Mede a extensão vertical de pixels pretos a partir da posição y atual
        altura_encontrada = 0
        
        while (y + altura_encontrada) < altura:
            p0 = pixels[0, y + altura_encontrada][:3]
            p1 = pixels[1, y + altura_encontrada][:3]
            
            # Verifica se x=0 ou x=1 bate com a cor alvo (RGB 0,0,0) dentro da tolerância
            cor_p0_ok = all(abs(p0[i] - cor_alvo[i]) <= tolerancia_cor for i in range(3))
            cor_p1_ok = all(abs(p1[i] - cor_alvo[i]) <= tolerancia_cor for i in range(3))
            
            if cor_p0_ok or cor_p1_ok:
                altura_encontrada += 1
            else:
                break
        
        # Se a sequência vertical tiver altura dentro da margem (36 a 46 pixels)
        if altura_minima <= altura_encontrada <= altura_maxima:
            posicoes_corte.append(y)
            print(f"Padrão preto ({altura_encontrada}px) encontrado em y={y}")
            y += altura_encontrada  # Pula o bloco detectado
        else:
            y += 1
            
    return posicoes_corte

def dividir_imagem_por_faixas(caminho_imagem, pasta_saida):
    """
    Divide a imagem verticalmente nas posições onde o padrão preto foi encontrado.
    """
    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size
    
    print(f"Imagem carregada: {largura}x{altura} pixels")
    
    posicoes_corte = encontrar_padrao_preto(imagem)
    
    if not posicoes_corte:
        print("Nenhum padrão preto foi encontrado na imagem!")
        return
    
    print(f"Encontradas {len(posicoes_corte)} ocorrências do padrão para corte.")
    
    os.makedirs(pasta_saida, exist_ok=True)
    
    posicao_anterior = 0
    
    for i, posicao_corte in enumerate(posicoes_corte):
        if posicao_corte <= posicao_anterior:
            continue
            
        # Corta o bloco superior até o início do padrão encontrado
        area_corte = (0, posicao_anterior, largura, posicao_corte)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{i+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")
        
        posicao_anterior = posicao_corte
    
    # Corta a seção final restante
    if posicao_anterior < altura:
        area_corte = (0, posicao_anterior, largura, altura)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{len(posicoes_corte)+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")

if __name__ == "__main__":
    caminho_imagem = "./pg6-cortadas-sem-bordas/pagina_enem_6_esquerda.png"  # Substitua pelo caminho da imagem
    pasta_saida = "pg6E"          # Substitua pela pasta de destino
    
    dividir_imagem_por_faixas(caminho_imagem, pasta_saida)
    print("Divisão concluída!")