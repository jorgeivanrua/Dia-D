/**
 * Pagination Manager - Sistema de paginación para tablas grandes
 * Optimización #1: Implementar paginación en tablas grandes
 */

class PaginationManager {
    constructor(containerId, options = {}) {
        this.containerId = containerId;
        this.currentPage = 1;
        this.itemsPerPage = options.itemsPerPage || 25;
        this.data = [];
        this.filteredData = [];
        this.renderCallback = options.renderCallback || null;
        this.paginationContainerId = options.paginationContainerId || `${containerId}_pagination`;
    }

    /**
     * Establecer datos
     */
    setData(data) {
        this.data = data;
        this.filteredData = data;
        this.currentPage = 1;
        this.render();
    }

    /**
     * Aplicar filtro
     */
    filter(filterFn) {
        this.filteredData = this.data.filter(filterFn);
        this.currentPage = 1;
        this.render();
    }

    /**
     * Obtener datos de la página actual
     */
    getCurrentPageData() {
        const start = (this.currentPage - 1) * this.itemsPerPage;
        const end = start + this.itemsPerPage;
        return this.filteredData.slice(start, end);
    }

    /**
     * Obtener número total de páginas
     */
    getTotalPages() {
        return Math.ceil(this.filteredData.length / this.itemsPerPage);
    }

    /**
     * Ir a página específica
     */
    goToPage(page) {
        const totalPages = this.getTotalPages();
        if (page < 1 || page > totalPages) return;
        
        this.currentPage = page;
        this.render();
    }

    /**
     * Página siguiente
     */
    nextPage() {
        this.goToPage(this.currentPage + 1);
    }

    /**
     * Página anterior
     */
    prevPage() {
        this.goToPage(this.currentPage - 1);
    }

    /**
     * Renderizar tabla y paginación
     */
    render() {
        // Renderizar datos usando callback
        if (this.renderCallback) {
            const pageData = this.getCurrentPageData();
            this.renderCallback(pageData);
        }

        // Renderizar controles de paginación
        this.renderPagination();
    }

    /**
     * Renderizar controles de paginación
     */
    renderPagination() {
        const container = document.getElementById(this.paginationContainerId);
        if (!container) return;

        const totalPages = this.getTotalPages();
        const totalItems = this.filteredData.length;

        if (totalPages <= 1) {
            container.innerHTML = '';
            return;
        }

        const start = (this.currentPage - 1) * this.itemsPerPage + 1;
        const end = Math.min(this.currentPage * this.itemsPerPage, totalItems);

        let html = `
            <div class="d-flex justify-content-between align-items-center">
                <div class="text-muted small">
                    Mostrando ${start} - ${end} de ${totalItems} registros
                </div>
                <nav>
                    <ul class="pagination pagination-sm mb-0">
                        <li class="page-item ${this.currentPage === 1 ? 'disabled' : ''}">
                            <a class="page-link" href="#" onclick="event.preventDefault(); window.paginationManagers['${this.containerId}'].prevPage()">
                                <i class="bi bi-chevron-left"></i>
                            </a>
                        </li>
        `;

        // Páginas
        const maxButtons = 5;
        let startPage = Math.max(1, this.currentPage - Math.floor(maxButtons / 2));
        let endPage = Math.min(totalPages, startPage + maxButtons - 1);

        if (endPage - startPage < maxButtons - 1) {
            startPage = Math.max(1, endPage - maxButtons + 1);
        }

        if (startPage > 1) {
            html += `
                <li class="page-item">
                    <a class="page-link" href="#" onclick="event.preventDefault(); window.paginationManagers['${this.containerId}'].goToPage(1)">1</a>
                </li>
            `;
            if (startPage > 2) {
                html += `<li class="page-item disabled"><span class="page-link">...</span></li>`;
            }
        }

        for (let i = startPage; i <= endPage; i++) {
            html += `
                <li class="page-item ${i === this.currentPage ? 'active' : ''}">
                    <a class="page-link" href="#" onclick="event.preventDefault(); window.paginationManagers['${this.containerId}'].goToPage(${i})">${i}</a>
                </li>
            `;
        }

        if (endPage < totalPages) {
            if (endPage < totalPages - 1) {
                html += `<li class="page-item disabled"><span class="page-link">...</span></li>`;
            }
            html += `
                <li class="page-item">
                    <a class="page-link" href="#" onclick="event.preventDefault(); window.paginationManagers['${this.containerId}'].goToPage(${totalPages})">${totalPages}</a>
                </li>
            `;
        }

        html += `
                        <li class="page-item ${this.currentPage === totalPages ? 'disabled' : ''}">
                            <a class="page-link" href="#" onclick="event.preventDefault(); window.paginationManagers['${this.containerId}'].nextPage()">
                                <i class="bi bi-chevron-right"></i>
                            </a>
                        </li>
                    </ul>
                </nav>
            </div>
        `;

        container.innerHTML = html;
    }

    /**
     * Cambiar items por página
     */
    setItemsPerPage(items) {
        this.itemsPerPage = items;
        this.currentPage = 1;
        this.render();
    }
}

// Registro global de paginadores
window.paginationManagers = window.paginationManagers || {};
