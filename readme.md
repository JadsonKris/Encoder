# Encoder
API deep learning as a service utilizando Tensorflow e fastAPI


# instalação:
1 sudo docker build -t api .
2 sudo docker run -i --network host api


# Rotas
'get': http://127.0.0.1:8000 retorna a mensagem "This is encoder API!".

'get': http://127.0.0.1:8000/image/ returna todas as imagens salvas em uma lista.

'get': http://127.0.0.1:8000/image/{id} retorna a imagem com o id escolhido no formato {image_input:"imagem convertida para base 64", image_output:"imagem convertida para base 64", ocr:"string", id:"int"}
se não tiver nenhuma imagem com o id enviado retorna erro 404.

'del': http://127.0.0.1:8000/image/{id} exclui a imagem do id enviado se não encontrar nenhuma imagem retorna erro 404.

'post': http://127.0.0.1:8000/image/ Recebe no request um json no formato {image_input:"imagem convertida para base 64"} e retorna {image_input:"imagem convertida para base 64", image_output:"imagem convertida para base 64", ocr:"string", id:"int"}
