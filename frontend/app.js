/**
 * TechMind AI — App JavaScript
 * Conecta la interfaz Stitch con el Backend de Spring Boot (localhost:8080) y FastAPI (localhost:8000)
 */

// URLs de API — se detectan automáticamente según el host donde corre el frontend.
// En local:  window.location.hostname = "localhost"
// En OCI:    window.location.hostname = "<IP-pública-OCI>" o dominio
const _HOST = window.location.hostname;
const API_BASE_URL = `http://${_HOST}:8080`;
const DS_API_URL   = `http://${_HOST}:8000`;

// Configuración visual por categoría
const CATEGORY_CONFIG = {
    'Backend': { icon: 'dns', colorClass: 'text-blue-700 dark:text-blue-400 border-blue-500/40 bg-blue-500/10' },
    'Frontend': { icon: 'view_quilt', colorClass: 'text-pink-700 dark:text-pink-400 border-pink-500/40 bg-pink-500/10' },
    'Data Science': { icon: 'analytics', colorClass: 'text-emerald-700 dark:text-emerald-400 border-emerald-500/40 bg-emerald-500/10' },
    'DevOps': { icon: 'terminal', colorClass: 'text-cyan-700 dark:text-cyan-400 border-cyan-500/40 bg-cyan-500/10' },
    'Mobile': { icon: 'smartphone', colorClass: 'text-amber-700 dark:text-amber-400 border-amber-500/40 bg-amber-500/10' },
    'Bases de Datos': { icon: 'storage', colorClass: 'text-orange-700 dark:text-orange-400 border-orange-500/40 bg-orange-500/10' },
    'Seguridad': { icon: 'shield', colorClass: 'text-rose-700 dark:text-rose-400 border-rose-500/40 bg-rose-500/10' },
    'Cloud': { icon: 'cloud_queue', colorClass: 'text-sky-700 dark:text-sky-400 border-sky-500/40 bg-sky-500/10' }
};

// ── Internacionalización (i18n) ─────────────────────────────────────────────
const TRANSLATIONS = {
    es: {
        brand_subtitle: 'Organización inteligente', nav_classifier: 'Clasificador',
        nav_history: 'Historial', nav_analytics: 'Análisis',
        theme_dark: 'Modo oscuro', theme_light: 'Modo claro',
        service_status: 'Estado de servicios', microservices: 'Microservicios',
        oci_server: 'Servidor OCI', ram_used: 'RAM Usada', free: 'Libre:',
        header_classifier_title: 'Clasificación de contenido técnico',
        header_classifier_subtitle: 'Ingresá textos para clasificarlos en tiempo real.',
        header_history_title: 'Historial de consultas',
        header_history_subtitle: 'Revisá y filtrá todas las predicciones.',
        header_analytics_title: 'Panel de análisis',
        header_analytics_subtitle: 'Visualizá métricas y estadísticas de las clasificaciones.',
        form_title: 'Ingresar contenido técnico', label_title: 'Título del documento o artículo',
        placeholder_title: 'ej. orquestación avanzada de contenedores con Kubernetes',
        label_body: 'Contenido técnico (texto crudo, markdown o resumen)',
        placeholder_body: 'Pegue aquí el texto o resumen técnico para que el modelo determine la categoría y extraiga los conceptos clave...',
        btn_classify: 'Clasificar con TechMind', btn_clear: 'Limpiar formulario',
        results_title: 'Resultado del análisis', predicted_category: 'Categoría predicha',
        waiting: 'Esperando análisis...', confidence: 'Confianza del Modelo',
        keywords_title: 'Palabras clave extraídas',
        keywords_placeholder: 'Las entidades detectadas aparecerán aquí...',
        btn_view_json: 'Ver JSON', recent_title: 'Contenidos clasificados recientemente',
        loading_history_grid: 'Cargando publicaciones guardadas desde PostgreSQL...',
        loading_detailed: 'Cargando historial detallado ...',
        no_data: 'No hay publicaciones guardadas en la base de datos aún.',
        no_results: 'No se encontraron registros para la categoría seleccionada.',
        confidence_label: 'Confianza:', delete_btn: 'Borrar', see_more: 'Ver más', see_less: 'Ver menos',
        search_placeholder: 'Buscar por título o palabra clave...',
        filter_label: 'Filtrar:', all_categories: 'Todas las categorías',
        total_classifications: 'Total Clasificaciones', top_category: 'Categoría Líder',
        avg_confidence: 'Confianza Promedio', dist_by_category: 'Distribución por categoría',
        activity_by_hour: 'Actividad por hora del día (24hs)',
        top_keywords: 'Palabras clave más frecuentes', top_terms: 'Top términos clasificados',
        json_modal_title: 'Resultado del análisis en JSON',
        copy_json: 'Copiar JSON', copied: '¡Copiado!',
        admin_login: 'Iniciar sesión', admin_options: 'Opciones de Administrador',
        admin_title: 'Iniciar sesión admin',
        admin_subtitle: 'Acceso a borrado y gestión de consultas',
        admin_user_label: 'Usuario administrador', admin_user_placeholder: 'Ej. admin',
        admin_pass_label: 'Contraseña', admin_cancel: 'Cancelar', admin_submit: 'Ingresar',
        active_session: 'Sesión Activa', logout: 'Cerrar Sesión',
        toast_fill_fields: 'Por favor, llena todos los campos',
        toast_classified: 'Contenido clasificado y guardado',
        toast_error: 'Hubo un error, por favor intenta de nuevo más tarde',
        toast_admin_login_ok: '🛡️ Sesión de Administrador iniciada',
        toast_admin_logout: 'Sesión de Administrador cerrada',
        toast_deleted: '🗑️ Consulta ID #{id} eliminada correctamente.',
        toast_delete_error: 'Error al eliminar:',
        toast_not_admin: 'Debe iniciar sesión como Administrador para eliminar registros.',
        toast_copied: '📋 JSON copiado al portapapeles con éxito',
        toast_copy_error: '⚠️ No se pudo copiar el contenido',
        toast_not_found: '⚠️ No se encontró la información de la consulta',
        error_db: 'Error al conectar con la base de datos.',
        no_keywords: 'Sin palabras clave', no_description: 'Sin descripción disponible',
        no_terms: 'Sin términos clave destacados', date_not_available: 'Fecha no disponible',
        no_keywords_data: 'Sin datos de palabras clave',
        confirm_delete: '⚠️ ¿Estás seguro de que deseas eliminar permanentemente la consulta ID #{id}?',
        no_session_json: '{\n  "mensaje": "Aún no se ha realizado ninguna clasificación en esta sesión."\n}',
        queries_label: 'Consultas',
    },
    en: {
        brand_subtitle: 'Intelligent organization', nav_classifier: 'Classifier',
        nav_history: 'History', nav_analytics: 'Analytics',
        theme_dark: 'Dark mode', theme_light: 'Light mode',
        service_status: 'Service status', microservices: 'Microservices',
        oci_server: 'OCI Server', ram_used: 'RAM Used', free: 'Free:',
        header_classifier_title: 'Technical content classification',
        header_classifier_subtitle: 'Enter texts to classify them in real time.',
        header_history_title: 'Query history',
        header_history_subtitle: 'Review and filter all predictions.',
        header_analytics_title: 'Analytics dashboard',
        header_analytics_subtitle: 'View metrics and statistics from classifications.',
        form_title: 'Enter technical content', label_title: 'Document or article title',
        placeholder_title: 'e.g. advanced container orchestration with Kubernetes',
        label_body: 'Technical content (raw text, markdown or summary)',
        placeholder_body: 'Paste the technical text or summary here so the model can determine the category and extract key concepts...',
        btn_classify: 'Classify with TechMind', btn_clear: 'Clear form',
        results_title: 'Analysis result', predicted_category: 'Predicted category',
        waiting: 'Waiting for analysis...', confidence: 'Model Confidence',
        keywords_title: 'Extracted keywords',
        keywords_placeholder: 'Detected entities will appear here...',
        btn_view_json: 'View JSON', recent_title: 'Recently classified content',
        loading_history_grid: 'Loading saved publications from PostgreSQL...',
        loading_detailed: 'Loading detailed history...',
        no_data: 'No publications saved in the database yet.',
        no_results: 'No records found for the selected category.',
        confidence_label: 'Confidence:', delete_btn: 'Delete', see_more: 'See more', see_less: 'See less',
        search_placeholder: 'Search by title or keyword...',
        filter_label: 'Filter:', all_categories: 'All categories',
        total_classifications: 'Total Classifications', top_category: 'Top Category',
        avg_confidence: 'Avg. Confidence', dist_by_category: 'Distribution by category',
        activity_by_hour: 'Activity by hour of day (24h)',
        top_keywords: 'Most frequent keywords', top_terms: 'Top classified terms',
        json_modal_title: 'Analysis result in JSON',
        copy_json: 'Copy JSON', copied: 'Copied!',
        admin_login: 'Admin Login', admin_options: 'Admin Options',
        admin_title: 'Admin login',
        admin_subtitle: 'Access to deletion and query management',
        admin_user_label: 'Admin username', admin_user_placeholder: 'e.g. admin',
        admin_pass_label: 'Password', admin_cancel: 'Cancel', admin_submit: 'Login',
        active_session: 'Active Session', logout: 'Logout',
        toast_fill_fields: 'Please fill in all fields',
        toast_classified: 'Content classified and saved',
        toast_error: 'An error occurred, please try again later',
        toast_admin_login_ok: '🛡️ Administrator session started',
        toast_admin_logout: 'Administrator session closed',
        toast_deleted: '🗑️ Query ID #{id} deleted successfully.',
        toast_delete_error: 'Error deleting:',
        toast_not_admin: 'You must log in as Administrator to delete records.',
        toast_copied: '📋 JSON copied to clipboard',
        toast_copy_error: '⚠️ Could not copy content',
        toast_not_found: '⚠️ Query information not found',
        error_db: 'Error connecting to database.',
        no_keywords: 'No keywords', no_description: 'No description available',
        no_terms: 'No key terms detected', date_not_available: 'Date not available',
        no_keywords_data: 'No keyword data',
        confirm_delete: '⚠️ Are you sure you want to permanently delete query ID #{id}?',
        no_session_json: '{\n  "message": "No classification has been performed in this session yet."\n}',
        queries_label: 'Queries',
    }
};

