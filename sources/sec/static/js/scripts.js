document.addEventListener('DOMContentLoaded', function() {
    let salonADeshabilitar = null;
    const salonContainer = document.querySelector('[data-salon-disponible]');
    if (salonContainer) {
        const salonId = salonContainer.getAttribute('data-salon-disponible');
        const disponible = salonContainer.textContent.trim() === "Si";
        const botonesContainer = document.querySelector(`[data-salon-botones="${salonId}"]`);
        const nombre = botonesContainer.querySelector('.cambiar-estado-salon')?.getAttribute('data-nombre');
        
        actualizarInterfazSalon(salonId, nombre, disponible);
    }
    function actualizarInterfazSalon(salonId, nombre, disponible) {
        // Actualizar el indicador de disponibilidad
        const disponibleIndicador = document.querySelector(`[data-salon-disponible="${salonId}"]`);
        if (disponibleIndicador) {
            disponibleIndicador.textContent = disponible ? "Si" : "No";
        }
        // Actualizar los botones
        const botonesContainer = document.querySelector(`[data-salon-botones="${salonId}"]`);
        if (botonesContainer) {
            if (disponible) {
              const urlModificar = botonesContainer.getAttribute('data-url-modificar');
                botonesContainer.innerHTML = `
                    <a href="${urlModificar}" class="btn botones">Editar</a>
                    <button class="btn btn-danger cambiar-estado-salon" 
                            data-id="${salonId}" 
                            data-nombre="${nombre}" 

                            data-disponible="true" 
                            data-bs-toggle="modal" 
                            data-bs-target="#deshabilitarModalSalon">
                        Deshabilitar
                    </button>
                `;
                document.querySelector('.listados-container').style.display = 'block'; // Cambia el selector según tu estructura
            } else {
                botonesContainer.innerHTML = `
                    <button class="btn btn-success cambiar-estado-salon" 
                            data-id="${salonId}" 
                            data-disponible="false">
                        Habilitar
                    </button>
                `;
                document.querySelector('.listados-container').style.display = 'none'; // Cambia el selector según tu estructura
            }
        }
    }
    function cambiarEstadoSalon(button) {
        const salonId = button.getAttribute('data-id');
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const cambiarEstadoUrl = "{% url 'cambiarEstadoSalon' %}";
        fetch(cambiarEstadoUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: `id=${salonId}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            actualizarInterfazSalon(data.salon_id, data.nombre, data.nuevo_estado);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Hubo un error al cambiar el estado del salón.');
        });
    }
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('cambiar-estado-salon')) {
            const button = e.target;
            const esDeshabilitacion = button.getAttribute('data-disponible') === 'true';
            if (esDeshabilitacion) {
                salonADeshabilitar = button;
                const nombreSalon = button.getAttribute('data-nombre');
                document.getElementById('salonNombre').textContent = nombreSalon;
                return;
            }
            cambiarEstadoSalon(button);
        }
    });
    // Manejador para el botón de confirmar deshabilitación
    const confirmarBtn = document.getElementById('confirmarDeshabilitarSalon');
    if (confirmarBtn) {
        confirmarBtn.addEventListener('click', function() {
            if (salonADeshabilitar) {
                cambiarEstadoSalon(salonADeshabilitar);
                const modal = bootstrap.Modal.getInstance(document.getElementById('deshabilitarModalSalon'));
                if (modal) {
                    modal.hide();
                }
                salonADeshabilitar = null;
            }
        });
    }
  });


    // Esperar a que el DataTable esté inicializado desde dataTable.js
    document.addEventListener('DOMContentLoaded', function() {
        const checkbox = document.getElementById('serviciosNoDisponibles');
        const tabla = document.querySelector('.dataTable');
        let dataTableInstance;

        // Función para obtener la instancia existente de DataTable
        function obtenerDataTable() {
            if ($.fn.DataTable.isDataTable(tabla)) {
                dataTableInstance = $(tabla).DataTable();
                return true;
            }
            return false;
        }
        // Función que intenta obtener DataTable cada 100ms
        function esperarDataTable(callback, intentos = 0) {
            if (obtenerDataTable()) {
                callback();
            } else if (intentos < 50) { // Máximo 5 segundos de espera
                setTimeout(() => esperarDataTable(callback, intentos + 1), 100);
            } else {
                console.error('No se pudo obtener la instancia de DataTable');
            }
        }
        function actualizarTabla(servicios) {
            if (!dataTableInstance) {
                console.error('DataTable no está inicializado');
                return;
            }
            // Destruir los event listeners anteriores para evitar duplicados
            $(tabla).find('.cambiar-estado, .editar-servicio').off();
            // Limpiar la tabla
            dataTableInstance.clear();
            // Preparar los datos para DataTable
            const nuevosDatos = servicios.map(servicio => [
                servicio.nombre,
                servicio.descripcion,
                servicio.precio,
                servicio.obligatorio ? 'Si' : 'No',
                servicio.disponible ? 'Si' : 'No',
                `<div class="btn-group" role="group">
                    ${servicio.disponible ? 
                        `<button class="btn btn-success editar-servicio me-3" data-id="${servicio.id}">Editar</button>
                        <button class="btn btn-danger cambiar-estado" data-id="${servicio.id}" data-disponible="true" data-bs-toggle="modal" data-bs-target="#deshabilitarModal">Deshabilitar</button>` :
                        `<button class="btn btn-success cambiar-estado" data-id="${servicio.id}" data-disponible="false">Habilitar</button>`
                    }
                </div>`
            ]);
            // Agregar los nuevos datos y redibujar
            dataTableInstance.rows.add(nuevosDatos).draw();
            // Actualizar los atributos de las filas
            dataTableInstance.rows().every(function(rowIdx) {
                const servicio = servicios[rowIdx];
                const node = this.node();
                node.id = `servicio-row-${servicio.id}`;
                node.className = 'servicio-row';
                node.setAttribute('data-disponible', servicio.disponible);
            });
        }
        function cargarServicios() {
            const url = new URL(window.location.href);
            url.searchParams.set('mostrar_todos', checkbox.checked);
            
            fetch(url.toString(), {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                actualizarTabla(data.servicios);
            })
            .catch(error => {
                console.error('Error al cargar los servicios:', error);
                alert('Error al cargar los servicios. Por favor, intente nuevamente.');
            });
        }
        function cambiarEstadoServicio(button) {
            const servicioId = button.data('id');
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            $.ajax({
              url: '{% url "cambiarEstadoServicio" %}',  // Ajusta esta URL según tu configuración
                type: 'POST',
                data: {
                    'id': servicioId,
                    'csrfmiddlewaretoken': csrfToken
                },
                success: function(response) {
                    cargarServicios();
                },
                error: function(xhr, status, error) {
                    console.error('Error en la solicitud AJAX:', error);
                    alert('Hubo un error al cambiar el estado del servicio.');
                }
            });
        }
        // Inicializar todo después de que DataTable esté listo
        esperarDataTable(() => {
            // Establecer estado inicial del checkbox
            checkbox.checked = false;
            // Configurar el event listener del checkbox
            checkbox.addEventListener('change', cargarServicios);
            // Configurar los event listeners para los botones usando delegación de eventos
            $(document).on('click', '.cambiar-estado', function(e) {
                const button = $(this);
                const esDeshabilitacion = button.data('disponible') === true;
                if (esDeshabilitacion) {
                    window.servicioADeshabilitar = button;
                    const nombreServicio = button.closest('tr').find('td:first').text().trim();
                    $('#servicioNombre').text(nombreServicio);
                    return;
                }
                cambiarEstadoServicio(button);
            });
            // Configurar el manejador para el botón de confirmar deshabilitación
            $('#confirmarDeshabilitar').on('click', function() {
                if (window.servicioADeshabilitar) {
                    cambiarEstadoServicio(window.servicioADeshabilitar);
                    $('#deshabilitarModal').modal('hide');
                    window.servicioADeshabilitar = null;
                }
            });
            // Cargar los datos iniciales
            cargarServicios();
        });
    });

