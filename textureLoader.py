from OpenGL.GL import glGenTextures, glBindTexture, glTexParameteri, glTexImage2D,\
    GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_TEXTURE_MAG_FILTER, GL_NEAREST, GL_RGB,\
    GL_RGBA, GL_UNSIGNED_BYTE

class TextureLoader(object):

    @staticmethod
    def load_texture(path):
        import pygame
        #Cargo la imagen a memoria. pygame se hace cargo de decodificarla correctamente
        surf = pygame.image.load(path)
        surf = pygame.transform.flip(surf, False, True)
        #Obtengo la matriz de colores de la imagen en forma de un array binario
        #Le indico el formato en que quiero almacenar los datos (RGBA) y que invierta la matriz, para poder usarla correctamente con OpenGL
        image = pygame.image.tostring(surf, 'RGBA', 1)
        #Obentego las dimensiones de la imagen
        ix, iy = surf.get_rect().size
        #Creo una textura vacia en memoria de video, y me quedo con el identificador (texid) para poder referenciarla
        texid = glGenTextures(1)
        #Activo esta nueva textura para poder cargarle informacion
        glBindTexture(GL_TEXTURE_2D, texid)
        #Seteo los tipos de filtro a usar para agrandar y achivar la textura
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        #Cargo la matriz de colores dentro de la textura
        #Los parametros que le paso son:
        # - Tipo de textura, en este caso GL_TEXTURE_2D
        # - Nivel de mipmap, en este caso 0 porque no estoy usando mas niveles
        # - Formato en que quiero almacenar los datos en memoria de video, GL_RGB en este caso, porque no necesito canal Alfa
        # - Ancho de la textura
        # - Alto de la textura
        # - Grosor en pixels del borde, en este caso 0 porque no quiero agregar borde a al imagen
        # - Formato de los datos de la imagen, en este caso GL_RGBA que es como lo leimos con pygame.image
        # - Formato de los canales de color, GL_UNSIGNED_BYTE quiere decir que son 8bits para cada canal
        # - La imagen, en este caso la matriz de colores que creamos con pygame.image.tostring
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        #Una vez que tengo todo cargado, desactivo la textura para evitar que se dibuje por error mas adelante
        #Cada vez que quiera usarla, puedo hacer glBindTexture con el identificador (texid) que me guarde al crearla
        glBindTexture(GL_TEXTURE_2D, 0)
        #devuelvo el identificador de la textura para que pueda ser usada mas adelante
        return texid