let currentLang = localStorage.getItem('lang') || 'es';
function t(key) {
    const lang = TRANSLATIONS[currentLang];
    return (lang && lang[key] !== undefined) ? lang[key] : (TRANSLATIONS.es[key] !== undefined ? TRANSLATIONS.es[key] : key);
}
let currentView = 'classifier';

let lastJsonResponse = null;
let lastInput = null;
let allHistoryData = [];
let healthStates = {
    springboot: false,
    fastapi: false,
    postgres: true
};

// Autenticación de Administrador
let adminToken = sessionStorage.getItem('adminToken') || null;
let adminUser  = sessionStorage.getItem('adminUser') || null;

function isLoggedInAsAdmin() {
    return adminToken !== null;
}

document.addEventListener('DOMContentLoaded', () => {
    // Load theme setting
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        document.documentElement.classList.remove('dark');
    } else {
        document.documentElement.classList.add('dark');
    }
    // Mobile: sidebar starts hidden, no icon init needed
    updateAdminUIState();
    applyTranslations();
    initHealthChecks();
    fetchSystemStats();
    setInterval(fetchSystemStats, 10000);
    setInterval(initHealthChecks, 30000);
    bindEvents();
    loadHistory(); // Carga el historial desde PostgreSQL al iniciar
});

// ── 1. Health Checks & Métricas de Servidor ───────────────────────────────

async function initHealthChecks() {
    // Check FastAPI
    try {
        const res = await fetch(`${DS_API_URL}/health`);
        const data = await res.json();
        if (data.status === 'ok') {
            setServiceStatus('status-fastapi', true, 'FastAPI ML :8000');
        } else {
            setServiceStatus('status-fastapi', false, 'FastAPI ML :8000');
        }
    } catch {
        setServiceStatus('status-fastapi', false, 'FastAPI ML :8000');
    }

    // Check Spring Boot
    try {
        const res = await fetch(`${API_BASE_URL}/actuator/health`);
        const data = await res.json();
        if (data.status === 'UP') {
            setServiceStatus('status-springboot', true, 'Spring Boot :8080');
        } else {
            setServiceStatus('status-springboot', false, 'Spring Boot :8080');
        }
    } catch {
        setServiceStatus('status-springboot', false, 'Spring Boot :8080');
    }

    // PostgreSQL status
    setServiceStatus('status-postgres', true, 'PostgreSQL :5432');
}

async function fetchSystemStats() {
    try {
        const res = await fetch(`${DS_API_URL}/system-stats`);
        if (!res.ok) return;
        const data = await res.json();

        // Uptime
        const uptimeValEl = document.getElementById('sys-uptime-val');
        if (uptimeValEl && data.uptime) uptimeValEl.textContent = data.uptime;

        // CPU
        const cpuValEl = document.getElementById('sys-cpu-val');
        const cpuBarEl = document.getElementById('sys-cpu-bar');
        if (cpuValEl) cpuValEl.textContent = `${data.cpu_percent}%`;
        if (cpuBarEl) cpuBarEl.style.width = `${Math.min(100, data.cpu_percent)}%`;

        // RAM
        const ramValEl = document.getElementById('sys-ram-val');
        const ramBarEl = document.getElementById('sys-ram-bar');
        const ramFreeEl = document.getElementById('sys-ram-free-badge');
        const ramPctEl = document.getElementById('sys-ram-pct');

        if (ramValEl) ramValEl.textContent = `${data.ram_used_mb} / ${data.ram_total_mb} MB`;
        if (ramPctEl) ramPctEl.textContent = `${data.ram_percent}%`;
        if (ramFreeEl) ramFreeEl.textContent = `${t('free')} ${data.ram_free_mb} MB`;
        if (ramBarEl) {
            ramBarEl.style.width = `${Math.min(100, data.ram_percent)}%`;
            if (data.ram_percent > 90) {
                ramBarEl.className = 'bg-rose-500 h-full transition-all duration-500';
            } else if (data.ram_percent > 80) {
                ramBarEl.className = 'bg-amber-500 h-full transition-all duration-500';
            } else {
                ramBarEl.className = 'bg-purple-500 h-full transition-all duration-500';
            }
        }

        // Swap
        const swapValEl = document.getElementById('sys-swap-val');
        const swapBarEl = document.getElementById('sys-swap-bar');
        if (swapValEl) swapValEl.textContent = `${data.swap_used_mb} / ${data.swap_total_mb} MB`;
        if (swapBarEl) swapBarEl.style.width = `${Math.min(100, data.swap_percent)}%`;

    } catch (e) {
        // Ignorar si no está disponible
    }
}

function setServiceStatus(elementId, isOk, text) {
    const el = document.getElementById(elementId);
    if (!el) return;
    const led = el.querySelector('.rounded-full');
    const label = el.querySelector('span');

    if (isOk) {
        led.className = 'w-2.5 h-2.5 rounded-full led-pulse shrink-0';
        led.style.backgroundColor = 'var(--led-ok-bg)';
        label.className = 'font-label-sm text-[11px] font-medium';
        label.style.color = 'var(--led-ok-text)';
    } else {
        led.className = 'w-2.5 h-2.5 rounded-full shrink-0';
        led.style.backgroundColor = 'var(--led-error-bg)';
        label.className = 'font-label-sm text-[11px] font-medium';
        label.style.color = 'var(--led-error-text)';
    }
    label.textContent = text;

    // Update trackers
    if (elementId === 'status-springboot') healthStates.springboot = isOk;
    if (elementId === 'status-fastapi') healthStates.fastapi = isOk;
    if (elementId === 'status-postgres') healthStates.postgres = isOk;

    // Update overall indicator
    const overallLed = document.getElementById('overall-status-led');
    if (overallLed) {
        const allUp = healthStates.springboot && healthStates.fastapi && healthStates.postgres;
        if (allUp) {
            overallLed.className = 'w-2.5 h-2.5 rounded-full led-pulse';
            overallLed.style.backgroundColor = 'var(--led-ok-bg)';
        } else {
            overallLed.className = 'w-2.5 h-2.5 rounded-full';
            overallLed.style.backgroundColor = 'var(--led-error-bg)';
        }
    }
}

// ── 2. Event Listeners ──────────────────────────────────────────────────────

