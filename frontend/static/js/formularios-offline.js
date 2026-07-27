/**
 * FormulariosOffline - Gestión offline de formularios E-14 y E-24
 */

class FormulariosOfflineManager {
    constructor() {
        this.init();
    }

    /**
     * Inicializar gestor
     */
    async init() {
        console.log('Inicializando FormulariosOfflineManager...');
        
        // Migrar datos de localStorage a IndexedDB si existen
        await this.migrarDatosLocales();
        
        // Configurar sincronización automática
        this.setupAutoSync();
    }

    /**
     * Migrar datos de localStorage a IndexedDB
     */
    async migrarDatosLocales() {
        try {
            // Verificar que syncManager esté disponible
            if (!window.syncManager) {
                console.warn('SyncManager no disponible, saltando migración');
                return;
            }

            // Migrar borradores E-14
            const borradoresE14 = localStorage.getItem('formularios_e14_borradores');
            if (borradoresE14) {
                const borradores = JSON.parse(borradoresE14);
                for (const key in borradores) {
                    const borrador = borradores[key];
                    borrador.tipo = 'formulario_e14';
                    await window.syncManager.guardarReporteOffline(borrador);
                }
                localStorage.removeItem('formularios_e14_borradores');
                console.log('Borradores E-14 migrados a IndexedDB');
            }

            // Migrar incidentes locales
            const incidentesLocales = localStorage.getItem('incidentes_locales');
            if (incidentesLocales) {
                const incidentes = JSON.parse(incidentesLocales);
                for (const incidente of incidentes) {
                    incidente.tipo = 'incidente';
                    await window.syncManager.guardarReporteOffline(incidente);
                }
                localStorage.removeItem('incidentes_locales');
                console.log('Incidentes migrados a IndexedDB');
            }

            // Migrar delitos locales
            const delitosLocales = localStorage.getItem('delitos_locales');
            if (delitosLocales) {
                const delitos = JSON.parse(delitosLocales);
                for (const delito of delitos) {
                    delito.tipo = 'delito';
                    await window.syncManager.guardarReporteOffline(delito);
                }
                localStorage.removeItem('delitos_locales');
                console.log('Delitos migrados a IndexedDB');
            }

        } catch (error) {
            console.error('Error migrando datos locales:', error);
        }
    }

    /**
     * Guardar formulario E-14 offline
     */
    async guardarFormularioE14Offline(data, fotos = []) {
        try {
            // Agregar tipo y metadatos importantes
            data.tipo = 'formulario_e14';
            
            // Agregar identificadores únicos para evitar confusión
            data.identificador_unico = `E14_M${data.mesa_id}_T${data.tipo_eleccion_id}_${Date.now()}`;
            
            // Guardar información del tipo de elección para referencia
            if (data.tipo_eleccion_nombre) {
                data.tipo_eleccion_display = data.tipo_eleccion_nombre;
            }
            
            // Guardar información de la mesa para referencia
            if (data.mesa_codigo) {
                data.mesa_display = data.mesa_codigo;
            }
            
            // Guardar en IndexedDB
            const tempId = await window.syncManager.guardarReporteOffline(data);
            
            // Guardar fotos si hay (pueden ser múltiples páginas del acta)
            if (fotos && fotos.length > 0) {
                for (let i = 0; i < fotos.length; i++) {
                    const foto = fotos[i];
                    const base64 = await this.convertirFotoABase64(foto);
                    
                    const evidencia = {
                        file_data: base64,
                        filename: foto.name,
                        mime_type: foto.type,
                        tipo_reporte: 'formulario_e14',
                        // Metadatos importantes para identificación
                        mesa_id: data.mesa_id,
                        tipo_eleccion_id: data.tipo_eleccion_id,
                        mesa_codigo: data.mesa_codigo,
                        tipo_eleccion_nombre: data.tipo_eleccion_nombre,
                        numero_pagina: i + 1,
                        total_paginas: fotos.length,
                        fecha_captura: new Date().toISOString(),
                        descripcion: `Acta E-14 - Mesa ${data.mesa_codigo} - ${data.tipo_eleccion_nombre} - Página ${i + 1}/${fotos.length}`
                    };
                    
                    await window.syncManager.guardarEvidenciaOffline(evidencia, tempId);
                }
                
                console.log(`✅ Guardadas ${fotos.length} fotos del E-14 (Mesa: ${data.mesa_codigo}, Elección: ${data.tipo_eleccion_nombre})`);
            }
            
            return tempId;
        } catch (error) {
            console.error('Error guardando formulario E-14 offline:', error);
            throw error;
        }
    }

