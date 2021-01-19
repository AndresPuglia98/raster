import pygame
from pygame.locals import *
from pygame import mixer
from OpenGL.GL import *
from OpenGL.GLU import *
from shaderManager import *
from obj import *
from textureLoader import *
from camera import Trackball

def draw_model(model, text):
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    #Habilito el array de coordenadas de textura
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)
    
    glVertexPointer(3, GL_FLOAT, 32, model.faces)

    glNormalPointer(GL_FLOAT, 32, model.faces[3:])
    
    #Paso la lista de coordenadas de textura para cada vertice
    glTexCoordPointer(2, GL_FLOAT, 32, model.faces[6:])

    #Cargo la textura "text" en la posicion activa (que es la 0 en este ejemplo)
    glBindTexture(GL_TEXTURE_2D, text)

    glDrawArrays(GL_TRIANGLES, 0, len(model.faces) // 8)
    
    #Luego de dibujar, desactivo la textura
    glBindTexture(GL_TEXTURE_2D, 0)

    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_NORMAL_ARRAY)
    glDisableClientState(GL_TEXTURE_COORD_ARRAY)

def load_animation(filenames):
    animation_models = []
    for filename in filenames:
        obj = Obj()
        obj.parse(filename)
        animation_models.append(obj)
    return animation_models

