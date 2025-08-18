import os
import time
import random
import json
from instagrapi import Client
from dotenv import load_dotenv

# --- Cargar Variables de Entorno ---
load_dotenv()
USERNAME = os.environ.get("INSTA_USERNAME")
PASSWORD = os.environ.get("INSTA_PASSWORD")
SESSION_DATA = os.environ.get("INSTA_SESSION_DATA")

# --- Parámetros del bot ---
TARGET_ACCOUNT = "leomessi"
MAX_FOLLOWS_PER_RUN = 25
MIN_DELAY = 15
MAX_DELAY = 45

# --- Inicialización del Cliente ---
cl = Client()
cl.delay_range = [2, 5]

def main():
    follow_counter = 0
    try:
        # --- Inicio de Sesión ---
        if SESSION_DATA:
            print("Encontrada sesión en variable de entorno. Cargando sesión...")
            cl.set_settings(json.loads(SESSION_DATA))  # ✅ Cargar sesión desde JSON
        
        cl.login(USERNAME, PASSWORD)
        print("Verificando el estado de la sesión...")
        cl.get_timeline_feed()  
        print(f"Inicio de sesión exitoso como {USERNAME}")
        print("-" * 20)

        # --- Paso 1: Obtener el ID y seguidores ---
        print(f"Buscando a la cuenta objetivo: {TARGET_ACCOUNT}")
        user_id = cl.user_id_from_username(TARGET_ACCOUNT)
        print(f"Obteniendo seguidores de {TARGET_ACCOUNT}...")
        followers = cl.user_followers(user_id, amount=MAX_FOLLOWS_PER_RUN + 50)
        print(f"Se encontraron {len(followers)} seguidores para procesar.")

        # --- Paso 2: Seguir usuarios ---
        for user_pk, user in followers.items():
            if follow_counter >= MAX_FOLLOWS_PER_RUN:
                print(f"Límite de {MAX_FOLLOWS_PER_RUN} seguimientos alcanzado.")
                break
            try:
                print(f"Intentando seguir a: {user.username} (ID: {user.pk})")
                success = cl.user_follow(user.pk)
                if success:
                    follow_counter += 1
                    delay = random.uniform(MIN_DELAY, MAX_DELAY)
                    print(f" -> Éxito. Esperando {delay:.2f} segundos...")
                    time.sleep(delay)
                else:
                    print(f" -> No se pudo seguir (ya seguido o cuenta privada).")
                    time.sleep(3)
            except Exception as e:
                print(f"Error inesperado al seguir a {user.username}: {e}")
                time.sleep(MAX_DELAY)

    except Exception as e:
        print(f"Ocurrió un error grave: {e}")
    finally:
        # ✅ Guardar nueva sesión y mostrarla
        new_session_data = json.dumps(cl.get_settings())
        print("-" * 20)
        print("Script finalizado.")
        print(f"Total de usuarios seguidos en esta sesión: {follow_counter}")
        print("\n!!! IMPORTANTE: COPIA EL SIGUIENTE BLOQUE Y ACTUALIZA EL SECRETO 'INSTA_SESSION_DATA' EN GITHUB !!!\n")
        print(new_session_data)


if __name__ == "__main__":
    main()
