#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
APP DE ADMINISTRACIÓN
Sistema de Cálculos y Herramientas - Tribunal de Trabajo 2 de Quilmes
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Agregar path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.auth import AuthSystem

# Inicializar sistema de autenticación
auth = AuthSystem()

st.markdown("# ⚙️ ADMINISTRACIÓN DEL SISTEMA")
st.markdown("---")

# Verificar que el usuario sea admin
if 'usuario' not in st.session_state or st.session_state.usuario['nivel'] != 'admin':
    st.error("🚫 Acceso denegado. Solo administradores pueden acceder a esta sección.")
    st.stop()

# Tabs para las diferentes funciones
tab1, tab2 = st.tabs(["👥 Gestión de Usuarios", "📊 Edición de Datasets"])

# TAB 1: GESTIÓN DE USUARIOS
with tab1:
    st.markdown("## 👥 Gestión de Usuarios")
    
    subtab1, subtab2, subtab3 = st.tabs(["Crear Usuario", "Ver Usuarios", "Modificar"])
    
    with subtab1:
        st.markdown("### ➕ Crear Nuevo Usuario")
        
        with st.form("form_crear_usuario"):
            col1, col2 = st.columns(2)
            
            with col1:
                nuevo_username = st.text_input("Nombre de usuario*", max_chars=50)
                nuevo_nombre = st.text_input("Nombre completo", max_chars=100)
            
            with col2:
                nuevo_password = st.text_input("Contraseña*", type="password", max_chars=50)
                nuevo_email = st.text_input("Email", max_chars=100)
            
            nuevo_nivel = st.selectbox("Nivel de acceso*", ["normal", "admin"])
            
            submitted = st.form_submit_button("Crear Usuario", use_container_width=True, type="primary")
            
            if submitted:
                if not nuevo_username or not nuevo_password:
                    st.error("Usuario y contraseña son obligatorios")
                else:
                    exito, mensaje = auth.crear_usuario(
                        username=nuevo_username,
                        password=nuevo_password,
                        nivel=nuevo_nivel,
                        nombre_completo=nuevo_nombre,
                        email=nuevo_email
                    )
                    
                    if exito:
                        st.success(mensaje)
                    else:
                        st.error(mensaje)
    
    with subtab2:
        st.markdown("### 📋 Usuarios del Sistema")
        
        usuarios = auth.obtener_usuarios()
        
        if usuarios:
            df_usuarios = pd.DataFrame(usuarios)
            df_display = df_usuarios[['username', 'nivel', 'nombre_completo', 'email', 'ultimo_acceso', 'activo']].copy()
            df_display.columns = ['Usuario', 'Nivel', 'Nombre', 'Email', 'Último Acceso', 'Activo']
            df_display['Activo'] = df_display['Activo'].map({True: '✅', False: '❌'})
            
            st.dataframe(df_display, use_container_width=True, hide_index=True)
            st.caption(f"Total de usuarios: {len(usuarios)}")
        else:
            st.info("No hay usuarios en el sistema")
    
    with subtab3:
        st.markdown("### ✏️ Modificar Usuario")
        
        usuarios = auth.obtener_usuarios()
        usernames = [u['username'] for u in usuarios]
        
        usuario_sel = st.selectbox("Seleccionar usuario", usernames)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔑 Cambiar Contraseña")
            with st.form("form_cambiar_pass"):
                nueva_pass = st.text_input("Nueva contraseña", type="password")
                confirmar_pass = st.text_input("Confirmar contraseña", type="password")
                
                if st.form_submit_button("Cambiar Contraseña"):
                    if nueva_pass != confirmar_pass:
                        st.error("Las contraseñas no coinciden")
                    elif nueva_pass:
                        exito, mensaje = auth.cambiar_password(usuario_sel, nueva_pass)
                        if exito:
                            st.success(mensaje)
                        else:
                            st.error(mensaje)
        
        with col2:
            st.markdown("#### 🗑️ Eliminar Usuario")
            st.warning(f"¿Eliminar usuario **{usuario_sel}**?")
            
            if st.button("🗑️ Eliminar", type="secondary", use_container_width=True):
                exito, mensaje = auth.eliminar_usuario(usuario_sel)
                if exito:
                    st.success(mensaje)
                    st.rerun()
                else:
                    st.error(mensaje)

