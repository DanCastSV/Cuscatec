# app_chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import PerfilUsuario
from django.contrib.auth.models import User
import google.generativeai as genai
import os
from dotenv import load_dotenv

# cargar .env y configurar la API
load_dotenv()  # busca .env en la raíz del proyecto
GENAI_API_KEY = os.getenv('GENAI_API_KEY')
genai.configure(api_key=GENAI_API_KEY)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs'].get('room_name', 'lobby')
        self.group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')
        
        # obtener información del usuario y grado
        perfil = await self.get_perfil_sync(self.user.id)
        nombre_usuario = self.user.username
        grado = perfil.grado if perfil else "No especificado"
        
        # obtener respuesta de Gemini con contexto del usuario
        response = await self.get_gemini_response(message, nombre_usuario, grado)
        
        # reenviar al grupo
        await self.channel_layer.group_send(
            self.group_name,
            {"type": "chat.message", "message": response}
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))

    @staticmethod
    @database_sync_to_async
    def get_perfil_sync(user_id):
        try:
            return PerfilUsuario.objects.get(user__id=user_id)
        except PerfilUsuario.DoesNotExist:
            return None

    @staticmethod
    @database_sync_to_async
    def get_gemini_response_sync(user_message, nombre_usuario, grado):
        try:
            # Usar gemini-2.5-flash (disponible y rápido)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # Crear un prompt que incluya el contexto del usuario y su grado
            prompt = f"""Eres un asistente educativo amable y útil. 
Estás ayudando a {nombre_usuario} quien está en {grado}.
Adapta tus respuestas al nivel de {grado}.
Sé conciso, educativo y motivador.

Pregunta del estudiante: {user_message}"""

            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error al conectar con Gemini: {str(e)}"

    async def get_gemini_response(self, message, nombre_usuario, grado):
        return await self.get_gemini_response_sync(message, nombre_usuario, grado)