function bindEvents() {
    const classifyBtn = document.getElementById('btn-classify');
    const jsonBtn = document.getElementById('btn-view-json');
    const jsonModalClose = document.getElementById('modal-close');

    if (classifyBtn) {
        classifyBtn.addEventListener('click', handleClassification);
    }
    if (jsonBtn) {
        jsonBtn.addEventListener('click', toggleJsonModal);
    }
    if (jsonModalClose) {
        jsonModalClose.addEventListener('click', toggleJsonModal);
    }

    // Sidebar selectors
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebar-overlay');
    const mainContent = document.getElementById('main-content');

    // ── Claude-style Sidebar ──────────────────────────────────────────────────

    const closeSidebar = () => {
        if (!sidebar) return;
        // Mobile: slide out
        sidebar.classList.add('-translate-x-full');
        sidebar.classList.remove('translate-x-0');
        if (sidebarOverlay) sidebarOverlay.classList.add('hidden');
    };

    const openSidebarMobile = () => {
        if (!sidebar) return;
        sidebar.classList.remove('-translate-x-full', 'sidebar-collapsed');
        sidebar.classList.add('translate-x-0');
        if (sidebarOverlay) sidebarOverlay.classList.remove('hidden');
    };

    let sidebarCollapsed = false;

    const collapseSidebar = () => {
        if (!sidebar) return;
        sidebarCollapsed = true;
        sidebar.classList.add('sidebar-collapsed');
        if (mainContent) mainContent.style.marginLeft = 'var(--sidebar-collapsed-width)';
        const toggleIcon = document.getElementById('sidebar-toggle-icon');
        if (toggleIcon) toggleIcon.textContent = 'chevron_right';
        localStorage.setItem('sidebarCollapsed', 'true');
    };

    const expandSidebar = () => {
        if (!sidebar) return;
        sidebarCollapsed = false;
        sidebar.classList.remove('sidebar-collapsed');
        if (mainContent) mainContent.style.marginLeft = 'var(--sidebar-width)';
        const toggleIcon = document.getElementById('sidebar-toggle-icon');
        if (toggleIcon) toggleIcon.textContent = 'chevron_left';
        localStorage.setItem('sidebarCollapsed', 'false');
    };

    // Desktop: toggle between collapsed (icons only) and expanded
    const sidebarToggle = document.getElementById('btn-sidebar-toggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', () => {
            if (window.innerWidth < 768) {
                // On mobile, clicking the toggle inside sidebar should close it
                closeSidebar();
            } else {
                if (sidebarCollapsed) {
                    expandSidebar();
                } else {
                    collapseSidebar();
                }
            }
        });
    }

    // Mobile hamburger button
    const sidebarMobile = document.getElementById('btn-sidebar-mobile');
    if (sidebarMobile) {
        sidebarMobile.addEventListener('click', openSidebarMobile);
    }

    // Overlay click closes sidebar on mobile
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', closeSidebar);
    }

    // Restore saved sidebar state
    const savedCollapsed = localStorage.getItem('sidebarCollapsed');
    if (window.innerWidth >= 768) {
        if (savedCollapsed === 'true') {
            collapseSidebar();
        } else {
            expandSidebar();
        }
        sidebar.classList.remove('-translate-x-full');
        sidebar.classList.add('md:translate-x-0');
    } else {
        // Mobile: hidden by default, remove any desktop margin
        if (mainContent) mainContent.style.marginLeft = '0';
    }

    // Sync sidebar state when crossing breakpoints
    let wasDesktop = window.innerWidth >= 768;
    const syncSidebarToBreakpoint = () => {
        if (!sidebar) return;
        const isDesktop = window.innerWidth >= 768;
        if (isDesktop === wasDesktop) return;
        wasDesktop = isDesktop;

        if (isDesktop) {
            // Switching to desktop
            sidebar.classList.remove('-translate-x-full', 'translate-x-0');
            sidebar.classList.add('md:translate-x-0');
            if (sidebarOverlay) sidebarOverlay.classList.add('hidden');
            if (sidebarCollapsed) {
                sidebar.classList.add('sidebar-collapsed');
                if (mainContent) mainContent.style.marginLeft = 'var(--sidebar-collapsed-width)';
            } else {
                sidebar.classList.remove('sidebar-collapsed');
                if (mainContent) mainContent.style.marginLeft = 'var(--sidebar-width)';
            }
        } else {
            // Switching to mobile
            sidebar.classList.add('-translate-x-full');
            sidebar.classList.remove('md:translate-x-0', 'translate-x-0', 'sidebar-collapsed');
            if (mainContent) mainContent.style.marginLeft = '0';
            if (sidebarOverlay) sidebarOverlay.classList.add('hidden');
        }
    };
    window.addEventListener('resize', syncSidebarToBreakpoint);

    // ── Clear Form Button ────────────────────────────────────────────────────
    const btnClearForm = document.getElementById('btn-clear-form');
    if (btnClearForm) {
        btnClearForm.addEventListener('click', () => {
            const titleInput = document.getElementById('content-title');
            const bodyInput = document.getElementById('content-body');
            if (titleInput) titleInput.value = '';
            if (bodyInput) bodyInput.value = '';
            if (titleInput) titleInput.focus();
        });
    }

    // Service Status Popover Control
    const statusTrigger = document.getElementById('btn-status-trigger');
    const statusPopover = document.getElementById('status-popover');
    const statusChevron = document.getElementById('status-chevron');

    if (statusTrigger && statusPopover) {
        statusTrigger.addEventListener('click', (e) => {
            e.stopPropagation();
            // Si el sidebar está colapsado en desktop, expandirlo primero
            if (sidebarCollapsed && window.innerWidth >= 768) {
                expandSidebar();
                // Mostrar el popover tras la animación de expansión
                setTimeout(() => {
                    statusPopover.classList.remove('opacity-0', 'pointer-events-none', 'translate-y-2');
                    statusPopover.classList.add('opacity-100', 'pointer-events-auto', 'translate-y-0');
                    if (statusChevron) statusChevron.style.transform = 'rotate(180deg)';
                }, 320);
                return;
            }
            const isOpen = !statusPopover.classList.contains('pointer-events-none');
            if (isOpen) {
                statusPopover.classList.add('opacity-0', 'pointer-events-none', 'translate-y-2');
                statusPopover.classList.remove('opacity-100', 'pointer-events-auto', 'translate-y-0');
                if (statusChevron) statusChevron.style.transform = 'rotate(0deg)';
            } else {
                statusPopover.classList.remove('opacity-0', 'pointer-events-none', 'translate-y-2');
                statusPopover.classList.add('opacity-100', 'pointer-events-auto', 'translate-y-0');
                if (statusChevron) statusChevron.style.transform = 'rotate(180deg)';
            }
        });

        // Close popover when clicking anywhere else
        document.addEventListener('click', () => {
            statusPopover.classList.add('opacity-0', 'pointer-events-none', 'translate-y-2');
            statusPopover.classList.remove('opacity-100', 'pointer-events-auto', 'translate-y-0');
            if (statusChevron) statusChevron.style.transform = 'rotate(0deg)';
        });

        // Prevent closing when clicking inside the popover
        statusPopover.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    }

    // View Switcher Control (SPA subpage logic)
    const navClassifier = document.getElementById('nav-classifier');
    const navHistory = document.getElementById('nav-history');
    const navAnalytics = document.getElementById('nav-analytics');
    const classifierView = document.getElementById('classifier-view-section');
    const historyView = document.getElementById('history-view-section');
    const analyticsView = document.getElementById('analytics-view-section');

    if (navClassifier && navHistory && navAnalytics && classifierView && historyView && analyticsView) {
        // Helper to update the main header title and subtitle dynamically
        const updateMainHeader = (title, subtitle) => {
            const headerTitle = document.getElementById('main-header-title');
            const headerSubtitle = document.getElementById('main-header-subtitle');
            if (headerTitle) headerTitle.textContent = title;
            if (headerSubtitle) headerSubtitle.textContent = subtitle;
        };

        const showClassifier = () => {
            classifierView.classList.remove('hidden');
            historyView.classList.add('hidden');
            analyticsView.classList.add('hidden');
            analyticsView.classList.remove('flex');

            navClassifier.className = "sidebar-nav-item active-nav flex items-center gap-3 transition-all cursor-pointer";
            navHistory.className = "sidebar-nav-item flex items-center gap-3 transition-all text-on-surface-variant cursor-pointer";
            navAnalytics.className = "sidebar-nav-item flex items-center gap-3 transition-all text-on-surface-variant cursor-pointer";

            currentView = 'classifier';
            updateMainHeader(t('header_classifier_title'), t('header_classifier_subtitle'));

            if (window.innerWidth < 768) {
                closeSidebar();
            }
        };

        const showHistory = () => {
            classifierView.classList.add('hidden');
            historyView.classList.remove('hidden');
            analyticsView.classList.add('hidden');
            analyticsView.classList.remove('flex');

            navHistory.className = "sidebar-nav-item active-nav flex items-center gap-3 transition-all cursor-pointer";
            navClassifier.className = "sidebar-nav-item flex items-center gap-3 transition-all text-on-surface-variant cursor-pointer";
            navAnalytics.className = "sidebar-nav-item flex items-center gap-3 transition-all text-on-surface-variant cursor-pointer";

            currentView = 'history';
            updateMainHeader(t('header_history_title'), t('header_history_subtitle'));

            loadDetailedHistory();

            if (window.innerWidth < 768) {
                closeSidebar();
            }
        };

        const showAnalytics = () => {
            classifierView.classList.add('hidden');
            historyView.classList.add('hidden');
            analyticsView.classList.remove('hidden');
            analyticsView.classList.add('flex');

            navAnalytics.className = "sidebar-nav-item active-nav flex items-center gap-3 transition-all cursor-pointer";
            navClassifier.className = "sidebar-nav-item flex items-center gap-3 transition-all text-on-surface-variant cursor-pointer";
            navHistory.className = "sidebar-nav-item flex items-center gap-3 transition-all text-on-surface-variant cursor-pointer";

            currentView = 'analytics';
            updateMainHeader(t('header_analytics_title'), t('header_analytics_subtitle'));

            loadAnalyticsDashboard();

            if (window.innerWidth < 768) {
                closeSidebar();
            }
        };

        const handleNavClick = (viewFunc) => {
            if (sidebarCollapsed && window.innerWidth >= 768) {
                expandSidebar();
            }
            viewFunc();
        };

        navClassifier.addEventListener('click', () => handleNavClick(showClassifier));
        navHistory.addEventListener('click', () => handleNavClick(showHistory));
        navAnalytics.addEventListener('click', () => handleNavClick(showAnalytics));

        const brandHome = document.getElementById('btn-brand-home');
        if (brandHome) {
            brandHome.addEventListener('click', () => handleNavClick(showClassifier));
        }
    }

    // Theme Toggle Control (Sidebar) — updateThemeToggleUI is a global function
    const themeToggle = document.getElementById('btn-theme-toggle');

    if (themeToggle) {
        updateThemeToggleUI();

        themeToggle.addEventListener('click', (e) => {
            e.preventDefault();
            document.documentElement.classList.toggle('dark');
            const nowDark = document.documentElement.classList.contains('dark');
            localStorage.setItem('theme', nowDark ? 'dark' : 'light');
            updateThemeToggleUI();

            // Re-render analytics dashboard if charts exist to update slice borders and legend text colors
            const analyticsViewEl = document.getElementById('analytics-view-section');
            if (analyticsViewEl && !analyticsViewEl.classList.contains('hidden')) {
                loadAnalyticsDashboard();
            }
        });
    }

    // Language Toggle Control
    const langToggle = document.getElementById('btn-lang-toggle');
    if (langToggle) {
        langToggle.addEventListener('click', () => {
            currentLang = currentLang === 'es' ? 'en' : 'es';
            localStorage.setItem('lang', currentLang);
            applyTranslations();
            // Refresh dynamic content that's currently visible
            loadHistory();
            const histViewEl = document.getElementById('history-view-section');
            const anlViewEl = document.getElementById('analytics-view-section');
            if (histViewEl && !histViewEl.classList.contains('hidden')) loadDetailedHistory();
            if (anlViewEl && !anlViewEl.classList.contains('hidden')) loadAnalyticsDashboard();
        });
    }

    // Filter Category and Search listeners
    const filterCategory = document.getElementById('filter-category');
    const searchHistory = document.getElementById('search-history');
    
    if (filterCategory) {
        filterCategory.addEventListener('change', (e) => {
            const searchQuery = searchHistory ? searchHistory.value.trim().toLowerCase() : '';
            loadDetailedHistory(e.target.value, searchQuery);
        });
    }

    if (searchHistory) {
        searchHistory.addEventListener('input', (e) => {
            const category = filterCategory ? filterCategory.value : 'all';
            loadDetailedHistory(category, e.target.value.trim().toLowerCase());
        });
    }

    // JSON Modal Controls — listeners ya vinculados arriba (líneas 188-193), no duplicar

    // Controles del Modal y Popover de Admin Login
    const adminAuthBtn = document.getElementById('btn-admin-auth');
    const adminPopover = document.getElementById('admin-user-popover');
    const adminLogoutBtn = document.getElementById('btn-admin-logout');
    const closeAdminBtn = document.getElementById('btn-close-admin-modal');
    const cancelAdminBtn = document.getElementById('btn-cancel-admin-modal');
    const formAdminLogin = document.getElementById('form-admin-login');

    if (adminAuthBtn) {
        adminAuthBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            if (isLoggedInAsAdmin()) {
                toggleAdminPopover();
            } else {
                showAdminLoginModal();
            }
        });
    }

    if (adminLogoutBtn) {
        adminLogoutBtn.addEventListener('click', () => {
            hideAdminPopover();
            handleAdminLogout();
        });
    }

    if (adminPopover) {
        adminPopover.addEventListener('click', (e) => e.stopPropagation());
    }

    if (closeAdminBtn) closeAdminBtn.addEventListener('click', hideAdminLoginModal);
    if (cancelAdminBtn) cancelAdminBtn.addEventListener('click', hideAdminLoginModal);

    // Close admin login modal on backdrop click
    const adminLoginModal = document.getElementById('admin-login-modal');
    if (adminLoginModal) {
        adminLoginModal.addEventListener('click', (e) => {
            if (e.target === adminLoginModal) {
                hideAdminLoginModal();
            }
        });
    }

    // Close admin user popover on click outside
    document.addEventListener('click', (e) => {
        if (adminPopover && !adminPopover.classList.contains('pointer-events-none')) {
            if (!adminPopover.contains(e.target) && adminAuthBtn && !adminAuthBtn.contains(e.target)) {
                hideAdminPopover();
            }
        }
    });

    if (formAdminLogin) {
        formAdminLogin.addEventListener('submit', (e) => {
            e.preventDefault();
            const u = document.getElementById('admin-username-input').value.trim();
            const p = document.getElementById('admin-password-input').value.trim();
            if (u && p) {
                handleAdminLogin(u, p);
            }
        });
    }
}

