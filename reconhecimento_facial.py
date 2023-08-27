import cv2
import face_recognition as fr
import pickle
import shutil
import os

# Verifica se o  a pasta das imagens não existe e, se não existir, cria-lá.
if not os.path.exists("imagensRostos"):
    os.makedirs("imagensRostos")


def cadastro_rosto(nome,diretorio_imagem):
    imgRosto = fr.load_image_file(f"{diretorio_imagem}")
    imgRosto = cv2.cvtColor(imgRosto, cv2.COLOR_BGR2RGB) #convertendo as cores para que fiquem com a cor original

    rosto_encode = fr.face_encodings(imgRosto)

    if len(rosto_encode) ==  0:
        return 0 ## não existem rostos na imagem
    else:
        if verificar_existencia_do_rosto(rosto_encode) == True: # rosto ja existe
            return 2
        elif verificar_existencia_do_nome(nome) == True:  #nome já existe
            return 3
        else :

            #criando dicionario para guardar o encode e o nome associado ao rosto
            rosto_dicionario ={"nome": nome, "encode":rosto_encode[0] }

            #buscar o arquivo de dados
            try:
                with open("encodes.pkl","rb") as arquivo:
                    dados_existentes = pickle.load(arquivo)
            except FileNotFoundError:
                dados_existentes=[]

            dados_existentes.append(rosto_dicionario)

            with open("encodes.pkl","wb") as arquivo:
                pickle.dump(dados_existentes,arquivo)

            partes = diretorio_imagem.split("\\")  # Divide a string usando a barra invertida como separador
            nome_arquivo = partes[-1]  # Pega o último item da lista resultante

            print(f"A face de {nome} foi salva")

            #copiando a imagem para ter salva no diretório que irá ser utilizaod para mostrar os rostos conhecidos

            destino = "imagensRostos"
            shutil.copy(diretorio_imagem,destino)

            destino_completo = os.path.join(destino, nome_arquivo)
            shutil.copy(diretorio_imagem, destino_completo)
            novo_nome = os.path.join(destino, nome + ".jpg")
            os.rename(destino_completo, novo_nome)

            return 1 # Rosto cadastrado com sucesso



def verificar_existencia_do_rosto(encode_Rosto):
    try:
        with open("encodes.pkl","rb") as arquivo:
            dados_existentes = pickle.load(arquivo)
    except FileNotFoundError:
        dados_existentes =[]

    # veficando se o rosto está na lista de encodes cadastrados

    for item in dados_existentes:
        encode_cadastrado = item['encode']
        comparacao = fr.compare_faces(encode_cadastrado,encode_Rosto)
        if comparacao[0]:
            return True

    return False

def verificar_existencia_do_nome(nome_Rosto):
    try:
        with open("encodes.pkl","rb") as arquivo:
            dados_existentes = pickle.load(arquivo)
    except FileNotFoundError:
        dados_existentes =[]

    # veficando se o rosto está na lista de encodes cadastrados

    for item in dados_existentes:
        nome_Cadastrado = item['nome']
        if nome_Cadastrado == nome_Rosto:
            return True

    return False


def buscar_pessoa_por_encode(encode_Rosto):
    try:
        with open("encodes.pkl", "rb") as arquivo:
            dados_existentes = pickle.load(arquivo)
    except FileNotFoundError:
        dados_existentes = []



    for item in dados_existentes:
        encode_cadastrado = item['encode']
        comparacao = fr.compare_faces(encode_cadastrado, encode_Rosto)
        if comparacao[0]:
            return item['nome'], item['encode']

    return "Rosto desconhecido", "0"

def buscar_todos_nomes():
    try:
        with open("encodes.pkl", "rb") as arquivo:
            dados_existentes = pickle.load(arquivo)
    except FileNotFoundError:
        dados_existentes = []
    nomes_cadastrados = []
    for item in dados_existentes:
       nomes_cadastrados.append(item['nome'])

    return nomes_cadastrados


def abrir_camera():
    import cv2
    import pickle
    import face_recognition as fr

    # Carregar os dados de encodes e nomes do arquivo pkl
    with open('encodes.pkl', 'rb') as f:
        dados = pickle.load(f)

    encodes = [item['encode'] for item in dados]
    nomes = [item['nome'] for item in dados]

    # Inicializar a câmera
    camera = cv2.VideoCapture(0)

    while True:
        ret, frame = camera.read()

        #buscando
        face_loc = fr.face_locations(frame)
        face_encode= fr.face_encodings(frame, face_loc)


        for face_location, face_encoding in zip(face_loc,face_encode):

            matches = fr.compare_faces(encodes, face_encoding)

            nome = "Desconhecido"


            if True in matches: #se for verdadeiro, assumo um index para usar dentro da lista nomes
                matched_idx = matches.index(True)
                nome= nomes[matched_idx]

            top, right, bottom, left = face_location


            cv2.putText(frame, nome (left, bottom + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

        cv2.imshow('Camera (Para finalizar, aperte a letra Q)', frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Liberar recursos
    camera.release()
    cv2.destroyAllWindows()
