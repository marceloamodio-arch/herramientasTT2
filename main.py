#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Cálculos y Herramientas
Tribunal de Trabajo 2 de Quilmes

Aplicación principal con autenticación y menú de acceso a todas las herramientas
"""

import streamlit as st
from pathlib import Path
import sys

# Configurar el path para importar módulos
sys.path.insert(0, str(Path(__file__).parent))

# Importar módulo de autenticación
from utils.auth import AuthSystem

# Importar session manager (opcional - para persistencia de sesión)
try:
    from utils.session_manager import SessionManager
    SESSION_MANAGER_AVAILABLE = True
except ImportError:
    SESSION_MANAGER_AVAILABLE = False
    SessionManager = None

# Configuración de la página
st.set_page_config(
    page_title="Sistema Tribunal de Trabajo 2 Quilmes",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Información de las aplicaciones disponibles
APLICACIONES = {
    "ibm": {
        "nombre": "Calculadora IBM",
        "icono": "💰",
        "descripcion": "Cálculo de Indemnización Base Mensual según normativa laboral vigente",
        "archivo": "apps.ibm",
        "función": "main",
        "nivel_requerido": "normal"
    },
    "actualizacion": {
        "nombre": "Actualización de Valores",
        "icono": "📈",
        "descripcion": "Actualización de montos mediante índices IPC, RIPTE y otros",
        "archivo": "apps.actualizacion",
        "función": "main",
        "nivel_requerido": "normal"
    },
    "lrt": {
        "nombre": "Calculadora LRT",
        "icono": "🧮",
        "descripcion": "Cálculo de indemnizaciones según Ley de Riesgos del Trabajo",
        "archivo": "apps.calculadora_lrt",
        "función": "main",
        "nivel_requerido": "normal"
    },
    "despidos": {
        "nombre": "Calculadora de Despidos",
        "icono": "📊",
        "descripcion": "Cálculo de indemnizaciones por despido según tipo y antigüedad",
        "archivo": "apps.calculadora_despidos",
        "función": "main",
        "nivel_requerido": "normal"
    },
    "honorarios": {
        "nombre": "Cálculo de Honorarios",
        "icono": "⚖️",
        "descripcion": "Determinación de honorarios profesionales según Ley 14.967",
        "archivo": "apps.honorarios",
        "función": "main",
        "nivel_requerido": "normal"
    },
    "admin": {
        "nombre": "Administración",
        "icono": "⚙️",
        "descripcion": "Gestión de usuarios y edición de datasets del sistema",
        "archivo": "apps.administracion",
        "función": "main",
        "nivel_requerido": "admin"
    }
}

# CSS personalizado para el sistema
def load_custom_css():
    st.markdown("""
        <style>
        /* Estilos generales */
        .main-title {
            text-align: center;
            color: #1f4788;
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            padding: 1rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .subtitle {
            text-align: center;
            color: #555;
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }
        
        /* Tarjetas de aplicaciones */
        .app-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
            border-left: 4px solid #667eea;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .app-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
        }
        
        .app-card h3 {
            color: #1f4788;
            margin-bottom: 0.5rem;
        }
        
        .app-card p {
            color: #666;
            font-size: 0.95rem;
        }
        
        /* Botones */
        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            font-weight: 600;
            border-radius: 8px;
            transition: all 0.3s;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
        }
        
        /* Información del footer */
        .footer {
            text-align: center;
            color: #888;
            font-size: 0.85rem;
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid #eee;
        }
        
        /* Login */
        .login-box {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)

