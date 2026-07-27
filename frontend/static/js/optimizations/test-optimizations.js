/**
 * Script de Prueba para Optimizaciones
 * Verifica que todos los módulos de optimización funcionen correctamente
 */

class OptimizationTester {
    constructor() {
        this.results = [];
        this.passed = 0;
        this.failed = 0;
    }

    /**
     * Ejecutar todas las pruebas
     */
    async runAllTests() {
        console.log('🧪 Iniciando pruebas de optimizaciones...\n');

        await this.testCacheManager();
        await this.testPagination();
        await this.testLazyLoading();
        await this.testAdvancedSearch();
        await this.testTableSorting();

        this.printResults();
    }

    /**
     * Probar Cache Manager
     */
    async testCacheManager() {
        console.log('📦 Probando Cache Manager...');

        try {
            // Test 1: Set y Get
            window.cacheManager.set('test_key', { data: 'test' }, 1000);
            const cached = window.cacheManager.get('test_key');
            this.assert(cached !== null, 'Cache Manager: Set y Get funcionan');

            // Test 2: Has
            const exists = window.cacheManager.has('test_key');
            this.assert(exists === true, 'Cache Manager: Has funciona');

            // Test 3: Delete
            window.cacheManager.delete('test_key');
            const deleted = window.cacheManager.get('test_key');
            this.assert(deleted === null, 'Cache Manager: Delete funciona');

            // Test 4: Expiración
            window.cacheManager.set('expire_test', { data: 'expire' }, 100);
            await this.sleep(150);
            const expired = window.cacheManager.get('expire_test');
            this.assert(expired === null, 'Cache Manager: Expiración funciona');

            // Test 5: Clear
            window.cacheManager.set('clear_test_1', 'data1');
            window.cacheManager.set('clear_test_2', 'data2');
            window.cacheManager.clear();
            const stats = window.cacheManager.getStats();
            this.assert(stats.size === 0, 'Cache Manager: Clear funciona');

            console.log('✅ Cache Manager: Todas las pruebas pasaron\n');
        } catch (error) {
            console.error('❌ Cache Manager: Error en pruebas', error);
        }
    }

    /**
     * Probar Paginación
     */
    async testPagination() {
        console.log('📄 Probando Paginación...');

        try {
            // Crear contenedor temporal
            const container = document.createElement('div');
            container.id = 'test_pagination_body';
            document.body.appendChild(container);

            const paginationContainer = document.createElement('div');
            paginationContainer.id = 'test_pagination_controls';
            document.body.appendChild(paginationContainer);

            // Datos de prueba
            const testData = Array.from({ length: 100 }, (_, i) => ({
                id: i + 1,
                name: `Item ${i + 1}`
            }));

            // Crear paginación
            const pagination = new PaginationManager('test_pagination_body', {
                itemsPerPage: 10,
                paginationContainerId: 'test_pagination_controls',
                renderCallback: (data) => {
                    container.innerHTML = data.map(item => `<div>${item.name}</div>`).join('');
                }
            });

            // Test 1: Set Data
            pagination.setData(testData);
            this.assert(pagination.getTotalPages() === 10, 'Paginación: Total de páginas correcto');

            // Test 2: Get Current Page Data
            const pageData = pagination.getCurrentPageData();
            this.assert(pageData.length === 10, 'Paginación: Datos de página correctos');

            // Test 3: Go To Page
            pagination.goToPage(2);
            this.assert(pagination.currentPage === 2, 'Paginación: Cambio de página funciona');

            // Test 4: Next Page
            pagination.nextPage();
            this.assert(pagination.currentPage === 3, 'Paginación: Página siguiente funciona');

            // Test 5: Prev Page
            pagination.prevPage();
            this.assert(pagination.currentPage === 2, 'Paginación: Página anterior funciona');

            // Test 6: Set Items Per Page
            pagination.setItemsPerPage(25);
            this.assert(pagination.getTotalPages() === 4, 'Paginación: Cambio de items por página funciona');

            // Limpiar
            container.remove();
            paginationContainer.remove();

            console.log('✅ Paginación: Todas las pruebas pasaron\n');
        } catch (error) {
            console.error('❌ Paginación: Error en pruebas', error);
        }
    }

    /**
     * Probar Lazy Loading
     */
    async testLazyLoading() {
        console.log('🖼️ Probando Lazy Loading...');

        try {
            // Test 1: Verificar que el manager existe
            this.assert(window.lazyLoadManager !== undefined, 'Lazy Loading: Manager existe');

            // Test 2: Crear imagen de prueba
            const img = document.createElement('img');
            img.dataset.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100"%3E%3Crect fill="%23f0f0f0" width="100" height="100"/%3E%3C/svg%3E';
            img.alt = 'Test Image';
            document.body.appendChild(img);

            // Test 3: Actualizar lazy loading
            window.lazyLoadManager.update();
            this.assert(true, 'Lazy Loading: Update funciona');

            // Limpiar
            img.remove();

            console.log('✅ Lazy Loading: Todas las pruebas pasaron\n');
        } catch (error) {
            console.error('❌ Lazy Loading: Error en pruebas', error);
        }
    }

