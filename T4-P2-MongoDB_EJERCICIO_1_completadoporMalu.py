import pygame
import time
import random
import pymongo
from datetime import datetime

###################### BLOQUE A COMPLETAR ##########################
# PALABRA CLAVE: CONEXIONES

# Conexiones con MongoDB
db_name = "practica_2_mongodb"
db_uri = 'mongodb://localhost:27017'
db_client = pymongo.MongoClient(db_uri)
db = db_client[db_name]

# Colecciones
coleccion_usuarios = db['usuarios']
coleccion_partidas = db['partidas']

###################### FIN DE BLOQUE A COMPLETAR ###################

# Función para pedir datos de usuario
def get_user_data():
    username = input("Ingrese su nombre de usuario: ")
    email = input("Ingrese su correo electrónico: ")
    
    ###################### BLOQUE A COMPLETAR ##########################
    # PALABRA CLAVE: USUARIO
    
    # Buscar si el usuario ya existe
    existing_user = coleccion_usuarios.find_one({"username": username})
    
    if existing_user is None:
        # Si no existe, crear nuevo usuario
        user = {
            "username": username,
            "email": email,
            "signup_date": datetime.now()
        }
        coleccion_usuarios.insert_one(user)
        print(f"✅ Usuario {username} registrado correctamente")
    else:
        # Si existe, usar el usuario existente
        print(f"👋 Bienvenido de nuevo, {username}!")
        user = existing_user
    
    ###################### FIN DE BLOQUE A COMPLETAR ###################
    
    print("\n🎮 Preparando el juego...")
    print("💡 Usa las flechas del teclado para mover la serpiente")
    print("💡 Presiona cualquier tecla en la ventana del juego para empezar\n")
    
    return user

# Colores
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Dimensiones de la pantalla
dis_width = 800
dis_height = 600

# Inicializar Pygame
pygame.init()
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Practica 2: Snake x MongoDB')

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def your_score(score):
    value = score_font.render("Puntuación: " + str(score), True, yellow)
    dis.blit(value, [0, 0])

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def gameLoop(user):
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    length_of_snake = 1
    steps = 0
    level = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    start_time = time.time()

    while not game_over:

        while game_close == True:
            dis.fill(blue)
            message("¡Chocaste! Presiona C para jugar de nuevo o Q para salir", red)
            your_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop(user)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                
            
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    steps += 1

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(white)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        your_score(length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            length_of_snake += 1
            if length_of_snake % 5 == 0:
                level += 1

        clock.tick(snake_speed)

    ###################### BLOQUE A COMPLETAR ##########################
    # PALABRA CLAVE: PARTIDA

    # Almacenar información de la partida en MongoDB
    game_data = {
        "user_id": user["username"],
        "score": length_of_snake - 1,
        "date": datetime.now(),
        "duration": time.time() - start_time,
        "level": level,
        "steps": steps,
        "final_position": {"x": x1, "y": y1}
    }
    
    # Insertar la partida en MongoDB
    coleccion_partidas.insert_one(game_data)
    
    # Mostrar resumen de la partida
    print("\n" + "="*60)
    print("🎮 ¡PARTIDA FINALIZADA!")
    print("="*60)
    print(f"👤 Jugador: {game_data['user_id']}")
    print(f"🏆 Puntuación: {game_data['score']} puntos")
    print(f"📊 Nivel alcanzado: {game_data['level']}")
    print(f"⏱️  Duración: {game_data['duration']:.2f} segundos")
    print(f"👣 Movimientos totales: {game_data['steps']}")
    print(f"📍 Posición final: X={game_data['final_position']['x']}, Y={game_data['final_position']['y']}")
    print(f"✅ Partida guardada en MongoDB correctamente")
    print("="*60 + "\n")
    
    ###################### FIN DE BLOQUE A COMPLETAR ###################
    
    pygame.quit()
    quit()

def main():
    print("\n" + "="*60)
    print("🐍 SNAKE GAME - Práctica MongoDB")
    print("="*60 + "\n")
    
    user = get_user_data()
    gameLoop(user)

if __name__ == "__main__":
    main()