    /**
     * Guardar formulario E-24 offline
     */
    async guardarFormularioE24Offline(data, fotos = []) {
        try {
            // Agregar tipo
            data.tipo = 'formulario_e24';
            
            // Guardar en IndexedDB
            const tempId = await window.syncManager.guardarReporteOffline(data);
            
            // Guardar fotos si hay
            if (fotos && fotos.length > 0) {
                for (const foto of fotos) {
                    const base64 = await this.convertirFotoABase64(foto);
                    
                    const evidencia = {
                        file_data: base64,
                        filename: foto.name,
                        mime_type: foto.type,
                        tipo_reporte: 'formulario_e24',
                        fecha_captura: new Date().toISOString()
                    };
                    
                    await window.syncManager.guardarEvidenciaOffline(evidencia, tempId);
                }
            }
            
            return tempId;
        } catch (error) {
            console.error('Error guardando formulario E-24 offline:', error);
            throw error;
        }
    }

    /**
     * Convertir foto a base64
     */
    convertirFotoABase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = reject;
            reader.readAsDataURL(file);
        });
    }

    /**
     * Configurar sincronización automática
     */
    setupAutoSync() {
        // Sincronizar cuando se recupera la conexión
        window.addEventListener('online', () => {
            console.log('Conexión restaurada, sincronizando formularios...');
            this.sincronizarFormularios();
        });
    }

    /**
     * Sincronizar formularios pendientes
     */
    async sincronizarFormularios() {
        try {
            if (!navigator.onLine) {
                console.log('Sin conexión, no se puede sincronizar');
                return;
            }

            if (!window.syncManager) {
                console.error('SyncManager no disponible');
                return;
            }

            // Usar el SyncManager para sincronizar
            await window.syncManager.syncPendingData();
            
        } catch (error) {
            console.error('Error sincronizando formularios:', error);
        }
    }

    /**
     * Obtener estadísticas de formularios pendientes
     */
    async obtenerEstadisticas() {
        try {
            if (!window.indexedDBService || !window.indexedDBService.db) {
                return {
                    formularios_e14: 0,
                    formularios_e24: 0,
                    incidentes: 0,
                    delitos: 0,
                    total: 0
                };
            }

            const reportesPendientes = await window.indexedDBService.obtenerReportesPendientes();
            
            const stats = {
                formularios_e14: 0,
                formularios_e24: 0,
                incidentes: 0,
                delitos: 0,
                total: reportesPendientes.length
            };

            reportesPendientes.forEach(reporte => {
                if (reporte.tipo === 'formulario_e14') {
                    stats.formularios_e14++;
                } else if (reporte.tipo === 'formulario_e24') {
                    stats.formularios_e24++;
                } else if (reporte.tipo === 'incidente') {
                    stats.incidentes++;
                } else if (reporte.tipo === 'delito') {
                    stats.delitos++;
                }
            });

            return stats;
        } catch (error) {
            console.error('Error obteniendo estadísticas:', error);
            return {
                formularios_e14: 0,
                formularios_e24: 0,
                incidentes: 0,
                delitos: 0,
                total: 0
            };
        }
    }
}

// ============================================
// FUNCIONES AUXILIARES PARA FORMULARIOS E-14
// ============================================

/**
 * Guardar formulario E-14 con detección de conexión
 */
async function guardarFormularioE14(data, fotos = []) {
    try {
        // Verificar si hay conexión
        if (!navigator.onLine) {
            // Guardar offline directamente
            await guardarFormularioE14Offline(data, fotos);
            return;
        }

        // Intentar guardar en el servidor
        const response = await APIClient.createFormularioE14(data);
        
        if (response.success && response.data) {
            const formularioId = response.data.id;
            
            // Subir fotos si hay
            if (fotos.length > 0) {
                Utils.showInfo('Subiendo fotos del acta...');
                
                try {
                    await subirFotosFormulario(fotos, 'formulario_e14', formularioId);
                } catch (uploadError) {
                    console.error('Error subiendo fotos:', uploadError);
                    Utils.showWarning('Formulario creado pero hubo errores al subir algunas fotos');
                }
            }
            
            Utils.showSuccess('✓ Formulario E-14 enviado exitosamente');
            return response;
        }
    } catch (error) {
        console.error('Error guardando formulario E-14:', error);
        
        // Si falla, intentar guardar offline
        if (window.formulariosOfflineManager) {
            try {
                await guardarFormularioE14Offline(data, fotos);
            } catch (offlineError) {
                console.error('Error guardando offline:', offlineError);
                Utils.showError('Error al guardar formulario: ' + error.message);
                throw error;
            }
        } else {
            Utils.showError('Error al guardar formulario: ' + error.message);
            throw error;
        }
    }
}

