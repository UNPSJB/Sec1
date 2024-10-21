$(document).ready(function() {
    // Busca todos los elementos con la clase dataTable
    $('.dataTable').DataTable({
        language: {
            search: "Buscar",
            emptyTable: "No hay datos disponibles en la tabla",
            lengthMenu: "Mostrar _MENU_ registros por página", 
            info: "Mostrando  _END_ registros de un total de _TOTAL_ registros",
            zeroRecords: "No se encontraron resultados",
            infoEmpty: "Mostrando 0 a 0 de 0 registros",
        }
    });
  });