def main():
    # Cargo paths de las animaciones
    run_paths = []
    for i in range(6):
        run_paths.append('animations/knight_run_{}.obj'.format(i))

    attack_paths = []
    for i in range(8):
        attack_paths.append('animations/knight_attack_{}.obj'.format(i))

    jump_paths = []
    for i in range(6):
        jump_paths.append('animations/knight_jump_{}.obj'.format(i))

    stand_paths = []
    for i in range(39):
        stand_paths.append('animations/knight_stand_{}.obj'.format(i))

    flip_paths = []
    for i in range(11):
        flip_paths.append('animations/knight_flip_{}.obj'.format(i))

    weapon_run_paths = []
    for i in range(6):
        weapon_run_paths.append('animations/weapon/weapon_k_run_{}.obj'.format(i))
    
    weapon_attack_paths = []
    for i in range(8):
        weapon_attack_paths.append('animations/weapon/weapon_k_attack_{}.obj'.format(i))

    weapon_jump_paths = []
    for i in range(6):
        weapon_jump_paths.append('animations/weapon/weapon_k_jump_{}.obj'.format(i))
    
    weapon_stand_paths = []
    for i in range(39):
        weapon_stand_paths.append('animations/weapon/weapon_k_stand_{}.obj'.format(i))
    
    weapon_flip_paths = []
    for i in range(11):
        weapon_flip_paths.append('animations/weapon/weapon_k_flip_{}.obj'.format(i))
    
    # Cargo animaciones
    run_models = load_animation(run_paths)
    attack_models = load_animation(attack_paths)
    jump_models = load_animation(jump_paths)
    stand_models = load_animation(stand_paths)
    weapon_run_models = load_animation(weapon_run_paths)
    weapon_attack_models = load_animation(weapon_attack_paths)
    weapon_jump_models = load_animation(weapon_jump_paths)
    weapon_stand_models = load_animation(weapon_stand_paths)
    flip_models = load_animation(flip_paths)
    weapon_flip_models = load_animation(weapon_flip_paths)


    # Creo los modelos a representar
    knight = Obj()
    knight.parse('obj/knight_texturas.obj')

    floor = Obj()
    floor.parse('obj/piso.obj')

    walls = Obj()
    walls.parse('obj/walls.obj')

    sky = Obj()
    sky.parse('obj/sky.obj')   

    # Pygame
    pygame.init()
    display = (1300,1300)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    pygame.mixer.music.load('sonidos/background_chill.mp3')
    pygame.mixer.music.play()

    shader_manager = ShaderManager()
    
    #Creo un programa de shading y guardo la referencia en la variable gouraud
    gouraud = shader_manager.createShader('shaders/gouraud_vs.hlsl',
                           'shaders/gouraud_fs.hlsl')
                           
    #Activo el manejo de texturas
    glEnable(GL_TEXTURE_2D)
    #Activo la textura 0 (hay 8 disponibles)
    glActiveTexture(GL_TEXTURE0)

    text_loader = TextureLoader()

    #Llamo a la funcion que levanta la textura a memoria de video
    text = text_loader.load_texture('texturas/knight_good.png')
    wall_text = text_loader.load_texture('texturas/brick.jpg')
    floor_text = text_loader.load_texture('texturas/floor4.jpg')
    sky_text = text_loader.load_texture('texturas/sky.jpg')
    night_text = text_loader.load_texture('texturas/night.jpg')
    weapon_text = text_loader.load_texture('animations/weapon/weapon_k.png')

    #Para el shader, me guardo una referencia a la variable que representa a la textura
    unif_textura = glGetUniformLocation(gouraud, 'textura')

    # Iluminación oscura (noche)
    glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.002,0.005,0.0099,1]) 
    glMaterial(GL_FRONT_AND_BACK, GL_AMBIENT, [2,0.5,2,1])
    glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, [1,1,1,1])
    glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, 16)

    glEnable(GL_LIGHT0)

    glLight(GL_LIGHT0, GL_DIFFUSE, [1,1,1,1])
    glLight(GL_LIGHT0, GL_AMBIENT, [0.1,0.1,0.1,1])
    glLight(GL_LIGHT0, GL_POSITION, [0,0,0,1])
    glLight(GL_LIGHT0, GL_SPECULAR, [1,1,1,1])

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 255,display[0],display[1])
    glFrustum(-1,1,-1,1,1,10000)
    
    # Niebla
    glEnable(GL_FOG)
    glFogf(GL_FOG_DENSITY, 0.3)
    glFogfv(GL_FOG_COLOR, [0.3,0.3,0.3,1])
    glFogf(GL_FOG_START, 0)
    glFogf(GL_FOG_END, 9500)
    glFogi(GL_FOG_MODE, GL_LINEAR)

    mode = GL_FILL
    z_buffer = True
    bfc = False
    bfcCW = True
    light = False
    end = False

    # Inicializo la camara
    cam = Trackball()
    cam.elev = -20
    cam.rot = 90
    cam.dist = 100

    # Indices de las animaciones
    indice_run = 0
    indice_run_w = 0
    indice_attack = 0
    indice_attack_w = 0
    indice_jump = 0
    indice_jump_w = 0
    indice_stand = 0
    indice_stand_w = 0
    indice_flip = 0
    indice_flip_w = 0

    # Para saber si el personaje mira hacia adelante cuando corre
    face_front = True

    # Parámetros para la física del salto del personaje
    mass = 1
    vel = 6
    is_jump = False
    jump = False

    # Inicializo variables de tiempo
    last_time = pygame.time.get_ticks()
    acum_t = 0

    # Efectos de sonido
    footsteps = mixer.Sound("sonidos/running.wav")
    sword = mixer.Sound("sonidos/sword.wav")
    while not end:
        keys_pressed = pygame.key.get_pressed()
        run = keys_pressed[pygame.K_w]
        run_back = keys_pressed[pygame.K_s]
        attack = keys_pressed[pygame.K_k]
        flip = keys_pressed[pygame.K_j]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jump = True
                if event.key == pygame.K_w:
                    footsteps.play()
                    face_front = True
                if event.key == pygame.K_s and (not event.key == pygame.K_w):
                    footsteps.play()
                    face_front = False
                if (event.key == pygame.K_k) and (not run) and (not run_back) and (not jump) and (not flip):
                    sword.play()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    footsteps.stop()
                if event.key == pygame.K_s:
                    footsteps.stop()
            if keys_pressed[pygame.K_m]:
                if mode == GL_LINE:
                    mode = GL_FILL
                else:
                    mode = GL_LINE
                glPolygonMode( GL_FRONT_AND_BACK, mode)
            if keys_pressed[pygame.K_z]:
                z_buffer = not z_buffer
                if z_buffer:
                    glEnable(GL_DEPTH_TEST)
                else:
                    glDisable(GL_DEPTH_TEST)
            if keys_pressed[pygame.K_b]:
                bfc = not bfc
                if bfc:
                    glEnable(GL_CULL_FACE)
                else:
                    glDisable(GL_CULL_FACE)
            if keys_pressed[pygame.K_c]:
                bfcCW = not bfcCW
                if bfcCW:
                    glFrontFace(GL_CW)
                else:
                    glFrontFace(GL_CCW)
            if keys_pressed[pygame.K_l]:
                light = not light
                if light:
                    #Con la tecla L habilito y deshabilito el shader
                    glUseProgram(gouraud)
                else:
                    glUseProgram(0)

            elif keys_pressed[pygame.K_ESCAPE]:
                end = True

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        #Camara

        # Zoom in
        if keys_pressed[pygame.K_e] and cam.dist > 60:
            cam.dist -= 5
        # Zoom out
        if keys_pressed[pygame.K_q] and cam.dist < 160:
            cam.dist += 5
        if keys_pressed[pygame.K_d]:
            cam.rot -= 5
        if keys_pressed[pygame.K_a]:
            cam.rot += 5
        if keys_pressed[pygame.K_UP] and cam.elev > -25:
            cam.elev -= 8
        if keys_pressed[pygame.K_DOWN] and cam.elev < 0:
            cam.elev += 8
        if keys_pressed[pygame.K_RIGHT]:
            cam.rot -= 5
        if keys_pressed[pygame.K_LEFT]:
            cam.rot += 5

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        cam.load_matrix()
        glRotatef(-90,1,0,0)

        # Dibijo el piso
        draw_model(floor, floor_text)

        # Dibujo las paredes y se rota la textura
        glPushMatrix()
        glRotatef(90,1,0,0)
        draw_model(walls, wall_text)
        glPopMatrix()

        if light:
            # Dibujo cielo nocturno
            draw_model(sky, night_text)
            #Si estoy usando shaders, le digo que la textura es la que esta activa en la posicion 0 (de las 8 disponibles)
            glUniform1i(unif_textura, 0)

        # Dibujo cielo normal
        draw_model(sky, sky_text)

        # Límites de desplazamiento del personaje
        if knight.pos[0] > 3750:
            knight.pos[0] = 3750
            cam.pos[0] = 3750
        if knight.pos[0] < -3750:
            knight.pos[0] = -3750
            cam.pos[0] = -3750

        # Actualizo la posición del personaje
        glTranslatef(knight.pos[0], knight.pos[1], knight.pos[2])

        # Cambio de dirección en la que mira el personaje
        if not face_front:
            glRotate(180,0,0,1)
        #Hasta acá corresponde a la matríz modelo del knight

        #Manejo de tiempo para animaciones
        current_time = pygame.time.get_ticks()
        delta_t = current_time - last_time
        last_time = current_time

        acum_t += delta_t

        # Manejo de animaciones
        if indice_run == 5:
            indice_run = 0
        if indice_run_w == 5:
            indice_run_w = 0
        if indice_attack == 7:
            indice_attack = 0
        if indice_attack_w == 7:
            indice_attack_w = 0
        if indice_jump == 5:
            indice_jump = 4
        if indice_jump_w == 5:
            indice_jump_w = 4
        if indice_stand == 38:
            indice_stand = 0
        if indice_stand_w == 38:
            indice_stand_w = 0
        if indice_flip == 11:
            indice_flip = 0
        if indice_flip_w == 11:
            indice_flip_w = 0

        action = False
        if run:
            action = True
            face_front = True
            knight.pos[0] += 20
            cam.pos[0] += 20
            if not jump:
                draw_model(run_models[indice_run], text)
                draw_model(weapon_run_models[indice_run_w], weapon_text)
                if acum_t > 60:
                    indice_run += 1
                    indice_run_w += 1
        if run_back and (not run):
            action = True
            knight.pos[0] -= 20
            cam.pos[0] -= 20
            if not jump:
                draw_model(run_models[indice_run], text)
                draw_model(weapon_run_models[indice_run_w], weapon_text)
                if acum_t > 60:
                    indice_run += 1
                    indice_run_w += 1
        if attack and (not run) and (not is_jump) and (not run_back):
            action = True
            draw_model(attack_models[indice_attack], text)
            draw_model(weapon_attack_models[indice_attack_w], weapon_text)
            if acum_t > 60:
                indice_attack += 1
                indice_attack_w += 1
        if flip and (not run) and (not is_jump) and (not run_back) and (not attack):
            action = True
            draw_model(flip_models[indice_flip], text)
            draw_model(weapon_flip_models[indice_flip_w], weapon_text)
            if acum_t > 60:
                indice_flip += 1
                indice_flip_w += 1        
        if jump:
            action = True
            is_jump = True
            draw_model(jump_models[indice_jump], text)
            draw_model(weapon_jump_models[indice_jump_w], weapon_text)
            if acum_t > 60:
                indice_jump += 1
                indice_jump_w += 1
        if is_jump:
            f = (1/2)*mass*(vel**2)
            knight.pos[2] += f
            vel -= acum_t/100
            if vel < 0:
                mass = -1
            if knight.pos[2] <= 0:
                knight.pos[2] = 0
                is_jump = False
                jump = False
                mass = 1
                vel = 6

        if not action:
            draw_model(stand_models[indice_stand], text)
            draw_model(weapon_stand_models[indice_stand_w], weapon_text)
            if acum_t > 60:
                indice_stand += 1
                indice_stand_w += 1

        # Velocidad de animaciones
        if acum_t > 60:
            # print('Tiempo!')
            acum_t = 0        

        pygame.display.flip()
    
    #Cuando salgo del loop, antes de cerrar el programa libero todos los recursos creados
    glDeleteProgram(gouraud)
    glDeleteTextures([text])
    pygame.quit()
    quit()

main()