import os
os.environ['XMODIFIERS'] = '@im=none'
import tkinter as tk
from tkinter import ttk, messagebox, font, filedialog, simpledialog
import json
import math
import re
from ebooklib import epub
import queue
import time
import random
import sqlite3
import base64
import io
import threading
import socket
import nacl.signing
import nacl.encoding
import nacl.utils
from PIL import Image, ImageTk
from librats_py import RatsNode, LogLevel, set_log_level

# Silenciar los logs internos de librats
set_log_level(LogLevel.WARN)

TEMATICAS = ["cultura", "política", "economía", "historia", "moda", "música", "libros", "viajes", "tecnología", "ciencia"]

# Mapeo de códigos ISO a nombres
MAPEO_IDIOMAS = {
    "es": "Español", "en": "English", "de": "Deutsch", "fr": "Français",
    "it": "Italiano", "pt": "Português", "ro": "Română", "sv": "Svenska",
    "no": "Norsk", "da": "Dansk", "ru": "Русский"
}
IDIOMAS = list(MAPEO_IDIOMAS.values())

TRADUCCIONES = {
    "es": {
        "Descubrir": "Descubrir", "Redactar": "Redactar", "Leyendo": "Leyendo", 
        "Mi espacio": "Mi espacio", "Autores": "Autores", "Avisos": "Avisos", 
        "Categoría:": "Categoría:", "Etiqueta:": "Etiqueta:", "Idioma:": "Idioma:", 
        "Buscar": "Buscar", "Todas": "Todas", "Todos": "Todos", 
        "Título:": "Título:", "Etiquetas:": "Etiquetas:", "Contenido:": "Contenido:", 
        "Publicar artículo": "Publicar artículo", "Mi perfil": "Mi perfil", 
        "Guardar Perfil": "Guardar Perfil", "Mis artículos publicados": "Mis artículos publicados", 
        "Almacenamiento": "Almacenamiento", "Autores seguidos": "Autores seguidos", 
        "Artículos guardados": "Artículos guardados", "Borrar guardado": "Borrar guardado", 
        "Doble clic para leer": "Doble clic para leer", "Guardar artículo": "Guardar artículo", 
        "Editar artículo": "Editar artículo", "Borrar artículo": "Borrar artículo", 
        "Seguir autor": "Seguir autor", "Seguir y Respaldar": "Seguir y Respaldar", 
        "Ver perfil del autor": "Ver perfil del autor", "Recientes de seguidos": "Recientes de seguidos", 
        "Descubrir por azar": "Descubrir por azar", "Nombre:": "Nombre:", "Descripción:": "Descripción:", 
        "Selecciona un autor": "Selecciona un autor", "Título": "Título", "Categoría": "Categoría", 
        "ID (Fecha)": "ID (Fecha)", "Cambiar límite": "Cambiar límite", "Automático": "Automático",
        "Ancho:": "Márgenes:", "Ajustar": "Ajustar"
    },
    "en": {
        "Descubrir": "Discover", "Redactar": "Compose", "Leyendo": "Reading", 
        "Mi espacio": "My Space", "Autores": "Authors", "Avisos": "Alerts", 
        "Categoría:": "Category:", "Etiqueta:": "Tag:", "Idioma:": "Language:", 
        "Buscar": "Search", "Todas": "All", "Todos": "All", 
        "Título:": "Title:", "Etiquetas:": "Tags:", "Contenido:": "Content:", 
        "Publicar artículo": "Publish article", "Mi perfil": "My profile", 
        "Guardar Perfil": "Save Profile", "Mis artículos publicados": "My published articles", 
        "Almacenamiento": "Storage", "Autores seguidos": "Followed authors", 
        "Artículos guardados": "Saved articles", "Borrar guardado": "Delete saved", 
        "Doble clic para leer": "Double click to read", "Guardar artículo": "Save article", 
        "Editar artículo": "Edit article", "Borrar artículo": "Delete article", 
        "Seguir autor": "Follow author", "Seguir y Respaldar": "Follow & Backup", 
        "Ver perfil del autor": "View author profile", "Recientes de seguidos": "Recent from followed", 
        "Descubrir por azar": "Discover randomly", "Nombre:": "Name:", "Descripción:": "Description:", 
        "Selecciona un autor": "Select an author", "Título": "Title", "Categoría": "Category", 
        "ID (Fecha)": "ID (Date)", "Cambiar límite": "Change limit", "Automático": "Automatic",
        "Ancho:": "Margins:", "Ajustar": "Adjust"
    },
    "de": { # Alemán
        "Descubrir": "Entdecken", "Redactar": "Verfassen", "Leyendo": "Lesen", 
        "Mi espacio": "Mein Bereich", "Autores": "Autoren", "Avisos": "Hinweise", 
        "Categoría:": "Kategorie:", "Etiqueta:": "Tag:", "Idioma:": "Sprache:", 
        "Buscar": "Suchen", "Todas": "Alle", "Todos": "Alle", 
        "Título:": "Titel:", "Etiquetas:": "Tags:", "Contenido:": "Inhalt:", 
        "Publicar artículo": "Artikel veröffentlichen", "Mi perfil": "Mein Profil", 
        "Guardar Perfil": "Profil speichern", "Mis artículos publicados": "Meine veröffentlichten Artikel", 
        "Almacenamiento": "Speicher", "Autores seguidos": "Gefolgte Autoren", 
        "Artículos guardados": "Gespeicherte Artikel", "Borrar guardado": "Gespeichertes löschen", 
        "Doble clic para leer": "Doppelklick zum Lesen", "Guardar artículo": "Artikel speichern", 
        "Editar artículo": "Artikel bearbeiten", "Borrar artículo": "Artikel löschen", 
        "Seguir autor": "Autor folgen", "Seguir y Respaldar": "Folgen & Sichern", 
        "Ver perfil del autor": "Autorenprofil ansehen", "Recientes de seguidos": "Neueste von Gefolgten", 
        "Descubrir por azar": "Zufällig entdecken", "Nombre:": "Name:", "Descripción:": "Beschreibung:", 
        "Selecciona un autor": "Wähle einen Autor", "Título": "Titel", "Categoría": "Kategorie", 
        "ID (Fecha)": "ID (Datum)", "Cambiar límite": "Limit ändern", "Automático": "Automatisch",
        "Ancho:": "Ränder:", "Ajustar": "Anpassen"
    },
    "fr": { # Francés
        "Descubrir": "Découvrir", "Redactar": "Rédiger", "Leyendo": "Lecture", 
        "Mi espacio": "Mon espace", "Autores": "Auteurs", "Avisos": "Alertes", 
        "Categoría:": "Catégorie:", "Etiqueta:": "Tag:", "Idioma:": "Langue:", 
        "Buscar": "Chercher", "Todas": "Toutes", "Todos": "Tous", 
        "Título:": "Titre:", "Etiquetas:": "Tags:", "Contenido:": "Contenu:", 
        "Publicar artículo": "Publier l'article", "Mi perfil": "Mon profil", 
        "Guardar Perfil": "Enregistrer le profil", "Mis artículos publicados": "Mes articles publiés", 
        "Almacenamiento": "Stockage", "Autores seguidos": "Auteurs suivis", 
        "Artículos guardados": "Articles sauvegardés", "Borrar guardado": "Supprimer la sauvegarde", 
        "Doble clic para leer": "Double-cliquez pour lire", "Guardar artículo": "Sauvegarder l'article", 
        "Editar artículo": "Modifier l'article", "Borrar artículo": "Supprimer l'article", 
        "Seguir autor": "Suivre l'auteur", "Seguir y Respaldar": "Suivre & Sauvegarder", 
        "Ver perfil del autor": "Voir le profil de l'auteur", "Recientes de seguidos": "Récent des suivis", 
        "Descubrir por azar": "Découvrir au hasard", "Nombre:": "Nom:", "Descripción:": "Description:", 
        "Selecciona un autor": "Sélectionnez un auteur", "Título": "Titre", "Categoría": "Catégorie", 
        "ID (Fecha)": "ID (Date)", "Cambiar límite": "Changer la limite", "Automático": "Automatique",
        "Ancho:": "Marges:", "Ajustar": "Ajuster"
    },
    "it": { # Italiano
        "Descubrir": "Scopri", "Redactar": "Scrivi", "Leyendo": "Lettura", 
        "Mi espacio": "Il mio spazio", "Autores": "Autori", "Avisos": "Avvisi", 
        "Categoría:": "Categoria:", "Etiqueta:": "Tag:", "Idioma:": "Lingua:", 
        "Buscar": "Cerca", "Todas": "Tutte", "Todos": "Tutti", 
        "Título:": "Titolo:", "Etiquetas:": "Tag:", "Contenido:": "Contenuto:", 
        "Publicar artículo": "Pubblica articolo", "Mi perfil": "Il mio profilo", 
        "Guardar Perfil": "Salva profilo", "Mis artículos publicados": "I miei articoli pubblicati", 
        "Almacenamiento": "Archiviazione", "Autores seguidos": "Autori seguiti", 
        "Artículos guardados": "Articoli salvati", "Borrar guardado": "Elimina salvato", 
        "Doble clic para leer": "Doppio clic per leggere", "Guardar artículo": "Salva articolo", 
        "Editar artículo": "Modifica articolo", "Borrar artículo": "Elimina articolo", 
        "Seguir autor": "Segui autore", "Seguir y Respaldar": "Segui e Supporta", 
        "Ver perfil del autor": "Vedi profilo autore", "Recientes de seguidos": "Recenti dai seguiti", 
        "Descubrir por azar": "Scopri a caso", "Nombre:": "Nome:", "Descripción:": "Descrizione:", 
        "Selecciona un autor": "Seleziona un autore", "Título": "Titolo", "Categoría": "Categoria", 
        "ID (Fecha)": "ID (Data)", "Cambiar límite": "Cambia limite", "Automático": "Automatico",
        "Ancho:": "Margini:", "Ajustar": "Regola"
    },
    "pt": { # Portugués
        "Descubrir": "Descobrir", "Redactar": "Escrever", "Leyendo": "Lendo", 
        "Mi espacio": "Meu espaço", "Autores": "Autores", "Avisos": "Avisos", 
        "Categoría:": "Categoria:", "Etiqueta:": "Etiqueta:", "Idioma:": "Idioma:", 
        "Buscar": "Buscar", "Todas": "Todas", "Todos": "Todos", 
        "Título:": "Título:", "Etiquetas:": "Etiquetas:", "Contenido:": "Conteúdo:", 
        "Publicar artículo": "Publicar artigo", "Mi perfil": "Meu perfil", 
        "Guardar Perfil": "Salvar perfil", "Mis artículos publicados": "Meus artigos publicados", 
        "Almacenamiento": "Armazenamento", "Autores seguidos": "Autores seguidos", 
        "Artículos guardados": "Artigos salvos", "Borrar guardado": "Excluir salvo", 
        "Doble clic para leer": "Clique duplo para ler", "Guardar artículo": "Salvar artigo", 
        "Editar artículo": "Editar artigo", "Borrar artículo": "Excluir artigo", 
        "Seguir autor": "Seguir autor", "Seguir y Respaldar": "Seguir e Apoiar", 
        "Ver perfil del autor": "Ver perfil do autor", "Recientes de seguidos": "Recentes de seguidos", 
        "Descubrir por azar": "Descobrir aleatoriamente", "Nombre:": "Nome:", "Descripción:": "Descrição:", 
        "Selecciona un autor": "Selecione um autor", "Título": "Título", "Categoría": "Categoria", 
        "ID (Fecha)": "ID (Data)", "Cambiar límite": "Mudar limite", "Automático": "Automático",
        "Ancho:": "Margens:", "Ajustar": "Ajustar"
    },
    "ro": { # Rumano
        "Descubrir": "Descoperă", "Redactar": "Scrie", "Leyendo": "Citind", 
        "Mi espacio": "Spațiul meu", "Autores": "Autori", "Avisos": "Alerte", 
        "Categoría:": "Categorie:", "Etiqueta:": "Etichetă:", "Idioma:": "Limbă:", 
        "Buscar": "Caută", "Todas": "Toate", "Todos": "Toți", 
        "Título:": "Titlu:", "Etiquetas:": "Etichete:", "Contenido:": "Conținut:", 
        "Publicar artículo": "Publică articolul", "Mi perfil": "Profilul meu", 
        "Guardar Perfil": "Salvează profilul", "Mis artículos publicados": "Articolele mele publicate", 
        "Almacenamiento": "Stocare", "Autores seguidos": "Autori urmăriți", 
        "Artículos guardados": "Articole salvate", "Borrar guardado": "Șterge salvat", 
        "Doble clic para leer": "Dublu clic pentru a citi", "Guardar artículo": "Salvează articolul", 
        "Editar artículo": "Editează articolul", "Borrar artículo": "Șterge articolul", 
        "Seguir autor": "Urmărește autorul", "Seguir y Respaldar": "Urmărește și Susține", 
        "Ver perfil del autor": "Vezi profilul autorului", "Recientes de seguidos": "Recente de la urmăriți", 
        "Descubrir por azar": "Descoperă la întâmplare", "Nombre:": "Nume:", "Descripción:": "Descriere:", 
        "Selecciona un autor": "Selectează un autor", "Título": "Titlu", "Categoría": "Categorie", 
        "ID (Fecha)": "ID (Dată)", "Cambiar límite": "Schimbă limita", "Automático": "Automat",
        "Ancho:": "Margini:", "Ajustar": "Ajustează"
    },
    "sv": { # Sueco
        "Descubrir": "Upptäck", "Redactar": "Skriv", "Leyendo": "Läser", 
        "Mi espacio": "Mitt utrymme", "Autores": "Författare", "Avisos": "Aviseringar", 
        "Categoría:": "Kategori:", "Etiqueta:": "Tagg:", "Idioma:": "Språk:", 
        "Buscar": "Sök", "Todas": "Alla", "Todos": "Alla", 
        "Título:": "Titel:", "Etiquetas:": "Taggar:", "Contenido:": "Innehåll:", 
        "Publicar artículo": "Publicera artikel", "Mi perfil": "Min profil", 
        "Guardar Perfil": "Spara profil", "Mis artículos publicados": "Mina publicerade artiklar", 
        "Almacenamiento": "Lagring", "Autores seguidos": "Följda författare", 
        "Artículos guardados": "Sparade artiklar", "Borrar guardado": "Radera sparad", 
        "Doble clic para leer": "Dubbelklicka för att läsa", "Guardar artículo": "Spara artikel", 
        "Editar artículo": "Redigera artikel", "Borrar artículo": "Radera artikel", 
        "Seguir autor": "Följ författare", "Seguir y Respaldar": "Följ & Säkerhetskopiera", 
        "Ver perfil del autor": "Visa författarprofil", "Recientes de seguidos": "Senaste från följda", 
        "Descubrir por azar": "Upptäck slumpmässigt", "Nombre:": "Namn:", "Descripción:": "Beskrivning:", 
        "Selecciona un autor": "Välj en författare", "Título": "Titel", "Categoría": "Kategori", 
        "ID (Fecha)": "ID (Datum)", "Cambiar límite": "Ändra gräns", "Automático": "Automatisk",
        "Ancho:": "Marginaler:", "Ajustar": "Justera"
    },
    "no": { # Noruego
        "Descubrir": "Oppdag", "Redactar": "Skriv", "Leyendo": "Leser", 
        "Mi espacio": "Min plass", "Autores": "Forfattere", "Avisos": "Varsler", 
        "Categoría:": "Kategori:", "Etiqueta:": "Tagg:", "Idioma:": "Språk:", 
        "Buscar": "Søk", "Todas": "Alle", "Todos": "Alle", 
        "Título:": "Tittel:", "Etiquetas:": "Tagger:", "Contenido:": "Innhold:", 
        "Publicar artículo": "Publiser artikkel", "Mi perfil": "Min profil", 
        "Guardar Perfil": "Lagre profil", "Mis artículos publicados": "Mine publiserte artikler", 
        "Almacenamiento": "Lagring", "Autores seguidos": "Fulgte forfattere", 
        "Artículos guardados": "Lagrede artikler", "Borrar guardado": "Slett lagret", 
        "Doble clic para leer": "Dobbeltklikk for å lese", "Guardar artículo": "Lagre artikkel", 
        "Editar artículo": "Rediger artikkel", "Borrar artículo": "Slett artikkel", 
        "Seguir autor": "Følg forfatter", "Seguir y Respaldar": "Følg & Sikkerhetskopier", 
        "Ver perfil del autor": "Se forfatterprofil", "Recientes de seguidos": "Nylige fra fulgte", 
        "Descubrir por azar": "Oppdag tilfeldig", "Nombre:": "Navn:", "Descripción:": "Beskrivelse:", 
        "Selecciona un autor": "Velg en forfatter", "Título": "Tittel", "Categoría": "Kategori", 
        "ID (Fecha)": "ID (Dato)", "Cambiar límite": "Endre grense", "Automático": "Automatisk",
        "Ancho:": "Marginer:", "Ajustar": "Juster"
    },
    "da": { # Danés
        "Descubrir": "Opdag", "Redactar": "Skriv", "Leyendo": "Læser", 
        "Mi espacio": "Mit rum", "Autores": "Forfattere", "Avisos": "Underretninger", 
        "Categoría:": "Kategori:", "Etiqueta:": "Tag:", "Idioma:": "Sprog:", 
        "Buscar": "Søg", "Todas": "Alle", "Todos": "Alle", 
        "Título:": "Titel:", "Etiquetas:": "Tags:", "Contenido:": "Indhold:", 
        "Publicar artículo": "Udgiv artikel", "Mi perfil": "Min profil", 
        "Guardar Perfil": "Gem profil", "Mis artículos publicados": "Mine udgivne artikler", 
        "Almacenamiento": "Lager", "Autores seguidos": "Fulgte forfattere", 
        "Artículos guardados": "Gemte artikler", "Borrar guardado": "Slet gemt", 
        "Doble clic para leer": "Dobbeltklik for at læse", "Guardar artículo": "Gem artikel", 
        "Editar artículo": "Rediger artikel", "Borrar artículo": "Slet artikel", 
        "Seguir autor": "Følg forfatter", "Seguir y Respaldar": "Følg & Sikkerhedskopier", 
        "Ver perfil del autor": "Se forfatterprofil", "Recientes de seguidos": "Seneste fra fulgte", 
        "Descubrir por azar": "Opdag tilfældigt", "Nombre:": "Navn:", "Descripción:": "Beskrivelse:", 
        "Selecciona un autor": "Vælg en forfatter", "Título": "Titel", "Categoría": "Kategori", 
        "ID (Fecha)": "ID (Dato)", "Cambiar límite": "Skift grænse", "Automático": "Automatisk",
        "Ancho:": "Margener:", "Ajustar": "Juster"
    },
    "ru": { # Ruso
        "Descubrir": "Обзор", "Redactar": "Написать", "Leyendo": "Чтение", 
        "Mi espacio": "Мое пространство", "Autores": "Авторы", "Avisos": "Уведомления", 
        "Categoría:": "Категория:", "Etiqueta:": "Тег:", "Idioma:": "Язык:", 
        "Buscar": "Поиск", "Todas": "Все", "Todos": "Все", 
        "Título:": "Заголовок:", "Etiquetas:": "Теги:", "Contenido:": "Содержание:", 
        "Publicar artículo": "Опубликовать статью", "Mi perfil": "Мой профиль", 
        "Guardar Perfil": "Сохранить профиль", "Mis artículos publicados": "Мои опубликованные статьи", 
        "Almacenamiento": "Хранилище", "Autores seguidos": "Отслеживаемые авторы", 
        "Artículos guardados": "Сохраненные статьи", "Borrar guardado": "Удалить сохраненное", 
        "Doble clic para leer": "Двойной клик для чтения", "Guardar artículo": "Сохранить статью", 
        "Editar artículo": "Редактировать статью", "Borrar artículo": "Удалить статью", 
        "Seguir autor": "Подписаться на автора", "Seguir y Respaldar": "Подписаться и поддержать", 
        "Ver perfil del autor": "Профиль автора", "Recientes de seguidos": "Новое от подписок", 
        "Descubrir por azar": "Случайный поиск", "Nombre:": "Имя:", "Descripción:": "Описание:", 
        "Selecciona un autor": "Выберите автора", "Título": "Заголовок", "Categoría": "Категория", 
        "ID (Fecha)": "ID (Дата)", "Cambiar límite": "Изменить лимит", "Automático": "Авто",
        "Ancho:": "Отступы:", "Ajustar": "Настроить"
    }
}

ARCHIVO_DB = "./blog_state/app_data.db"