def mostrar_login():
    """Muestra pantalla de login"""
    auth = AuthSystem()
    session_mgr = SessionManager() if SESSION_MANAGER_AVAILABLE else None
    
    # Header
    st.markdown("""
        <div style='text-align: center; padding: 3rem 0 2rem 0;'>
            <h1 style='color: #667eea; font-size: 4rem; margin: 0;'>⚖️</h1>
            <h1 style='color: #1f4788; margin: 1rem 0 0.5rem 0;'>Sistema de Cálculos y Herramientas</h1>
            <p style='color: #666; font-size: 1.1rem;'>Tribunal de Trabajo N° 2 de Quilmes</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Formulario de login centrado
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown("### 🔐 Iniciar Sesión")
        
        with st.form("login_form"):
            username = st.text_input(
                "Usuario", 
                placeholder="Ingresa tu usuario",
                help="Usuario creado por el administrador"
            )
            password = st.text_input(
                "Contraseña", 
                type="password", 
                placeholder="Ingresa tu contraseña"
            )
            
            # Solo mostrar checkbox si SessionManager está disponible
            recordar = False
            if SESSION_MANAGER_AVAILABLE:
                recordar = st.checkbox("🔒 Mantener sesión iniciada", value=True, help="Mantiene tu sesión activa incluso al refrescar la página")
            
            col_btn1, col_btn2 = st.columns([1, 1])
            
            with col_btn1:
                submit = st.form_submit_button("🔓 Ingresar", use_container_width=True, type="primary")
            
            if submit:
                if not username or not password:
                    st.error("⚠️ Por favor completa todos los campos")
                else:
                    # Autenticar usuario
                    autenticado, usuario_data = auth.autenticar(username, password)
                    
                    if autenticado:
                        # Guardar usuario en sesión
                        st.session_state.autenticado = True
                        st.session_state.usuario = usuario_data
                        
                        # Si marcó "recordar sesión" y está disponible, crear sesión persistente
                        if recordar and SESSION_MANAGER_AVAILABLE and session_mgr:
                            session_id = session_mgr.create_session(username, usuario_data)
                            st.session_state.session_id = session_id
                            # Guardar en URL para persistencia
                            st.query_params['sid'] = session_id
                        
                        st.success(f"✅ Bienvenido, {usuario_data['nombre_completo'] or usuario_data['username']}!")
                        st.rerun()
                    else:
                        st.error("❌ Usuario o contraseña incorrectos")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Información de ayuda
        with st.expander("ℹ️ Ayuda e Información"):
            st.markdown("""
                                
                **Niveles de usuario:**
                - **Normal**: Acceso a calculadoras y herramientas
                - **Administrador**: Acceso completo + gestión del sistema
                
                **¿Olvidaste tu contraseña?**  
                Contacta al administrador del sistema para restablecerla.
            """)
    
    # Footer
    st.markdown("""
        <div class='footer'>
            <p>
                <strong>Sistema de Cálculos y Herramientas</strong><br>
                Tribunal de Trabajo N° 2 de Quilmes<br>
                Provincia de Buenos Aires, Argentina
            </p>
        </div>
    """, unsafe_allow_html=True)

def mostrar_header():
    """Muestra el encabezado del sistema cuando está logueado"""
    col1, col2, col3 = st.columns([1, 8, 2])
    
    with col2:
        st.markdown('<h1 class="main-title">Sistema de Cálculos y Herramientas</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Tribunal de Trabajo N° 2 de Quilmes</p>', unsafe_allow_html=True)
    
    with col3:
        usuario = st.session_state.usuario
        st.markdown(f"**👤 {usuario['username']}**")
        st.caption(f"Nivel: {usuario['nivel']}")
        
        if st.button("🚪 Cerrar Sesión", use_container_width=True, type="secondary"):
            # Borrar sesión persistente si existe
            if SESSION_MANAGER_AVAILABLE and 'session_id' in st.session_state:
                session_mgr = SessionManager()
                session_mgr.delete_session(st.session_state.session_id)
            
            # Limpiar query params
            st.query_params.clear()
            
            st.session_state.clear()
            st.rerun()
    
    st.markdown("---")

def ejecutar_aplicacion(app_key):
    """Ejecuta la aplicación seleccionada"""
    app_info = APLICACIONES[app_key]
    
    # Verificar permisos
    if app_info['nivel_requerido'] == 'admin' and st.session_state.usuario['nivel'] != 'admin':
        st.error("🚫 No tienes permisos para acceder a esta aplicación. Solo administradores.")
        if st.button("⬅️ Volver al menú"):
            st.session_state.app_actual = None
            st.rerun()
        return
    
    try:
        # Botón de volver
        col1, col2, col3 = st.columns([1, 4, 1])
        with col1:
            if st.button("⬅️ Volver", key="btn_volver"):
                st.session_state.app_actual = None
                st.rerun()
        
        with col2:
            st.markdown(f"## {app_info['icono']} {app_info['nombre']}")
        
        st.markdown("---")
        
        # Ejecutar la aplicación directamente
        import importlib.util
        
        modulo_nombre = app_info['archivo']
        archivo_path = f"{modulo_nombre.replace('.', '/')}.py"
        
        try:
            # Cargar módulo desde archivo
            spec = importlib.util.spec_from_file_location(modulo_nombre, archivo_path)
            modulo = importlib.util.module_from_spec(spec)
            sys.modules[modulo_nombre] = modulo
            
            # Ejecutar el módulo
            spec.loader.exec_module(modulo)
            
        except FileNotFoundError:
            st.error(f"❌ No se encuentra el archivo: {archivo_path}")
            st.info("""
                **Posibles soluciones:**
                1. Verifica que el archivo existe en la carpeta apps/
                2. Asegúrate de haber ejecutado el script de migración
                3. Revisa que el nombre del archivo es correcto
            """)
            
            if st.button("Volver al menú principal"):
                st.session_state.app_actual = None
                st.rerun()
                
        except Exception as e:
            st.error(f"❌ Error al ejecutar la aplicación: {e}")
            st.exception(e)
            
            if st.button("Volver al menú principal", key="btn_exec_error"):
                st.session_state.app_actual = None
                st.rerun()
    
    except Exception as e:
        st.error(f"❌ Error inesperado: {e}")
        st.exception(e)
        
        if st.button("Volver al menú principal", key="btn_error_volver"):
            st.session_state.app_actual = None
            st.rerun()

def mostrar_menu_principal():
    """Muestra el menú principal con todas las aplicaciones"""
    mostrar_header()
    
    # Cargar datasets para mostrar últimos datos
    try:
        import pandas as pd
        
        df_ripte = pd.read_csv("data/dataset_ripte.csv")
        df_ripte['fecha'] = pd.to_datetime(df_ripte['año'].astype(str) + '-' + 
                                          df_ripte['mes'].str[:3].map({
                                              'Ene': '01', 'Feb': '02', 'Mar': '03', 'Abr': '04',
                                              'May': '05', 'Jun': '06', 'Jul': '07', 'Ago': '08',
                                              'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dic': '12'
                                          }) + '-01')
        
        df_ipc = pd.read_csv("data/dataset_ipc.csv")
        df_ipc['periodo'] = pd.to_datetime(df_ipc['periodo'])
        
        df_tasa = pd.read_csv("data/dataset_tasa.csv")
        df_tasa['Desde'] = pd.to_datetime(df_tasa['Desde'])
        df_tasa['Hasta'] = pd.to_datetime(df_tasa['Hasta'])
        
        # Obtener últimos datos
        ultimo_ripte_txt = ""
        ultimo_ipc_txt = ""
        ultima_tasa_txt = ""
        
        if not df_ripte.empty:
            ultimo_ripte = df_ripte.iloc[-1]
            fecha_ripte = ultimo_ripte['fecha']
            valor_ripte = ultimo_ripte['índice RIPTE']
            mes_ripte = fecha_ripte.month
            año_ripte = fecha_ripte.year
            ultimo_ripte_txt = f"RIPTE {mes_ripte}/{año_ripte}: {valor_ripte:,.0f}"
        
        if not df_ipc.empty:
            ultimo_ipc = df_ipc.iloc[-1]
            fecha_ipc = ultimo_ipc['periodo']
            variacion_ipc = ultimo_ipc['variacion_mensual']
            mes_ipc = fecha_ipc.month
            año_ipc = fecha_ipc.year
            ultimo_ipc_txt = f"IPC {mes_ipc}/{año_ipc}: {variacion_ipc:.2f}%"
        
        if not df_tasa.empty:
            ultima_tasa = df_tasa.iloc[0]
            valor_tasa = ultima_tasa['Valor']
            fecha_hasta = ultima_tasa['Hasta']
            fecha_txt = fecha_hasta.strftime("%d/%m/%Y")
            ultima_tasa_txt = f"TASA {fecha_txt}: {valor_tasa:.2f}%"
        
        # Mostrar alerta con últimos datos
        st.warning(f"**📊 Últimos Datos:** {ultimo_ripte_txt} | {ultimo_ipc_txt} | {ultima_tasa_txt}")
    
    except Exception as e:
        # Si hay error, simplemente no mostrar la alerta
        pass
    
    # Mensaje de bienvenida personalizado
    usuario = st.session_state.usuario
    
    st.markdown(f"""
        <div style='background-color: #f0f2f6; padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem;'>
            <h3 style='color: #1f4788; margin-top: 0;'>👋 Bienvenido/a, {usuario['nombre_completo'] or usuario['username']}</h3>
            <p style='margin-bottom: 0; color: #555;'>
                Selecciona una de las herramientas disponibles para comenzar a trabajar.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Mostrar aplicaciones disponibles según nivel de usuario
    nivel_usuario = usuario['nivel']
    
    # Filtrar aplicaciones según permisos
    apps_disponibles = {
        k: v for k, v in APLICACIONES.items()
        if v['nivel_requerido'] == 'normal' or nivel_usuario == 'admin'
    }
    
    st.markdown("### 🛠️ Aplicaciones Disponibles")
    
    # Mostrar aplicaciones en grid de 2 columnas
    apps_list = list(apps_disponibles.items())
    
    for i in range(0, len(apps_list), 2):
        cols = st.columns(2)
        
        for j, col in enumerate(cols):
            if i + j < len(apps_list):
                app_key, app_info = apps_list[i + j]
                with col:
                    with st.container():
                        # Marcar apps de admin
                        admin_badge = " 🔒 ADMIN" if app_info['nivel_requerido'] == 'admin' else ""
                        
                        st.markdown(f"""
                            <div class='app-card'>
                                <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>{app_info['icono']}</div>
                                <h3>{app_info['nombre']}{admin_badge}</h3>
                                <p>{app_info['descripcion']}</p>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"Abrir aplicación", key=f"btn_{app_key}", use_container_width=True):
                            st.session_state.app_actual = app_key
                            st.rerun()
    
    # Footer
    st.markdown("""
        <div class='footer'>
            <p>
                <strong>Sistema de Cálculos y Herramientas - Tribunal de Trabajo N° 2 de Quilmes</strong><br>
                Desarrollado para optimizar las tareas judiciales y administrativas<br>
                © 2024 - Todos los derechos reservados
            </p>
        </div>
    """, unsafe_allow_html=True)

def main():
    """Función principal del sistema"""
    # Cargar estilos CSS
    load_custom_css()
    
    # Inicializar estado de sesión
    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False
    
    if 'app_actual' not in st.session_state:
        st.session_state.app_actual = None
    
    # Intentar restaurar sesión persistente (solo si está disponible)
    if not st.session_state.autenticado and SESSION_MANAGER_AVAILABLE:
        session_mgr = SessionManager()
        
        # Buscar session_id en query params o en session_state
        session_id = None
        if 'sid' in st.query_params:
            session_id = st.query_params['sid']
        elif 'session_id' in st.session_state:
            session_id = st.session_state.session_id
        
        if session_id:
            user_data = session_mgr.get_session(session_id)
            
            if user_data:
                # Sesión válida encontrada - restaurar
                st.session_state.autenticado = True
                st.session_state.usuario = user_data
                st.session_state.session_id = session_id
                # Mantener session_id en URL
                st.query_params['sid'] = session_id
    
    # Verificar autenticación
    if not st.session_state.autenticado:
        mostrar_login()
    else:
        # Usuario autenticado - mostrar sistema
        if st.session_state.app_actual:
            ejecutar_aplicacion(st.session_state.app_actual)
        else:
            mostrar_menu_principal()

if __name__ == "__main__":
    main()
