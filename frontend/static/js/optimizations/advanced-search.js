/**
 * Advanced Search Manager - Búsqueda avanzada con filtros
 * Optimización #4: Implementar búsqueda avanzada con filtros
 */

class AdvancedSearchManager {
    constructor(data, options = {}) {
        this.data = data;
        this.filters = {};
        this.searchTerm = '';
        this.searchFields = options.searchFields || [];
        this.sortField = options.sortField || null;
        this.sortOrder = options.sortOrder || 'asc'; // 'asc' o 'desc'
    }

    /**
     * Establecer datos
     */
    setData(data) {
        this.data = data;
    }

    /**
     * Establecer término de búsqueda
     */
    setSearchTerm(term) {
        this.searchTerm = term.toLowerCase().trim();
    }

    /**
     * Agregar filtro
     */
    addFilter(field, value) {
        if (value === '' || value === null || value === undefined) {
            delete this.filters[field];
        } else {
            this.filters[field] = value;
        }
    }

    /**
     * Remover filtro
     */
    removeFilter(field) {
        delete this.filters[field];
    }

    /**
     * Limpiar todos los filtros
     */
    clearFilters() {
        this.filters = {};
        this.searchTerm = '';
    }

    /**
     * Establecer ordenamiento
     */
    setSort(field, order = 'asc') {
        this.sortField = field;
        this.sortOrder = order;
    }

    /**
     * Buscar en un objeto
     */
    searchInObject(obj, term) {
        if (!term) return true;

        // Si hay campos específicos, buscar solo en ellos
        if (this.searchFields.length > 0) {
            return this.searchFields.some(field => {
                const value = this.getNestedValue(obj, field);
                return value && String(value).toLowerCase().includes(term);
            });
        }

        // Buscar en todos los campos
        return Object.values(obj).some(value => {
            if (value === null || value === undefined) return false;
            return String(value).toLowerCase().includes(term);
        });
    }

    /**
     * Aplicar filtros a un objeto
     */
    applyFilters(obj) {
        return Object.entries(this.filters).every(([field, filterValue]) => {
            const objValue = this.getNestedValue(obj, field);
            
            // Filtro de rango (para números)
            if (typeof filterValue === 'object' && filterValue.min !== undefined && filterValue.max !== undefined) {
                return objValue >= filterValue.min && objValue <= filterValue.max;
            }
            
            // Filtro de array (contiene)
            if (Array.isArray(filterValue)) {
                return filterValue.includes(objValue);
            }
            
            // Filtro exacto
            return objValue === filterValue;
        });
    }

    /**
     * Obtener valor anidado de un objeto
     */
    getNestedValue(obj, path) {
        return path.split('.').reduce((current, prop) => current?.[prop], obj);
    }

    /**
     * Ordenar datos
     */
    sortData(data) {
        if (!this.sortField) return data;

        return [...data].sort((a, b) => {
            const aVal = this.getNestedValue(a, this.sortField);
            const bVal = this.getNestedValue(b, this.sortField);

            if (aVal === bVal) return 0;

            let comparison = 0;
            if (typeof aVal === 'string' && typeof bVal === 'string') {
                comparison = aVal.localeCompare(bVal);
            } else {
                comparison = aVal < bVal ? -1 : 1;
            }

            return this.sortOrder === 'asc' ? comparison : -comparison;
        });
    }

    /**
     * Ejecutar búsqueda y filtrado
     */
    search() {
        let results = this.data;

        // Aplicar búsqueda por término
        if (this.searchTerm) {
            results = results.filter(item => this.searchInObject(item, this.searchTerm));
        }

        // Aplicar filtros
        results = results.filter(item => this.applyFilters(item));

        // Aplicar ordenamiento
        results = this.sortData(results);

        return results;
    }

    /**
     * Obtener estadísticas de búsqueda
     */
    getStats() {
        const results = this.search();
        return {
            total: this.data.length,
            filtered: results.length,
            percentage: ((results.length / this.data.length) * 100).toFixed(1)
        };
    }
}

/**
 * Helper para crear búsqueda avanzada en tablas
 */
class TableSearchHelper {
    constructor(tableId, searchManager) {
        this.tableId = tableId;
        this.searchManager = searchManager;
        this.createSearchUI();
    }

    /**
     * Crear interfaz de búsqueda
     */
    createSearchUI() {
        const container = document.getElementById(`${this.tableId}_search_container`);
        if (!container) return;

        container.innerHTML = `
            <div class="row mb-3">
                <div class="col-md-6">
                    <div class="input-group">
                        <span class="input-group-text"><i class="bi bi-search"></i></span>
                        <input type="text" class="form-control" id="${this.tableId}_search_input" 
                               placeholder="Buscar...">
                        <button class="btn btn-outline-secondary" type="button" 
                                onclick="document.getElementById('${this.tableId}_search_input').value = ''; 
                                         window.tableSearchHelpers['${this.tableId}'].performSearch()">
                            <i class="bi bi-x"></i>
                        </button>
                    </div>
                </div>
                <div class="col-md-6 text-end">
                    <button class="btn btn-outline-primary" type="button" 
                            onclick="window.tableSearchHelpers['${this.tableId}'].toggleAdvancedFilters()">
                        <i class="bi bi-funnel"></i> Filtros Avanzados
                    </button>
                </div>
            </div>
            <div id="${this.tableId}_advanced_filters" class="card mb-3" style="display: none;">
                <div class="card-body">
                    <h6 class="card-title">Filtros Avanzados</h6>
                    <div id="${this.tableId}_filters_content"></div>
                </div>
            </div>
            <div id="${this.tableId}_search_stats" class="text-muted small mb-2"></div>
        `;

        // Event listener para búsqueda en tiempo real
        document.getElementById(`${this.tableId}_search_input`).addEventListener('input', (e) => {
            this.performSearch();
        });
    }

    /**
     * Realizar búsqueda
     */
    performSearch() {
        const searchInput = document.getElementById(`${this.tableId}_search_input`);
        this.searchManager.setSearchTerm(searchInput.value);
        
        const results = this.searchManager.search();
        this.updateStats();
        
        // Disparar evento personalizado con resultados
        const event = new CustomEvent('searchComplete', { detail: { results } });
        document.dispatchEvent(event);
    }

    /**
     * Actualizar estadísticas
     */
    updateStats() {
        const stats = this.searchManager.getStats();
        const statsContainer = document.getElementById(`${this.tableId}_search_stats`);
        
        if (statsContainer) {
            statsContainer.innerHTML = `
                Mostrando ${stats.filtered} de ${stats.total} registros (${stats.percentage}%)
            `;
        }
    }

    /**
     * Toggle filtros avanzados
     */
    toggleAdvancedFilters() {
        const filtersDiv = document.getElementById(`${this.tableId}_advanced_filters`);
        if (filtersDiv) {
            filtersDiv.style.display = filtersDiv.style.display === 'none' ? 'block' : 'none';
        }
    }
}

// Registro global
window.tableSearchHelpers = window.tableSearchHelpers || {};
