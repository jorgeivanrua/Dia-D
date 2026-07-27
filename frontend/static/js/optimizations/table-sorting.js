/**
 * Table Sorting Manager - Ordenamiento en tablas
 * Optimización #5: Agregar ordenamiento en tablas
 */

class TableSortingManager {
    constructor(tableId, options = {}) {
        this.tableId = tableId;
        this.table = document.getElementById(tableId);
        this.currentSort = {
            column: null,
            order: 'asc'
        };
        this.options = {
            sortableClass: options.sortableClass || 'sortable',
            sortAscClass: options.sortAscClass || 'sort-asc',
            sortDescClass: options.sortDescClass || 'sort-desc',
            ...options
        };
        
        this.init();
    }

    /**
     * Inicializar ordenamiento
     */
    init() {
        if (!this.table) {
            console.error(`Tabla ${this.tableId} no encontrada`);
            return;
        }

        const headers = this.table.querySelectorAll('thead th');
        headers.forEach((header, index) => {
            if (header.classList.contains(this.options.sortableClass)) {
                header.style.cursor = 'pointer';
                header.innerHTML += ' <i class="bi bi-arrow-down-up sort-icon"></i>';
                
                header.addEventListener('click', () => {
                    this.sortByColumn(index, header);
                });
            }
        });
    }

    /**
     * Ordenar por columna
     */
    sortByColumn(columnIndex, header) {
        const tbody = this.table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));

        // Determinar orden
        let order = 'asc';
        if (this.currentSort.column === columnIndex) {
            order = this.currentSort.order === 'asc' ? 'desc' : 'asc';
        }

        // Ordenar filas
        rows.sort((a, b) => {
            const aCell = a.cells[columnIndex];
            const bCell = b.cells[columnIndex];

            let aValue = this.getCellValue(aCell);
            let bValue = this.getCellValue(bCell);

            // Detectar tipo de dato
            const isNumeric = !isNaN(aValue) && !isNaN(bValue);
            const isDate = this.isDate(aValue) && this.isDate(bValue);

            if (isNumeric) {
                aValue = parseFloat(aValue);
                bValue = parseFloat(bValue);
            } else if (isDate) {
                aValue = new Date(aValue);
                bValue = new Date(bValue);
            } else {
                aValue = String(aValue).toLowerCase();
                bValue = String(bValue).toLowerCase();
            }

            let comparison = 0;
            if (aValue < bValue) comparison = -1;
            if (aValue > bValue) comparison = 1;

            return order === 'asc' ? comparison : -comparison;
        });

        // Limpiar tbody y agregar filas ordenadas
        tbody.innerHTML = '';
        rows.forEach(row => tbody.appendChild(row));

        // Actualizar UI
        this.updateSortIndicators(columnIndex, order, header);

        // Guardar estado
        this.currentSort = { column: columnIndex, order };

        // Disparar evento
        const event = new CustomEvent('tableSorted', {
            detail: { column: columnIndex, order }
        });
        this.table.dispatchEvent(event);
    }

    /**
     * Obtener valor de celda
     */
    getCellValue(cell) {
        // Buscar data-sort attribute primero
        if (cell.hasAttribute('data-sort')) {
            return cell.getAttribute('data-sort');
        }

        // Buscar en badges o spans
        const badge = cell.querySelector('.badge');
        if (badge) {
            return badge.textContent.trim();
        }

        return cell.textContent.trim();
    }

    /**
     * Verificar si es fecha
     */
    isDate(value) {
        const date = new Date(value);
        return date instanceof Date && !isNaN(date);
    }

    /**
     * Actualizar indicadores de ordenamiento
     */
    updateSortIndicators(columnIndex, order, activeHeader) {
        // Limpiar todos los indicadores
        const headers = this.table.querySelectorAll('thead th');
        headers.forEach(header => {
            const icon = header.querySelector('.sort-icon');
            if (icon) {
                icon.className = 'bi bi-arrow-down-up sort-icon';
            }
        });

        // Actualizar indicador activo
        const icon = activeHeader.querySelector('.sort-icon');
        if (icon) {
            icon.className = order === 'asc' 
                ? 'bi bi-sort-up sort-icon text-primary'
                : 'bi bi-sort-down sort-icon text-primary';
        }
    }

    /**
     * Resetear ordenamiento
     */
    reset() {
        this.currentSort = { column: null, order: 'asc' };
        const headers = this.table.querySelectorAll('thead th');
        headers.forEach(header => {
            const icon = header.querySelector('.sort-icon');
            if (icon) {
                icon.className = 'bi bi-arrow-down-up sort-icon';
            }
        });
    }
}

// Registro global
window.tableSortingManagers = window.tableSortingManagers || {};

/**
 * Helper para inicializar ordenamiento en tabla
 */
function initTableSorting(tableId, options = {}) {
    const manager = new TableSortingManager(tableId, options);
    window.tableSortingManagers[tableId] = manager;
    return manager;
}