/**
 * Guardar formulario E-14 offline
 */
async function guardarFormularioE14Offline(data, fotos) {
    try {
        if (!window.formulariosOfflineManager) {
            throw new Error('FormulariosOfflineManager no disponible');
        }

        await window.formulariosOfflineManager.guardarFormularioE14Offline(data, fotos);
        
        Utils.showWarning('⚠️ Sin conexión. Formulario E-14 guardado localmente y se sincronizará automáticamente.');
        
    } catch (error) {
        console.error('Error guardando formulario E-14 offline:', error);
        throw error;
    }
}

/**
 * Guardar formulario E-24 con detección de conexión
 */
async function guardarFormularioE24(data, fotos = []) {
    try {
        // Verificar si hay conexión
        if (!navigator.onLine) {
            // Guardar offline directamente
            await guardarFormularioE24Offline(data, fotos);
            return;
        }

        // Intentar guardar en el servidor
        const response = await APIClient.createFormularioE24(data);
        
        if (response.success && response.data) {
            const formularioId = response.data.id;
            
            // Subir fotos si hay
            if (fotos.length > 0) {
                Utils.showInfo('Subiendo fotos del acta...');
                
                try {
                    await subirFotosFormulario(fotos, 'formulario_e24', formularioId);
                } catch (uploadError) {
                    console.error('Error subiendo fotos:', uploadError);
                    Utils.showWarning('Formulario creado pero hubo errores al subir algunas fotos');
                }
            }
            
            Utils.showSuccess('✓ Formulario E-24 enviado exitosamente');
            return response;
        }
    } catch (error) {
        console.error('Error guardando formulario E-24:', error);
        
        // Si falla, intentar guardar offline
        if (window.formulariosOfflineManager) {
            try {
                await guardarFormularioE24Offline(data, fotos);
            } catch (offlineError) {
                console.error('Error guardando offline:', offlineError);
                Utils.showError('Error al guardar formulario: ' + error.message);
                throw error;
            }
        } else {
            Utils.showError('Error al guardar formulario: ' + error.message);
            throw error;
        }
    }
}

/**
 * Guardar formulario E-24 offline
 */
async function guardarFormularioE24Offline(data, fotos) {
    try {
        if (!window.formulariosOfflineManager) {
            throw new Error('FormulariosOfflineManager no disponible');
        }

        await window.formulariosOfflineManager.guardarFormularioE24Offline(data, fotos);
        
        Utils.showWarning('⚠️ Sin conexión. Formulario E-24 guardado localmente y se sincronizará automáticamente.');
        
    } catch (error) {
        console.error('Error guardando formulario E-24 offline:', error);
        throw error;
    }
}

/**
 * Subir fotos de formulario
 */
async function subirFotosFormulario(fotos, tipoFormulario, formularioId) {
    if (!window.uploadManager) {
        throw new Error('UploadManager no disponible');
    }

    return await window.uploadManager.uploadWithProgressModal(
        fotos,
        tipoFormulario,
        formularioId
    );
}

// Crear instancia global
window.formulariosOfflineManager = null;

// Inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        // Esperar a que IndexedDB esté listo
        setTimeout(() => {
            window.formulariosOfflineManager = new FormulariosOfflineManager();
        }, 1500);
    });
} else {
    setTimeout(() => {
        window.formulariosOfflineManager = new FormulariosOfflineManager();
    }, 1500);
}

// Exponer funciones globalmente
window.guardarFormularioE14 = guardarFormularioE14;
window.guardarFormularioE14Offline = guardarFormularioE14Offline;
window.guardarFormularioE24 = guardarFormularioE24;
window.guardarFormularioE24Offline = guardarFormularioE24Offline;
window.subirFotosFormulario = subirFotosFormulario;

console.log('✅ FormulariosOfflineManager cargado');
