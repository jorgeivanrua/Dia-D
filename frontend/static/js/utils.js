/**
 * Utilidades generales
 */
class Utils {
    static showAlert(message, type = 'info', duration = 5000, containerId = 'alert-container') {
        const container = document.getElementById(containerId);
        if (!container) return;
        
        const alertId = 'alert-' + Date.now();
        const alertHtml = `
            <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        container.innerHTML = alertHtml;
        
        if (duration > 0) {
            setTimeout(() => {
                const alertElement = document.getElementById(alertId);
                if (alertElement) {
                    const bsAlert = new bootstrap.Alert(alertElement);
                    bsAlert.close();
                }
            }, duration);
        }
    }
    
    static showSuccess(message, duration = 3000, containerId = 'alert-container') {
        this.showAlert(message, 'success', duration, containerId);
    }
    
    static showError(message, duration = 8000, containerId = 'alert-container') {
        this.showAlert(message, 'danger', duration, containerId);
    }
    
    static toggleSpinner(buttonId, textId, spinnerId, isLoading = true) {
        const button = document.getElementById(buttonId);
        const text = document.getElementById(textId);
        const spinner = document.getElementById(spinnerId);
        
        if (!button || !text || !spinner) return;
        
        if (isLoading) {
            button.disabled = true;
            text.classList.add('d-none');
            spinner.classList.remove('d-none');
        } else {
            button.disabled = false;
            text.classList.remove('d-none');
            spinner.classList.add('d-none');
        }
    }
    
    static populateSelect(selectId, options, valueKey = 'id', textKey = 'nombre', placeholder = 'Seleccione...') {
        const select = document.getElementById(selectId);
        if (!select) return;
        
        select.innerHTML = `<option value="">${placeholder}</option>`;
        
        options.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option[valueKey];
            optionElement.textContent = option[textKey];
            select.appendChild(optionElement);
        });
    }
    
    static enableSelect(selectId, enable = true) {
        const select = document.getElementById(selectId);
        if (!select) return;
        
        if (enable) {
            select.disabled = false;
            select.classList.remove('disabled');
        } else {
            select.disabled = true;
            select.classList.add('disabled');
            select.innerHTML = '<option value="">Seleccione opción anterior primero</option>';
        }
    }
    
    static getFormData(formId) {
        const form = document.getElementById(formId);
        if (!form) return {};
        
        const formData = new FormData(form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        return data;
    }
    
    static validateRequired(formId, requiredFields) {
        const errors = [];
        
        requiredFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (!field || !field.value.trim()) {
                errors.push(`El campo ${fieldId} es requerido`);
            }
        });
        
        return errors;
    }
    
    static setLoading(elementId, isLoading = true) {
        const element = document.getElementById(elementId);
        if (!element) return;
        
        if (isLoading) {
            element.disabled = true;
            element.classList.add('disabled');
        } else {
            element.disabled = false;
            element.classList.remove('disabled');
        }
    }
    
    static formatNumber(number) {
        if (number === null || number === undefined) return '0';
        return new Intl.NumberFormat('es-CO').format(number);
    }
    
    static formatDate(dateString) {
        if (!dateString) return 'N/A';
        
        const date = new Date(dateString);
        return date.toLocaleDateString('es-CO', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
    
    static showWarning(message, duration = 5000, containerId = 'alert-container') {
        this.showAlert(message, 'warning', duration, containerId);
    }
    
    static showInfo(message, duration = 5000, containerId = 'alert-container') {
        this.showAlert(message, 'info', duration, containerId);
    }
    
    /**
     * Formatear fecha y hora
     */
    static formatDateTime(dateString) {
        if (!dateString) return 'N/A';
        
        try {
            const date = new Date(dateString);
            
            // Verificar si la fecha es válida
            if (isNaN(date.getTime())) {
                return 'Fecha inválida';
            }
            
            // Formato: DD/MM/YYYY HH:MM
            const day = String(date.getDate()).padStart(2, '0');
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const year = date.getFullYear();
            const hours = String(date.getHours()).padStart(2, '0');
            const minutes = String(date.getMinutes()).padStart(2, '0');
            
            return `${day}/${month}/${year} ${hours}:${minutes}`;
        } catch (error) {
            console.error('Error formateando fecha:', error);
            return 'Error';
        }
    }
}

window.Utils = Utils;