// ── 2.1. Autenticación y Administración ──────────────────────────────────────

function toggleAdminPopover() {
    const popover = document.getElementById('admin-user-popover');
    const chevron = document.getElementById('admin-auth-chevron');
    if (!popover) return;

    const isOpen = !popover.classList.contains('pointer-events-none');
    if (isOpen) {
        hideAdminPopover();
    } else {
        popover.classList.remove('opacity-0', 'pointer-events-none', '-translate-y-2');
        popover.classList.add('opacity-100', 'pointer-events-auto', 'translate-y-0');
        if (chevron) chevron.style.transform = 'rotate(180deg)';
    }
}

function hideAdminPopover() {
    const popover = document.getElementById('admin-user-popover');
    const chevron = document.getElementById('admin-auth-chevron');
    if (popover) {
        popover.classList.add('opacity-0', 'pointer-events-none', '-translate-y-2');
        popover.classList.remove('opacity-100', 'pointer-events-auto', 'translate-y-0');
    }
    if (chevron) chevron.style.transform = 'rotate(0deg)';
}

function showAdminLoginModal() {
    const modal = document.getElementById('admin-login-modal');
    if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }
    const input = document.getElementById('admin-username-input');
    if (input) input.focus();
}

function hideAdminLoginModal() {
    const modal = document.getElementById('admin-login-modal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
    const err = document.getElementById('admin-login-error');
    if (err) err.classList.add('hidden');
    const uInput = document.getElementById('admin-username-input');
    const pInput = document.getElementById('admin-password-input');
    if (uInput) uInput.value = '';
    if (pInput) pInput.value = '';
}

async function handleAdminLogin(username, password) {
    const errorEl = document.getElementById('admin-login-error');
    const errorTextEl = document.getElementById('admin-login-error-text');
    if (errorEl) errorEl.classList.add('hidden');

    try {
        const res = await fetch(`${DS_API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        const data = await res.json();
        if (!res.ok) {
            throw new Error(data.detail || 'Usuario o contraseña incorrectos');
        }
        adminToken = data.token;
        adminUser = data.username;
        sessionStorage.setItem('adminToken', adminToken);
        sessionStorage.setItem('adminUser', adminUser);

        hideAdminLoginModal();
        updateAdminUIState();
        showToast(t('toast_admin_login_ok'), 'success', 1800);
        loadHistory();
        loadDetailedHistory();
    } catch (err) {
        if (errorEl && errorTextEl) {
            errorTextEl.textContent = err.message || 'Error de autenticación.';
            errorEl.classList.remove('hidden');
        }
    }
}

async function handleAdminLogout() {
    if (adminToken) {
        try {
            await fetch(`${DS_API_URL}/auth/logout`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${adminToken}` }
            });
        } catch {
            // Ignorar errores de red en logout
        }
    }
    adminToken = null;
    adminUser = null;
    sessionStorage.removeItem('adminToken');
    sessionStorage.removeItem('adminUser');
    updateAdminUIState();
    showToast(t('toast_admin_logout'), 'info', 1800);
    loadHistory();
    const filterCat = document.getElementById('filter-category');
    const searchHist = document.getElementById('search-history');
    const cat = filterCat ? filterCat.value : 'all';
    const q = searchHist ? searchHist.value.trim().toLowerCase() : '';
    loadDetailedHistory(cat, q);
}

function updateAdminUIState() {
    const authBtnText = document.getElementById('admin-auth-text');
    const authBtnIcon = document.getElementById('admin-auth-icon');
    const authBtn = document.getElementById('btn-admin-auth');
    const chevron = document.getElementById('admin-auth-chevron');
    const popoverUser = document.getElementById('popover-admin-username');

    if (isLoggedInAsAdmin()) {
        if (authBtnText) authBtnText.textContent = `Admin (${adminUser})`;
        if (authBtnIcon) authBtnIcon.textContent = 'verified_user';
        if (chevron) chevron.classList.remove('hidden');
        if (popoverUser) popoverUser.textContent = adminUser || 'Admin';
        if (authBtn) {
            authBtn.classList.remove('bg-surface-container-high');
            authBtn.classList.add('bg-emerald-500/20', 'border-emerald-500/40', 'text-emerald-950', 'dark:text-emerald-300', 'font-bold');
            authBtn.title = 'Opciones de Administrador';
        }
    } else {
        if (authBtnText) authBtnText.textContent = t('admin_login');
        if (authBtnIcon) authBtnIcon.textContent = 'admin_panel_settings';
        if (chevron) chevron.classList.add('hidden');
        hideAdminPopover();
        if (authBtn) {
            authBtn.classList.remove('bg-emerald-500/20', 'border-emerald-500/40', 'text-emerald-950', 'dark:text-emerald-300', 'font-bold');
            authBtn.classList.add('bg-surface-container-high');
            authBtn.title = 'Iniciar Sesión Administrador';
        }
    }
}