class BlogP2PApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blog P2P — Fase 1")
        
        # HACER LA VENTANA RESPONSIVA AL MONITOR
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        # Tomamos el 90% del ancho y alto de la pantalla, para que quepan los bordes del sistema
        ancho_ventana = int(ancho_pantalla * 0.9)
        alto_ventana = int(alto_pantalla * 0.9)
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}")
        
        self.event_queue = queue.Queue()

        # Estado local
        self.nombre_usuario = "Usuario Anónimo"
        self.mis_articulos = {}              
        self.articulos_descubiertos = []     
        self.articulos_guardados = {}        
        self.autores_seguidos = set()        
        self.autores_respaldados = set()     
        self.mi_descripcion = ""
        self.mi_horario = ""
        self.mi_utc_offset = 0.0
        self.perfiles_autores = {}     

        self.articulo_actual_id = None
        self.articulo_actual_contenido = None
        self.editando_id = None 
        self._guardados_ids = []
        self._recientes_ids = []
        self._autores_lista_ids = []
        self.respaldos_pendientes = set() 

        self.imagenes_temporales = {}
        self.imagenes_lectura = []    
        self.contador_imagenes = 0

        self.limite_mb = 100 
        self.llave_privada = None
        self.llave_publica = None
        self.pagina_actual = 1
        self.articulos_por_pagina = 20
        self.ancho_columnas = 80  # <--- CONTROL DE ANCHO DINÁMICO
        self.margen_texto = 130   # Margen por defecto (10 clics de +)
        self.ultima_publicacion = 0
        self._save_timer = None
        self.borradores = {}
        # Variables de estado que estaban mal ubicadas
        self.lapidas = set()
        self.notificaciones_etiquetas = []
        self.etiquetas_revocadas = {}
        self.borradores = {}
        self.alerta_espacio_mostrada = False
        self.mis_colecciones = {}
        self.colecciones_descubiertas = {}
        self.respaldos_red = {}
        self.quien_tiene = {} # Diccionario: {articulo_id: [peer_id1, peer_id2]}
        self.coleccion_en_lectura = None
        self.indice_coleccion = 0
        self.autor_perfil_actual = None
        
        # Detectar idioma del sistema
        try:
            # Intenta obtener el idioma del sistema (ej: es_ES.UTF-8, en_US, de_DE)
            lang_env = os.environ.get('LANG', 'es_ES')
            idioma_sistema = lang_env[:2].lower()
        except:
            idioma_sistema = "es"
        
        # Si el idioma del sistema no está en nuestras traducciones, usamos inglés por defecto (o español)
        if idioma_sistema not in TRADUCCIONES:
            idioma_sistema = "en" 
            
        self.idioma_actual = MAPEO_IDIOMAS.get(idioma_sistema, "English")
        self.lang_code = idioma_sistema

        self._init_db()
        self._cargar_datos()

        self._construir_interfaz()
        self._refrescar_todo_visual()

        self.node = RatsNode(0, protocol="blog-p2p/1.0", data_dir="./blog_state")
        self._configurar_nodo()
        
        # ¡NUEVO! Iniciar la red en un hilo separado para que la ventana no se congele
        threading.Thread(target=self.node.start, daemon=True).start()
        
        # Imprimimos el ID (puede tardar un milisegundo en asignarse, pero no bloquea la UI)
        self.root.after(500, lambda: print(f"✅ Nodo iniciado. Peer ID: {self.node.local_id}"))

        self.root.after(100, self._procesar_cola)
        self.root.protocol("WM_DELETE_WINDOW", self._al_cerrar)

    # ------------------------------------------------------------------
    # BASE DE DATOS SQLITE
    # ------------------------------------------------------------------
    def _init_db(self):
        os.makedirs("./blog_state", exist_ok=True)
        self.conn = sqlite3.connect(ARCHIVO_DB)
        self.cursor = self.conn.cursor()
        
        # Tabla para configuraciones simples (nombre, descripción, horario, etc)
        self.cursor.execute("CREATE TABLE IF NOT EXISTS config (clave TEXT PRIMARY KEY, valor TEXT)")
        # Tablas para los artículos y perfiles
        self.cursor.execute("CREATE TABLE IF NOT EXISTS articulos_propios (id TEXT PRIMARY KEY, datos TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS articulos_descubiertos (id TEXT PRIMARY KEY, datos TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS articulos_guardados (id TEXT PRIMARY KEY, datos TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS perfiles (id TEXT PRIMARY KEY, datos TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS colecciones (id TEXT PRIMARY KEY, datos TEXT, es_propia INTEGER)")
        self.conn.commit()
        
        # Llamamos a la migración por si el usuario tiene la base de datos vieja
        self._migrar_datos_viejos()

    def _migrar_datos_viejos(self):
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='kv_store'")
            if not self.cursor.fetchone():
                return # No hay datos viejos, no hay nada que migrar

            print("🔄 Migrando base de datos antigua a nuevo formato...")
            self.cursor.execute("SELECT clave, valor FROM kv_store")
            filas = self.cursor.fetchall()
            for clave, valor_json in filas:
                if clave == "mis_articulos":
                    for k, v in json.loads(valor_json).items():
                        self.cursor.execute("INSERT OR REPLACE INTO articulos_propios (id, datos) VALUES (?, ?)", (k, json.dumps(v, ensure_ascii=False)))
                elif clave == "articulos_descubiertos":
                    for v in json.loads(valor_json):
                        self.cursor.execute("INSERT OR REPLACE INTO articulos_descubiertos (id, datos) VALUES (?, ?)", (v["id"], json.dumps(v, ensure_ascii=False)))
                elif clave == "articulos_guardados":
                    for k, v in json.loads(valor_json).items():
                        self.cursor.execute("INSERT OR REPLACE INTO articulos_guardados (id, datos) VALUES (?, ?)", (k, json.dumps(v, ensure_ascii=False)))
                elif clave == "perfiles_autores":
                    for k, v in json.loads(valor_json).items():
                        self.cursor.execute("INSERT OR REPLACE INTO perfiles (id, datos) VALUES (?, ?)", (k, json.dumps(v, ensure_ascii=False)))
                elif clave == "mis_colecciones":
                    for k, v in json.loads(valor_json).items():
                        self.cursor.execute("INSERT OR REPLACE INTO colecciones (id, datos, es_propia) VALUES (?, ?, 1)", (k, json.dumps(v, ensure_ascii=False)))
                elif clave == "colecciones_descubiertas":
                    for k, v in json.loads(valor_json).items():
                        self.cursor.execute("INSERT OR REPLACE INTO colecciones (id, datos, es_propia) VALUES (?, ?, 0)", (k, json.dumps(v, ensure_ascii=False)))
                else:
                    self.cursor.execute("INSERT OR REPLACE INTO config (clave, valor) VALUES (?, ?)", (clave, valor_json))
            
            self.cursor.execute("DROP TABLE kv_store")
            self.conn.commit()
            print("✅ Migración completada con éxito.")
        except Exception as e:
            print(f"Error en migración: {e}")

    def _guardar_kv(self, clave, valor):
        try:
            self.cursor.execute("INSERT OR REPLACE INTO config (clave, valor) VALUES (?, ?)", 
                                (clave, json.dumps(valor, ensure_ascii=False)))
            self.conn.commit()
        except Exception as e:
            print(f"Error en _guardar_kv: {e}")

    def _leer_kv(self, clave, defecto):
        try:
            self.cursor.execute("SELECT valor FROM config WHERE clave = ?", (clave,))
            fila = self.cursor.fetchone()
            if fila:
                return json.loads(fila[0])
        except Exception:
            pass
        return defecto

    def _cargar_datos(self):
        try:
            # 1. Cargar configuraciones simples
            self.cursor.execute("SELECT clave, valor FROM config")
            for clave, valor in self.cursor.fetchall():
                val = json.loads(valor)
                if clave == "autores_seguidos": self.autores_seguidos = set(val)
                elif clave == "autores_respaldados": self.autores_respaldados = set(val)
                elif clave == "lapidas": self.lapidas = set(val)
                elif clave == "notificaciones_etiquetas": self.notificaciones_etiquetas = val
                elif clave == "etiquetas_revocadas": self.etiquetas_revocadas = val
                elif clave == "borradores": self.borradores = val
                elif clave == "respaldos_red": self.respaldos_red = val
                else:
                    if hasattr(self, clave):
                        setattr(self, clave, val)

            # 2. Cargar artículos
            self.cursor.execute("SELECT id, datos FROM articulos_propios")
            self.mis_articulos = {r[0]: json.loads(r[1]) for r in self.cursor.fetchall()}
            
            self.cursor.execute("SELECT id, datos FROM articulos_descubiertos")
            self.articulos_descubiertos = [json.loads(r[1]) for r in self.cursor.fetchall()]
            
            self.cursor.execute("SELECT id, datos FROM articulos_guardados")
            self.articulos_guardados = {r[0]: json.loads(r[1]) for r in self.cursor.fetchall()}
            
            # 3. Cargar perfiles
            self.cursor.execute("SELECT id, datos FROM perfiles")
            self.perfiles_autores = {r[0]: json.loads(r[1]) for r in self.cursor.fetchall()}
            
            # 4. Cargar colecciones
            self.cursor.execute("SELECT id, datos, es_propia FROM colecciones")
            for r in self.cursor.fetchall():
                if r[2] == 1: self.mis_colecciones[r[0]] = json.loads(r[1])
                else: self.colecciones_descubiertas[r[0]] = json.loads(r[1])
                
            # 5. Cargar llaves criptográficas
            sk_guardada = self._leer_kv("llave_privada", "")
            if sk_guardada:
                self.llave_privada = nacl.signing.SigningKey(sk_guardada.encode(), encoder=nacl.encoding.HexEncoder)
                self.llave_publica = self.llave_privada.verify_key.encode(encoder=nacl.encoding.HexEncoder).decode()
            else:
                self.llave_privada = nacl.signing.SigningKey.generate()
                self.llave_publica = self.llave_privada.verify_key.encode(encoder=nacl.encoding.HexEncoder).decode()
                self._guardar_kv("llave_privada", self.llave_privada.encode(encoder=nacl.encoding.HexEncoder).decode())
                
        except Exception as e:
            print(f"Error al cargar datos de SQLite: {e}")

    def _guardar_datos(self):
        if hasattr(self, '_save_timer') and self._save_timer:
            self.root.after_cancel(self._save_timer)
        self._save_timer = self.root.after(2000, self._ejecutar_guardado_real)

    def _ejecutar_guardado_real(self):
        self._save_timer = None
        if threading.current_thread() is not threading.main_thread():
            self.root.after(0, self._ejecutar_guardado_real)
            return
        try:
            # 1. Guardar Configuraciones
            config_data = {
                "nombre_usuario": self.nombre_usuario, "mi_descripcion": self.mi_descripcion,
                "mi_horario": self.mi_horario, "mi_utc_offset": self.mi_utc_offset,
                "limite_mb": self.limite_mb, "ancho_columnas": self.ancho_columnas,
                "autores_seguidos": list(self.autores_seguidos), "autores_respaldados": list(self.autores_respaldados),
                "lapidas": list(self.lapidas), "borradores": self.borradores,
                "notificaciones_etiquetas": self.notificaciones_etiquetas, "etiquetas_revocadas": self.etiquetas_revocadas,
                "respaldos_red": self.respaldos_red
            }
            for k, v in config_data.items():
                self.cursor.execute("INSERT OR REPLACE INTO config (clave, valor) VALUES (?, ?)", (k, json.dumps(v, ensure_ascii=False)))

            # 2. Guardar Artículos (y borrar los que ya no existen)
            for aid, art in self.mis_articulos.items():
                self.cursor.execute("INSERT OR REPLACE INTO articulos_propios (id, datos) VALUES (?, ?)", (aid, json.dumps(art, ensure_ascii=False)))
            ids_propios = list(self.mis_articulos.keys())
            if ids_propios:
                self.cursor.execute(f"DELETE FROM articulos_propios WHERE id NOT IN ({','.join('?' * len(ids_propios))})", ids_propios)
            else:
                self.cursor.execute("DELETE FROM articulos_propios")

            for art in self.articulos_descubiertos:
                self.cursor.execute("INSERT OR REPLACE INTO articulos_descubiertos (id, datos) VALUES (?, ?)", (art["id"], json.dumps(art, ensure_ascii=False)))
            ids_descubiertos = [a["id"] for a in self.articulos_descubiertos]
            if ids_descubiertos:
                self.cursor.execute(f"DELETE FROM articulos_descubiertos WHERE id NOT IN ({','.join('?' * len(ids_descubiertos))})", ids_descubiertos)
            else:
                self.cursor.execute("DELETE FROM articulos_descubiertos")

            for aid, art in self.articulos_guardados.items():
                self.cursor.execute("INSERT OR REPLACE INTO articulos_guardados (id, datos) VALUES (?, ?)", (aid, json.dumps(art, ensure_ascii=False)))
            ids_guardados = list(self.articulos_guardados.keys())
            if ids_guardados:
                self.cursor.execute(f"DELETE FROM articulos_guardados WHERE id NOT IN ({','.join('?' * len(ids_guardados))})", ids_guardados)
            else:
                self.cursor.execute("DELETE FROM articulos_guardados")

            # 3. Guardar Perfiles
            for pid, perfil in self.perfiles_autores.items():
                self.cursor.execute("INSERT OR REPLACE INTO perfiles (id, datos) VALUES (?, ?)", (pid, json.dumps(perfil, ensure_ascii=False)))
            
            # 4. Guardar Colecciones
            for cid, col in self.mis_colecciones.items():
                self.cursor.execute("INSERT OR REPLACE INTO colecciones (id, datos, es_propia) VALUES (?, ?, 1)", (cid, json.dumps(col, ensure_ascii=False)))
            for cid, col in self.colecciones_descubiertas.items():
                self.cursor.execute("INSERT OR REPLACE INTO colecciones (id, datos, es_propia) VALUES (?, ?, 0)", (cid, json.dumps(col, ensure_ascii=False)))

            self.conn.commit()
        except Exception as e:
            print(f"Error al guardar en SQLite: {e}")

    def _guardar_like_rapido(self, articulo_id):
        try:
            if articulo_id in self.mis_articulos:
                art = self.mis_articulos[articulo_id]
                self.cursor.execute("INSERT OR REPLACE INTO articulos_propios (id, datos) VALUES (?, ?)", (articulo_id, json.dumps(art, ensure_ascii=False)))
            for a in self.articulos_descubiertos:
                if a["id"] == articulo_id:
                    self.cursor.execute("INSERT OR REPLACE INTO articulos_descubiertos (id, datos) VALUES (?, ?)", (articulo_id, json.dumps(a, ensure_ascii=False)))
                    break
            if articulo_id in self.articulos_guardados:
                art = self.articulos_guardados[articulo_id]
                self.cursor.execute("INSERT OR REPLACE INTO articulos_guardados (id, datos) VALUES (?, ?)", (articulo_id, json.dumps(art, ensure_ascii=False)))
            self.conn.commit()
        except Exception as e:
            print(f"Error guardando like rápido: {e}")

    def _calcular_espacio_usado(self):
        total_bytes = 0
        for art in list(self.articulos_guardados.values()) + list(self.mis_articulos.values()):
            total_bytes += len(json.dumps(art, ensure_ascii=False).encode('utf-8'))
        return total_bytes / (1024 * 1024)

    def _actualizar_barra_espacio(self):
        usado = self._calcular_espacio_usado()
        porcentaje = min((usado / self.limite_mb) * 100, 100)
        self.barra_espacio['value'] = porcentaje
        self.label_espacio.config(text=f"{usado:.1f} MB / {self.limite_mb} MB")
        
        # getattr evita que la app se cierre si la variable no existe (como pasó en Debian)
        alerta_mostrada = getattr(self, 'alerta_espacio_mostrada', False)
        
        if porcentaje >= 90 and not alerta_mostrada:
            self.alerta_espacio_mostrada = True
            messagebox.showwarning("Almacenamiento casi lleno", 
                f"Has usado el {porcentaje:.0f}% de tu límite de almacenamiento.\n\n"
                "Te recomendamos borrar artículos o aumentar el límite en 'Mi espacio'.")
        elif porcentaje < 80:
            self.alerta_espacio_mostrada = False

    def _refrescar_todo_visual(self):
        self.entrada_nombre.delete(0, "end")
        self.entrada_nombre.insert(0, self.nombre_usuario)
        self.texto_desc_perfil.delete("1.0", "end")
        self.texto_desc_perfil.insert("1.0", self.mi_descripcion)
        self.entrada_horario.delete(0, "end")
        self.entrada_horario.insert(0, self.mi_horario)
        self._refrescar_guardados()
        self._refrescar_autores()
        self._aplicar_filtro()
        self._refrescar_recientes()
        self._actualizar_barra_espacio()
        self._refrescar_mis_articulos()
        self._refrescar_mis_colecciones()

    def _refrescar_mis_articulos(self):
        for item in self.lista_mis_articulos.get_children():
            self.lista_mis_articulos.delete(item)
        mis_arts = list(self.mis_articulos.values())
        mis_arts.sort(key=lambda x: x["id"], reverse=True)
        for art in mis_arts:
            self.lista_mis_articulos.insert("", "end", iid=art["id"], values=(art["titulo"], art.get("tematica", ""), art["id"]))

    def _abrir_dialogo_crear_coleccion(self):
        if not self.articulos_guardados:
            messagebox.showinfo("Sin artículos", "No tienes artículos guardados para crear una colección.")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Crear Nueva Colección")
        dialog.geometry("500x550")
        
        frame_btn = ttk.Frame(dialog)
        frame_btn.pack(side="bottom", fill="x", pady=10)
        
        def guardar():
            titulo = entrada_titulo.get().strip()
            desc = texto_desc.get("1.0", "end-1c").strip()
            seleccion = lista.curselection()
            
            # --- CORRECCIÓN: Mensajes separados y precisos ---
            if not titulo:
                messagebox.showwarning("Falta título", "Debes ponerle un título a la colección.", parent=dialog)
                return
            if not seleccion:
                messagebox.showwarning("Falta selección", "Debes seleccionar al menos un artículo de la lista.", parent=dialog)
                return
            # -----------------------------------------------
                
            arts_seleccionados = [ids_guardados[i] for i in seleccion]
            col_id = f"col-{self.node.local_id[:6]}-{int(time.time())}"
            
            self.mis_colecciones[col_id] = {
                "id": col_id,
                "titulo": titulo,
                "descripcion": desc,
                "articulos": arts_seleccionados,
                "autor": self.node.local_id,
                "autor_nombre": self.nombre_usuario,
                "descargas": 0
            }
            self._guardar_datos()
            self._refrescar_mis_colecciones()
            dialog.destroy()
            messagebox.showinfo("Colección creada", f"La colección '{titulo}' ha sido creada con {len(arts_seleccionados)} artículos.")
            self._publicar_coleccion(col_id)
            
        ttk.Button(frame_btn, text="Guardar Colección", command=guardar).pack()

        ttk.Label(dialog, text="Título de la colección:").pack(anchor="w", padx=10, pady=(10,0))
        entrada_titulo = ttk.Entry(dialog)
        entrada_titulo.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(dialog, text="Descripción:").pack(anchor="w", padx=10)
        texto_desc = tk.Text(dialog, height=3, wrap="word")
        texto_desc.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(dialog, text="¿Cuáles de los artículos guardados quieres añadir a la nueva colección?:").pack(anchor="w", padx=10)
        lista = tk.Listbox(dialog, selectmode=tk.MULTIPLE, selectbackground="#4a6984", selectforeground="white")
        lista.pack(fill="both", expand=True, padx=10, pady=5)
        
        ids_guardados = list(self.articulos_guardados.keys())
        for aid in ids_guardados:
            art = self.articulos_guardados[aid]
            
            # --- CORRECCIÓN: Buscar el autor en los perfiles si no está guardado en el artículo ---
            autor_nombre = art.get("autor_nombre", "")
            if not autor_nombre:
                autor_id = art.get("autor", "")
                perfil = self.perfiles_autores.get(autor_id, {})
                autor_nombre = perfil.get("nombre", "Desconocido")
            # -----------------------------------------------------------------------------------
            
            lista.insert("end", f"{art['titulo']} (de {autor_nombre})")

    def _refrescar_mis_colecciones(self):
        if not hasattr(self, 'lista_mis_colecciones'): return
        for item in self.lista_mis_colecciones.get_children():
            self.lista_mis_colecciones.delete(item)
        
        # Obtener mi ID de forma segura (puede que el nodo aún no exista al arrancar)
        mi_id = getattr(self, 'node', None)
        mi_id = mi_id.local_id if mi_id else ""
        
        for col_id, col in self.mis_colecciones.items():
            display_title = col["titulo"]
            if col.get("autor") != mi_id:
                display_title = f"Col. de {col.get('autor_nombre', 'Desconocido')}: {display_title}"
            self.lista_mis_colecciones.insert("", "end", iid=col_id, values=(display_title, len(col["articulos"])))

    def _borrar_coleccion(self):
        sel = self.lista_mis_colecciones.selection()
        if not sel: return
        col_id = sel[0]
        titulo = self.mis_colecciones[col_id]["titulo"]
        
        if messagebox.askyesno("Borrar colección", f"¿Seguro que quieres borrar la colección '{titulo}'?\nLos artículos individuales seguirán en tus guardados."):
            del self.mis_colecciones[col_id]
            self._guardar_datos()
            self._refrescar_mis_colecciones()

    def _editar_coleccion_desde_lista(self):
        sel = self.lista_mis_colecciones.selection()
        if not sel: return
        self._editar_coleccion(sel[0])

    def _descargar_epub_desde_lista(self):
        sel = self.lista_mis_colecciones.selection()
        if not sel: 
            messagebox.showinfo("Sin selección", "Selecciona una colección de la lista para descargar.")
            return
        self._exportar_coleccion_epub(sel[0])

    def _abrir_coleccion_detalle_desde_mis_colecciones(self, event):
        item = self.lista_mis_colecciones.identify_row(event.y)
        if item:
            self._leer_coleccion(item)

    def _leer_coleccion(self, col_id):
        col = self.mis_colecciones.get(col_id) or self.colecciones_descubiertas.get(col_id)
        if not col or not col.get("articulos"):
            messagebox.showinfo("Colección vacía", "Esta colección no tiene artículos.")
            return
        
        self.coleccion_en_lectura = col
        self.indice_coleccion = 0
        self._nav_ir_a_articulo()

    def _nav_ir_a_articulo(self):
        if not self.coleccion_en_lectura: return
        arts = self.coleccion_en_lectura.get("articulos", [])
        if not arts: return
        
        # Asegurar que el índice esté en rango
        if self.indice_coleccion < 0: self.indice_coleccion = 0
        if self.indice_coleccion >= len(arts): self.indice_coleccion = len(arts) - 1
        
        aid = arts[self.indice_coleccion]
        
        # Abrir el artículo (el título mostrará la info de la colección automáticamente)
        self._abrir_por_id(aid, desde_coleccion=True)

    def _nav_coleccion_siguiente(self):
        if self.coleccion_en_lectura:
            self.indice_coleccion += 1
            self._nav_ir_a_articulo()

    def _nav_coleccion_anterior(self):
        if self.coleccion_en_lectura:
            self.indice_coleccion -= 1
            self._nav_ir_a_articulo()

    def _mostrar_autores_coleccion_actual(self):
        if not self.coleccion_en_lectura: return
        
        # 1. Recolectar todos los autores únicos de los artículos de la colección
        autores = {}  # Diccionario: {autor_id: autor_nombre}
        for aid in self.coleccion_en_lectura.get("articulos", []):
            art = self.mis_articulos.get(aid) or self.articulos_guardados.get(aid)
            if not art:
                art = next((a for a in self.articulos_descubiertos if a["id"] == aid), None)
                
            if art:
                autor_id = art.get("autor")
                autor_nombre = art.get("autor_nombre", "")
                
                if not autor_nombre and autor_id in self.perfiles_autores:
                    autor_nombre = self.perfiles_autores[autor_id].get("nombre", "Desconocido")
                    
                if autor_id:
                    autores[autor_id] = autor_nombre if autor_nombre else "Desconocido"
                    
        if not autores:
            messagebox.showinfo("Sin autores", "No se pudieron encontrar los autores de esta colección.")
            return
            
        # 2. Crear la ventana de diálogo
        dialog = tk.Toplevel(self.root)
        dialog.title("Autores de la colección")
        dialog.geometry("400x350")
        
        ttk.Label(dialog, text=f"Autores en '{self.coleccion_en_lectura['titulo']}'", font=("TkDefaultFont", 12, "bold")).pack(pady=10)
        
        listbox = tk.Listbox(dialog, selectbackground="#4a6984", selectforeground="white")
        listbox.pack(fill="both", expand=True, padx=20, pady=5)
        
        autor_ids = list(autores.keys())
        for aid in autor_ids:
            listbox.insert("end", autores[aid])
            
        def abrir_perfil(event):
            sel = listbox.curselection()
            if sel:
                autor_id = autor_ids[sel[0]]
                # Destruimos la ventana PRIMERO para que no se quede colgada
                dialog.destroy() 
                self._abrir_perfil_autor(autor_id)
                return "break" # Evita que el doble clic haga algo más por defecto
                
        # Doble clic para abrir el perfil del autor
        listbox.bind("<Double-1>", abrir_perfil)
        
        ttk.Button(dialog, text="Cerrar", command=dialog.destroy).pack(pady=10)

    def _al_doble_clic_autor_lectura(self, event):
        if hasattr(self, 'autor_articulo_actual') and self.autor_articulo_actual:
            self._abrir_perfil_autor(self.autor_articulo_actual)
            return "break"

    def _ver_curador_actual(self):
        if self.coleccion_en_lectura:
            self._abrir_perfil_autor(self.coleccion_en_lectura["autor"])

    def _descargar_epub_coleccion_actual(self):
        if self.coleccion_en_lectura:
            self._exportar_coleccion_epub(self.coleccion_en_lectura["id"])

    def _abrir_coleccion_detalle_desde_perfil(self, event):
        item = self.lista_colecciones_autor.identify_row(event.y)
        if item:
            self._leer_coleccion(item)

    def _mostrar_ventana_coleccion(self, col_id):
        col = self.mis_colecciones.get(col_id) or self.colecciones_descubiertas.get(col_id)
        if not col: return
        
        es_mia = (col.get("autor") == self.node.local_id)
        ya_importada = col_id in self.mis_colecciones
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Colección: {col['titulo']}")
        dialog.geometry("600x550")
        
        ttk.Label(dialog, text=col['titulo'], font=("TkDefaultFont", 16, "bold")).pack(pady=(10, 0))
        ttk.Label(dialog, text=f"Curada por: {col.get('autor_nombre', 'Desconocido')} | Descargas: {col.get('descargas', 0)}", font=("TkDefaultFont", 10, "italic")).pack(pady=(0, 10))
        
        texto_desc = tk.Text(dialog, height=3, wrap="word", bg="#f0f0f0", relief="flat")
        texto_desc.insert("1.0", col.get("descripcion", "Sin descripción."))
        texto_desc.config(state="disabled")
        texto_desc.pack(fill="x", padx=20, pady=5)
        
        ttk.Label(dialog, text="Artículos en esta colección (doble clic para leer individualmente):").pack(anchor="w", padx=20, pady=(10,0))
        lista_arts = tk.Listbox(dialog, height=10, selectbackground="#4a6984", selectforeground="white")
        lista_arts.pack(fill="both", expand=True, padx=20, pady=5)
        
        arts_ordenados = col.get("articulos", [])
        for aid in arts_ordenados:
            art_meta = self.mis_articulos.get(aid) or self.articulos_guardados.get(aid)
            if not art_meta:
                art_meta = next((a for a in self.articulos_descubiertos if a["id"] == aid), None)
            if art_meta:
                autor_orig = art_meta.get("autor_nombre", "Desconocido")
                lista_arts.insert("end", f"{art_meta['titulo']}  —  (Original de: {autor_orig})")
            else:
                lista_arts.insert("end", f"[Artículo no descargado] ID: {aid}")
                
        def leer_individual(event):
            sel = lista_arts.curselection()
            if sel:
                self._abrir_por_id(arts_ordenados[sel[0]])
                dialog.destroy()
        lista_arts.bind("<Double-1>", leer_individual)
                
        frame_btns = ttk.Frame(dialog)
        frame_btns.pack(pady=10)
        
        ttk.Button(frame_btns, text="▶ Leer Colección Completa", command=lambda: [self._leer_coleccion(col_id), dialog.destroy()]).pack(side="left", padx=5)
        ttk.Button(frame_btns, text="Descargar como EPUB", command=lambda: self._exportar_coleccion_epub(col_id)).pack(side="left", padx=5)
        
        if es_mia:
            ttk.Button(frame_btns, text="Editar", command=lambda: [dialog.destroy(), self._editar_coleccion(col_id)]).pack(side="left", padx=5)
        elif not ya_importada:
            ttk.Button(frame_btns, text="Añadir a mi espacio", command=lambda: [self._importar_coleccion(col_id), dialog.destroy()]).pack(side="left", padx=5)
        else:
            ttk.Label(frame_btns, text="Ya está en tu espacio", foreground="green").pack(side="left", padx=5)
            
        ttk.Button(frame_btns, text="Cerrar", command=dialog.destroy).pack(side="left", padx=5)

    def _exportar_coleccion_epub(self, col_id):
        col = self.mis_colecciones.get(col_id) or self.colecciones_descubiertas.get(col_id)
        if not col: return
        
        ruta = filedialog.asksaveasfilename(
            defaultextension=".epub", 
            filetypes=[("EPUB", "*.epub")], 
            title="Guardar colección como libro",
            initialfile=f"{col['titulo']}.epub"
        )
        if not ruta: return

        try:
            libro = epub.EpubBook()
            libro.set_identifier(f"col_{col_id}")
            libro.set_title(col['titulo'])
            libro.set_language(self.lang_code)
            libro.add_author(col.get('autor_nombre', self.nombre_usuario))

            capitulos = []
            for i, aid in enumerate(col.get("articulos", [])):
                art = self.mis_articulos.get(aid) or self.articulos_guardados.get(aid)
                if not art: continue
                if aid in self.articulos_descubiertos:
                    art = next((a for a in self.articulos_descubiertos if a["id"] == aid), art)

                titulo = art.get("titulo", "Sin título")
                autor_orig = art.get("autor_nombre", "Desconocido")
                contenido = art.get("contenido", {})
                texto = contenido.get("texto", "") if isinstance(contenido, dict) else str(contenido)
                imagenes = contenido.get("imagenes", {}) if isinstance(contenido, dict) else {}
                
                html = f"<h1>{titulo}</h1><p><i>Original de: {autor_orig}</i></p>"
                for img_id, b64 in imagenes.items():
                    texto = texto.replace(f"[{img_id}]", f'<br/><img src="data:image/png;base64,{b64}" style="max-width:100%;" /><br/>')
                
                for p in texto.split('\n'):
                    if p.strip(): html += f"<p>{p}</p>"
                
                c = epub.EpubHtml(title=titulo, file_name=f'cap_{i}.xhtml', lang=self.lang_code)
                c.content = html
                libro.add_item(c)
                capitulos.append(c)

            libro.toc = tuple(capitulos)
            libro.add_item(epub.EpubNcx())
            libro.add_item(epub.EpubNav())
            libro.spine = ['nav'] + capitulos
            epub.write_epub(ruta, libro, {})
            messagebox.showinfo("Exportado", f"Colección exportada con éxito en:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el libro:\n{e}")


    def _editar_coleccion(self, col_id):
        if col_id not in self.mis_colecciones: return
        col = self.mis_colecciones[col_id]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Editar Colección")
        dialog.geometry("500x550")
        
        frame_btn = ttk.Frame(dialog)
        frame_btn.pack(side="bottom", fill="x", pady=10)
        
        def guardar():
            titulo = entrada_titulo.get().strip()
            desc = texto_desc.get("1.0", "end-1c").strip()
            seleccion = lista.curselection()
            
            if not titulo:
                messagebox.showwarning("Falta título", "Debes ponerle un título a la colección.", parent=dialog)
                return
            if not seleccion:
                messagebox.showwarning("Falta selección", "Debes seleccionar al menos un artículo.", parent=dialog)
                return
                
            arts_seleccionados = [ids_guardados[i] for i in seleccion]
            
            self.mis_colecciones[col_id]["titulo"] = titulo
            self.mis_colecciones[col_id]["descripcion"] = desc
            self.mis_colecciones[col_id]["articulos"] = arts_seleccionados
            
            self._guardar_datos()
            self._refrescar_mis_colecciones()
            self._publicar_coleccion(col_id)
            dialog.destroy()
            messagebox.showinfo("Colección actualizada", "Los cambios han sido guardados y publicados.")
            
        ttk.Button(frame_btn, text="Guardar Cambios", command=guardar).pack()

        ttk.Label(dialog, text="Título de la colección:").pack(anchor="w", padx=10, pady=(10,0))
        entrada_titulo = ttk.Entry(dialog)
        entrada_titulo.insert(0, col["titulo"])
        entrada_titulo.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(dialog, text="Descripción:").pack(anchor="w", padx=10)
        texto_desc = tk.Text(dialog, height=3, wrap="word")
        texto_desc.insert("1.0", col.get("descripcion", ""))
        texto_desc.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(dialog, text="Selecciona los artículos (Ctrl o Shift para varios):").pack(anchor="w", padx=10)
        lista = tk.Listbox(dialog, selectmode=tk.MULTIPLE, selectbackground="#4a6984", selectforeground="white")
        lista.pack(fill="both", expand=True, padx=10, pady=5)
        
        ids_guardados = list(self.articulos_guardados.keys())
        arts_actuales = col.get("articulos", [])
        
        for i, aid in enumerate(ids_guardados):
            art = self.articulos_guardados[aid]
            autor_nombre = art.get("autor_nombre", "")
            if not autor_nombre:
                perfil = self.perfiles_autores.get(art.get("autor", ""), {})
                autor_nombre = perfil.get("nombre", "Desconocido")
            lista.insert("end", f"{art['titulo']} (de {autor_nombre})")
            if aid in arts_actuales:
                lista.selection_set(i)

    def _menu_contextual_mis_articulos(self, event):
        # Identificar qué fila se ha clickeado con el botón derecho
        item = self.lista_mis_articulos.identify_row(event.y)
        if item:
            # Seleccionar la fila visualmente para que el usuario sepa cuál está eligiendo
            self.lista_mis_articulos.selection_set(item)
            
            # Establecer el ID como el artículo actual para que las funciones de editar y borrar actúen sobre él
            self.articulo_actual_id = item
            
            # Crear el menú
            menu = tk.Menu(self.root, tearoff=0)
            menu.add_command(label="Editar", command=self._preparar_edicion)
            menu.add_command(label="Borrar", command=self._borrar_mi_articulo)
            
            # Mostrar el menú en la posición del ratón
            menu.tk_popup(event.x_root, event.y_root)


    def _abrir_mi_articulo_doble_clic(self, event):
        item = self.lista_mis_articulos.identify_row(event.y)
        if item:
            self.lista_mis_articulos.selection_set(item)
            self._abrir_por_id(item)

    def _firmar_mensaje(self, diccionario):
        """Firma un diccionario con la llave privada del usuario."""
        if not self.llave_privada: return ""
        # Convertimos el diccionario a texto ordenado para que la firma sea exacta
        mensaje_bytes = json.dumps(diccionario, sort_keys=True).encode('utf-8')
        signed = self.llave_privada.sign(mensaje_bytes)
        return signed.signature.hex()

    def _verificar_firma(self, diccionario, firma_hex, llave_publica_hex):
        """Verifica si la firma coincide con el mensaje y la llave pública."""
        if not firma_hex or not llave_publica_hex: return False
        try:
            vk = nacl.signing.VerifyKey(llave_publica_hex.encode(), encoder=nacl.encoding.HexEncoder)
            mensaje_bytes = json.dumps(diccionario, sort_keys=True).encode('utf-8')
            vk.verify(mensaje_bytes, bytes.fromhex(firma_hex))
            return True
        except Exception:
            return False

    def _t(self, texto):
        return TRADUCCIONES.get(self.lang_code, TRADUCCIONES["es"]).get(texto, texto)

    # ------------------------------------------------------------------
    # CONSTRUCCIÓN DE LA INTERFAZ
    # ------------------------------------------------------------------
    def _construir_interfaz(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)
        self._construir_tab_descubrir()
        self._construir_tab_leyendo()
        self._construir_tab_publicar()
        self._construir_tab_mi_espacio()
        self._construir_tab_autores()
        self._construir_tab_notificaciones()  # <-- NUEVA LÍNEA

    def _toggle_suscripcion_oficial(self):
        self.suscrito_oficial = self.var_suscrito.get()
        self._guardar_datos()
        if self.suscrito_oficial:
            self.autores_seguidos.add(ID_FUNDADOR)
            print("⭐ Suscrito al blog oficial.")
        else:
            self.autores_seguidos.discard(ID_FUNDADOR)
            print("❌ Desuscrito del blog oficial.")
        self._refrescar_autores()
        self._refrescar_recientes()

    def _construir_tab_descubrir(self):
        self.tab_descubrir = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_descubrir, text=self._t("Descubrir"))

        # Filtros
        frame_filtros = ttk.Frame(self.tab_descubrir)
        frame_filtros.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame_filtros, text=self._t("Categoría:")).pack(side="left")
        self.combo_filtro_categoria = ttk.Combobox(frame_filtros, values=[self._t("Todas")] + TEMATICAS, state="readonly", width=15)
        self.combo_filtro_categoria.current(0)
        self.combo_filtro_categoria.pack(side="left", padx=5)
        self.combo_filtro_categoria.bind("<<ComboboxSelected>>", lambda e: self._reiniciar_paginacion())

        ttk.Label(frame_filtros, text=self._t("Etiqueta:")).pack(side="left", padx=(15, 0))
        self.entrada_filtro = ttk.Entry(frame_filtros, width=20)
        self.entrada_filtro.pack(side="left", padx=5)
        self._configurar_portapapeles(self.entrada_filtro)

        ttk.Label(frame_filtros, text=self._t("Idioma:")).pack(side="left", padx=(15, 0))
        self.combo_filtro_idioma = ttk.Combobox(frame_filtros, values=[self._t("Todos")] + IDIOMAS, state="readonly", width=12)
        self.combo_filtro_idioma.current(0)
        self.combo_filtro_idioma.pack(side="left", padx=5)
        self.combo_filtro_idioma.bind("<<ComboboxSelected>>", lambda e: self._reiniciar_paginacion())

        ttk.Button(frame_filtros, text=self._t("Buscar"), command=self._reiniciar_paginacion).pack(side="left", padx=5)
        ttk.Button(frame_filtros, text="¡Sorpréndeme!", command=self._sorprendeme).pack(side="left", padx=(15, 0))

        # Lienzo y Barra de Desplazamiento (Scroll)
        frame_scroll = ttk.Frame(self.tab_descubrir)
        frame_scroll.pack(fill="both", expand=True, padx=10, pady=5)

        # yscrollincrement=15 define que cada paso del scroll son 15 píxeles (muy fluido)
        self.canvas_descubrir = tk.Canvas(frame_scroll, bg="#f9f9f9", highlightthickness=0, yscrollincrement=15)
        scrollbar = ttk.Scrollbar(frame_scroll, orient="vertical", command=self.canvas_descubrir.yview)
        self.frame_tarjetas = ttk.Frame(self.canvas_descubrir)

        self.frame_tarjetas.bind(
            "<Configure>",
            lambda e: self.canvas_descubrir.configure(scrollregion=self.canvas_descubrir.bbox("all"))
        )
        self.canvas_window = self.canvas_descubrir.create_window((0, 0), window=self.frame_tarjetas, anchor="nw")
        self.canvas_descubrir.configure(yscrollcommand=scrollbar.set)

        self.canvas_descubrir.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Ajustar el ancho del frame interno al ancho del canvas
        self.canvas_descubrir.bind('<Configure>', lambda e: self.canvas_descubrir.itemconfig(self.canvas_window, width=e.width))
        # Soporte para rueda del ratón (Smooth Scroll para Linux y Windows)
        self.canvas_descubrir.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas_descubrir.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas_descubrir.bind_all("<Button-5>", self._on_mousewheel)

        # Paginación
        frame_paginacion = ttk.Frame(self.tab_descubrir)
        frame_paginacion.pack(fill="x", padx=5, pady=5)
        self.btn_pag_anterior = ttk.Button(frame_paginacion, text="◀ Anterior", command=self._pagina_anterior)
        self.btn_pag_anterior.pack(side="left", padx=10)
        self.lbl_paginacion = ttk.Label(frame_paginacion, text="Página 1 de 1", font=("TkDefaultFont", 10, "bold"))
        self.lbl_paginacion.pack(side="left", expand=True)
        self.btn_pag_siguiente = ttk.Button(frame_paginacion, text="Siguiente ▶", command=self._pagina_siguiente)
        self.btn_pag_siguiente.pack(side="right", padx=10)
        
        # Lista para mantener referencias a las imágenes y que no se borren de la memoria
        self.imagenes_tarjetas = []

    def _on_mousewheel(self, event):
        # Al haber definido yscrollincrement=15, un paso del scroll moverá 15 píxeles.
        if event.num == 4: # Scroll Up (Linux)
            self.canvas_descubrir.yview_scroll(-1, "units")
        elif event.num == 5: # Scroll Down (Linux)
            self.canvas_descubrir.yview_scroll(1, "units")
        else: # Windows / Mac
            self.canvas_descubrir.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _configurar_etiquetas_texto(self, text_widget):
        f_bold = font.Font(family="Helvetica", size=13, weight="bold")
        f_italic = font.Font(family="Helvetica", size=13, slant="italic")
        f_underline = font.Font(family="Helvetica", size=13, underline=True)
        text_widget.tag_configure("bold", font=f_bold)
        text_widget.tag_configure("italic", font=f_italic)
        text_widget.tag_configure("underline", font=f_underline)
        text_widget.tag_configure("center", justify="center")

    def _crear_barra_formato(self, parent, text_widget):
        self._configurar_etiquetas_texto(text_widget)
        barra = ttk.Frame(parent)

        def toggle_tag(tag):
            try:
                start = text_widget.index("sel.first")
                end = text_widget.index("sel.last")
                if tag in text_widget.tag_names("sel.first"):
                    text_widget.tag_remove(tag, start, end)
                else:
                    text_widget.tag_add(tag, start, end)
                    text_widget.tag_raise(tag)
            except tk.TclError:
                if tag in text_widget.tag_names("insert"):
                    text_widget.tag_remove(tag, "insert")
                else:
                    text_widget.tag_add(tag, "insert")
                    text_widget.tag_raise(tag)

        def apply_font(family, size):
            # Quitar cualquier tag de fuente anterior para que no se acumulen
            for t in text_widget.tag_names():
                if t.startswith("font_") or t in ["h1_tag", "h2_tag"]:
                    try:
                        start = text_widget.index("sel.first")
                        end = text_widget.index("sel.last")
                        text_widget.tag_remove(t, start, end)
                    except tk.TclError:
                        text_widget.tag_remove(t, "insert")
            
            tag_name = f"font_{family}_{size}"
            text_widget.tag_configure(tag_name, font=(family, int(size)))
            try:
                start = text_widget.index("sel.first")
                end = text_widget.index("sel.last")
            except tk.TclError:
                start = "insert"
                end = "insert"
            text_widget.tag_add(tag_name, start, end)

        def apply_align(align):
            tag_name = f"align_{align}"
            text_widget.tag_configure(tag_name, justify=align)
            try:
                start = text_widget.index("sel.first")
                end = text_widget.index("sel.last")
            except tk.TclError:
                linea = text_widget.index("insert").split(".")[0]
                start = f"{linea}.0"
                end = f"{linea}.end"
            
            primera_linea = start.split(".")[0]
            ultima_linea = end.split(".")[0]
            start_completo = f"{primera_linea}.0"
            end_completo = f"{ultima_linea}.end"
            
            text_widget.tag_add(tag_name, start_completo, end_completo)
            text_widget.tag_raise(tag_name)

        def apply_h1():
            apply_font("Helvetica", 28)
            text_widget.tag_configure("h1_tag", font=("Helvetica", 28, "bold"))
            try:
                start = text_widget.index("sel.first")
                end = text_widget.index("sel.last")
            except tk.TclError:
                start = "insert"
                end = "insert"
            text_widget.tag_remove("bold", start, end) # Evitar conflicto
            text_widget.tag_add("h1_tag", start, end)

        def apply_h2():
            apply_font("Helvetica", 20)
            text_widget.tag_configure("h2_tag", font=("Helvetica", 20, "bold"))
            try:
                start = text_widget.index("sel.first")
                end = text_widget.index("sel.last")
            except tk.TclError:
                start = "insert"
                end = "insert"
            text_widget.tag_remove("bold", start, end)
            text_widget.tag_add("h2_tag", start, end)

        def clear_format():
            # Quita TODOS los tags de la selección, volviendo al texto normal
            try:
                start = text_widget.index("sel.first")
                end = text_widget.index("sel.last")
            except tk.TclError:
                start = "insert"
                end = "insert"
                
            for tag in text_widget.tag_names():
                if tag != "sel":
                    text_widget.tag_remove(tag, start, end)

        # 1. Deshacer / Rehacer
        ttk.Button(barra, text="↶", width=3, command=lambda: text_widget.edit_undo()).pack(side="left", padx=2)
        ttk.Button(barra, text="↷", width=3, command=lambda: text_widget.edit_redo()).pack(side="left", padx=2)
        
        ttk.Separator(barra, orient="vertical").pack(side="left", fill="y", padx=5)

        # 2. Negrita, Cursiva, Subrayado, Normal
        ttk.Button(barra, text="N", width=3, command=lambda: toggle_tag("bold")).pack(side="left", padx=2)
        ttk.Button(barra, text="K", width=3, command=lambda: toggle_tag("italic")).pack(side="left", padx=2)
        ttk.Button(barra, text="S", width=3, command=lambda: toggle_tag("underline")).pack(side="left", padx=2)
        ttk.Button(barra, text="Normal", command=clear_format).pack(side="left", padx=2)

        ttk.Separator(barra, orient="vertical").pack(side="left", fill="y", padx=5)

        # 3. Fuente y Tamaño
        fuentes = ["Helvetica", "Times", "Courier", "Arial", "Verdana"]
        combo_fuente = ttk.Combobox(barra, values=fuentes, width=10, state="readonly")
        combo_fuente.set("Helvetica")
        combo_fuente.pack(side="left", padx=2)

        tamanos = ["10", "12", "14", "16", "18", "24", "32"]
        combo_tamano = ttk.Combobox(barra, values=tamanos, width=4, state="readonly")
        combo_tamano.set("13")
        combo_tamano.pack(side="left", padx=2)

        ttk.Button(barra, text="Aplicar", command=lambda: apply_font(combo_fuente.get(), combo_tamano.get())).pack(side="left", padx=2)

        ttk.Separator(barra, orient="vertical").pack(side="left", fill="y", padx=5)

        # 4. Títulos (H1, H2)
        ttk.Button(barra, text="H1", width=3, command=apply_h1).pack(side="left", padx=2)
        ttk.Button(barra, text="H2", width=3, command=apply_h2).pack(side="left", padx=2)

        ttk.Separator(barra, orient="vertical").pack(side="left", fill="y", padx=5)

        # 5. Alineación
        ttk.Button(barra, text="Izq", width=3, command=lambda: apply_align("left")).pack(side="left", padx=2)
        ttk.Button(barra, text="Cen", width=3, command=lambda: apply_align("center")).pack(side="left", padx=2)

        ttk.Separator(barra, orient="vertical").pack(side="left", fill="y", padx=5)

        # 6. Imagen
        ttk.Button(barra, text="Imagen", command=self._insertar_imagen).pack(side="left", padx=2)
        
        return barra

    def _insertar_imagen(self):
        ruta = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if not ruta: return
        try:
            img = Image.open(ruta)
            if img.width > 600:
                ratio = 600 / img.width
                img = img.resize((600, int(img.height * ratio)), Image.Resampling.LANCZOS)
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
            
            self.contador_imagenes += 1
            img_id = f"IMG_{self.contador_imagenes}"
            self.imagenes_temporales[img_id] = img_b64
            self.texto_contenido.insert("insert", f"\n[{img_id}]\n")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen:\n{e}")

    def _construir_tab_publicar(self):
        self.tab_publicar = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_publicar, text=self._t("Redactar"))

        frame_centrado = ttk.Frame(self.tab_publicar)
        frame_centrado.pack(expand=True, fill="both", padx=10, pady=10)
        
        frame_form = ttk.Frame(frame_centrado)
        frame_form.pack(expand=True, fill="both")

        ttk.Label(frame_form, text=self._t("Título:")).grid(row=0, column=0, sticky="w", pady=5)
        self.entrada_titulo = ttk.Entry(frame_form, width=self.ancho_columnas)
        self.entrada_titulo.grid(row=0, column=1, sticky="ew", pady=5)
        self._configurar_portapapeles(self.entrada_titulo)

        ttk.Label(frame_form, text=self._t("Etiquetas:")).grid(row=1, column=0, sticky="w", pady=5)
        self.entrada_etiqueta = ttk.Entry(frame_form, width=self.ancho_columnas)
        self.entrada_etiqueta.grid(row=1, column=1, sticky="w", pady=5)
        self._configurar_portapapeles(self.entrada_etiqueta)

        ttk.Label(frame_form, text=self._t("Categoría:")).grid(row=2, column=0, sticky="w", pady=5)
        self.combo_tematica = ttk.Combobox(frame_form, values=TEMATICAS, state="readonly", width=30)
        self.combo_tematica.grid(row=2, column=1, sticky="w", pady=5)
        self.combo_tematica.current(0)

        ttk.Label(frame_form, text=self._t("Idioma del artículo:")).grid(row=3, column=0, sticky="w", pady=5)
        self.combo_idioma_publicar = ttk.Combobox(frame_form, values=[self._t("Automático")] + IDIOMAS, state="readonly", width=30)
        self.combo_idioma_publicar.current(0)
        self.combo_idioma_publicar.grid(row=3, column=1, sticky="w", pady=5)

        ttk.Label(frame_form, text=self._t("Contenido:")).grid(row=4, column=0, sticky="nw", pady=5)
        
        frame_contenido = ttk.Frame(frame_form)
        frame_contenido.grid(row=4, column=1, sticky="nsew", pady=5)
        
        self.frame_barra_top = ttk.Frame(frame_contenido)
        self.frame_barra_top.pack(side="top", fill="x", pady=(0, 2), padx=self.margen_texto)

        # LA MAGIA: Caja ancha, texto con márgenes
        self.texto_contenido = tk.Text(frame_contenido, width=1, height=20, wrap="word", 
                                       bg="white", fg="black", font=("Helvetica", 13), insertbackground="black", relief="solid", bd=1,
                                       padx=self.margen_texto, pady=15, undo=True) # <-- AÑADIR undo=True
        self.texto_contenido.pack(side="bottom", fill="both", expand=True)
        self._configurar_portapapeles(self.texto_contenido)

        barra = self._crear_barra_formato(self.frame_barra_top, self.texto_contenido)
        barra.pack(side="left")
        
        ttk.Button(self.frame_barra_top, text="-", width=3, command=lambda: self._ajustar_ancho(-10)).pack(side="left", padx=2)
        ttk.Label(self.frame_barra_top, text="Márgenes:").pack(side="left", padx=2)
        ttk.Button(self.frame_barra_top, text="+", width=3, command=lambda: self._ajustar_ancho(10)).pack(side="left", padx=2)

        frame_btns_publicar = ttk.Frame(frame_form)
        frame_btns_publicar.grid(row=5, column=1, sticky="e", pady=10)
        
        ttk.Button(frame_btns_publicar, text="Cargar Borrador", command=self._mostrar_dialogo_borradores).pack(side="left", padx=5)
        ttk.Button(frame_btns_publicar, text="Guardar Borrador", command=self._guardar_borrador).pack(side="left", padx=5)
        
        self.btn_publicar = ttk.Button(frame_btns_publicar, text=self._t("Publicar artículo"), command=self._publicar_articulo)
        self.btn_publicar.pack(side="left", padx=5)

        frame_form.columnconfigure(1, weight=1)
        frame_form.rowconfigure(4, weight=1)

    def _construir_tab_leyendo(self):
        self.tab_leyendo = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_leyendo, text=self._t("Leyendo"))

        self.tab_leyendo.columnconfigure(0, weight=0, minsize=260) 
        self.tab_leyendo.columnconfigure(1, weight=1)             
        self.tab_leyendo.rowconfigure(0, weight=1)

        frame_izq = ttk.Frame(self.tab_leyendo)
        frame_izq.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        frame_izq.columnconfigure(0, weight=1)
        
        # LA MAGIA: Hacemos que las 3 filas de las listas (3, 5 y 8) compartan el espacio equitativamente
        frame_izq.rowconfigure(3, weight=1) # Fila de Autores
        frame_izq.rowconfigure(5, weight=1) # Fila de Guardados
        frame_izq.rowconfigure(8, weight=1) # Fila de Recientes

        fila = 0
        ttk.Label(frame_izq, text=self._t("Almacenamiento"), font=("TkDefaultFont", 10, "bold")).grid(row=fila, column=0, sticky="w"); fila+=1
        
        frame_espacio = ttk.Frame(frame_izq)
        frame_espacio.grid(row=fila, column=0, sticky="ew", pady=(2, 10)); fila+=1
        self.label_espacio = ttk.Label(frame_espacio, text="0 MB / 100 MB")
        self.label_espacio.pack(anchor="w")
        self.barra_espacio = ttk.Progressbar(frame_espacio, orient="horizontal", mode="determinate", maximum=100)
        self.barra_espacio.pack(fill="x", pady=(2, 2))
        ttk.Button(frame_espacio, text=self._t("Cambiar límite"), command=self._cambiar_limite).pack(anchor="e")

        ttk.Label(frame_izq, text=self._t("Autores seguidos"), font=("TkDefaultFont", 10, "bold")).grid(row=fila, column=0, sticky="w"); fila+=1
        self.lista_autores = tk.Listbox(frame_izq, height=1) # Altura inicial mínima
        self.lista_autores.grid(row=fila, column=0, sticky="nsew", pady=(2, 10)); fila+=1
        self.lista_autores.bind("<<ListboxSelect>>", self._al_seleccionar_autor)
        self.lista_autores.bind("<Double-1>", self._abrir_autor_seleccionado_doble_clic)

        ttk.Label(frame_izq, text=self._t("Artículos guardados"), font=("TkDefaultFont", 10, "bold")).grid(row=fila, column=0, sticky="w"); fila+=1
        self.lista_guardados = tk.Listbox(frame_izq, height=1) # Altura inicial mínima
        self.lista_guardados.grid(row=fila, column=0, sticky="nsew", pady=(2, 5)); fila+=1
        self.lista_guardados.bind("<Double-1>", self._abrir_guardado_doble_clic)
        
        frame_btn_borrar = ttk.Frame(frame_izq)
        frame_btn_borrar.grid(row=fila, column=0, sticky="ew", pady=(0, 10)); fila+=1
        ttk.Button(frame_btn_borrar, text="Borrar", command=self._borrar_guardado).pack(side="left", padx=2)
        ttk.Button(frame_btn_borrar, text="Exportar EPUB", command=self._exportar_epub).pack(side="right", padx=2)

        self.etiqueta_titulo_recientes = ttk.Label(frame_izq, text=self._t("Recientes de seguidos"), font=("TkDefaultFont", 10, "bold"))
        self.etiqueta_titulo_recientes.grid(row=fila, column=0, sticky="w"); fila+=1
        
        self.lista_recientes = tk.Listbox(frame_izq, height=1) # Altura inicial mínima
        self.lista_recientes.grid(row=fila, column=0, sticky="nsew", pady=(2, 0))
        self.lista_recientes.bind("<Double-1>", self._abrir_reciente_doble_clic)

        frame_centro = ttk.Frame(self.tab_leyendo)
        frame_centro.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        
        # NUEVO: Contenedor fijo para el título y las métricas (FORZADO AL TOP)
        self.frame_header_lectura = ttk.Frame(frame_centro)
        self.frame_header_lectura.pack(side="top", fill="x", pady=(5, 5))

        self.etiqueta_titulo_lectura = ttk.Label(self.frame_header_lectura, text=self._t("Doble clic para leer"), font=("TkDefaultFont", 14, "bold"), wraplength=800, justify="center")
        self.etiqueta_titulo_lectura.pack(anchor="center")
        
        self.lbl_metricas_respaldo = tk.Label(self.frame_header_lectura, text="", font=("TkDefaultFont", 10, "bold"), fg="#0d5c1d", bg="#d4edda", padx=10, pady=3, relief="solid", bd=1)
        self.lbl_metricas_respaldo.pack(pady=(5, 0))

        # Ya no usamos frame_coleccion_nav arriba, todo irá abajo
        self.frame_coleccion_nav = ttk.Frame(frame_centro) 

        self.texto_lectura = tk.Text(frame_centro, width=1, height=1, wrap="word", 
                                     bg="white", fg="black", font=("Helvetica", 13), relief="solid", bd=1, state="disabled",
                                     padx=self.margen_texto, pady=0)
        self.texto_lectura.pack(side="top", fill="both", expand=True)
        self._configurar_etiquetas_texto(self.texto_lectura)
        self.texto_lectura.tag_configure("autor_link", foreground="#005a9e", underline=True)
        self.texto_lectura.tag_bind("autor_link", "<Double-1>", self._al_doble_clic_autor_lectura)
        self._configurar_portapapeles_lectura(self.texto_lectura)

        # Barra inferior unificada con TODOS los botones (se empaquetarán dinámicamente)
        self.frame_botones_lectura = ttk.Frame(frame_centro)
        self.frame_botones_lectura.pack(side="bottom", pady=10, padx=10, anchor="center")
        
        # 1. Botones de Artículo Normal
        self.btn_guardar = ttk.Button(self.frame_botones_lectura, text="Guardar", command=self._guardar_articulo_actual)
        self.btn_editar = ttk.Button(self.frame_botones_lectura, text="Editar", command=self._preparar_edicion)
        self.btn_borrar = ttk.Button(self.frame_botones_lectura, text="Borrar", command=self._borrar_mi_articulo)
        self.btn_seguir = ttk.Button(self.frame_botones_lectura, text="Seguir autor", command=self._seguir_autor_actual)
        self.btn_seguir_resp = ttk.Button(self.frame_botones_lectura, text="Seguir y Respaldar", command=self._seguir_y_respaldar)
        self.btn_ver_autor = ttk.Button(self.frame_botones_lectura, text="Ver autor", command=self._ver_perfil_actual)
        self.btn_quitar_etiqueta = tk.Button(self.frame_botones_lectura, text="Quitarme la etiqueta", bg="#d9534f", fg="white", font=("TkDefaultFont", 9, "bold"), command=self._quitar_etiqueta_actual)

        # 2. Likes
        self.lbl_heart = tk.Label(self.frame_botones_lectura, text="★", font=("Segoe UI Symbol", 18), fg="#D4AF37", cursor="hand2")
        self.lbl_count = tk.Label(self.frame_botones_lectura, text="(0)", font=("Helvetica", 13, "bold"), fg="black", cursor="hand2")
        self.lbl_heart.bind("<Button-1>", self._dar_me_gusta)
        self.lbl_count.bind("<Button-1>", self._dar_me_gusta)

        # 3. Márgenes
        self.lbl_margenes = ttk.Label(self.frame_botones_lectura, text="Márgenes:")
        self.btn_margen_menos = ttk.Button(self.frame_botones_lectura, text="-", width=3, command=lambda: self._ajustar_ancho(-10))
        self.btn_margen_mas = ttk.Button(self.frame_botones_lectura, text="+", width=3, command=lambda: self._ajustar_ancho(10))

        # 4. Botones de Colección
        self.btn_ver_curador = ttk.Button(self.frame_botones_lectura, text="Ver curador", command=self._ver_curador_actual)
        self.btn_art_anterior = ttk.Button(self.frame_botones_lectura, text="◀ Artículo anterior", command=self._nav_coleccion_anterior)
        self.btn_art_siguiente = ttk.Button(self.frame_botones_lectura, text="Artículo siguiente ▶", command=self._nav_coleccion_siguiente)
        self.btn_descargar_epub_col = ttk.Button(self.frame_botones_lectura, text="Descargar como EPUB", command=self._descargar_epub_coleccion_actual)
        self.btn_autores_coleccion = ttk.Button(self.frame_botones_lectura, text="Autores de la colección", command=self._mostrar_autores_coleccion_actual)

    def _construir_tab_mi_espacio(self):
        self.tab_mi_espacio = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_mi_espacio, text=self._t("Mi espacio"))

        self.tab_mi_espacio.columnconfigure(0, weight=3)
        self.tab_mi_espacio.columnconfigure(1, weight=2)
        self.tab_mi_espacio.rowconfigure(0, weight=1)

        # --- COLUMNA IZQUIERDA: PERFIL Y ARTÍCULOS ---
        frame_izq = ttk.Frame(self.tab_mi_espacio)
        frame_izq.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=10)

        frame_perfil = ttk.Frame(frame_izq)
        frame_perfil.pack(fill="x", pady=(0, 10))
        
        ttk.Label(frame_perfil, text=self._t("Mi perfil"), font=("TkDefaultFont", 14, "bold")).pack(anchor="w")
        
        frame_nombre = ttk.Frame(frame_perfil)
        frame_nombre.pack(fill="x", pady=5)
        ttk.Label(frame_nombre, text=self._t("Nombre:")).pack(side="left")
        self.entrada_nombre = ttk.Entry(frame_nombre)
        self.entrada_nombre.pack(side="left", fill="x", expand=True, padx=5)
        self._configurar_portapapeles(self.entrada_nombre)
        ttk.Label(frame_perfil, text=self._t("Descripción:")).pack(anchor="w")
        self.texto_desc_perfil = tk.Text(frame_perfil, height=3, wrap="word", bg="white", fg="black", font=("Helvetica", 10))
        self.texto_desc_perfil.pack(fill="x", pady=(0, 5))
        self._configurar_portapapeles(self.texto_desc_perfil)
        ttk.Label(frame_perfil, text="Horario de conexión (ej. 18:00 - 22:00):").pack(anchor="w")
        self.entrada_horario = ttk.Entry(frame_perfil)
        self.entrada_horario.pack(fill="x", pady=(0, 5))
        self._configurar_portapapeles(self.entrada_horario)
        
        tip_gmt = ttk.Label(frame_perfil, text="El sistema traducirá esta hora automáticamente a la hora local de quien visite tu perfil.", font=("TkDefaultFont", 9, "italic"), foreground="#555555")
        tip_gmt.pack(anchor="w", pady=(0, 10))

        ttk.Button(frame_perfil, text=self._t("Guardar Perfil"), command=self._actualizar_nombre).pack(anchor="e")

        ttk.Label(frame_izq, text=self._t("Mis artículos publicados"), font=("TkDefaultFont", 12, "bold")).pack(anchor="w", pady=(10, 5))
        
        columnas = ("titulo", "categoria", "fecha")
        self.lista_mis_articulos = ttk.Treeview(frame_izq, columns=columnas, show="headings", height=10)
        self.lista_mis_articulos.heading("titulo", text=self._t("Título"))
        self.lista_mis_articulos.heading("categoria", text=self._t("Categoría"))
        self.lista_mis_articulos.heading("fecha", text=self._t("ID (Fecha)"))
        self.lista_mis_articulos.column("titulo", width=300)
        self.lista_mis_articulos.column("categoria", width=100)
        self.lista_mis_articulos.column("fecha", width=150)
        self.lista_mis_articulos.pack(fill="both", expand=True, pady=(0, 10))
        self.lista_mis_articulos.bind("<Double-1>", self._abrir_mi_articulo_doble_clic)
        self.lista_mis_articulos.bind("<Button-3>", self._menu_contextual_mis_articulos)

        # --- COLUMNA DERECHA: MIS COLECCIONES ---
        frame_der = ttk.Frame(self.tab_mi_espacio)
        frame_der.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=10)
        
        ttk.Label(frame_der, text="Mis Colecciones", font=("TkDefaultFont", 12, "bold")).pack(anchor="w", pady=(10, 5))
        
        columnas_col = ("titulo", "cantidad")
        self.lista_mis_colecciones = ttk.Treeview(frame_der, columns=columnas_col, show="headings", height=12)
        self.lista_mis_colecciones.heading("titulo", text="Título de la Colección")
        self.lista_mis_colecciones.heading("cantidad", text="Artículos")
        self.lista_mis_colecciones.column("titulo", width=250)
        self.lista_mis_colecciones.column("cantidad", width=80)
        self.lista_mis_colecciones.pack(fill="both", expand=True, pady=(0, 10))
        self.lista_mis_colecciones.bind("<Double-1>", self._abrir_coleccion_detalle_desde_mis_colecciones)
        
        frame_btns_col = ttk.Frame(frame_der)
        frame_btns_col.pack(fill="x")
        frame_btns_col = ttk.Frame(frame_der)
        frame_btns_col.pack(fill="x")
        ttk.Button(frame_btns_col, text="Crear Colección", command=self._abrir_dialogo_crear_coleccion).pack(side="left", padx=2)
        ttk.Button(frame_btns_col, text="Borrar Colección", command=self._borrar_coleccion).pack(side="left", padx=2)
        ttk.Button(frame_btns_col, text="Editar Colección", command=self._editar_coleccion_desde_lista).pack(side="left", padx=2)
        ttk.Button(frame_btns_col, text="Descargar EPUB", command=self._descargar_epub_desde_lista).pack(side="left", padx=2)

    def _construir_tab_autores(self):
        self.tab_autores = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_autores, text=self._t("Autores"))

        frame_principal = ttk.Frame(self.tab_autores)
        frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

        self.lbl_nombre_autor = ttk.Label(frame_principal, text=self._t("Selecciona un autor"), font=("TkDefaultFont", 16, "bold"))
        self.lbl_nombre_autor.pack(pady=(0, 5))

        self.lbl_estado_conexion = ttk.Label(frame_principal, text="", font=("TkDefaultFont", 10, "italic"), foreground="gray")
        self.lbl_estado_conexion.pack(pady=(0, 10))

        self.texto_desc_autor = tk.Text(frame_principal, height=4, wrap="word", bg="white", fg="black", font=("Helvetica", 12), relief="solid", bd=1, state="disabled")
        self.texto_desc_autor.pack(fill="x", pady=(0, 15))

        ttk.Label(frame_principal, text=self._t("Artículos publicados (más recientes primero):"), font=("TkDefaultFont", 10, "bold")).pack(anchor="w")
        columnas = ("titulo", "categoria", "fecha")
        self.lista_articulos_autor = ttk.Treeview(frame_principal, columns=columnas, show="headings", height=7)
        self.lista_articulos_autor.heading("titulo", text=self._t("Título"))
        self.lista_articulos_autor.heading("categoria", text=self._t("Categoría"))
        self.lista_articulos_autor.heading("fecha", text=self._t("ID (Fecha)"))
        self.lista_articulos_autor.column("titulo", width=400)
        self.lista_articulos_autor.column("categoria", width=150)
        self.lista_articulos_autor.column("fecha", width=200)
        self.lista_articulos_autor.pack(fill="both", expand=True, pady=5)
        self.lista_articulos_autor.bind("<Double-1>", lambda e: self._abrir_articulo_doble_clic_autor(e))

        ttk.Label(frame_principal, text="Colecciones públicas de este autor:", font=("TkDefaultFont", 10, "bold")).pack(anchor="w", pady=(10, 0))
        self.lista_colecciones_autor = ttk.Treeview(frame_principal, columns=("titulo", "descargas"), show="headings", height=6)
        self.lista_colecciones_autor.heading("titulo", text="Título de la Colección")
        self.lista_colecciones_autor.heading("descargas", text="Descargas")
        self.lista_colecciones_autor.column("titulo", width=400)
        self.lista_colecciones_autor.column("descargas", width=150)
        self.lista_colecciones_autor.pack(fill="both", expand=True, pady=5)
        self.lista_colecciones_autor.bind("<Double-1>", self._abrir_coleccion_detalle_desde_perfil)

        frame_btns_autor = ttk.Frame(frame_principal)
        frame_btns_autor.pack(fill="x", pady=(10, 0))
        ttk.Button(frame_btns_autor, text="Seguir", command=self._seguir_autor_actual).pack(side="left", padx=5)
        ttk.Button(frame_btns_autor, text="Seguir y Respaldar", command=self._seguir_y_respaldar).pack(side="left", padx=5)
        ttk.Button(frame_btns_autor, text="Dejar de seguir", command=self._dejar_de_seguir).pack(side="left", padx=5)
        ttk.Button(frame_btns_autor, text="Dejar de respaldar", command=self._dejar_de_respaldar).pack(side="left", padx=5)

    def _construir_tab_notificaciones(self):
        self.tab_notificaciones = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_notificaciones, text="Avisos")

        frame_principal = ttk.Frame(self.tab_notificaciones)
        frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(frame_principal, text="Notificaciones de etiquetas", font=("TkDefaultFont", 16, "bold")).pack(pady=(0, 10))
        
        self.lista_notificaciones = tk.Listbox(frame_principal, height=15)
        self.lista_notificaciones.pack(fill="both", expand=True, pady=5)
        # NUEVO: Doble clic para abrir el artículo
        self.lista_notificaciones.bind("<Double-1>", self._abrir_desde_notificacion)
        
        frame_btns = ttk.Frame(frame_principal)
        frame_btns.pack(fill="x", pady=10)
        
        ttk.Button(frame_btns, text="Quitarme la etiqueta", command=self._revocar_etiqueta).pack(side="left", padx=5)
        ttk.Button(frame_btns, text="Borrar aviso", command=self._borrar_notificacion).pack(side="left", padx=5)

        self._refrescar_notificaciones()

    def _abrir_desde_notificacion(self, event):
        sel = self.lista_notificaciones.curselection()
        if not sel: return
        
        notif = self.notificaciones_etiquetas[sel[0]]
        
        # Si el aviso es de un nuevo seguidor, abrimos su perfil
        if notif.get("es_seguidor"):
            self._abrir_perfil_autor(notif["autor"])
            return
            
        # Si es una etiqueta, abrimos el artículo
        aid = notif["articulo_id"]
        if not any(a["id"] == aid for a in self.articulos_descubiertos):
            anuncio_temporal = {
                "id": aid,
                "titulo": notif["titulo"],
                "autor": notif["autor"],
                "autor_nombre": notif["autor_nombre"],
                "etiquetas": [self.nombre_usuario],
                "tematica": "",
                "likes": []
            }
            self.articulos_descubiertos.append(anuncio_temporal)
            self._aplicar_filtro()
            
        self._abrir_por_id(aid)

    def _refrescar_notificaciones(self):
        if not hasattr(self, 'lista_notificaciones'): return
        self.lista_notificaciones.delete(0, "end")
        for notif in self.notificaciones_etiquetas:
            self.lista_notificaciones.insert("end", f"{notif['titulo']} (por {notif['autor_nombre']})")

    def _revocar_etiqueta(self):
        sel = self.lista_notificaciones.curselection()
        if not sel:
            messagebox.showinfo("Sin selección", "Selecciona un aviso para quitarte la etiqueta.")
            return
        
        notif = self.notificaciones_etiquetas[sel[0]]
        aid = notif["articulo_id"]
        mi_nombre = self.nombre_usuario
        
        if aid not in self.etiquetas_revocadas:
            self.etiquetas_revocadas[aid] = []
        if mi_nombre not in self.etiquetas_revocadas[aid]:
            self.etiquetas_revocadas[aid].append(mi_nombre)
            
        # Actualizar modelo local (ignorando mayúsculas/minúsculas)
        for art in self.articulos_descubiertos:
            if art["id"] == aid:
                art["etiquetas"] = [e for e in art.get("etiquetas", []) if e.lower() != mi_nombre.lower()]
        if aid in self.articulos_guardados:
            self.articulos_guardados[aid]["etiquetas"] = [e for e in self.articulos_guardados[aid].get("etiquetas", []) if e.lower() != mi_nombre.lower()]
                
        self._aplicar_filtro()
        self._refrescar_guardados()
        
        mensaje = {"id": aid, "nombre_a_quitar": mi_nombre}
        try:
            self.node.broadcast_json("tag_revoked", mensaje)
            print(f"🛡️ Revocación de identidad emitida para {aid}")
        except Exception as e:
            print(f"Error al emitir revocación: {e}")
            
        del self.notificaciones_etiquetas[sel[0]]
        self._refrescar_notificaciones()
        self._guardar_datos()
        messagebox.showinfo("Identidad protegida", f"Tu nombre ha sido retirado de la etiqueta.\nLa red respetará tu decisión.")

    def _borrar_notificacion(self):
        sel = self.lista_notificaciones.curselection()
        if sel:
            del self.notificaciones_etiquetas[sel[0]]
            self._refrescar_notificaciones()
            self._guardar_datos()

    # --- UTILIDADES ---
    def _ajustar_ancho(self, cantidad):
        nuevo_margen = self.margen_texto + cantidad
        # Límite: el margen puede ir de 10 a 250 píxeles
        if 10 <= nuevo_margen <= 250:
            self.margen_texto = nuevo_margen
            
            # 1. Cambiamos SOLO el margen horizontal (padx) del texto. 
            self.texto_lectura.config(padx=self.margen_texto)
            self.texto_contenido.config(padx=self.margen_texto)
            
            # 2. La barra superior del editor de publicar también se ajusta
            self.frame_barra_top.pack_configure(padx=self.margen_texto)
            
            # Guardar en la base de datos 1 segundo después
            if hasattr(self, '_save_timer'):
                self.root.after_cancel(self._save_timer)
            self._save_timer = self.root.after(1000, self._guardar_datos)

    def _cambiar_limite(self):
        nuevo = simpledialog.askinteger("Límite de espacio", "¿Cuántos MB deseas dedicar al almacenamiento (mínimo 10)?", initialvalue=self.limite_mb, minvalue=10, parent=self.root)
        if nuevo:
            self.limite_mb = nuevo
            self._guardar_datos()
            self._actualizar_barra_espacio()

    def _configurar_portapapeles(self, widget):
        widget.bind("<Control-v>", lambda e: self._pegar(widget))
        widget.bind("<Control-V>", lambda e: self._pegar(widget))
        widget.bind("<Control-c>", lambda e: self._copiar(widget))
        widget.bind("<Control-C>", lambda e: self._copiar(widget))
        widget.bind("<Control-x>", lambda e: self._cortar(widget))
        widget.bind("<Control-X>", lambda e: self._cortar(widget))
        widget.bind("<Control-a>", lambda e: self._seleccionar_todo(widget))
        widget.bind("<Control-A>", lambda e: self._seleccionar_todo(widget))
        widget.bind("<Button-3>", lambda e: self._menu_contextual(e, widget))

    def _configurar_portapapeles_lectura(self, widget):
        widget.bind("<Control-c>", lambda e: self._copiar(widget))
        widget.bind("<Control-C>", lambda e: self._copiar(widget))
        widget.bind("<Control-a>", lambda e: self._seleccionar_todo(widget))
        widget.bind("<Control-A>", lambda e: self._seleccionar_todo(widget))
        widget.bind("<Button-3>", lambda e: self._menu_contextual_lectura(e, widget))

    def _pegar(self, widget):
        try:
            texto = self.root.clipboard_get()
            widget.insert("insert", texto)
        except tk.TclError:
            pass
        return "break"

    def _copiar(self, widget):
        try:
            if isinstance(widget, tk.Text):
                texto = widget.get("sel.first", "sel.last")
            else:
                texto = widget.selection_get()
            self.root.clipboard_clear()
            self.root.clipboard_append(texto)
        except tk.TclError:
            pass
        return "break"

    def _cortar(self, widget):
        self._copiar(widget)
        try:
            widget.delete("sel.first", "sel.last")
        except tk.TclError:
            pass
        return "break"

    def _seleccionar_todo(self, widget):
        if isinstance(widget, tk.Text):
            widget.tag_add("sel", "1.0", "end")
        else:
            widget.select_range(0, "end")
            widget.icursor("end")
        return "break"

    def _menu_contextual(self, event, widget):
        menu = tk.Menu(widget, tearoff=0)
        menu.add_command(label="Pegar", command=lambda: self._pegar(widget))
        menu.add_command(label="Copiar", command=lambda: self._copiar(widget))
        menu.add_command(label="Cortar", command=lambda: self._cortar(widget))
        menu.add_separator()
        menu.add_command(label="Seleccionar todo", command=lambda: self._seleccionar_todo(widget))
        menu.tk_popup(event.x_root, event.y_root)

    def _menu_contextual_lectura(self, event, widget):
        menu = tk.Menu(widget, tearoff=0)
        menu.add_command(label="Copiar", command=lambda: self._copiar(widget))
        menu.add_separator()
        menu.add_command(label="Seleccionar todo", command=lambda: self._seleccionar_todo(widget))
        menu.tk_popup(event.x_root, event.y_root)

    # --- CONFIGURACIÓN DEL NODO ---
    def _configurar_nodo(self):
        self.node.enable_pubsub()
        self.node.enable_json()
        self.node.enable_dht()
        self.node.enable_mdns()
        self.node.on_json("get_collections", self._al_recibir_get_collections)
        self.node.on_json("collection_list", self._al_recibir_collection_list)
        self.node.on_json("remove_ping", self._al_recibir_remove_ping)

        try:
            self.node.on_peer_connected(self._al_conectar_peer)
        except Exception as e:
            print(f"Nota: no se pudo activar el log de conexiones: {e}")

        # Suscribirse al tema del mes actual y al del mes pasado (para no perder artículos recientes)
        import datetime
        ahora = datetime.datetime.now()
        mes_actual = ahora.strftime("%Y-%m")
        mes_pasado = (ahora.replace(day=1) - datetime.timedelta(days=1)).strftime("%Y-%m")
        
        for tematica in TEMATICAS:
            self.node.subscribe(f"blog:tematica:{tematica}:{mes_actual}", self._al_recibir_anuncio)
            self.node.subscribe(f"blog:tematica:{tematica}:{mes_pasado}", self._al_recibir_anuncio)

        self.node.on_json("get_article", self._al_pedir_articulo)
        self.node.on_json("article_content", self._al_recibir_contenido)
        self.node.on_json("sync_request", self._al_recibir_sync_request)
        self.node.on_json("sync_response", self._al_recibir_sync_response)
        self.node.on_json("like_article", self._al_recibir_like)
        self.node.subscribe("blog:backups", self._al_recibir_backup)
        self.node.subscribe("blog:backups_remove", self._al_recibir_backup_remove)
        self.node.on_json("save_ping", self._al_recibir_save_ping)
        self.node.on_json("tag_notification", self._al_recibir_tag_notification)
        self.node.on_json("tag_revoked", self._al_recibir_tag_revoked)
        self.node.subscribe("blog:colecciones", self._al_recibir_coleccion)
        self.node.on_json("collection_downloaded", self._al_recibir_coleccion_descargada)
        self.node.on_json("follow_ping", self._al_recibir_follow_ping)

    def _al_conectar_peer(self, peer_id):
        print(f"🟢 ¡NUEVO PAR CONECTADO!: {peer_id[:12]}...")
        
        # Actualizar la hora de última conexión de este peer
        if peer_id not in self.perfiles_autores:
            self.perfiles_autores[peer_id] = {}
        self.perfiles_autores[peer_id]["ultima_conexion"] = time.time()
        self._guardar_datos()

        self._enviar_json_seguro(peer_id, "get_collections", {})
        # Pedimos el catálogo y enviamos nuestras lápidas
        self._enviar_json_seguro(peer_id, "sync_request", {"lapidas": list(self.lapidas)})

    def _al_recibir_sync_request(self, peer_id, value):
        # 1. Enviar lápidas a la cola segura
        lapidas_remotas = value.get("lapidas", []) if isinstance(value, dict) else []
        for aid in lapidas_remotas:
            self.event_queue.put(("lapida_recibida", aid))

        # 2. Procesar los respaldos
        respaldos_remotos = value.get("backups", []) if isinstance(value, dict) else []
        self.event_queue.put(("procesar_respaldos_remotos", (peer_id, respaldos_remotos)))

        # 3. Enviar nuestro catálogo completo
        articulos = list(self.mis_articulos.values())
        articulos.sort(key=lambda x: x["id"], reverse=True)
        catalogo = []
        for art in articulos:
            catalogo.append({
                "id": art["id"], "titulo": art["titulo"], "etiquetas": art["etiquetas"],
                "tematica": art["tematica"], "autor": art["autor"],
                "autor_nombre": art.get("autor_nombre", "Usuario Anónimo"),
                "autor_descripcion": art.get("autor_descripcion", ""),
                "autor_horario": art.get("autor_horario", ""),
                "autor_utc_offset": art.get("autor_utc_offset", 0.0),
                "idioma": art.get("idioma", "Español"),
                "likes": art.get("likes", []),
                "respaldos": len(self.respaldos_red.get(art["id"], []))
            })
        
        respuesta = {
            "catalogo": catalogo, 
            "lapidas": list(self.lapidas),
            "backups": list(self.articulos_guardados.keys())
        }
        self._enviar_json_seguro(peer_id, "sync_response", respuesta)

        # 4. Pedir catálogo si no es respuesta
        es_respuesta = value.get("is_reply", False) if isinstance(value, dict) else False
        if not es_respuesta:
            self._enviar_json_seguro(peer_id, "sync_request", {
                "lapidas": list(self.lapidas), 
                "is_reply": True, 
                "backups": list(self.articulos_guardados.keys())
            })

    def _al_recibir_sync_response(self, peer_id, value):
        if isinstance(value, dict):
            catalogo = value.get("catalogo", [])
            lapidas_remotas = value.get("lapidas", [])
            respaldos_remotos = value.get("backups", [])
            self.event_queue.put(("procesar_respaldos_remotos", (peer_id, respaldos_remotos)))

            for aid in lapidas_remotas:
                self.event_queue.put(("lapida_recibida", aid))
            
            # Limpieza de fantasmas
            ids_en_catalogo = [a["id"] for a in catalogo]
            for art in list(self.articulos_descubiertos):
                if art.get("autor") == peer_id and art["id"] not in ids_en_catalogo and art["id"] != self.articulo_actual_id:
                    self.event_queue.put(("lapida_recibida", art["id"]))
                    
            for aid, art in list(self.articulos_guardados.items()):
                if art.get("autor") == peer_id and aid not in ids_en_catalogo and aid != self.articulo_actual_id:
                    self.event_queue.put(("lapida_recibida", aid))

            for anuncio in catalogo:
                if anuncio["id"] not in self.lapidas:
                    if "autor_descripcion" in anuncio and "autor" in anuncio:
                        self.perfiles_autores[anuncio["autor"]] = {
                            "nombre": anuncio.get("autor_nombre", ""), 
                            "descripcion": anuncio["autor_descripcion"],
                            "horario": anuncio.get("autor_horario", ""),
                            "utc_offset": anuncio.get("autor_utc_offset", 0.0)
                        }
                    self.event_queue.put(("nuevo_articulo", anuncio))
                    
        elif isinstance(value, list):
            for anuncio in value:
                if anuncio["id"] not in self.lapidas:
                    if "autor_descripcion" in anuncio and "autor" in anuncio:
                        self.perfiles_autores[anuncio["autor"]] = {
                            "nombre": anuncio.get("autor_nombre", ""), 
                            "descripcion": anuncio["autor_descripcion"],
                            "horario": anuncio.get("autor_horario", ""),
                            "utc_offset": anuncio.get("autor_utc_offset", 0.0)
                        }
                    self.event_queue.put(("nuevo_articulo", anuncio))
        
        self.event_queue.put(("refrescar_ui", None))

    def _procesar_respaldos_remotos(self, peer_id, ids_respaldados):
        ids_respaldados = set(ids_respaldados)
        actualizado = False
        afectados = []
        ahora = time.time()
        
        for aid in self.mis_articulos:
            # --- CONVERSIÓN A PRUEBA DE BALAS ---
            if aid not in self.respaldos_red:
                self.respaldos_red[aid] = {}
            elif isinstance(self.respaldos_red[aid], list):
                # Si es una lista vieja, la convertimos a diccionario con hora actual
                self.respaldos_red[aid] = {peer: ahora for peer in self.respaldos_red[aid]}
            # ------------------------------------

            if aid in ids_respaldados:
                if peer_id not in self.respaldos_red[aid]:
                    self.respaldos_red[aid][peer_id] = ahora
                    actualizado = True
                    afectados.append(aid)
                else:
                    self.respaldos_red[aid][peer_id] = ahora # Actualiza la hora
            else:
                if peer_id in self.respaldos_red[aid]:
                    del self.respaldos_red[aid][peer_id]
                    actualizado = True
                    afectados.append(aid)
        
        if actualizado:
            self._guardar_datos()
            for aid in afectados:
                art = self.mis_articulos[aid]
                anuncio = {
                    "id": art["id"], "titulo": art["titulo"], "etiquetas": art["etiquetas"],
                    "tematica": art["tematica"], "autor": art["autor"],
                    "autor_nombre": art.get("autor_nombre", self.nombre_usuario), 
                    "autor_descripcion": art.get("autor_descripcion", self.mi_descripcion),
                    "idioma": art.get("idioma", "Español"),
                    "is_update": True, "likes": art.get("likes", []),
                    "respaldos": len(self.respaldos_red[aid])
                }
                self.node.publish(f"blog:tematica:{art['tematica']}", json.dumps(anuncio).encode())
            self.event_queue.put(("actualizar_respaldos", self.articulo_actual_id))

    # --- PUBLICAR Y LIKES ---
    def _actualizar_nombre(self):
        nuevo = self.entrada_nombre.get().strip()
        nueva_desc = self.texto_desc_perfil.get("1.0", "end-1c").strip()
        nuevo_horario = self.entrada_horario.get().strip()
        
        import time
        self.mi_utc_offset = -time.timezone / 3600.0
        self.mi_horario = nuevo_horario
        if nuevo:
            self.nombre_usuario = nuevo
            self.mi_descripcion = nueva_desc
            self.perfiles_autores[self.node.local_id] = {
                "nombre": self.nombre_usuario, 
                "descripcion": self.mi_descripcion,
                "horario": self.mi_horario,
                "utc_offset": self.mi_utc_offset
            }
            
            for art in self.mis_articulos.values():
                art["autor_nombre"] = self.nombre_usuario
                art["autor_descripcion"] = self.mi_descripcion
                art["autor_horario"] = self.mi_horario
                art["autor_utc_offset"] = self.mi_utc_offset
                
            self._guardar_datos()
            
            msg_perfil = {
                "autor": self.node.local_id, 
                "nombre": self.nombre_usuario, 
                "descripcion": self.mi_descripcion,
                "horario": self.mi_horario,
                "utc_offset": self.mi_utc_offset,
                "llave": self.llave_publica
            }
            msg_perfil["firma"] = self._firmar_mensaje(msg_perfil)
            self.node.publish("blog:system:profiles", json.dumps(msg_perfil).encode())
            
            for art in self.mis_articulos.values():
                anuncio = {
                    "id": art["id"], "titulo": art["titulo"], "etiquetas": art["etiquetas"],
                    "tematica": art["tematica"], "autor": art["autor"],
                    "autor_nombre": art["autor_nombre"], "autor_descripcion": art["autor_descripcion"],
                    "autor_horario": art.get("autor_horario", ""),
                    "autor_utc_offset": art.get("autor_utc_offset", 0.0),
                    "idioma": art.get("idioma", "Español"),
                    "is_update": True, "likes": art.get("likes", [])
                }
                self.node.publish(f"blog:tematica:{art['tematica']}", json.dumps(anuncio).encode())
                
            messagebox.showinfo("Perfil", "Perfil actualizado y sincronizado en la red.")

    def _publicar_articulo(self):
        if self._calcular_espacio_usado() >= self.limite_mb:
            messagebox.showerror("Espacio lleno", "Has alcanzado tu límite de almacenamiento. Aumenta el límite o borra artículos.")
            return

        titulo = self.entrada_titulo.get().strip()
        # Regla anti-spam: 5 minutos entre publicaciones (solo si no estamos editando)
        ahora = time.time()
        if self.ultima_publicacion > 0 and (ahora - self.ultima_publicacion) < 300 and not self.editando_id:
            minutos_restantes = int((300 - (ahora - self.ultima_publicacion)) / 60) + 1
            respuesta = messagebox.askyesno("Límite de tiempo", 
                f"Para evitar el spam, debes esperar {minutos_restantes} minutos antes de publicar otro artículo.\n\n"
                "¿Quieres guardar este artículo como borrador para publicarlo más tarde?")
            if respuesta:
                self._guardar_borrador()
            return

        # Regla anti-spam: no repetir título (solo si es un artículo nuevo)
        if not self.editando_id:
            for art in self.mis_articulos.values():
                if art["titulo"].strip().lower() == titulo.strip().lower():
                    messagebox.showwarning("Título duplicado", "Ya tienes un artículo con este mismo título. Por favor, usa otro.")
                    return
        etiquetas_raw = self.entrada_etiqueta.get().strip()
        tematica = self.combo_tematica.get()
        contenido_texto = self.texto_contenido.get("1.0", "end-1c").strip()
        
        if not titulo or not contenido_texto or not etiquetas_raw:
            messagebox.showwarning("Faltan datos", "Todos los campos son obligatorios.")
            return

        # Determinar idioma
        idioma_seleccionado = self.combo_idioma_publicar.get()
        if idioma_seleccionado == self._t("Automático"):
            idioma_final = self.idioma_actual
        else:
            idioma_final = idioma_seleccionado

        lista_etiquetas = [e.strip() for e in etiquetas_raw.split(',') if e.strip()]
        
        if self.editando_id:
            articulo_id = self.editando_id
        else:
            articulo_id = f"{self.node.local_id[:8]}-{int(time.time())}"

        contenido_rico = {"texto": contenido_texto, "tags": {}, "imagenes": dict(self.imagenes_temporales)}
        # Guardar todos los tags aplicados
        todos_los_tags = self.texto_contenido.tag_names()
        for tag in todos_los_tags:
            if tag == "sel": continue
            rangos = self.texto_contenido.tag_ranges(tag)
            if rangos:
                contenido_rico["tags"][tag] = [str(r) for r in rangos]
                
                config = {}
                try:
                    fuente = self.texto_contenido.tag_cget(tag, "font")
                    if fuente: config["font"] = fuente
                    alineacion = self.texto_contenido.tag_cget(tag, "justify")
                    if alineacion: config["justify"] = alineacion
                except:
                    pass
                
                if config:
                    contenido_rico.setdefault("tag_configs", {})[tag] = config

        self.mis_articulos[articulo_id] = {
            "id": articulo_id, "titulo": titulo, "etiquetas": lista_etiquetas,
            "tematica": tematica, "contenido": contenido_rico,
            "autor": self.node.local_id, "autor_nombre": self.nombre_usuario,
            "autor_descripcion": self.mi_descripcion,
            "autor_horario": self.mi_horario,           # <--- AÑADIR ESTO
            "autor_utc_offset": self.mi_utc_offset,     # <--- AÑADIR ESTO
            "idioma": idioma_final,
            "likes": []
        }

        anuncio = {
            "id": articulo_id, "titulo": titulo, "etiquetas": lista_etiquetas,
            "tematica": tematica, "autor": self.node.local_id, "autor_nombre": self.nombre_usuario,
            "autor_descripcion": self.mi_descripcion,
            "autor_horario": self.mi_horario,           # <--- AÑADIR ESTO
            "autor_utc_offset": self.mi_utc_offset,     # <--- AÑADIR ESTO
            "idioma": idioma_final,
            "is_update": True if self.editando_id else False,
            "likes": [],
            "host": self._obtener_ip_local(),
            "port": self.node.listen_port
        }
        # Si el autor tiene este artículo en sus guardados, actualizar su contenido también
        if articulo_id in self.articulos_guardados:
            self.articulos_guardados[articulo_id]["contenido"] = contenido_rico
            self.articulos_guardados[articulo_id]["titulo"] = titulo
            self._refrescar_guardados()

        # --- NUEVO: Detectar si se etiquetó a otro autor conocido ---
        for etiqueta in lista_etiquetas:
            for autor_id, perfil in self.perfiles_autores.items():
                if perfil.get("nombre", "").lower() == etiqueta.lower() and autor_id != self.node.local_id:
                    if self._esta_conectado(autor_id):
                        notif = {
                            "articulo_id": articulo_id,
                            "titulo": titulo,
                            "autor": self.node.local_id,
                            "autor_nombre": self.nombre_usuario
                        }
                        self._enviar_json_seguro(autor_id, "tag_notification", notif)
        # -------------------------------------------------------------

        import datetime
        mes_actual = datetime.datetime.now().strftime("%Y-%m")
        
        self.node.publish(f"blog:tematica:{tematica}:{mes_actual}", json.dumps(anuncio).encode())
        for etiqueta in lista_etiquetas:
            self.node.publish(f"blog:etiqueta:{etiqueta.lower()}:{mes_actual}", json.dumps(anuncio).encode())

        self._agregar_a_lista(anuncio)
        self._guardar_datos()
        self._refrescar_mis_articulos()
        self._actualizar_barra_espacio()
        
        if self.editando_id:
            messagebox.showinfo("Actualizado", "Artículo actualizado y sincronizado.")
            self.editando_id = None
            self.btn_publicar.config(text=self._t("Publicar artículo"))
        else:
            messagebox.showinfo("Publicado", f"Artículo publicado con ID:\n{articulo_id}")
        self.ultima_publicacion = ahora            
        self._limpiar_formulario()

    def _guardar_borrador(self):
        titulo = self.entrada_titulo.get().strip()
        if not titulo:
            messagebox.showwarning("Error", "El título es obligatorio para guardar un borrador.")
            return
        
        self.borradores[titulo] = {
            "titulo": titulo,
            "etiquetas": self.entrada_etiqueta.get().strip(),
            "tematica": self.combo_tematica.get(),
            "idioma": self.combo_idioma_publicar.get(),
            "texto": self.texto_contenido.get("1.0", "end-1c"),
            "imagenes": dict(self.imagenes_temporales)
        }
        self._guardar_datos()
        messagebox.showinfo("Borrador", "Borrador guardado exitosamente.")
        self._limpiar_formulario()

    def _mostrar_dialogo_borradores(self):
        if not self.borradores:
            messagebox.showinfo("Sin borradores", "No tienes borradores guardados.")
            return
            
        dialog = tk.Toplevel(self.root)
        dialog.title("Cargar Borrador")
        dialog.geometry("400x300")
        
        listbox = tk.Listbox(dialog)
        listbox.pack(fill="both", expand=True, padx=10, pady=10)
        for titulo in self.borradores.keys():
            listbox.insert("end", titulo)
            
        def cargar_seleccionado():
            sel = listbox.curselection()
            if not sel: return
            titulo = listbox.get(sel[0])
            borrador = self.borradores[titulo]
            
            self.entrada_titulo.delete(0, "end")
            self.entrada_titulo.insert(0, borrador["titulo"])
            self.entrada_etiqueta.delete(0, "end")
            self.entrada_etiqueta.insert(0, borrador["etiquetas"])
            self.combo_tematica.set(borrador["tematica"])
            self.combo_idioma_publicar.set(borrador["idioma"])
            self.texto_contenido.delete("1.0", "end")
            self.texto_contenido.insert("1.0", borrador["texto"])
            self.imagenes_temporales = dict(borrador["imagenes"])
            
            dialog.destroy()
            messagebox.showinfo("Borrador cargado", "Puedes seguir editando y publicar cuando estés listo.")
            
        ttk.Button(dialog, text="Cargar seleccionado", command=cargar_seleccionado).pack(pady=5)

    def _limpiar_formulario(self):
        self.entrada_titulo.delete(0, "end")
        self.entrada_etiqueta.delete(0, "end")
        self.texto_contenido.delete("1.0", "end")
        self.imagenes_temporales.clear()

    def _dar_me_gusta(self, event=None):
        if not self.articulo_actual_id: return
        
        if self.articulo_actual_id in self.mis_articulos:
            messagebox.showinfo("Tu artículo", "No puedes darle 'Me gusta' a tu propio artículo.")
            return
        
        anuncio = next((a for a in self.articulos_descubiertos if a["id"] == self.articulo_actual_id), None)
        if not anuncio: return
        
        likes_actuales = anuncio.get("likes", [])
        if self.node.local_id in likes_actuales:
            messagebox.showinfo("Ya votaste", "Ya le has dado 'Me gusta' a este artículo.")
            return

        # 1. Guardar el like localmente
        likes_actuales.append(self.node.local_id)
        anuncio["likes"] = likes_actuales
        
        self.lbl_count.config(text=f"({len(likes_actuales)})")
        if self.articulo_actual_id in self.articulos_guardados:
            self.articulos_guardados[self.articulo_actual_id]["likes"] = likes_actuales
            
        self._guardar_like_rapido(self.articulo_actual_id)
        
        # 2. Refrescar la lista de Descubrir para que la estrella suba a 1
        self._aplicar_filtro()

        # 3. FIRMAR Y ENVIAR AL AUTOR (PASO 4)
        payload = {"id": self.articulo_actual_id, "peer": self.node.local_id, "llave": self.llave_publica}
        payload["firma"] = self._firmar_mensaje(payload)

        from librats_py.exceptions import RatsNoSuchPeerError
        try:
            self.node.send_json(anuncio["autor"], "like_article", payload)
            print("⭐ Like enviado al autor.")
        except RatsNoSuchPeerError:
            print(f"⭐ Like guardado localmente. El autor {anuncio['autor'][:8]} está offline.")
        except Exception as e:
            print(f"Error enviando like: {e}")

    def _al_recibir_like(self, peer_id, value):
        firma = value.pop("firma", "")
        llave = value.get("llave", "")
        
        if not self._verificar_firma(value, firma, llave):
            print(f"🚨 ALERTA: Like falso detectado de {peer_id[:8]}")
            return

        articulo_id = value.get("id")
        peer_que_vota = value.get("peer")
        
        if articulo_id in self.mis_articulos:
            likes = self.mis_articulos[articulo_id].get("likes", [])
            if peer_que_vota not in likes:
                likes.append(peer_que_vota)
                self.mis_articulos[articulo_id]["likes"] = likes
                self._guardar_like_rapido(articulo_id)
                if self.articulo_actual_id == articulo_id:
                    self.lbl_count.config(text=f"({len(likes)})")

    def _al_recibir_save_ping(self, peer_id, value):
        aid = value.get("id")
        if aid and aid in self.mis_articulos:
            # --- CONVERSIÓN A PRUEBA DE BALAS ---
            if aid not in self.respaldos_red:
                self.respaldos_red[aid] = {}
            elif isinstance(self.respaldos_red[aid], list):
                self.respaldos_red[aid] = {peer: time.time() for peer in self.respaldos_red[aid]}
            # ------------------------------------
            
            self.respaldos_red[aid][peer_id] = time.time()
            self._guardar_datos()
            
            art = self.mis_articulos[aid]
            anuncio = {
                "id": art["id"], "titulo": art["titulo"], "etiquetas": art["etiquetas"],
                "tematica": art["tematica"], "autor": art["autor"],
                "autor_nombre": art.get("autor_nombre", self.nombre_usuario), 
                "autor_descripcion": art.get("autor_descripcion", self.mi_descripcion),
                "idioma": art.get("idioma", "Español"),
                "is_update": True, "likes": art.get("likes", []),
                "respaldos": len(self.respaldos_red[aid])
            }
            self.node.publish(f"blog:tematica:{art['tematica']}", json.dumps(anuncio).encode())
            self.event_queue.put(("actualizar_respaldos", aid))

    def _al_recibir_follow_ping(self, peer_id, value):
        nombre_seguidor = value.get("nombre", "Alguien")
        descripcion_seguidor = value.get("descripcion", "")
        tipo = value.get("tipo", "seguir") # "seguir" o "respaldar"
        
        # ¡LA SOLUCIÓN! Guardamos su perfil para que cuando hagamos doble clic, sepa quién es.
        self.perfiles_autores[peer_id] = {
            "nombre": nombre_seguidor,
            "descripcion": descripcion_seguidor
        }
        self._guardar_datos()
        
        texto_aviso = f"👤 {nombre_seguidor} te ha empezado a {tipo}"
        
        notif = {
            "articulo_id": f"perfil-{peer_id}", # Usamos un ID falso para que el doble clic sepa que es un perfil
            "titulo": texto_aviso,
            "autor": peer_id,
            "autor_nombre": nombre_seguidor,
            "es_seguidor": True  # <-- Bandera para saber que es un perfil
        }
        
        if not any(n["articulo_id"] == notif["articulo_id"] for n in self.notificaciones_etiquetas):
            self.notificaciones_etiquetas.append(notif)
            self._guardar_datos()
            self.root.after(0, self._refrescar_notificaciones)
            self.root.after(0, lambda: self.notebook.tab(self.tab_notificaciones, text="Avisos (¡Nuevo!)"))
            print(f"🔔 Nuevo seguidor: {nombre_seguidor}")

    def _al_recibir_backup(self, peer_id, topic, data):
        try:
            msg = json.loads(data.decode())
            aid = msg.get("id")
            dueno = msg.get("peer")
            if aid and dueno:
                if aid not in self.quien_tiene:
                    self.quien_tiene[aid] = []
                if dueno not in self.quien_tiene[aid]:
                    self.quien_tiene[aid].append(dueno)
        except Exception as e:
            pass

    def _al_recibir_backup_remove(self, peer_id, topic, data):
        try:
            msg = json.loads(data.decode())
            aid = msg.get("id")
            dueno = msg.get("peer")
            if aid in self.quien_tiene and dueno in self.quien_tiene[aid]:
                self.quien_tiene[aid].remove(dueno)
        except Exception as e:
            pass

        articulos_filtrados = []
        for articulo in self.articulos_descubiertos:
            if filtro_categoria != self._t("Todas") and articulo.get("tematica") != filtro_categoria:
                continue
            if filtro_etiqueta:
                etiquetas_articulo = [str(e).lower() for e in articulo.get("etiquetas", [])]
                if filtro_etiqueta not in etiquetas_articulo:
                    continue
            if filtro_idioma != self._t("Todos") and articulo.get("idioma", "Español") != filtro_idioma:
                continue
            articulos_filtrados.append(articulo)

        # --- NUEVO: Ordenar del más nuevo al más antiguo ---
        def obtener_timestamp(art):
            try:
                # El ID tiene el formato "hash-timestamp", así que extraemos el timestamp
                return int(art["id"].split("-")[-1])
            except:
                return 0 # Si falla, se va al final
        
        articulos_filtrados.sort(key=obtener_timestamp, reverse=True)
        # ---------------------------------------------------

    def _al_recibir_remove_ping(self, peer_id, value):
        aid = value.get("id")
        if aid and aid in self.mis_articulos:
            if aid in self.respaldos_red and peer_id in self.respaldos_red[aid]:
                self.respaldos_red[aid].remove(peer_id)
                self._guardar_datos()
                print(f"🗑️ Nodo {peer_id[:8]}... ha dejado de respaldar tu artículo {aid}")
                
                # Re-publicar el anuncio para actualizar el contador en toda la red
                art = self.mis_articulos[aid]
                anuncio = {
                    "id": art["id"], "titulo": art["titulo"], "etiquetas": art["etiquetas"],
                    "tematica": art["tematica"], "autor": art["autor"],
                    "autor_nombre": art.get("autor_nombre", self.nombre_usuario), 
                    "autor_descripcion": art.get("autor_descripcion", self.mi_descripcion),
                    "idioma": art.get("idioma", "Español"),
                    "is_update": True, "likes": art.get("likes", []),
                    "respaldos": len(self.respaldos_red[aid])
                }
                self.node.publish(f"blog:tematica:{art['tematica']}", json.dumps(anuncio).encode())
                
                # Actualizar la vista del autor si tiene el artículo abierto
                self.event_queue.put(("actualizar_respaldos", aid))

    def _al_recibir_tag_notification(self, peer_id, value):
        notif = {
            "articulo_id": value["articulo_id"],
            "titulo": value["titulo"],
            "autor": value["autor"],
            "autor_nombre": value["autor_nombre"]
        }
        # Evitar duplicados
        if not any(n["articulo_id"] == notif["articulo_id"] for n in self.notificaciones_etiquetas):
            self.notificaciones_etiquetas.append(notif)
            self._guardar_datos()
            self.root.after(0, self._refrescar_notificaciones)
            # Avisar visualmente en la pestaña
            self.root.after(0, lambda: self.notebook.tab(self.tab_notificaciones, text="Avisos (¡Nuevo!)"))
            print(f"🔔 Nueva notificación: te etiquetaron en '{notif['titulo']}'")

    def _al_recibir_tag_revoked(self, peer_id, value):
        aid = value.get("id")
        nombre_revocado = value.get("nombre_a_quitar")
        
        if aid and nombre_revocado:
            # 1. Registrar la revocación localmente
            if aid not in self.etiquetas_revocadas:
                self.etiquetas_revocadas[aid] = []
            if nombre_revocado not in self.etiquetas_revocadas[aid]:
                self.etiquetas_revocadas[aid].append(nombre_revocado)
                
            # 2. Actualizar la vista en 'Descubrir' y 'Guardados' (ignorando mayúsculas/minúsculas)
            for art in self.articulos_descubiertos:
                if art["id"] == aid:
                    art["etiquetas"] = [e for e in art.get("etiquetas", []) if e.lower() != nombre_revocado.lower()]
            
            if aid in self.articulos_guardados:
                self.articulos_guardados[aid]["etiquetas"] = [e for e in self.articulos_guardados[aid].get("etiquetas", []) if e.lower() != nombre_revocado.lower()]
            
            # 3. Refrescar la interfaz local (si el autor está viendo la lista, verá la etiqueta desaparecer)
            self._aplicar_filtro()
            self._refrescar_guardados()
            self._guardar_datos()
            
            # Si el autor tiene abierto este artículo en el editor, podemos limpiar el campo de etiquetas 
            # para que no se vuelva a publicar con ellas por accidente.
            if self.editando_id == aid:
                etiquetas_actuales = self.entrada_etiqueta.get().split(',')
                etiquetas_limpias = [e.strip() for e in etiquetas_actuales if e.strip().lower() != nombre_revocado.lower()]
                self.entrada_etiqueta.delete(0, "end")
                self.entrada_etiqueta.insert(0, ", ".join(etiquetas_limpias))

            print(f"🛡️ Revocación respetada: '{nombre_revocado}' ya no se muestra en el artículo {aid}")

    def _publicar_coleccion(self, col_id):
        if col_id not in self.mis_colecciones: return
        col = self.mis_colecciones[col_id]
        try:
            self.node.publish("blog:colecciones", json.dumps(col).encode())
            print(f"📢 Colección publicada: {col['titulo']}")
        except Exception as e:
            print(f"Error al publicar colección: {e}")

    def _al_recibir_coleccion(self, peer_id, topic, data):
        try:
            col = json.loads(data.decode())
            if col.get("autor") != self.node.local_id:
                self.colecciones_descubiertas[col["id"]] = col
                self._guardar_datos()
                if self.autor_perfil_actual == col.get("autor"):
                    self._abrir_perfil_autor(col.get("autor"))
        except Exception as e:
            print(f"Error recibiendo colección: {e}")

    def _al_recibir_coleccion_descargada(self, peer_id, value):
        col_id = value.get("id")
        if col_id in self.mis_colecciones and self.mis_colecciones[col_id].get("autor") == self.node.local_id:
            self.mis_colecciones[col_id]["descargas"] = self.mis_colecciones[col_id].get("descargas", 0) + 1
            self._guardar_datos()
            self._publicar_coleccion(col_id) # Re-publicar para actualizar el contador
            self._refrescar_mis_colecciones()
            print(f"⬇️ Tu colección {col_id} ha sido descargada. Total: {self.mis_colecciones[col_id]['descargas']}")

    def _al_recibir_get_collections(self, peer_id, value):
        try:
            self._enviar_json_seguro(peer_id, "collection_list", list(self.mis_colecciones.values()))
        except Exception as e:
            print(f"Error enviando colecciones: {e}")

    def _al_recibir_collection_list(self, peer_id, value):
        if isinstance(value, list):
            actualizado = False
            for col in value:
                if col.get("autor") != self.node.local_id:
                    if col.get("id") not in self.colecciones_descubiertas:
                        actualizado = True
                    self.colecciones_descubiertas[col["id"]] = col
            if actualizado:
                self._guardar_datos()
                if self.autor_perfil_actual:
                    self._abrir_perfil_autor(self.autor_perfil_actual)

    def _importar_coleccion(self, col_id):
        col = self.colecciones_descubiertas.get(col_id)
        if not col: return
        if col_id in self.mis_colecciones:
            messagebox.showinfo("Ya importada", "Ya tienes esta colección en tu espacio.")
            return
            
        self.mis_colecciones[col_id] = col
        self._guardar_datos()
        self._refrescar_mis_colecciones()
        
        try:
            self._enviar_json_seguro(col["autor"], "collection_downloaded", {"id": col_id})
            print("📥 Colección importada. Notificado al autor.")
        except Exception as e:
            print(f"No se pudo notificar al autor: {e}")
        
        messagebox.showinfo("Importada", "La colección ha sido añadida a 'Mi espacio'.")

    # --- CALLBACKS DE RED ---
    def _al_recibir_anuncio(self, peer_id, topic, data):
        # Si la cola de procesamiento ya está muy llena (ej. 200 mensajes), ignoramos para no colapsar la RAM
        if self.event_queue.qsize() > 200:
            print("⚠️ Cola de red saturada. Ignorando anuncio.")
            return
            
        # Rechazar mensajes que pesen más de 1 MB (los anuncios solo son metadatos)
        if len(data) > 1024 * 1024:
            print(f"🚨 Anuncio gigante de {peer_id[:8]} rechazado por seguridad.")
            return
            
        self.event_queue.put(("anuncio_crudo", (peer_id, topic, data)))

    def _al_pedir_articulo(self, peer_id, value):
        self.event_queue.put(("peticion_articulo", (peer_id, value)))

    def _al_recibir_contenido(self, peer_id, value):
        # Si la cola está llena, rechazamos
        if self.event_queue.qsize() > 200:
            return
            
        self.event_queue.put(("contenido_articulo", value))

    def _al_pedir_articulo(self, peer_id, value):
        # Solo encolamos la petición. El trabajo pesado va al hilo principal.
        self.event_queue.put(("peticion_articulo", (peer_id, value)))

    def _al_recibir_contenido(self, peer_id, value):
        self.event_queue.put(("contenido_articulo", value))

    def _procesar_cola(self):
        refrescar_pantalla = False
        try:
            # Procesamos hasta 100 eventos de red de golpe
            for _ in range(100):
                tipo, dato = self.event_queue.get_nowait()
                
                if tipo == "nuevo_articulo":
                    self._agregar_a_lista(dato)
                    refrescar_pantalla = True
                elif tipo == "contenido_articulo":
                    self._procesar_contenido_recibido(dato)
                    refrescar_pantalla = True
                elif tipo == "perfil_actualizado":
                    if self.notebook.select() == str(self.tab_autores):
                        self._abrir_perfil_autor(dato)
                elif tipo == "anuncio_crudo":
                    peer_id, topic, data = dato
                    self._procesar_anuncio_crudo(peer_id, topic, data)
                elif tipo == "peticion_articulo":
                    peer_id, value = dato
                    self._responder_peticion_articulo(peer_id, value)
                elif tipo == "lapida_recibida":
                    self._procesar_lapida(dato)
                    refrescar_pantalla = True
                elif tipo == "refrescar_ui":
                    refrescar_pantalla = True
                elif tipo == "actualizar_respaldos":
                    if self.articulo_actual_id == dato:
                        num_respaldos = len(self.respaldos_red.get(dato, []))
                        if num_respaldos > 0:
                            self.lbl_metricas_respaldo.config(text=f"🟢 Respaldado por {num_respaldos} nodo(s) en la red")
                        else:
                            self.lbl_metricas_respaldo.config(text="⚪ Aún no tiene respaldos en la red")
                        self.lbl_metricas_respaldo.pack(pady=(5, 0)) # <-- ¡Aseguramos que se muestre!
                elif tipo == "procesar_respaldos_remotos":
                    peer_id, ids = dato
                    self._procesar_respaldos_remotos(peer_id, ids)
        except queue.Empty:
            pass
            
        # Si hubo cambios, actualizamos la tabla UNA SOLA VEZ aquí afuera
        if refrescar_pantalla:
            self._aplicar_filtro()
            self._refrescar_recientes()
            
        # Volvemos a revisar en 100 ms
        self.root.after(100, self._procesar_cola)

    def _responder_peticion_articulo(self, peer_id, value):
        if not isinstance(value, dict):
            return
            
        target = value.get("target")
        if target and target != self.node.local_id:
            return 

        articulo_id = value.get("id")
        if not articulo_id or not isinstance(articulo_id, str):
            return
            
        # Evitar inyecciones de IDs gigantes
        if len(articulo_id) > 100:
            return

        art = None
        if articulo_id in self.mis_articulos:
            art = self.mis_articulos[articulo_id]
        elif articulo_id in self.articulos_guardados:
            art = self.articulos_guardados[articulo_id]

        if art is None:
            return

        autor_nombre = art.get("autor_nombre") or self.nombre_usuario
        autor_desc = art.get("autor_descripcion") or self.mi_descripcion

        num_resp = len(self.respaldos_red.get(articulo_id, {}))
        if num_resp == 0 and articulo_id in self.articulos_guardados:
            num_resp = 1

        self._enviar_json_seguro(peer_id, "article_content", {
            "id": articulo_id, "titulo": art["titulo"], "contenido": art["contenido"],
            "likes": art.get("likes", []), "etiquetas": art.get("etiquetas", []),
            "tematica": art.get("tematica", ""), "autor": art.get("autor", self.node.local_id),
            "autor_nombre": autor_nombre, "autor_descripcion": autor_desc,
            "autor_horario": art.get("autor_horario", ""),
            "autor_utc_offset": art.get("autor_utc_offset", 0.0),
            "idioma": art.get("idioma", "Español"),
            "respaldos": num_resp
        })

    def _procesar_lapida(self, aid):
        """Aplica una lápida: elimina el artículo de todas las listas locales."""
        if aid not in self.lapidas:
            self.lapidas.add(aid)
            
        # 1. Eliminar de la lista de Descubrir
        self.articulos_descubiertos = [a for a in self.articulos_descubiertos if a["id"] != aid]
        
        # 2. Eliminar de Guardados (si lo teníamos respaldado)
        if aid in self.articulos_guardados:
            del self.articulos_guardados[aid]
            self._refrescar_guardados()
            
        # 3. Eliminar de pendientes de respaldo
        self.respaldos_pendientes.discard(aid)
        
        # 4. Si el usuario lo está leyendo en ese momento, limpiar el panel
        if self.articulo_actual_id == aid:
            self.articulo_actual_id = None
            self.etiqueta_titulo_lectura.config(text=self._t("Doble clic para leer"))
            self._cambiar_texto_lectura("")
            self.lbl_count.config(text="(0)")
            self.btn_editar.pack_forget()
            self.btn_borrar.pack_forget()
            
        self._aplicar_filtro()
        self._guardar_datos()

    def _procesar_anuncio_crudo(self, peer_id, topic, data):
        try:
            mensaje = json.loads(data.decode())
            
            if topic == "blog:system:profiles":
                firma = mensaje.pop("firma", "")
                llave = mensaje.get("llave", "")
                if self._verificar_firma(mensaje, firma, llave):
                    self.perfiles_autores[mensaje["autor"]] = {
                        "nombre": str(mensaje.get("nombre", "Anónimo"))[:50], # Límite de 50 letras
                        "descripcion": str(mensaje.get("descripcion", ""))[:500], # Límite de 500 letras
                        "horario": str(mensaje.get("horario", ""))[:50],
                        "utc_offset": float(mensaje.get("utc_offset", 0.0)),
                        "llave": llave
                    }
                    self._guardar_datos()
                    self.event_queue.put(("perfil_actualizado", mensaje["autor"]))
                return

            anuncio = mensaje
            if anuncio.get("is_delete"):
                firma = anuncio.pop("firma", "")
                llave = anuncio.get("llave", "")
                if self._verificar_firma(anuncio, firma, llave):
                    self._procesar_lapida(anuncio["id"])
                else:
                    print("🚨 ALERTA: Intento de borrado falso bloqueado.")
                return

            # VALIDACIÓN DE CAMPOS OBLIGATORIOS
            if "id" not in anuncio or "titulo" not in anuncio or "autor" not in anuncio:
                print("🚨 Anuncio malformado rechazado.")
                return

            # SANEAMIENTO (Evitar textos absurdamente largos)
            anuncio["titulo"] = str(anuncio.get("titulo", "Sin título"))[:200]
            anuncio["tematica"] = str(anuncio.get("tematica", ""))[:50]
            if "etiquetas" in anuncio and isinstance(anuncio["etiquetas"], list):
                anuncio["etiquetas"] = [str(e)[:30] for e in anuncio["etiquetas"]][:10] # Max 10 etiquetas

            if "autor" in anuncio:
                autor_id = anuncio["autor"]
                if autor_id not in self.perfiles_autores:
                    self.perfiles_autores[autor_id] = {}
                
                if "autor_nombre" in anuncio:
                    self.perfiles_autores[autor_id]["nombre"] = str(anuncio["autor_nombre"])[:50]
                if "autor_descripcion" in anuncio:
                    self.perfiles_autores[autor_id]["descripcion"] = str(anuncio["autor_descripcion"])[:500]
                if "autor_horario" in anuncio:
                    self.perfiles_autores[autor_id]["horario"] = str(anuncio["autor_horario"])[:50]
                if "autor_utc_offset" in anuncio:
                    self.perfiles_autores[autor_id]["utc_offset"] = float(anuncio["autor_utc_offset"])

            aid_anuncio = anuncio["id"]
            if aid_anuncio in self.lapidas:
                return

            if aid_anuncio in self.etiquetas_revocadas:
                revocadas_lower = [r.lower() for r in self.etiquetas_revocadas[aid_anuncio]]
                anuncio["etiquetas"] = [e for e in anuncio.get("etiquetas", []) if e.lower() not in revocadas_lower]

            self.event_queue.put(("nuevo_articulo", anuncio))

            if anuncio.get("is_update"):
                try:
                    self.node.broadcast_json("get_article", {"id": anuncio["id"], "target": anuncio["autor"]})
                except Exception:
                    pass
        except Exception as e:
            print(f"Error procesando anuncio: {e}")

    def _procesar_sync_response(self, value):
        """Procesa una respuesta de sincronización en el hilo principal."""
        if not isinstance(value, list):
            return
        for anuncio in value:
            if "autor_descripcion" in anuncio and "autor" in anuncio:
                self.perfiles_autores[anuncio["autor"]] = {"nombre": anuncio.get("autor_nombre", ""), "descripcion": anuncio["autor_descripcion"]}

            self.event_queue.put(("nuevo_articulo", anuncio))
            if anuncio["autor"] in self.autores_respaldados and anuncio["id"] not in self.articulos_guardados:
                self.respaldos_pendientes.add(anuncio["id"])
                self._enviar_json_seguro(anuncio["autor"], "get_article", {"id": anuncio["id"]})
        self._guardar_datos()

    def _procesar_contenido_recibido(self, value):
        aid = value.get("id")
        
        # VALIDACIÓN DE TAMAÑO DEL ARTÍCULO COMPLETO
        try:
            tamano_mb = len(json.dumps(value).encode('utf-8')) / (1024 * 1024)
            if tamano_mb > 5.0: # Si pesa más de 5 MB, lo rechazamos
                print(f"🚨 Artículo {aid} rechazado: excede el límite de 5 MB.")
                return
        except:
            pass

        if aid in self.respaldos_pendientes:
            self.respaldos_pendientes.remove(aid)
            
            if (self._calcular_espacio_usado() + tamano_mb) > self.limite_mb:
                print(f"⚠️ No hay espacio para respaldar {aid}")
                return
                
            anuncio = next((a for a in self.articulos_descubiertos if a["id"] == aid), None)
            if anuncio:
                self.articulos_guardados[aid] = {
                    "id": aid, "titulo": str(value.get("titulo", anuncio["titulo"]))[:200],
                    "contenido": value.get("contenido"), "autor": value.get("autor", anuncio.get("autor")),
                    "autor_nombre": value.get("autor_nombre", anuncio.get("autor_nombre")),
                    "autor_descripcion": value.get("autor_descripcion", anuncio.get("autor_descripcion")),
                    "likes": value.get("likes", anuncio.get("likes", []))
                }
                self._refrescar_guardados()
                self._guardar_datos()
                self._actualizar_barra_espacio()
                print(f"💾 Artículo respaldado: {value.get('titulo')}")
        else:
            if aid in self.etiquetas_revocadas:
                if "etiquetas" in value:
                    revocadas_lower = [r.lower() for r in self.etiquetas_revocadas[aid]]
                    value["etiquetas"] = [e for e in value["etiquetas"] if e.lower() not in revocadas_lower]

            if aid in self.articulos_guardados:
                self.articulos_guardados[aid]["contenido"] = value.get("contenido")
                self.articulos_guardados[aid]["titulo"] = str(value.get("titulo", ""))[:200]
                self.articulos_guardados[aid]["etiquetas"] = value.get("etiquetas", [])
                self.articulos_guardados[aid]["tematica"] = value.get("tematica", "")
                self.articulos_guardados[aid]["autor"] = value.get("autor", self.articulos_guardados[aid].get("autor"))
                self.articulos_guardados[aid]["autor_nombre"] = value.get("autor_nombre", self.articulos_guardados[aid].get("autor_nombre"))
                self.articulos_guardados[aid]["autor_descripcion"] = value.get("autor_descripcion", self.articulos_guardados[aid].get("autor_descripcion", ""))
                self.articulos_guardados[aid]["likes"] = value.get("likes", [])
                self.articulos_guardados[aid]["respaldos"] = value.get("respaldos", self.articulos_guardados[aid].get("respaldos", 1))
                self._refrescar_guardados()

            for a in self.articulos_descubiertos:
                if a["id"] == aid:
                    a["titulo"] = str(value.get("titulo", a["titulo"]))[:200]
                    a["etiquetas"] = value.get("etiquetas", a.get("etiquetas", []))
                    a["tematica"] = value.get("tematica", a.get("tematica", ""))
                    a["likes"] = value.get("likes", a.get("likes", []))
                    a["idioma"] = value.get("idioma", a.get("idioma", "Español"))
                    respaldos_recibidos = value.get("respaldos", 0)
                    if respaldos_recibidos > 0: a["respaldos"] = respaldos_recibidos
                    a["autor"] = value.get("autor", a.get("autor"))
                    a["autor_nombre"] = value.get("autor_nombre", a.get("autor_nombre"))
                    a["autor_descripcion"] = value.get("autor_descripcion", a.get("autor_descripcion"))
                    break
            self._aplicar_filtro()
            self._guardar_datos()

            if self.articulo_actual_id == aid:
                self._mostrar_articulo(aid, value.get("titulo", ""), value.get("contenido"), value.get("likes", []))

    # --- LISTA PRINCIPAL Y FILTROS ---
    def _agregar_a_lista(self, anuncio):
        if isinstance(anuncio.get("etiquetas"), str):
            anuncio["etiquetas"] = [e.strip() for e in anuncio["etiquetas"].split(',')]
            
        for i, existente in enumerate(self.articulos_descubiertos):
            if existente["id"] == anuncio["id"]:
                self.articulos_descubiertos[i] = anuncio
                # Ya no llamamos a _aplicar_filtro ni _refrescar_recientes aquí
                self._guardar_datos()
                return
                
        self.articulos_descubiertos.append(anuncio)
        # Ya no llamamos a _aplicar_filtro ni _refrescar_recientes aquí
        self._guardar_datos()

    def _aplicar_filtro(self):
        # Limpiar tarjetas anteriores
        for widget in self.frame_tarjetas.winfo_children():
            widget.destroy()
        self.imagenes_tarjetas.clear()

        filtro_categoria = self.combo_filtro_categoria.get()
        filtro_etiqueta = self.entrada_filtro.get().strip().lower()
        filtro_idioma = self.combo_filtro_idioma.get()

        articulos_filtrados = []
        for articulo in self.articulos_descubiertos:
            if filtro_categoria != self._t("Todas") and articulo.get("tematica") != filtro_categoria:
                continue
            if filtro_etiqueta:
                etiquetas_articulo = [str(e).lower() for e in articulo.get("etiquetas", [])]
                if filtro_etiqueta not in etiquetas_articulo:
                    continue
            if filtro_idioma != self._t("Todos") and articulo.get("idioma", "Español") != filtro_idioma:
                continue
            articulos_filtrados.append(articulo)

        # --- ORDENAMIENTO A PRUEBA DE BALAS ---
        def obtener_timestamp(art):
            try:
                # Intentar extraer del ID (formato: "hash-timestamp")
                return int(art["id"].split("-")[-1])
            except Exception as e:
                print(f"Error obteniendo timestamp de {art.get('id')}: {e}")
                return 0 
        
        articulos_filtrados.sort(key=obtener_timestamp, reverse=True)
        # --------------------------------------

        total_articulos = len(articulos_filtrados)
        total_paginas = max(1, math.ceil(total_articulos / self.articulos_por_pagina))
        if self.pagina_actual > total_paginas: self.pagina_actual = total_paginas
        if self.pagina_actual < 1: self.pagina_actual = 1

        # Primero calculamos el inicio y el fin de la página
        inicio = (self.pagina_actual - 1) * self.articulos_por_pagina
        fin = inicio + self.articulos_por_pagina

        # Ahora sí, actualizamos el texto usando las variables ya definidas
        mostrando = len(articulos_filtrados[inicio:fin])
        self.lbl_paginacion.config(text=f"Página {self.pagina_actual} de {total_paginas}, mostrando {mostrando} de {total_articulos} artículos en la red")

        # Dibujar las tarjetas en el orden correcto
        for articulo in articulos_filtrados[inicio:fin]:
            self._crear_tarjeta_articulo(articulo)

    def _crear_tarjeta_articulo(self, art):
        card = tk.Frame(self.frame_tarjetas, bg="white", bd=1, relief="solid", padx=15, pady=15)
        card.pack(fill="x", pady=10, padx=10)
        card.columnconfigure(0, weight=1)

        # Autor y Fecha
        autor = art.get("autor_nombre", "Desconocido")
        fecha_str = art.get("id", "").split("-")[-1]
        try:
            fecha = time.strftime('%d de %b', time.localtime(int(fecha_str)))
        except:
            fecha = "Hace poco"
            
        lbl_autor = tk.Label(card, text=f"👤 {autor}  ·  {fecha}", font=("Helvetica", 10), bg="white", fg="#666")
        lbl_autor.grid(row=0, column=0, sticky="w")

        # Título
        lbl_titulo = tk.Label(card, text=art.get("titulo", "Sin título"), font=("Helvetica", 16, "bold"), bg="white", fg="#000", wraplength=500, justify="left")
        lbl_titulo.grid(row=1, column=0, sticky="w", pady=(5, 5))

        # --- NUEVO: Vista Previa del Texto ---
        snippet = "Abre el artículo para leer más..."
        full_art = self.mis_articulos.get(art["id"]) or self.articulos_guardados.get(art["id"])
        if full_art and isinstance(full_art.get("contenido"), dict):
            texto_completo = full_art["contenido"].get("texto", "")
            # Limpiar saltos de línea
            texto_limpio = " ".join(texto_completo.split())
            if len(texto_limpio) > 120:
                snippet = texto_limpio[:120] + "..."
            else:
                snippet = texto_limpio

        lbl_snippet = tk.Label(card, text=snippet, font=("Helvetica", 11, "italic"), bg="white", fg="#555", wraplength=500, justify="left")
        lbl_snippet.grid(row=2, column=0, sticky="w", pady=(0, 10))

        # --- NUEVO: Categoría y Etiquetas ---
        categoria = art.get("tematica", "Sin categoría").capitalize()
        etiquetas = ", ".join(art.get("etiquetas", []))
        
        texto_meta = f"Categoría: {categoria}"
        if etiquetas:
            texto_meta += f"   |   Etiquetas: {etiquetas}"
            
        lbl_meta = tk.Label(card, text=texto_meta, font=("Helvetica", 9), bg="white", fg="#888")
        lbl_meta.grid(row=3, column=0, sticky="w")

        # Métricas (Likes y Respaldos)
        likes = len(art.get("likes", []))
        respaldos = art.get("respaldos", 0)
        frame_metricas = tk.Frame(card, bg="white")
        frame_metricas.grid(row=4, column=0, sticky="w", pady=(10, 0))
        lbl_metricas = tk.Label(frame_metricas, text=f"⭐ {likes}   ⚡ {respaldos} respaldos", font=("Helvetica", 10), bg="white", fg="#444")
        lbl_metricas.pack()

        # --- Imagen de vista previa ---
        imagen_b64 = None
        if full_art and isinstance(full_art.get("contenido"), dict):
            imgs = full_art["contenido"].get("imagenes", {})
            if imgs:
                imagen_b64 = list(imgs.values())[0]

        if imagen_b64:
            try:
                img_data = base64.b64decode(imagen_b64)
                img = Image.open(io.BytesIO(img_data))
                img.thumbnail((150, 150))
                photo = ImageTk.PhotoImage(img)
                self.imagenes_tarjetas.append(photo)
                lbl_img = tk.Label(card, image=photo, bg="white")
                lbl_img.grid(row=0, column=1, rowspan=5, padx=(20, 0), sticky="e")
            except: pass

        # --- Efecto Hover Orgánico ---
        def on_enter(e):
            for w in [card, lbl_autor, lbl_titulo, lbl_snippet, lbl_meta, frame_metricas, lbl_metricas]:
                w.configure(bg="#f0f0f0")

        def on_leave(e):
            for w in [card, lbl_autor, lbl_titulo, lbl_snippet, lbl_meta, frame_metricas, lbl_metricas]:
                w.configure(bg="white")

        for widget in [card, lbl_autor, lbl_titulo, lbl_snippet, lbl_meta, frame_metricas, lbl_metricas]:
            widget.bind("<Button-1>", lambda e, a=art: self._abrir_por_id(a["id"]))
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    def _reiniciar_paginacion(self):
        self.pagina_actual = 1
        self.canvas_descubrir.yview_moveto(0) # <-- Sube al inicio
        self._aplicar_filtro()

    def _pagina_anterior(self):
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
            self.canvas_descubrir.yview_moveto(0) # <-- Sube al inicio
            self._aplicar_filtro()

    def _pagina_siguiente(self):
        filtro_categoria = self.combo_filtro_categoria.get()
        filtro_etiqueta = self.entrada_filtro.get().strip().lower()
        filtro_idioma = self.combo_filtro_idioma.get()
        
        total = 0
        for a in self.articulos_descubiertos:
            if filtro_categoria != self._t("Todas") and a.get("tematica") != filtro_categoria: continue
            if filtro_etiqueta and filtro_etiqueta not in [e.lower() for e in a.get("etiquetas", [])]: continue
            if filtro_idioma != self._t("Todos") and a.get("idioma", "Español") != filtro_idioma: continue
            total += 1
            
        total_paginas = max(1, math.ceil(total / self.articulos_por_pagina))
        
        if self.pagina_actual < total_paginas:
            self.pagina_actual += 1
            self.canvas_descubrir.yview_moveto(0) # <-- Sube al inicio
            self._aplicar_filtro()

    # --- ABRIR Y MOSTRAR ---
    def _abrir_articulo_doble_clic(self, event):
        item = self.lista_articulos.identify_row(event.y)
        if item:
            self.lista_articulos.selection_set(item)
            self._abrir_por_id(item)

    def _abrir_guardado_doble_clic(self, event):
        sel = self.lista_guardados.curselection()
        if sel:
            self._abrir_por_id(self._guardados_ids[sel[0]])

    def _abrir_reciente_doble_clic(self, event):
        sel = self.lista_recientes.curselection()
        if sel:
            self._abrir_por_id(self._recientes_ids[sel[0]])

    def _descubrir_por_azar(self):
        if self.articulos_descubiertos:
            self._abrir_por_id(random.choice(self.articulos_descubiertos)["id"])

    def _sorprendeme(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("¡Sorpréndeme!")
        dialog.geometry("500x280") # Ventana más alta
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        msg = ("El botón '¡Sorpréndeme!' busca artículos de categorías que normalmente no lees.\n\n"
               "Su objetivo es romper la burbuja de filtro: te mostrará algo nuevo, "
               "priorizando las temáticas que menos has explorado en tus guardados.")
        
        # Empaquetamos el label con expand para que ocupe el espacio superior
        ttk.Label(dialog, text=msg, justify="center", wraplength=450, font=("TkDefaultFont", 11)).pack(pady=20, expand=True)
        
        def continuar():
            dialog.destroy()
            self._ejecutar_sorprendeme()
            
        # El botón se ancla abajo para que siempre sea visible
        ttk.Button(dialog, text="OK", command=continuar).pack(side="bottom", pady=15)
        self.root.wait_window(dialog)

        def continuar():
            dialog.destroy()
            self._ejecutar_sorprendeme()
            
        ttk.Button(dialog, text="OK", command=continuar).pack(pady=10)
        self.root.wait_window(dialog)

    def _ejecutar_sorprendeme(self):
        # 2. Determinar cuáles son las categorías habituales del usuario
        categorias_habituales = set()
        # Revisamos tanto los artículos guardados como los publicados por el propio usuario
        for art in list(self.articulos_guardados.values()) + list(self.mis_articulos.values()):
            tem = art.get("tematica")
            if tem:
                categorias_habituales.add(tem)
                
        # 3. Filtrar los artículos descubiertos que NO pertenezcan a esas categorías
        articulos_sorpresa = []
        for art in self.articulos_descubiertos:
            if art.get("tematica") not in categorias_habituales:
                articulos_sorpresa.append(art)
                
        # 4. Elegir uno al azar y abrirlo
        if articulos_sorpresa:
            elegido = random.choice(articulos_sorpresa)
            self._abrir_por_id(elegido["id"])
        else:
            # Mensaje amigable si no hay artículos fuera de su burbuja
            messagebox.showinfo(
                "Sin sorpresas por ahora", 
                "¡Parece que ya has explorado todas las categorías disponibles!\n\n"
                "Vuelve a intentarlo cuando haya nuevos artículos de otras temáticas en la red."
            )

    def _abrir_por_id(self, articulo_id, desde_coleccion=False):
        self.notebook.select(self.tab_leyendo)
        self.articulo_actual_id = articulo_id
        
        if not desde_coleccion:
            self.coleccion_en_lectura = None
            if hasattr(self, 'frame_coleccion_nav'):
                self.frame_coleccion_nav.pack_forget()
        
        if articulo_id in self.mis_articulos:
            art = self.mis_articulos[articulo_id]
            self._mostrar_articulo(articulo_id, art["titulo"], art["contenido"], art.get("likes", []))
            return
        if articulo_id in self.articulos_guardados:
            art = self.articulos_guardados[articulo_id]
            self._mostrar_articulo(articulo_id, art["titulo"], art["contenido"], art.get("likes", []))
            return

        anuncio = next((a for a in self.articulos_descubiertos if a["id"] == articulo_id), None)
        if anuncio:
            self.etiqueta_titulo_lectura.config(text=anuncio["titulo"])
            self.lbl_count.config(text=f"({len(anuncio.get('likes', []))})")
            self.lbl_heart.config(fg="#D4AF37")
            self.btn_quitar_etiqueta.pack_forget()
            
            # --- NUEVA LÓGICA P2P ---
            autor_id = anuncio.get("autor")
            
            # Si el autor está conectado, le pedimos a él (es más rápido)
            if self._esta_conectado(autor_id):
                self._cambiar_texto_lectura("Solicitando el artículo al autor...")
                self._pedir_articulo_con_reintentos(autor_id, articulo_id)
            else:
                # El autor está desconectado. ¿Sabemos quién más lo tiene?
                peers_con_copia = self.quien_tiene.get(articulo_id, [])
                
                if peers_con_copia:
                    # Pedir al primero de la lista que sepamos que lo tiene
                    peer_amigo = peers_con_copia[0]
                    self._cambiar_texto_lectura(f"El autor está desconectado.\nSolicitando copia al nodo respaldador...")
                    self._pedir_articulo_con_reintentos(peer_amigo, articulo_id)
                else:
                    # No conocemos a nadie que lo tenga. Broadcast de emergencia.
                    self._cambiar_texto_lectura("El autor está desconectado.\nBuscando copias respaldadas en toda la red...")
                    self.node.broadcast_json("get_article", {"id": articulo_id}) 
                    self.root.after(10000, lambda: self._timeout_busqueda(articulo_id))

    def _timeout_busqueda(self, articulo_id):
        # Solo mostramos el aviso si seguimos esperando el mismo artículo
        if self.articulo_actual_id == articulo_id and self.texto_lectura.get("1.0", "end-1c").startswith("El autor está desconectado"):
            self._cambiar_texto_lectura("No se encontraron nodos con este artículo en la red.\n\n"
                                        "Puede que nadie lo haya respaldado aún, o que los nodos estén desconectados.")

    def _exportar_epub(self):
        if not self.articulos_guardados:
            messagebox.showinfo("Sin artículos", "No tienes artículos guardados para exportar.")
            return
            
        ruta = filedialog.asksaveasfilename(
            defaultextension=".epub", 
            filetypes=[("EPUB", "*.epub")], 
            title="Guardar libro para e-reader",
            initialfile="Mi_Blog_P2P.epub"
        )
        if not ruta: return

        try:
            libro = epub.EpubBook()
            libro.set_identifier(f"blogp2p_{self.node.local_id[:8]}")
            libro.set_title("Colección de Blog P2P")
            libro.set_language(self.lang_code)
            libro.add_author(self.nombre_usuario)

            capitulos = []
            for i, (aid, art) in enumerate(self.articulos_guardados.items()):
                titulo = art["titulo"]
                contenido = art["contenido"]
                texto = contenido.get("texto", "")
                imagenes = contenido.get("imagenes", {})
                
                html = f"<h1>{titulo}</h1>"
                
                # Reemplazar marcadores de imagen con etiquetas <img> reales
                for img_id, b64 in imagenes.items():
                    texto = texto.replace(f"[{img_id}]", f'<br/><img src="data:image/png;base64,{b64}" style="max-width:100%;" /><br/>')
                
                # Convertir el texto a párrafos HTML
                parrafos = texto.split('\n')
                for p in parrafos:
                    if p.strip():
                        html += f"<p>{p}</p>"
                
                c = epub.EpubHtml(title=titulo, file_name=f'cap_{i}.xhtml', lang=self.lang_code)
                c.content = html
                libro.add_item(c)
                capitulos.append(c)

            libro.toc = tuple(capitulos)
            libro.add_item(epub.EpubNcx())
            libro.add_item(epub.EpubNav())
            libro.spine = ['nav'] + capitulos

            epub.write_epub(ruta, libro, {})
            messagebox.showinfo("Exportado", f"Libro generado con éxito en:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el libro:\n{e}")

    def _cambiar_texto_lectura(self, valor, autor_id=None, autor_nombre=None):
        self.texto_lectura.config(state="normal")
        self.texto_lectura.delete("1.0", "end")
        self.imagenes_lectura.clear()

        if isinstance(valor, str):
            self.texto_lectura.insert("1.0", valor)
        elif isinstance(valor, dict):
            texto = valor.get("texto", "")
            imagenes = valor.get("imagenes", {})
            self.texto_lectura.insert("1.0", texto)
            
            # Restaurar la configuración de los tags (fuentes, tamaños, alineación)
            for tag, config in valor.get("tag_configs", {}).items():
                kwargs = {}
                if "font" in config:
                    kwargs["font"] = config["font"]
                if "justify" in config:
                    kwargs["justify"] = config["justify"]
                    
                if kwargs:
                    try:
                        self.texto_lectura.tag_configure(tag, **kwargs)
                    except Exception as e:
                        print(f"Error al configurar tag {tag}: {e}")

            # Aplicar los tags al texto
            for tag, rangos in valor.get("tags", {}).items():
                for i in range(0, len(rangos), 2):
                    try:
                        self.texto_lectura.tag_add(tag, rangos[i], rangos[i+1])
                    except:
                        pass
            
            # ¡LA MAGIA! Forzar prioridad de negrita, cursiva y subrayado en el lector
            for special_tag in ["bold", "italic", "underline"]:
                if special_tag in self.texto_lectura.tag_names():
                    self.texto_lectura.tag_raise(special_tag)
            
            for img_id, b64 in imagenes.items():
                marcador = f"[{img_id}]"
                idx = self.texto_lectura.search(marcador, "1.0", tk.END)
                if idx:
                    try:
                        img_data = base64.b64decode(b64)
                        img = Image.open(io.BytesIO(img_data))
                        photo = ImageTk.PhotoImage(img)
                        self.imagenes_lectura.append(photo)
                        end_idx = f"{idx}+{len(marcador)}c"
                        self.texto_lectura.delete(idx, end_idx)
                        self.texto_lectura.image_create(idx, image=photo)
                        linea = self.texto_lectura.index(idx).split('.')[0]
                        self.texto_lectura.tag_add("center", f"{linea}.0", f"{linea}.end")
                    except Exception as e:
                        print(f"Error al cargar imagen: {e}")

        # Añadir margen superior y firma del autor
        if autor_nombre:
            self.autor_articulo_actual = autor_id
            firma = f"\nPor: {autor_nombre}\n\n"
            self.texto_lectura.insert("1.0", firma)
            self.texto_lectura.tag_add("autor_link", "2.5", f"2.5+{len(autor_nombre)}c")
        else:
            self.texto_lectura.insert("1.0", "\n")

        self.texto_lectura.config(state="disabled")

    def _mostrar_articulo(self, aid, titulo, contenido, likes=None):
        self.articulo_actual_id = aid
        self.articulo_actual_contenido = contenido
        
        # 1. Buscar la información del autor para la firma
        autor_id = None
        autor_nombre = None
        if aid in self.mis_articulos:
            autor_id = self.mis_articulos[aid].get("autor")
            autor_nombre = self.nombre_usuario
        elif aid in self.articulos_guardados:
            autor_id = self.articulos_guardados[aid].get("autor")
            autor_nombre = self.articulos_guardados[aid].get("autor_nombre")
        else:
            anuncio = next((a for a in self.articulos_descubiertos if a["id"] == aid), None)
            if anuncio:
                autor_id = anuncio.get("autor")
                autor_nombre = anuncio.get("autor_nombre")

        # Si el nombre está vacío o es genérico, buscamos en los perfiles conocidos
        if not autor_nombre or autor_nombre in ["Desconocido", "Usuario Anónimo", ""]:
            if autor_id and autor_id in self.perfiles_autores:
                autor_nombre = self.perfiles_autores[autor_id].get("nombre", "Desconocido")
            elif not autor_nombre:
                autor_nombre = "Desconocido"

        # 2. Configurar el título principal (con soporte para colecciones)
        if self.coleccion_en_lectura:
            arts = self.coleccion_en_lectura.get("articulos", [])
            total = len(arts)
            pos = self.indice_coleccion + 1
            self.etiqueta_titulo_lectura.config(text=f"{titulo}   —   (Artículo {pos} de {total})")
        else:
            if titulo:
                self.etiqueta_titulo_lectura.config(text=titulo)
            else:
                self.etiqueta_titulo_lectura.config(text="Artículo sin título")

        # 3. Calcular y mostrar los respaldos
        # 3. Calcular y mostrar los respaldos (SOLO ACTIVOS EN LAS ÚLTIMAS 24 HORAS)
        num_respaldos = 0
        ahora = time.time()
        hace_24h = ahora - 86400
        
        if aid in self.mis_articulos:
            lista = self.respaldos_red.get(aid, {})
            if isinstance(lista, dict):
                num_respaldos = sum(1 for t in lista.values() if t > hace_24h)
            else:
                num_respaldos = len(lista) # Compatibilidad con datos viejos
        else:
            art_meta = self.articulos_guardados.get(aid)
            if not art_meta:
                art_meta = next((a for a in self.articulos_descubiertos if a["id"] == aid), None)
            if art_meta:
                num_respaldos = art_meta.get("respaldos", 0)

        if hasattr(self, 'lbl_metricas_respaldo'):
            if num_respaldos > 0:
                self.lbl_metricas_respaldo.config(text=f"⚡ Respaldado por {num_respaldos} nodo(s) activos las últimas 24 horas")
            else:
                self.lbl_metricas_respaldo.config(text="☁ Aún no tiene respaldos activos en las últimas 24 horas")
                self.lbl_metricas_respaldo.pack(pady=(5, 0))

        # 4. Cargar el texto y los likes
        self._cambiar_texto_lectura(contenido, autor_id, autor_nombre)
        
        if likes is None: likes = []
        self.lbl_count.config(text=f"({len(likes)})")
        
        # 5. Limpiar y configurar los botones inferiores
        for widget in self.frame_botones_lectura.winfo_children():
            widget.pack_forget()
            
        if self.coleccion_en_lectura:
            self.btn_ver_curador.pack(side="left", padx=3)
            self.lbl_margenes.pack(side="left", padx=(15, 2))
            self.btn_margen_menos.pack(side="left", padx=2)
            self.btn_margen_mas.pack(side="left", padx=2)
            self.btn_art_anterior.pack(side="left", padx=(15, 3))
            self.btn_art_siguiente.pack(side="left", padx=3)
            self.btn_descargar_epub_col.pack(side="left", padx=3)
            self.btn_autores_coleccion.pack(side="left", padx=3)
        else:
            self.btn_guardar.pack(side="left", padx=3)
            if aid in self.mis_articulos:
                self.btn_editar.pack(side="left", padx=3)
                self.btn_borrar.pack(side="left", padx=3)
                self.lbl_heart.config(fg="grey")
            else:
                self.btn_seguir.pack(side="left", padx=3)
                self.btn_seguir_resp.pack(side="left", padx=3)
                self.lbl_heart.config(fg="#D4AF37")
                
                art_meta = self.articulos_guardados.get(aid)
                if not art_meta:
                    art_meta = next((a for a in self.articulos_descubiertos if a["id"] == aid), None)
                etiquetas = art_meta.get("etiquetas", []) if art_meta else []
                estoy_etiquetado = any(self.nombre_usuario.lower() == str(e).lower() for e in etiquetas)
                if not estoy_etiquetado and any(n.get("articulo_id") == aid for n in self.notificaciones_etiquetas):
                    estoy_etiquetado = True
                if estoy_etiquetado:
                    self.btn_quitar_etiqueta.pack(side="left", padx=3)

            self.btn_ver_autor.pack(side="left", padx=3)
            self.lbl_heart.pack(side="left")
            self.lbl_count.pack(side="left", padx=(3, 15))
            self.lbl_margenes.pack(side="left", padx=(5, 2))
            self.btn_margen_menos.pack(side="left", padx=2)
            self.btn_margen_mas.pack(side="left", padx=2)

    # --- GUARDAR / SEGUIR ---
    def _quitar_etiqueta_actual(self):
        if not self.articulo_actual_id: return
        aid = self.articulo_actual_id
        mi_nombre = self.nombre_usuario

        if messagebox.askyesno("Quitar etiqueta", "¿Seguro que quieres retirar tu nombre de las etiquetas de este artículo?\n\nLa red respetará tu decisión."):
            if aid not in self.etiquetas_revocadas:
                self.etiquetas_revocadas[aid] = []
            if mi_nombre not in self.etiquetas_revocadas[aid]:
                self.etiquetas_revocadas[aid].append(mi_nombre)

            # Actualizar modelo local (ignorando mayúsculas/minúsculas)
            for art in self.articulos_descubiertos:
                if art["id"] == aid:
                    art["etiquetas"] = [e for e in art.get("etiquetas", []) if e.lower() != mi_nombre.lower()]
            if aid in self.articulos_guardados:
                self.articulos_guardados[aid]["etiquetas"] = [e for e in self.articulos_guardados[aid].get("etiquetas", []) if e.lower() != mi_nombre.lower()]

            self.notificaciones_etiquetas = [n for n in self.notificaciones_etiquetas if n.get("articulo_id") != aid]
            self._refrescar_notificaciones()

            try:
                self.node.broadcast_json("tag_revoked", {"id": aid, "nombre_a_quitar": mi_nombre})
                print(f"🛡️ Revocación de identidad emitida para {aid} desde la vista de lectura")
            except Exception as e:
                print(f"Error al emitir revocación: {e}")

            self._aplicar_filtro()
            self._refrescar_guardados()
            self._guardar_datos()
            
            self.btn_quitar_etiqueta.pack_forget()
            messagebox.showinfo("Identidad protegida", "Tu nombre ha sido retirado de la etiqueta de este artículo.")

    def _dialogo_guardar_con_imagenes(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Opciones de guardado")
        dialog.geometry("500x200")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        # Centrar la ventana en la pantalla
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (dialog.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill="both", expand=True)

        msg = "Este artículo contiene imágenes.\n¿Cómo deseas guardarlo?"
        ttk.Label(main_frame, text=msg, justify="center", font=("TkDefaultFont", 12, "bold")).pack(pady=(0, 10))
        
        sub_msg = "Guardarlo sin imágenes ahorra espacio en tu disco."
        ttk.Label(main_frame, text=sub_msg, justify="center", font=("TkDefaultFont", 10)).pack(pady=(0, 20))

        frame_btns = ttk.Frame(main_frame)
        frame_btns.pack(fill="x", pady=10)

        resultado = [None]
        def elegir(val):
            resultado[0] = val
            dialog.destroy()

        ttk.Button(frame_btns, text="Con imágenes", command=lambda: elegir(True), width=15).pack(side="left", padx=5)
        ttk.Button(frame_btns, text="Sin imágenes", command=lambda: elegir(False), width=15).pack(side="left", padx=5)
        ttk.Button(frame_btns, text="Cancelar", command=lambda: elegir(None), width=12).pack(side="right", padx=5)

        self.root.wait_window(dialog)
        return resultado[0]
    def _guardar_articulo_actual(self):
        if not self.articulo_actual_id or self.articulo_actual_contenido is None:
            messagebox.showinfo("Sin artículo", "No hay artículo abierto.")
            return
        aid = self.articulo_actual_id
        if aid in self.articulos_guardados:
            messagebox.showinfo("Ya guardado", "Ya está en guardados.")
            return

        contenido_a_guardar = self.articulo_actual_contenido

        if isinstance(contenido_a_guardar, dict) and contenido_a_guardar.get("imagenes"):
            resp = self._dialogo_guardar_con_imagenes()
            if resp is None:
                return
            elif resp is False:
                import copy
                contenido_a_guardar = copy.deepcopy(contenido_a_guardar)
                texto = contenido_a_guardar.get("texto", "")
                for img_id in contenido_a_guardar.get("imagenes", {}).keys():
                    texto = texto.replace(f"[{img_id}]", "[imagen no disponible, este artículo fue respaldado sin imágenes]")
                contenido_a_guardar["texto"] = texto
                contenido_a_guardar["imagenes"] = {}

        tamano_nuevo = len(json.dumps(contenido_a_guardar).encode('utf-8')) / (1024 * 1024)
        if (self._calcular_espacio_usado() + tamano_nuevo) > self.limite_mb:
            messagebox.showerror("Sin espacio", "Has alcanzado tu límite de almacenamiento. Aumenta el límite o borra artículos.")
            return

        autor = ""
        autor_nombre = ""
        autor_desc = ""
        likes = []
        
        if aid in self.mis_articulos:
            autor = self.mis_articulos[aid]["autor"]
            autor_nombre = self.nombre_usuario
            autor_desc = self.mi_descripcion
            likes = self.mis_articulos[aid].get("likes", [])
        else:
            anuncio = next((a for a in self.articulos_descubiertos if a["id"] == aid), None)
            if anuncio: 
                autor = anuncio.get("autor")
                autor_nombre = anuncio.get("autor_nombre", "")
                autor_desc = anuncio.get("autor_descripcion", "")
                likes = anuncio.get("likes", [])
                
        if not autor_nombre or autor_nombre in ["Desconocido", "Usuario Anónimo", ""]:
            if autor and autor in self.perfiles_autores:
                autor_nombre = self.perfiles_autores[autor].get("nombre", "Desconocido")
            elif not autor_nombre:
                autor_nombre = "Desconocido"

        titulo = self.etiqueta_titulo_lectura.cget("text").split("   —")[0]
        # Averiguar cuántos respaldos tenía el anuncio original (si lo conocemos)
        respaldos_actuales = 1
        anuncio_orig = next((a for a in self.articulos_descubiertos if a["id"] == aid), None)
        if anuncio_orig:
            respaldos_actuales = max(1, anuncio_orig.get("respaldos", 0) + 1)

        self.articulos_guardados[aid] = {
            "id": aid, 
            "titulo": titulo, 
            "contenido": contenido_a_guardar, 
            "autor": autor, 
            "autor_nombre": autor_nombre,
            "autor_descripcion": autor_desc,
            "likes": likes,
            "respaldos": respaldos_actuales  # <-- NUEVO
        }
        self._refrescar_guardados()
        self._guardar_datos()
        self._actualizar_barra_espacio()
        if autor and autor != self.node.local_id:
            try:
                self._enviar_json_seguro(autor, "save_ping", {"id": aid})
            except Exception:
                pass

        # Anunciar a toda la red que ahora tenemos una copia
        try:
            self.node.publish("blog:backups", json.dumps({"id": aid, "peer": self.node.local_id}).encode())
            # Guardarlo en nuestra propia tabla
            if aid not in self.quien_tiene: self.quien_tiene[aid] = []
            if self.node.local_id not in self.quien_tiene[aid]: self.quien_tiene[aid].append(self.node.local_id)
        except Exception as e:
            print(f"Error al anunciar copia: {e}")
        
        # Refrescar la vista de lectura para mostrar el nuevo contador de respaldos
        if self.articulo_actual_id == aid:
            self._mostrar_articulo(aid, titulo, contenido_a_guardar, likes)
            
        messagebox.showinfo("Guardado", "Artículo añadido.")

    def _borrar_guardado(self):
        sel = self.lista_guardados.curselection()
        if not sel:
            messagebox.showinfo("Sin selección", "Selecciona un artículo de la lista para borrar.")
            return
        
        # Obtenemos el índice real y sacamos el ID exacto
        indice = sel[0]
        aid = self._guardados_ids[indice]
        
        if aid not in self.articulos_guardados:
            return

        titulo = self.articulos_guardados[aid]["titulo"]
        
        if messagebox.askyesno("Confirmar", f"¿Seguro que quieres borrar el artículo guardado:\n'{titulo}'?"):
            # Avisar al autor que ya no respaldamos este artículo
            autor_del_articulo = self.articulos_guardados[aid].get("autor")
            if autor_del_articulo and autor_del_articulo != self.node.local_id:
                try:
                    self._enviar_json_seguro(autor_del_articulo, "remove_ping", {"id": aid})
                except Exception:
                    pass

            # ¡NUEVO! Anunciar a toda la red que ya no tenemos esta copia
            try:
                self.node.publish("blog:backups_remove", json.dumps({"id": aid, "peer": self.node.local_id}).encode())
            except Exception:
                pass

            # Eliminamos del diccionario
            del self.articulos_guardados[aid]
            
            # Forzamos el refresco de la interfaz
            self._refrescar_guardados()
            self._guardar_datos()
            self._actualizar_barra_espacio()
            
            # Si el artículo que borramos es el que estamos leyendo, limpiamos la pantalla
            if self.articulo_actual_id == aid:
                self.articulo_actual_id = None
                self.articulo_actual_contenido = None
                self.etiqueta_titulo_lectura.config(text=self._t("Doble clic para leer"))
                self._cambiar_texto_lectura("")
                self.lbl_count.config(text="(0)")
                self.lbl_heart.config(fg="grey")
                self.btn_editar.pack_forget()
                self.btn_borrar.pack_forget()
                if hasattr(self, 'lbl_metricas_respaldo'):
                    self.lbl_metricas_respaldo.pack_forget()
            
            print(f"🗑️ Artículo eliminado de los guardados: {titulo}")

    def _refrescar_guardados(self):
        self.lista_guardados.delete(0, "end")
        self._guardados_ids = list(self.articulos_guardados.keys())
        for aid in self._guardados_ids:
            self.lista_guardados.insert("end", self.articulos_guardados[aid]["titulo"][:32])

    def _seguir_autor_actual(self):
        self._logica_seguir(respaldar=False)

    def _seguir_y_respaldar(self):
        self._logica_seguir(respaldar=True)

    def _logica_seguir(self, respaldar=False):
        if not self.articulo_actual_id: return
        aid = self.articulo_actual_id
        autor = None
        if aid in self.mis_articulos: autor = self.mis_articulos[aid]["autor"]
        else:
            anuncio = next((a for a in self.articulos_descubiertos if a["id"] == aid), None)
            if anuncio: autor = anuncio["autor"]
        if not autor or autor == self.node.local_id: return

        self.autores_seguidos.add(autor)
        if respaldar:
            self.autores_respaldados.add(autor)
            for art in self.articulos_descubiertos:
                if art["autor"] == autor and art["id"] not in self.articulos_guardados:
                    self.respaldos_pendientes.add(art["id"])
                    self._enviar_json_seguro(autor, "get_article", {"id": art["id"]})
        # --- NUEVO: Enviar el aviso de seguimiento al autor ---
        try:
            tipo_aviso = "respaldar" if respaldar else "seguir"
            self._enviar_json_seguro(autor, "follow_ping", {
                "nombre": self.nombre_usuario, 
                "descripcion": self.mi_descripcion,
                "tipo": tipo_aviso
            })
        except Exception as e:
            print(f"No se pudo enviar el aviso de seguimiento: {e}")
        # -----------------------------------------------------
            messagebox.showinfo("Respaldando", "Has empezado a respaldar a este autor. Sus artículos se están descargando.")

        self._refrescar_autores()
        self._refrescar_recientes()
        self._guardar_datos()

    def _dejar_de_seguir(self):
        autor_id = self.autor_perfil_actual
        if not autor_id or autor_id == self.node.local_id:
            messagebox.showinfo("Perfil no válido", "No puedes dejar de seguirte a ti mismo o no hay un perfil abierto.")
            return
            
        nombre = self.lbl_nombre_autor.cget("text")
        if messagebox.askyesno("Dejar de seguir", f"¿Dejar de seguir a {nombre}?\n\nSus artículos ya no aparecerán en 'Recientes de seguidos'."):
            self.autores_seguidos.discard(autor_id)
            self.autores_respaldados.discard(autor_id)
            self._refrescar_autores()
            self._refrescar_recientes()
            self._guardar_datos()
            messagebox.showinfo("Hecho", f"Has dejado de seguir a {nombre}.")

    def _dejar_de_respaldar(self):
        autor_id = self.autor_perfil_actual
        if not autor_id or autor_id == self.node.local_id:
            messagebox.showinfo("Perfil no válido", "No puedes dejar de respaldarte a ti mismo o no hay un perfil abierto.")
            return
            
        nombre = self.lbl_nombre_autor.cget("text")
        if autor_id not in self.autores_respaldados:
            messagebox.showinfo("No respaldado", f"No estás respaldando a {nombre}.")
            return
            
        if messagebox.askyesno("Dejar de respaldar", f"¿Dejar de respaldar a {nombre}?\n\nSus artículos ya no se ofrecerán a la red desde tu nodo. Los que ya tienes guardados se conservan como guardados personales."):
            self.autores_respaldados.discard(autor_id)
            self._refrescar_autores()
            self._guardar_datos()
            messagebox.showinfo("Hecho", f"Has dejado de respaldar a {nombre}.")

    def _refrescar_autores(self):
        self.lista_autores.delete(0, "end")
        self._autores_lista_ids = []
        for autor_id in sorted(self.autores_seguidos):
            nombre = autor_id[:16] + "..."
            for art in self.articulos_descubiertos:
                if art.get("autor") == autor_id and art.get("autor_nombre"):
                    nombre = art["autor_nombre"]; break
            if autor_id in self.autores_respaldados:
                nombre += " (Respaldado)"
            self.lista_autores.insert("end", nombre)
            self._autores_lista_ids.append(autor_id)

    def _al_seleccionar_autor(self, event):
        sel = self.lista_autores.curselection()
        if not sel: return
        autor_id = self._autores_lista_ids[sel[0]]
        nombre_mostrar = self.lista_autores.get(sel[0])
        self.etiqueta_titulo_recientes.config(text=f"Artículos de {nombre_mostrar}")
        self.lista_recientes.delete(0, "end")
        self._recientes_ids = []
        for art in self.articulos_descubiertos:
            if art.get("autor") == autor_id:
                self.lista_recientes.insert("end", art["titulo"][:32])
                self._recientes_ids.append(art["id"])

    def _refrescar_recientes(self):
        if self.lista_autores.curselection(): return
        self.etiqueta_titulo_recientes.config(text=self._t("Recientes de seguidos"))
        self.lista_recientes.delete(0, "end")
        self._recientes_ids = []
        for art in self.articulos_descubiertos:
            if art.get("autor") in self.autores_seguidos:
                self.lista_recientes.insert("end", art["titulo"][:32])
                self._recientes_ids.append(art["id"])

    def _abrir_autor_seleccionado_doble_clic(self, event):
        sel = self.lista_autores.curselection()
        if sel:
            autor_id = self._autores_lista_ids[sel[0]]
            self._abrir_perfil_autor(autor_id)

    def _preparar_edicion(self):
        if not self.articulo_actual_id or self.articulo_actual_id not in self.mis_articulos:
            return
        
        art = self.mis_articulos[self.articulo_actual_id]
        self.editando_id = self.articulo_actual_id
        
        self.entrada_titulo.delete(0, "end")
        self.entrada_titulo.insert(0, art["titulo"])
        self.entrada_etiqueta.delete(0, "end")
        self.entrada_etiqueta.insert(0, ", ".join(art["etiquetas"]))
        self.combo_tematica.set(art["tematica"])
        
        # Cargar idioma
        idioma_art = art.get("idioma", self._t("Automático"))
        if idioma_art in IDIOMAS:
            self.combo_idioma_publicar.set(idioma_art)
        else:
            self.combo_idioma_publicar.set(self._t("Automático"))
        
        self.texto_contenido.delete("1.0", "end")
        contenido_rico = art["contenido"]
        self.texto_contenido.insert("1.0", contenido_rico.get("texto", ""))
        
        for tag, rangos in contenido_rico.get("tags", {}).items():
            for i in range(0, len(rangos), 2):
                self.texto_contenido.tag_add(tag, rangos[i], rangos[i+1])
                
        self.imagenes_temporales = dict(contenido_rico.get("imagenes", {}))
        
        self.notebook.select(self.tab_publicar)
        self.btn_publicar.config(text="Guardar cambios")

    def _borrar_mi_articulo(self):
        if not self.articulo_actual_id or self.articulo_actual_id not in self.mis_articulos:
            return
        
        aid = self.articulo_actual_id
        if messagebox.askyesno("Borrar artículo", "¿Seguro que quieres borrar este artículo permanentemente?\nSe enviará una orden a los que lo tengan guardado."):
            del self.mis_articulos[aid]
            
            # Registrar la lápida
            self.lapidas.add(aid)
            
            # FIRMAR EL MENSAJE DE BORRADO (PASO 4)
            mensaje_borrado = {"id": aid, "is_delete": True, "autor": self.node.local_id, "llave": self.llave_publica}
            mensaje_borrado["firma"] = self._firmar_mensaje(mensaje_borrado)
            
            for tematica in TEMATICAS:
                self.node.publish(f"blog:tematica:{tematica}", json.dumps(mensaje_borrado).encode())
            
            self._guardar_datos()
            self._refrescar_mis_articulos()
            self._actualizar_barra_espacio()
            self.etiqueta_titulo_lectura.config(text=self._t("Doble clic para leer"))
            self._cambiar_texto_lectura("")
            self.lbl_count.config(text="(0)")
            self.lbl_heart.config(fg="grey")
            self.btn_editar.pack_forget()
            self.btn_borrar.pack_forget()
            messagebox.showinfo("Borrado", "Artículo eliminado y orden de borrado enviada a la red.")

    def _ver_perfil_actual(self):
        if not self.articulo_actual_id: return
        
        autor_id = None
        if self.articulo_actual_id in self.mis_articulos:
            autor_id = self.node.local_id
        else:
            anuncio = next((a for a in self.articulos_descubiertos if a["id"] == self.articulo_actual_id), None)
            if anuncio:
                autor_id = anuncio["autor"]
                
        if autor_id:
            self._abrir_perfil_autor(autor_id)

    def _abrir_perfil_autor(self, autor_id):
        self.autor_perfil_actual = autor_id
        self.notebook.select(self.tab_autores)
        
        perfil = self.perfiles_autores.get(autor_id, {})
        nombre = perfil.get("nombre", "Autor Desconocido")
        desc = perfil.get("descripcion", "")
        
        if not desc:
            for art in self.articulos_descubiertos:
                if art.get("autor") == autor_id and art.get("autor_descripcion"):
                    desc = art["autor_descripcion"]
                    nombre = art.get("autor_nombre", nombre)
                    break
        
        if not desc:
            desc = "Este autor aún no ha escrito una descripción."
        
        if autor_id == self.node.local_id:
            nombre = self.nombre_usuario
            desc = self.mi_descripcion if self.mi_descripcion else "Aún no has escrito una descripción."

        self.lbl_nombre_autor.config(text=nombre)
        
        # --- LÓGICA DE ESTADO DE CONEXIÓN ---
        if autor_id == self.node.local_id:
            self.lbl_estado_conexion.config(text="● Tú (en línea ahora)", foreground="green")
        elif hasattr(self, '_esta_conectado') and self._esta_conectado(autor_id):
            self.lbl_estado_conexion.config(text="● En línea ahora", foreground="green")
        else:
            horario_autor = perfil.get("horario", "")
            if horario_autor:
                self.lbl_estado_conexion.config(text=f"◷ Suele conectarse: {horario_autor}", foreground="#555")
            else:
                ultima_vez = perfil.get("ultima_conexion", 0)
                if ultima_vez > 0:
                    import datetime
                    dt_local = datetime.datetime.fromtimestamp(ultima_vez)
                    self.lbl_estado_conexion.config(text=f"○ Activo por última vez: {dt_local.strftime('%d/%m/%Y a las %H:%M')}", foreground="gray")
                else:
                    self.lbl_estado_conexion.config(text="○ Estado de conexión desconocido", foreground="gray")
        # -----------------------------------

        self.texto_desc_autor.config(state="normal")
        self.texto_desc_autor.delete("1.0", "end")
        self.texto_desc_autor.insert("1.0", desc)
        self.texto_desc_autor.config(state="disabled")
        
        # --- ARTÍCULOS ---
        for item in self.lista_articulos_autor.get_children():
            self.lista_articulos_autor.delete(item)
            
        mis_arts = []
        if autor_id == self.node.local_id:
            mis_arts = list(self.mis_articulos.values())
        else:
            mis_arts = [a for a in self.articulos_descubiertos if a["autor"] == autor_id]
            
        mis_arts.sort(key=lambda x: x["id"], reverse=True)
        
        for art in mis_arts:
            self.lista_articulos_autor.insert("", "end", iid=art["id"], values=(art["titulo"], art.get("tematica", ""), art["id"]))

        # --- COLECCIONES PÚBLICAS ---
        for item in self.lista_colecciones_autor.get_children():
            self.lista_colecciones_autor.delete(item)
            
        cols_autor = []
        if autor_id == self.node.local_id:
            cols_autor = [c for c in self.mis_colecciones.values() if c.get("autor") == self.node.local_id]
        else:
            cols_autor = [c for c in self.colecciones_descubiertas.values() if c.get("autor") == autor_id]
            cols_autor.extend([c for c in self.mis_colecciones.values() if c.get("autor") == autor_id])
            
        for col in cols_autor:
            self.lista_colecciones_autor.insert("", "end", iid=col["id"], values=(col["titulo"], col.get("descargas", 0)))

    def _abrir_articulo_doble_clic_autor(self, event):
        item = self.lista_articulos_autor.identify_row(event.y)
        if item:
            self.lista_articulos_autor.selection_set(item)
            self._abrir_por_id(item)

    def _obtener_ip_local(self):
        import socket
        try:
            # Esto obtiene la IP de la interfaz que usaría para salir a Internet.
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    def _traducir_horario(self, horario_str, utc_offset_autor):
        if not horario_str: return ""
        import re
        from datetime import datetime, timedelta
        import time
        
        # Calcular mi offset actual
        mi_utc_offset = -time.timezone / 3600.0
        diferencia = mi_utc_offset - utc_offset_autor
        
        if diferencia == 0:
            return horario_str
            
        # Buscar todas las horas en formato HH:MM dentro del texto (ej: 18:00)
        horas = re.findall(r'(\d{1,2}):(\d{2})', horario_str)
        if not horas:
            return horario_str
            
        nueva_hora_str = horario_str
        for h, m in horas:
            try:
                dt = datetime.now().replace(hour=int(h), minute=int(m))
                dt_nueva = dt + timedelta(hours=diferencia)
                hora_orig = f"{h.zfill(2)}:{m}"
                hora_nueva = dt_nueva.strftime("%H:%M")
                nueva_hora_str = nueva_hora_str.replace(hora_orig, hora_nueva)
            except:
                pass
                
        return f"{horario_str} (equivale a {nueva_hora_str} en tu hora local)"

    def _esta_conectado(self, peer_id):
        """Devuelve True si el peer ya está en la lista de conectados."""
        try:
            return peer_id in self.node.peer_ids
        except Exception:
            return False

    def _conectar_a_peer(self, host, port):
        """Intenta conectar con el peer usando su IP y puerto."""
        if host and port:
            try:
                self.node.connect(host, port)
                # Damos un instante para que la conexión se establezca.
                self.root.after(500, lambda: None)
            except Exception as e:
                print(f"No se pudo conectar a {host}:{port} -> {e}")

    def _pedir_articulo_con_reintentos(self, peer_id, articulo_id, intentos=15):
        """Intenta enviar get_article; si el peer aún no está listo, reintenta."""
        if intentos <= 0:
            print(f"❌ Autor {peer_id[:12]} no responde. Buscando en toda la red...")
            self._cambiar_texto_lectura("El autor no responde.\nBuscando copias respaldadas en la red P2P...")
            # ¡EL CAMBIO CLAVE! Broadcast SIN target, para que cualquiera que lo tenga responda.
            try:
                self.node.broadcast_json("get_article", {"id": articulo_id})
                self.root.after(10000, lambda: self._timeout_busqueda(articulo_id))
            except Exception as e:
                print(f"Error en broadcast: {e}")
            return

        from librats_py.exceptions import RatsNoSuchPeerError
        try:
            self.node.send_json(peer_id, "get_article", {"id": articulo_id, "target": peer_id})
            print(f"✅ get_article enviado a {peer_id[:12]}")
        except RatsNoSuchPeerError:
            self.root.after(200, lambda: self._pedir_articulo_con_reintentos(peer_id, articulo_id, intentos - 1))
        except Exception as e:
            print(f"Error enviando get_article: {e}")
            self.root.after(200, lambda: self._pedir_articulo_con_reintentos(peer_id, articulo_id, intentos - 1))

    def _enviar_json_seguro(self, peer_id, tipo, datos):
        """Envía un mensaje JSON y captura el error si el peer ya no está."""
        from librats_py.exceptions import RatsNoSuchPeerError
        try:
            self.node.send_json(peer_id, tipo, datos)
        except RatsNoSuchPeerError:
            print(f"El par {peer_id[:12]}... ya no está conectado. No se pudo enviar '{tipo}'.")
            self.root.after(0, lambda: messagebox.showwarning(
                "Autor desconectado",
                "El autor de este artículo ya no está en línea. Inténtalo de nuevo más tarde."
            ))

    def _al_cerrar(self):
        self._guardar_datos()
        self.conn.close()
        self.node.destroy()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BlogP2PApp(root)
    root.mainloop()