# TAB 2: EDICIÓN DE DATASETS
with tab2:
    st.markdown("## 📊 Edición de Datasets")
    
    datasets = {
        "JUS": "data/Dataset_JUS.csv",
        "IPC": "data/dataset_ipc.csv",
        "RIPTE": "data/dataset_ripte.csv",
        "Pisos Salariales": "data/dataset_pisos.csv",
        "Tasa Activa": "data/dataset_tasa.csv"
    }
    
    dataset_sel = st.selectbox("Seleccionar dataset", list(datasets.keys()))
    archivo = datasets[dataset_sel]
    
    try:
        df = pd.read_csv(archivo, encoding='utf-8')
        
        st.markdown(f"### 📄 Dataset: {dataset_sel}")
        st.caption(f"Archivo: `{archivo}` | Filas: {len(df)} | Columnas: {len(df.columns)}")
        
        tab_ver, tab_agregar, tab_editar = st.tabs(["Ver Datos", "Agregar Fila", "Editar/Eliminar"])
        
        with tab_ver:
            st.dataframe(df, use_container_width=True)
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar CSV",
                data=csv,
                file_name=f"{dataset_sel}_export.csv",
                mime="text/csv"
            )
        
        with tab_agregar:
            st.markdown("#### ➕ Agregar Nueva Fila")
            
            # Mensaje especial para Tasa Activa
            if dataset_sel == "Tasa Activa":
                st.info("ℹ️ **Tasa Activa**: Las nuevas filas se agregan al **inicio** (arriba) de la tabla, ya que este dataset está ordenado de más reciente a más antiguo.")
            
            with st.form("form_agregar_fila"):
                st.write("Complete los valores para cada columna:")
                
                nuevos_valores = {}
                cols = st.columns(min(3, len(df.columns)))
                
                for idx, columna in enumerate(df.columns):
                    with cols[idx % 3]:
                        nuevos_valores[columna] = st.text_input(f"{columna}")
                
                if st.form_submit_button("Agregar Fila", type="primary"):
                    try:
                        nueva_fila = pd.DataFrame([nuevos_valores])
                        
                        # Para Tasa Activa, agregar al inicio (arriba)
                        if dataset_sel == "Tasa Activa":
                            df_actualizado = pd.concat([nueva_fila, df], ignore_index=True)
                        else:
                            # Para otros datasets, agregar al final (abajo)
                            df_actualizado = pd.concat([df, nueva_fila], ignore_index=True)
                        
                        df_actualizado.to_csv(archivo, index=False, encoding='utf-8')
                        
                        st.success(f"✅ Fila agregada exitosamente a {dataset_sel}")
                        st.rerun()
                    
                    except Exception as e:
                        st.error(f"Error al agregar fila: {str(e)}")
        
        with tab_editar:
            st.markdown("#### ✏️ Editar Datos")
            
            df_editado = st.data_editor(
                df,
                use_container_width=True,
                num_rows="dynamic"
            )
            
            col1, col2 = st.columns([1, 4])
            
            with col1:
                if st.button("💾 Guardar Cambios", type="primary", use_container_width=True):
                    try:
                        df_editado.to_csv(archivo, index=False, encoding='utf-8')
                        st.success("✅ Cambios guardados exitosamente")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al guardar: {str(e)}")
            
            with col2:
                st.caption("⚠️ Los cambios se aplicarán inmediatamente")
    
    except Exception as e:
        st.error(f"Error al cargar dataset: {str(e)}")

st.markdown("---")
st.caption("**Administración del Sistema** | Tribunal de Trabajo N° 2 de Quilmes")