async function deletePrediction(id) {
    if (!isLoggedInAsAdmin()) {
        showToast(t('toast_not_admin'), 'warning');
        return;
    }

    if (!confirm(t('confirm_delete').replace('{id}', id))) {
        return;
    }

    try {
        const res = await fetch(`${DS_API_URL}/predicciones/${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${adminToken}`
            }
        });
        if (!res.ok) {
            const data = await res.json().catch(() => ({}));
            throw new Error(data.detail || 'No se pudo eliminar la consulta');
        }

        showToast(t('toast_deleted').replace('{id}', id), 'success');

        const jsonModal = document.getElementById('json-modal');
        if (jsonModal && !jsonModal.classList.contains('hidden')) {
            toggleJsonModal();
        }

        loadHistory();
        const filterCat = document.getElementById('filter-category');
        const searchHist = document.getElementById('search-history');
        const cat = filterCat ? filterCat.value : 'all';
        const q = searchHist ? searchHist.value.trim().toLowerCase() : '';
        loadDetailedHistory(cat, q);

        const analyticsView = document.getElementById('analytics-view-section');
        if (analyticsView && !analyticsView.classList.contains('hidden')) {
            loadAnalyticsDashboard();
        }
    } catch (err) {
        showToast(`${t('toast_delete_error')} ${err.message}`, 'error');
    }
}


// ── 3. Clasificación via Spring Boot ────────────────────────────────────────

async function handleClassification() {
    const titleInput = document.getElementById('content-title');
    const bodyInput = document.getElementById('content-body');

    const titulo = titleInput.value.trim();
    const texto = bodyInput.value.trim();

    if (!titulo || !texto) {
        showToast(t('toast_fill_fields'), 'warning');
        return;
    }

    setLoadingState(true);

    try {
        const response = await fetch(`${API_BASE_URL}/contenido`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ titulo, texto })
        });

        if (!response.ok) {
            const errData = await response.json().catch(() => ({}));
            throw new Error(errData.message || errData.titulo || `Error HTTP ${response.status}`);
        }

        const data = await response.json();
        // Redondear probabilidad a 2 decimales y asegurar timestamp ISO local
        if (data.probabilidad != null) {
            data.probabilidad = Math.round(data.probabilidad * 100) / 100;
        }
        if (!data.created_at) {
            data.created_at = getLocalISOString();
        }
        lastJsonResponse = data;
        lastInput = { titulo, texto };

        // Renderizar resultado
        renderResult(data);

        // Limpiar los campos de entrada para nuevas búsquedas
        document.getElementById('content-title').value = '';
        document.getElementById('content-body').value = '';

        // Recargar vistas activas solo si están visibles para proteger recursos del servidor
        setTimeout(() => {
            loadHistory();
            const analyticsView = document.getElementById('analytics-view-section');
            if (analyticsView && !analyticsView.classList.contains('hidden')) {
                loadAnalyticsDashboard();
            }
        }, 600);

        showToast(t('toast_classified'), 'success');

    } catch (err) {
        console.error('Error al clasificar:', err);
        showToast(t('toast_error'), 'error');
    } finally {
        setLoadingState(false);
    }
}

// ── 4. Render de Resultados ─────────────────────────────────────────────────

function renderResult(data) {
    const { categoria, probabilidad, informaciones_adicionales } = data;

    // 1. Categoría
    const badgeContainer = document.getElementById('category-badge-container');
    const config = CATEGORY_CONFIG[categoria] || { icon: 'topic', colorClass: 'text-primary-fixed border-primary/30 bg-primary/10' };

    badgeContainer.innerHTML = `
        <div class="inline-flex max-w-full items-center gap-2 sm:gap-3 px-4 sm:px-6 py-2.5 rounded-full border text-lg sm:text-xl font-bold shadow-[0_0_25px_rgba(139,92,246,0.25)] ${config.colorClass} transition-all duration-300 transform scale-105">
            <span class="material-symbols-outlined text-xl sm:text-2xl shrink-0">${config.icon}</span>
            <span class="min-w-0">${categoria}</span>
        </div>
    `;

    // 2. Porcentaje de Confianza (Con 1 decimal)
    const percentage = Number((probabilidad || 0) * 100).toFixed(1);
    document.getElementById('confidence-score').textContent = `${percentage}%`;
    const bar = document.getElementById('confidence-bar');
    bar.style.width = `${percentage}%`;

    // 3. Keywords
    const keywordsList = document.getElementById('keywords-list');
    if (informaciones_adicionales && informaciones_adicionales.length > 0) {
        keywordsList.innerHTML = informaciones_adicionales.map(kw => {
            const capitalized = kw.charAt(0).toUpperCase() + kw.slice(1);
            return `
                <span class="px-3.5 py-1.5 rounded-full bg-primary/10 border border-primary/30 text-primary-fixed font-label-sm text-sm hover:scale-105 hover:bg-primary/20 transition-all cursor-default flex items-center gap-1.5 shadow-sm">
                    <span class="w-1.5 h-1.5 rounded-full bg-primary-fixed"></span>
                    ${escapeHtml(capitalized)}
                </span>
            `;
        }).join('');
    } else {
        keywordsList.innerHTML = `<span class="text-on-surface-variant text-sm italic">${t('no_terms')}</span>`;
    }

    // Efecto visual
    const card = document.getElementById('results-card');
    if (card) {
        card.style.boxShadow = '0 0 35px rgba(208, 188, 255, 0.3)';
        setTimeout(() => card.style.boxShadow = '', 1000);
    }
}

// ── 5. Cargar e Renderizar Historial ─────────────────────────────────────────

