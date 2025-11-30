"""
Gestor de sesiones persistentes
Mantiene las sesiones activas incluso al refrescar el navegador
"""

import os
import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path

class SessionManager:
    def __init__(self, session_file="data/sessions.json"):
        self.session_file = session_file
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Crear archivo de sesiones si no existe"""
        if not os.path.exists(self.session_file):
            os.makedirs(os.path.dirname(self.session_file), exist_ok=True)
            self._save_sessions({})
    
    def _load_sessions(self):
        """Cargar sesiones desde archivo"""
        try:
            with open(self.session_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_sessions(self, sessions):
        """Guardar sesiones en archivo"""
        with open(self.session_file, 'w', encoding='utf-8') as f:
            json.dump(sessions, f, indent=2)
    
    def _clean_expired_sessions(self):
        """Eliminar sesiones expiradas"""
        sessions = self._load_sessions()
        now = datetime.now()
        
        # Filtrar sesiones válidas
        valid_sessions = {}
        for session_id, data in sessions.items():
            expiry = datetime.fromisoformat(data['expiry'])
            if expiry > now:
                valid_sessions[session_id] = data
        
        if len(valid_sessions) != len(sessions):
            self._save_sessions(valid_sessions)
        
        return valid_sessions
    
    def create_session(self, username, user_data, days=7):
        """
        Crear una nueva sesión
        
        Args:
            username: Nombre de usuario
            user_data: Datos del usuario
            days: Días hasta que expire la sesión
        
        Returns:
            session_id: ID de la sesión creada
        """
        sessions = self._clean_expired_sessions()
        
        # Crear ID de sesión único
        timestamp = datetime.now().isoformat()
        session_id = hashlib.sha256(f"{username}{timestamp}".encode()).hexdigest()
        
        # Guardar sesión
        sessions[session_id] = {
            'username': username,
            'user_data': user_data,
            'created': timestamp,
            'expiry': (datetime.now() + timedelta(days=days)).isoformat()
        }
        
        self._save_sessions(sessions)
        return session_id
    
    def get_session(self, session_id):
        """
        Obtener datos de una sesión
        
        Args:
            session_id: ID de la sesión
        
        Returns:
            user_data o None si la sesión no existe o expiró
        """
        sessions = self._clean_expired_sessions()
        
        if session_id in sessions:
            session_data = sessions[session_id]
            expiry = datetime.fromisoformat(session_data['expiry'])
            
            if expiry > datetime.now():
                return session_data['user_data']
        
        return None
    
    def delete_session(self, session_id):
        """
        Eliminar una sesión
        
        Args:
            session_id: ID de la sesión a eliminar
        """
        sessions = self._load_sessions()
        
        if session_id in sessions:
            del sessions[session_id]
            self._save_sessions(sessions)
    
    def delete_user_sessions(self, username):
        """
        Eliminar todas las sesiones de un usuario 
        
        Args:
            username: Nombre de usuario
        """
        sessions = self._load_sessions()
        
        # Filtrar sesiones que no sean del usuario
        sessions = {
            sid: data for sid, data in sessions.items()
            if data['username'] != username
        }
        
        self._save_sessions(sessions)