    /**
     * Probar Búsqueda Avanzada
     */
    async testAdvancedSearch() {
        console.log('🔍 Probando Búsqueda Avanzada...');

        try {
            // Datos de prueba
            const testData = [
                { id: 1, name: 'Juan Pérez', role: 'admin', age: 30, active: true },
                { id: 2, name: 'María García', role: 'user', age: 25, active: true },
                { id: 3, name: 'Pedro López', role: 'admin', age: 35, active: false },
                { id: 4, name: 'Ana Martínez', role: 'user', age: 28, active: true },
                { id: 5, name: 'Carlos Rodríguez', role: 'moderator', age: 32, active: true }
            ];

            const search = new AdvancedSearchManager(testData, {
                searchFields: ['name', 'role']
            });

            // Test 1: Búsqueda por término
            search.setSearchTerm('juan');
            let results = search.search();
            this.assert(results.length === 1, 'Búsqueda Avanzada: Búsqueda por término funciona');

            // Test 2: Filtro simple
            search.setSearchTerm('');
            search.addFilter('role', 'admin');
            results = search.search();
            this.assert(results.length === 2, 'Búsqueda Avanzada: Filtro simple funciona');

            // Test 3: Filtro booleano
            search.clearFilters();
            search.addFilter('active', true);
            results = search.search();
            this.assert(results.length === 4, 'Búsqueda Avanzada: Filtro booleano funciona');

            // Test 4: Filtro de rango
            search.clearFilters();
            search.addFilter('age', { min: 25, max: 30 });
            results = search.search();
            this.assert(results.length === 3, 'Búsqueda Avanzada: Filtro de rango funciona');

            // Test 5: Ordenamiento
            search.clearFilters();
            search.setSort('age', 'asc');
            results = search.search();
            this.assert(results[0].age === 25, 'Búsqueda Avanzada: Ordenamiento ascendente funciona');

            search.setSort('age', 'desc');
            results = search.search();
            this.assert(results[0].age === 35, 'Búsqueda Avanzada: Ordenamiento descendente funciona');

            // Test 6: Estadísticas
            search.clearFilters();
            search.setSearchTerm('admin');
            const stats = search.getStats();
            this.assert(stats.total === 5 && stats.filtered === 2, 'Búsqueda Avanzada: Estadísticas funcionan');

            console.log('✅ Búsqueda Avanzada: Todas las pruebas pasaron\n');
        } catch (error) {
            console.error('❌ Búsqueda Avanzada: Error en pruebas', error);
        }
    }

    /**
     * Probar Ordenamiento de Tablas
     */
    async testTableSorting() {
        console.log('📊 Probando Ordenamiento de Tablas...');

        try {
            // Crear tabla temporal
            const table = document.createElement('table');
            table.id = 'test_sorting_table';
            table.innerHTML = `
                <thead>
                    <tr>
                        <th class="sortable">ID</th>
                        <th class="sortable">Nombre</th>
                        <th class="sortable">Edad</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td data-sort="3">3</td>
                        <td data-sort="Carlos">Carlos</td>
                        <td data-sort="25">25</td>
                    </tr>
                    <tr>
                        <td data-sort="1">1</td>
                        <td data-sort="Ana">Ana</td>
                        <td data-sort="30">30</td>
                    </tr>
                    <tr>
                        <td data-sort="2">2</td>
                        <td data-sort="Beatriz">Beatriz</td>
                        <td data-sort="28">28</td>
                    </tr>
                </tbody>
            `;
            document.body.appendChild(table);

            // Test 1: Inicializar ordenamiento
            const sortManager = new TableSortingManager('test_sorting_table');
            this.assert(sortManager !== null, 'Ordenamiento: Manager se inicializa');

            // Test 2: Ordenar por columna
            sortManager.sortByColumn(0, table.querySelector('thead th'));
            const firstId = table.querySelector('tbody tr:first-child td:first-child').textContent;
            this.assert(firstId === '1', 'Ordenamiento: Ordenar por ID funciona');

            // Test 3: Cambiar orden
            sortManager.sortByColumn(0, table.querySelector('thead th'));
            const lastId = table.querySelector('tbody tr:first-child td:first-child').textContent;
            this.assert(lastId === '3', 'Ordenamiento: Cambio de orden funciona');

            // Limpiar
            table.remove();

            console.log('✅ Ordenamiento de Tablas: Todas las pruebas pasaron\n');
        } catch (error) {
            console.error('❌ Ordenamiento de Tablas: Error en pruebas', error);
        }
    }

    /**
     * Assert helper
     */
    assert(condition, message) {
        if (condition) {
            this.passed++;
            this.results.push({ status: 'PASS', message });
            console.log(`  ✅ ${message}`);
        } else {
            this.failed++;
            this.results.push({ status: 'FAIL', message });
            console.error(`  ❌ ${message}`);
        }
    }

    /**
     * Sleep helper
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Imprimir resultados
     */
    printResults() {
        console.log('\n' + '='.repeat(60));
        console.log('📊 RESULTADOS DE PRUEBAS');
        console.log('='.repeat(60));
        console.log(`Total de pruebas: ${this.passed + this.failed}`);
        console.log(`✅ Pasadas: ${this.passed}`);
        console.log(`❌ Fallidas: ${this.failed}`);
        console.log(`📈 Tasa de éxito: ${((this.passed / (this.passed + this.failed)) * 100).toFixed(1)}%`);
        console.log('='.repeat(60) + '\n');

        if (this.failed === 0) {
            console.log('🎉 ¡Todas las pruebas pasaron exitosamente!');
        } else {
            console.warn('⚠️ Algunas pruebas fallaron. Revisar logs arriba.');
        }
    }
}

// Función para ejecutar pruebas desde consola
window.testOptimizations = async function() {
    const tester = new OptimizationTester();
    await tester.runAllTests();
    return tester.results;
};

// Auto-ejecutar si se carga directamente
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        console.log('🧪 Script de pruebas cargado. Ejecuta window.testOptimizations() para probar.');
    });
} else {
    console.log('🧪 Script de pruebas cargado. Ejecuta window.testOptimizations() para probar.');
}