async function loadHistory() {
    const historyGrid = document.getElementById('history-grid');
    if (!historyGrid) return;

    try {
        const res = await fetch(`${DS_API_URL}/predicciones?limit=50`);
        if (!res.ok) throw new Error('No se pudo consultar el historial');

        allHistoryData = await res.json();

        // Pre-populate category counts for filter dropdown
        updateCategoryFilterCounts(allHistoryData);

        if (allHistoryData && allHistoryData.length > 0) {
            // Mostrar los 3 más recientes en el grid de la página
            const recent = allHistoryData.slice(0, 3);
            historyGrid.innerHTML = recent.map(entry => {
                const config = CATEGORY_CONFIG[entry.categoria] || { colorClass: 'text-primary-fixed border-primary/30 bg-primary/10' };
                const prob = entry.probabilidad != null ? Number(entry.probabilidad) : 0;
                const probPct = Number(prob * 100).toFixed(1);
                const timeLabel = formatTimeString(entry.created_at);
                const textStr = entry.texto || entry.titulo || '';
                const isLong = textStr.length > 30;
                const expandBtnHtml = isLong ? `
                    <div class="flex justify-end mt-1.5">
                        <button type="button" class="btn-toggle-expand px-2.5 py-1 rounded-full border border-primary/25 bg-primary/10 hover:bg-primary/20 text-primary-fixed text-[11px] font-label-sm font-bold transition-all flex items-center gap-1 cursor-pointer active:scale-95 shadow-sm" title="${t('see_more')}">
                            <span>${t('see_more')}</span>
                            <span class="material-symbols-outlined text-xs pointer-events-none">expand_more</span>
                        </button>
                    </div>
                ` : '';

                const deleteBtnHtml = isLoggedInAsAdmin() ? `
                    <button type="button" class="btn-delete-entry px-2.5 py-1 rounded-lg border border-rose-500/40 bg-rose-500/15 hover:bg-rose-500/30 text-rose-300 text-[11px] font-label-sm font-bold transition-all flex items-center gap-1 cursor-pointer active:scale-95 shadow-sm" data-id="${entry.id}" title="${t('delete_btn')}">
                        <span class="material-symbols-outlined text-xs pointer-events-none" style="color: var(--led-error-text)">delete</span>
                        <span class="pointer-events-none font-bold" style="color: var(--led-error-text)">${t('delete_btn')}</span>
                    </button>
                ` : '';

                return `
                    <div class="glass-panel p-4 sm:p-5 rounded-xl border border-black/5 dark:border-white/5 hover:border-primary/30 transition-all group hover:-translate-y-1 duration-300 min-w-0 flex flex-col justify-between">
                        <div>
                            <div class="flex flex-wrap justify-between items-start gap-2 mb-3">
                                <span class="px-2.5 py-1 rounded-md text-[11px] font-label-sm border font-medium ${config.colorClass}">${escapeHtml(entry.categoria || 'Sin categoría')}</span>
                                <span class="text-on-surface-variant font-label-sm text-[11px] shrink-0">${timeLabel}</span>
                            </div>
                            <h4 class="font-body-md text-body-md text-on-surface font-medium group-hover:text-primary-fixed transition-colors line-clamp-1">${escapeHtml(entry.titulo || 'Sin título')}</h4>
                            <p class="history-card-body text-on-surface-variant text-xs mt-1 line-clamp-2 opacity-80 leading-relaxed transition-all">${escapeHtml(textStr)}</p>
                            ${expandBtnHtml}
                        </div>
                        <div class="mt-4 flex flex-wrap items-center justify-between opacity-90 pt-2.5 border-t border-black/5 dark:border-white/5 gap-2">
                            <div class="flex items-center gap-1.5">
                                <span class="font-label-sm text-[11px] text-on-surface-variant font-medium">${t('confidence_label')} ${probPct}%</span>
                            </div>
                            <div class="flex items-center gap-2">
                                ${deleteBtnHtml}
                                <button type="button" class="btn-view-entry-json px-2.5 py-1 rounded-lg border border-primary/30 bg-primary/15 hover:bg-primary/25 text-primary-fixed text-[11px] font-label-sm font-bold transition-all flex items-center gap-1 cursor-pointer active:scale-95 shadow-sm" data-id="${entry.id}" title="${t('btn_view_json')}">
                                    <span class="material-symbols-outlined text-xs pointer-events-none">code</span>
                                    <span class="pointer-events-none">${t('btn_view_json')}</span>
                                </button>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
        } else {
            historyGrid.innerHTML = `
                <div class="col-span-full py-8 text-center glass-panel rounded-xl">
                    <p class="text-on-surface-variant text-sm font-label-sm">${t('no_data')}</p>
                </div>
            `;
        }
    } catch (err) {
        console.warn('Error al cargar historial desde PostgreSQL:', err);
        historyGrid.innerHTML = `
            <div class="col-span-full py-8 text-center glass-panel rounded-xl border border-rose-500/30 dark:border-rose-500/20 bg-rose-500/10 dark:bg-rose-950/20">
                <span class="material-symbols-outlined text-4xl text-rose-600 dark:text-rose-400 mb-2">error</span>
                <p class="text-rose-700 dark:text-rose-200 text-sm font-semibold">${t('error_db')}</p>
                <p class="text-rose-600/80 dark:text-rose-400/80 text-xs mt-1 font-label-sm">${err.message || ''}</p>
            </div>
        `;
    }
}

// ── 6a. Actualizar conteo de categorías en el filtro ─────────────────────────

function updateCategoryFilterCounts(data) {
    const filterSelect = document.getElementById('filter-category');
    if (!filterSelect || !data) return;

    // Count entries per category
    const counts = {};
    data.forEach(entry => {
        const cat = entry.categoria || 'Sin categoría';
        counts[cat] = (counts[cat] || 0) + 1;
    });

    // Map of option values to their base label
    const categoryLabels = {
        'all': t('all_categories'),
        'Backend': 'Backend',
        'Frontend': 'Frontend',
        'Data Science': 'Data Science',
        'DevOps': 'DevOps',
        'Mobile': 'Mobile',
        'Bases de Datos': 'Bases de Datos',
        'Seguridad': 'Seguridad',
        'Cloud': 'Cloud'
    };

    // Update each option text with the count
    Array.from(filterSelect.options).forEach(option => {
        const value = option.value;
        const baseLabel = categoryLabels[value] || value;
        if (value === 'all') {
            option.textContent = `${baseLabel} (${data.length})`;
        } else {
            const count = counts[value] || 0;
            option.textContent = `${baseLabel} (${count})`;
        }
    });
}

// ── 6b. Historial Detallado (Subpágina) ──────────────────────────────────────

async function loadDetailedHistory(categoryFilter = 'all', searchQuery = '') {
    const listContainer = document.getElementById('detailed-history-list');
    if (!listContainer) return;

    try {
        listContainer.innerHTML = `
            <div class="py-8 text-center glass-panel rounded-xl">
                <span class="material-symbols-outlined text-4xl text-outline mb-2 animate-spin">refresh</span>
                <p class="text-on-surface-variant text-sm font-label-sm">${t('loading_detailed')}</p>
            </div>
        `;

        const res = await fetch(`${DS_API_URL}/predicciones?limit=100`);
        if (!res.ok) throw new Error('No se pudo consultar el historial');
        
        allHistoryData = await res.json();

        // Update category filter options with counts
        updateCategoryFilterCounts(allHistoryData);
        
        let filteredData = allHistoryData;
        if (categoryFilter !== 'all') {
            filteredData = allHistoryData.filter(entry => entry.categoria === categoryFilter);
        }

        if (searchQuery) {
            filteredData = filteredData.filter(entry => {
                const matchTitle = entry.titulo && entry.titulo.toLowerCase().includes(searchQuery);
                const matchKeywords = entry.keywords && entry.keywords.some(k => k.toLowerCase().includes(searchQuery));
                return matchTitle || matchKeywords;
            });
        }

        if (filteredData && filteredData.length > 0) {
            listContainer.innerHTML = filteredData.map(entry => {
                const config = CATEGORY_CONFIG[entry.categoria] || { icon: 'topic', colorClass: 'text-primary-fixed border-primary/30 bg-primary/10' };
                const prob = entry.probabilidad != null ? Number(entry.probabilidad) : 0;
                const probPct = Number(prob * 100).toFixed(1);
                
                let dateStr = t('date_not_available');
                if (entry.created_at) {
                    const d = parseDate(entry.created_at);
                    if (d) {
                        dateStr = d.toLocaleString([], { dateStyle: 'short', timeStyle: 'medium' });
                    }
                }

                const keywordsPills = (entry.keywords || []).map(k => {
                    const capitalized = k.charAt(0).toUpperCase() + k.slice(1);
                    return `
                        <span class="px-2.5 py-1 rounded bg-primary/10 border border-primary/20 text-primary-fixed text-[11px] font-mono">${escapeHtml(capitalized)}</span>
                    `;
                }).join(' ');

                const textStr = entry.texto || entry.titulo || '';
                const isLong = textStr.length > 30;
                const expandBtnHtml = isLong ? `
                    <div class="flex justify-end mt-1.5">
                        <button type="button" class="btn-toggle-expand px-2.5 py-1 rounded-full border border-primary/25 bg-primary/10 hover:bg-primary/20 text-primary-fixed text-[11px] font-label-sm font-bold transition-all flex items-center gap-1 cursor-pointer active:scale-95 shadow-sm" title="${t('see_more')}">
                            <span>${t('see_more')}</span>
                            <span class="material-symbols-outlined text-xs pointer-events-none">expand_more</span>
                        </button>
                    </div>
                ` : '';

                const deleteBtnHtml = isLoggedInAsAdmin() ? `
                    <button type="button" class="btn-delete-entry px-3 py-1.5 rounded-xl border border-rose-500/40 bg-rose-500/15 hover:bg-rose-500/30 text-rose-300 text-xs font-label-sm font-bold transition-all flex items-center gap-1.5 cursor-pointer active:scale-95 shadow-sm" data-id="${entry.id}" title="${t('delete_btn')}">
                        <span class="material-symbols-outlined text-sm pointer-events-none" style="color: var(--led-error-text)">delete</span>
                        <span class="pointer-events-none font-bold" style="color: var(--led-error-text)">${t('delete_btn')}</span>
                    </button>
                ` : '';

                return `
                    <div class="p-4 sm:p-5 rounded-2xl glass-panel border border-black/5 dark:border-white/5 hover:border-primary/20 transition-all flex flex-col md:flex-row md:items-start justify-between gap-4 md:gap-5 group hover:shadow-lg hover:shadow-primary/5 duration-300">
                        <div class="flex-1 min-w-0 space-y-2">
                            <div class="flex flex-wrap items-center gap-x-2.5 gap-y-1.5">
                                <span class="px-3 py-1 rounded-full text-xs font-label-sm border font-semibold ${config.colorClass} flex items-center gap-1.5 shadow-sm">
                                    <span class="material-symbols-outlined text-sm">${config.icon}</span>
                                    ${escapeHtml(entry.categoria || 'Sin categoría')}
                                </span>
                                <span class="text-xs font-mono text-outline opacity-60">ID #${entry.id}</span>
                                <span class="text-xs text-on-surface-variant font-medium flex items-center gap-1">
                                    <span class="material-symbols-outlined text-sm opacity-60">schedule</span>
                                    ${dateStr}
                                </span>
                            </div>
                            <h5 class="text-on-surface font-bold text-base sm:text-lg group-hover:text-primary-fixed transition-colors">${escapeHtml(entry.titulo)}</h5>
                            <p class="history-card-body text-on-surface-variant text-sm line-clamp-2 opacity-80 leading-relaxed transition-all">${escapeHtml(textStr || 'Sin descripción disponible')}</p>
                            ${expandBtnHtml}
                            <div class="flex flex-wrap gap-1.5 pt-1">
                                ${keywordsPills || `<span class="text-xs text-on-surface-variant italic opacity-60">${t('no_keywords')}</span>`}
                            </div>
                        </div>
                        <div class="flex flex-row md:flex-col items-center md:items-end justify-between gap-3 border-t md:border-t-0 md:border-l border-black/10 dark:border-white/10 pt-3 md:pt-0 md:pl-5 md:min-w-[140px] shrink-0">
                            <div class="text-left md:text-right">
                                <span class="block text-xs font-label-sm text-on-surface-variant uppercase tracking-wider font-semibold">Confianza</span>
                                <span class="text-xl sm:text-2xl font-black text-primary-fixed">${probPct}%</span>
                            </div>
                            <div class="flex items-center gap-2">
                                ${deleteBtnHtml}
                                <button type="button" class="btn-view-entry-json px-3 py-1.5 rounded-xl border border-primary/30 bg-primary/15 hover:bg-primary/25 text-primary-fixed text-xs font-label-sm font-bold transition-all flex items-center gap-1.5 cursor-pointer active:scale-95 shadow-sm" data-id="${entry.id}" title="${t('btn_view_json')}">
                                    <span class="material-symbols-outlined text-sm pointer-events-none">code</span>
                                    <span class="pointer-events-none">${t('btn_view_json')}</span>
                                </button>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
        } else {
            listContainer.innerHTML = `
                <div class="py-12 text-center glass-panel rounded-xl border border-black/5 dark:border-white/5">
                    <span class="material-symbols-outlined text-5xl text-outline mb-3 opacity-60">filter_list_off</span>
                    <p class="text-on-surface-variant text-base font-semibold">${t('no_results')}</p>
                </div>
            `;
        }
    } catch (err) {
        console.warn('Error al cargar historial detallado:', err);
        listContainer.innerHTML = `
            <div class="py-12 text-center glass-panel rounded-xl border border-rose-500/30 dark:border-rose-500/20 bg-rose-500/10 dark:bg-rose-950/20">
                <span class="material-symbols-outlined text-5xl text-rose-600 dark:text-rose-400 mb-3">error</span>
                <p class="text-rose-700 dark:text-rose-200 text-base font-semibold">${t('error_db')}</p>
                <p class="text-rose-600/80 dark:text-rose-400/80 text-xs mt-1 font-label-sm">${err.message}</p>
            </div>
        `;
    }
}

// ── 7. Modal JSON Crudo y Visualización de Consultas ─────────────────────────

function showHistoryEntryJsonInModal(id) {
    if (!id) return;
    const entry = allHistoryData.find(item => String(item.id) === String(id));
    if (!entry) {
        showToast(t('toast_not_found'), 'warning');
        return;
    }

    const localDate = parseDate(entry.created_at);
    const formattedCreatedAt = localDate ? getLocalISOString(localDate) : entry.created_at;

    const fullPayload = {
        entrada: { titulo: entry.titulo, texto: entry.texto },
        resultado: {
            id: entry.id,
            categoria: entry.categoria,
            probabilidad: entry.probabilidad,
            informaciones_adicionales: entry.keywords,
            created_at: formattedCreatedAt
        }
    };

    const modal = document.getElementById('json-modal');
    const jsonPre = document.getElementById('json-content');
    if (modal && jsonPre) {
        jsonPre.textContent = JSON.stringify(fullPayload, null, 2);
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }
}

function toggleJsonModal() {
    const modal = document.getElementById('json-modal');
    if (!modal) return;

    if (modal.classList.contains('hidden')) {
        const jsonPre = document.getElementById('json-content');
        if (lastJsonResponse) {
            const localDate = parseDate(lastJsonResponse.created_at);
            const formattedResult = {
                ...lastJsonResponse,
                created_at: localDate ? getLocalISOString(localDate) : getLocalISOString()
            };
            const fullPayload = {
                entrada: lastInput || { titulo: "", texto: "" },
                resultado: formattedResult
            };
            jsonPre.textContent = JSON.stringify(fullPayload, null, 2);
        } else {
            jsonPre.textContent = t('no_session_json');
        }
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    } else {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}

function copyJsonToClipboard() {
    const jsonPre = document.getElementById('json-content');
    const copyBtn = document.getElementById('btn-copy-json');
    const copyText = document.getElementById('copy-btn-text');
    if (!jsonPre || !jsonPre.textContent) return;

    navigator.clipboard.writeText(jsonPre.textContent).then(() => {
        if (copyBtn && copyText) {
            const originalText = copyText.textContent;
            const originalIcon = copyBtn.querySelector('.material-symbols-outlined').textContent;
            
            copyText.textContent = t('copied');
            copyBtn.querySelector('.material-symbols-outlined').textContent = 'check';
            copyBtn.classList.add('bg-emerald-500/20', 'border-emerald-500/40', 'text-emerald-300');
            
            showToast(t('toast_copied'), 'info');

            setTimeout(() => {
                copyText.textContent = t('copy_json');
                copyBtn.querySelector('.material-symbols-outlined').textContent = 'content_copy';
                copyBtn.classList.remove('bg-emerald-500/20', 'border-emerald-500/40', 'text-emerald-300');
            }, 2000);
        }
    }).catch(err => {
        console.error('Error al copiar JSON:', err);
        showToast(t('toast_copy_error'), 'error');
    });
}

// Global Backdrop Click & Escape Key listeners for JSON Modal, Expand & View buttons
document.addEventListener('click', (e) => {
    const modal = document.getElementById('json-modal');
    if (modal && !modal.classList.contains('hidden') && e.target === modal) {
        toggleJsonModal();
    }

    const copyBtn = e.target.closest('#btn-copy-json');
    if (copyBtn) {
        copyJsonToClipboard();
    }

    const expandBtn = e.target.closest('.btn-toggle-expand');
    if (expandBtn) {
        // Encontrar el párrafo .history-card-body que es previo al div contenedor del botón
        const parentDiv = expandBtn.parentElement;
        const p = parentDiv ? parentDiv.previousElementSibling : null;
        if (p && p.classList.contains('history-card-body')) {
            const isExpanded = p.classList.contains('line-clamp-none');
            if (isExpanded) {
                p.classList.remove('line-clamp-none');
                p.classList.add('line-clamp-2');
                expandBtn.innerHTML = `<span>Ver más</span><span class="material-symbols-outlined text-xs pointer-events-none">expand_more</span>`;
            } else {
                p.classList.remove('line-clamp-2');
                p.classList.add('line-clamp-none');
                expandBtn.innerHTML = `<span>Ver menos</span><span class="material-symbols-outlined text-xs pointer-events-none">expand_less</span>`;
            }
        }
    }

    const viewItemBtn = e.target.closest('.btn-view-entry-json');
    if (viewItemBtn) {
        const id = viewItemBtn.getAttribute('data-id');
        showHistoryEntryJsonInModal(id);
    }

    const deleteBtn = e.target.closest('.btn-delete-entry');
    if (deleteBtn) {
        const id = deleteBtn.getAttribute('data-id');
        deletePrediction(id);
    }
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        const modal = document.getElementById('json-modal');
        if (modal && !modal.classList.contains('hidden')) {
            toggleJsonModal();
        }
    }
});

// ── Helpers ─────────────────────────────────────────────────────────────────

function getLocalISOString(date = new Date()) {
    if (!date || isNaN(date.getTime())) date = new Date();
    const tzo = -date.getTimezoneOffset();
    const dif = tzo >= 0 ? '+' : '-';
    const pad = (num) => String(Math.floor(Math.abs(num))).padStart(2, '0');
    return date.getFullYear() +
        '-' + pad(date.getMonth() + 1) +
        '-' + pad(date.getDate()) +
        'T' + pad(date.getHours()) +
        ':' + pad(date.getMinutes()) +
        ':' + pad(date.getSeconds()) +
        dif + pad(tzo / 60) +
        ':' + pad(tzo % 60);
}

function parseDate(isoStr) {
    if (!isoStr) return null;
    let str = String(isoStr).trim();
    if (!str) return null;

    if (str.includes(' ') && !str.includes('T')) {
        str = str.replace(' ', 'T');
    }

    str = str.replace(/(\.\d{3})\d+/, '$1');

    const hasTimezone = /[Zz]$|[+-]\d{2}(:?\d{2})?$/.test(str);
    if (!hasTimezone) {
        str += 'Z';
    }

    const d = new Date(str);
    return isNaN(d.getTime()) ? null : d;
}

function formatTimeString(isoStr) {
    const d = parseDate(isoStr);
    if (!d) return 'Reciente';
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function setLoadingState(isLoading) {
    const btn = document.getElementById('btn-classify');
    if (!btn) return;

    if (isLoading) {
        btn.disabled = true;
        btn.innerHTML = `
            <div class="absolute inset-0 bg-gradient-to-r from-inverse-primary to-primary-container opacity-80"></div>
            <div class="relative flex items-center justify-center gap-2">
                <span class="material-symbols-outlined text-lg animate-spin">refresh</span>
                Analizando...
            </div>
        `;
    } else {
        btn.disabled = false;
        btn.innerHTML = `
            <div class="absolute inset-0 bg-gradient-to-r from-inverse-primary to-primary-container group-hover:scale-105 transition-transform duration-300"></div>
            <div class="relative flex items-center justify-center gap-2.5">
                <span class="material-symbols-outlined text-lg">science</span>
                <span>Clasificar con TechMind</span>
            </div>
        `;
    }
}

function showToast(message, type = 'info', duration = 2000) {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    const isError = type === 'error';
    const bgClass = isError ? 'bg-rose-100 dark:bg-rose-950/90 border-rose-500/50 text-rose-950 dark:text-rose-300 font-bold' :
        type === 'warning' ? 'bg-amber-100 dark:bg-amber-950/90 border-amber-500/50 text-amber-950 dark:text-amber-200 font-bold' :
        type === 'info' ? 'bg-purple-100 dark:bg-purple-950/90 border-purple-500/50 text-purple-950 dark:text-purple-200 font-bold' :
        'bg-emerald-100 dark:bg-emerald-950/90 border-emerald-600/50 text-emerald-950 dark:text-emerald-200 font-bold';

    toast.className = `glass-panel px-4 py-3 rounded-xl border ${bgClass} font-label-sm text-sm shadow-xl backdrop-blur-xl transition-all duration-300 transform translate-y-2 opacity-0 flex items-center gap-2 break-words`;
    toast.innerHTML = `<span class="min-w-0">${message}</span>`;

    container.appendChild(toast);

    setTimeout(() => {
        toast.classList.remove('translate-y-2', 'opacity-0');
    }, 10);

    setTimeout(() => {
        toast.classList.add('opacity-0', '-translate-y-2');
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/[&<>"']/g, m => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m]));
}

// ── 6. Dashboard de Analytics & Gráficos (Chart.js) ──────────────────────────

let chartCategoriesInstance = null;
let chartHourlyInstance = null;
let chartKeywordsInstance = null;

async function loadAnalyticsDashboard() {
    try {
        const tzOffset = -new Date().getTimezoneOffset();
        const res = await fetch(`${DS_API_URL}/analytics?t=${Date.now()}&tz_offset=${tzOffset}`);
        if (!res.ok) return;
        const data = await res.json();

        // 1. KPIs
        const kpiTotal = document.getElementById('kpi-total-queries');
        const kpiTop = document.getElementById('kpi-top-category');
        const kpiAvg = document.getElementById('kpi-avg-confidence');

        if (kpiTotal) kpiTotal.textContent = data.total_count || 0;
        if (kpiTop) kpiTop.textContent = data.top_categoria || 'N/A';
        if (kpiAvg) kpiAvg.textContent = `${Number(data.avg_prob || 0).toFixed(1)}%`;

        if (typeof Chart === 'undefined') return;

        const isDark = document.documentElement.classList.contains('dark');
        const textColor = isDark ? '#cbc3d7' : '#231f18';
        const gridColor = isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.08)';
        const sliceBorderColor = isDark ? '#171f33' : '#e8e2d5';

        // 2. Chart 1: Doughnut (Distribución por Categoría)
        const ctxCat = document.getElementById('chart-categories');
        if (ctxCat) {
            const catLabels = Object.keys(data.categorias || {});
            const catValues = Object.values(data.categorias || {});
            const colors = [
                '#a078ff', '#4edea3', '#38bdf8', '#fbbf24',
                '#f43f5e', '#fb923c', '#818cf8', '#2dd4bf'
            ];

            if (chartCategoriesInstance) chartCategoriesInstance.destroy();

            chartCategoriesInstance = new Chart(ctxCat, {
                type: 'doughnut',
                data: {
                    labels: catLabels,
                    datasets: [{
                        data: catValues,
                        backgroundColor: colors.slice(0, catLabels.length),
                        borderWidth: 2,
                        borderColor: sliceBorderColor
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                color: textColor,
                                font: { family: 'Inter', size: window.innerWidth < 640 ? 10 : 11 },
                                usePointStyle: true,
                                pointStyle: 'circle',
                                padding: window.innerWidth < 640 ? 8 : 12
                            }
                        }
                    }
                }
            });
        }

        // 3. Chart 2: Area Line (Actividad por Hora del Día)
        const ctxHour = document.getElementById('chart-hourly');
        if (ctxHour) {
            const hourLabels = Array.from({ length: 24 }, (_, i) => `${String(i).padStart(2, '0')}:00`);
            const hourValues = data.horas || Array(24).fill(0);

            if (chartHourlyInstance) chartHourlyInstance.destroy();

            chartHourlyInstance = new Chart(ctxHour, {
                type: 'line',
                data: {
                    labels: hourLabels,
                    datasets: [{
                        label: t('queries_label'),
                        data: hourValues,
                        borderColor: '#38bdf8',
                        backgroundColor: 'rgba(56, 189, 248, 0.15)',
                        fill: true,
                        tension: 0.4,
                        pointRadius: 3,
                        pointBackgroundColor: '#38bdf8'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { ticks: { color: textColor, font: { size: 10 } }, grid: { color: gridColor } },
                        y: { ticks: { color: textColor, precision: 0 }, grid: { color: gridColor }, beginAtZero: true }
                    },
                    plugins: {
                        legend: { display: false }
                    }
                }
            });
        }

        // 4. Keywords Tag Cloud Container
        const kwContainer = document.getElementById('keywords-cloud-container');
        if (kwContainer) {
            const kwList = data.top_keywords || [];
            if (kwList.length === 0) {
                kwContainer.innerHTML = `<span class="font-label-sm text-xs text-on-surface-variant opacity-60">${t('no_keywords_data')}</span>`;
            } else {
                const maxCount = Math.max(...kwList.map(k => k.count), 1);
                kwContainer.innerHTML = kwList.map(item => {
                    const ratio = item.count / maxCount;
                    const badgeClass = ratio > 0.7
                        ? 'bg-purple-500/20 text-purple-700 dark:text-purple-300 border-purple-500/40 text-sm py-1.5 px-3.5 font-bold shadow-md'
                        : ratio > 0.4
                        ? 'bg-cyan-500/15 text-cyan-700 dark:text-cyan-300 border-cyan-500/30 text-xs py-1 px-3 font-semibold'
                        : 'bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border-emerald-500/20 text-xs py-1 px-2.5 font-medium';

                    return `
                        <div class="inline-flex items-center gap-1.5 rounded-xl border ${badgeClass} transition-all hover:scale-105 cursor-default">
                            <span class="capitalize">#${escapeHtml(item.word)}</span>
                            <span class="text-[10px] opacity-75 bg-surface-container-high px-1.5 py-0.5 rounded-md font-mono">${item.count}</span>
                        </div>
                    `;
                }).join('');
            }
        }

    } catch (e) {
        console.error('Error cargando analytics:', e);
    }
}

// ── Internacionalización: helpers globales ────────────────────────────────────

function updateThemeToggleUI() {
    const icon = document.getElementById('theme-toggle-icon');
    const text = document.getElementById('theme-toggle-text');
    const isDark = document.documentElement.classList.contains('dark');
    if (icon) icon.textContent = isDark ? 'light_mode' : 'dark_mode';
    if (text) text.textContent = isDark ? t('theme_light') : t('theme_dark');
}

function applyTranslations() {
    document.documentElement.lang = currentLang;

    // Actualizar todos los elementos estáticos con data-i18n / data-i18n-placeholder
    document.querySelectorAll('[data-i18n]').forEach(el => {
        el.textContent = t(el.dataset.i18n);
    });
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        el.placeholder = t(el.dataset.i18nPlaceholder);
    });

    // Indicador del botón de idioma (muestra el idioma al que se puede cambiar)
    const langText = document.getElementById('lang-toggle-text');
    if (langText) langText.textContent = currentLang === 'es' ? 'EN' : 'ES';

    // Elementos cuyo texto es gestionado dinámicamente
    updateThemeToggleUI();
    updateAdminUIState();

    // Actualizar el header según la vista activa
    const headerTitle = document.getElementById('main-header-title');
    const headerSubtitle = document.getElementById('main-header-subtitle');
    const viewHeaders = {
        classifier: { title: t('header_classifier_title'), subtitle: t('header_classifier_subtitle') },
        history:    { title: t('header_history_title'),    subtitle: t('header_history_subtitle') },
        analytics:  { title: t('header_analytics_title'),  subtitle: t('header_analytics_subtitle') }
    };
    const h = viewHeaders[currentView] || viewHeaders.classifier;
    if (headerTitle) headerTitle.textContent = h.title;
    if (headerSubtitle) headerSubtitle.textContent = h.subtitle;

    // Restaurar estado inicial de la tarjeta de resultados si no hay clasificación activa
    if (!lastJsonResponse) {
        const categoryBadge = document.getElementById('category-badge-container');
        if (categoryBadge) {
            categoryBadge.innerHTML = `
                <div class="inline-flex max-w-full items-center gap-3 px-4 sm:px-6 py-2.5 rounded-full border text-base sm:text-lg font-bold bg-primary/10 border-primary/30 text-primary-fixed">
                    <span>${t('waiting')}</span>
                </div>
            `;
        }
        const keywordsList = document.getElementById('keywords-list');
        if (keywordsList) {
            keywordsList.innerHTML = `<span class="text-on-surface-variant text-sm sm:text-base italic opacity-60">${t('keywords_placeholder')}</span>`;
        }
    }

    // Actualizar el texto del botón de copiar JSON
    const copyBtnText = document.getElementById('copy-btn-text');
    if (copyBtnText) copyBtnText.textContent = t('copy_json');
}
