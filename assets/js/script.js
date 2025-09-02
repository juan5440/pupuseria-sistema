let carrito = [];
let historialVentas = [];

// Modo oscuro
const themeToggle = document.getElementById('themeToggle');
const body = document.body;

if (localStorage.getItem('darkMode') === 'true') {
    body.classList.add('dark-mode');
    themeToggle.textContent = 'Modo Claro';
}

themeToggle.addEventListener('click', () => {
    body.classList.toggle('dark-mode');
    const isDark = body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDark);
    themeToggle.textContent = isDark ? 'Modo Claro' : 'Modo Oscuro';
});

function agregarAlCarrito(nombre, precio) {
    const producto = carrito.find(p => p.nombre === nombre);
    if (producto) {
        producto.cantidad++;
    } else {
        carrito.push({ nombre, precio, cantidad: 1 });
    }
    actualizarCarrito();
}

function eliminarDelCarrito(index) {
    carrito.splice(index, 1);
    actualizarCarrito();
}

function actualizarCarrito() {
    const tbody = document.getElementById('carritoBody');
    tbody.innerHTML = '';

    let total = 0;
    carrito.forEach((p, i) => {
        const subtotal = p.precio * p.cantidad;
        total += subtotal;
        const tr = document.createElement('tr');
        tr.innerHTML = `
      <td>${p.nombre}</td>
      <td>$${p.precio.toFixed(2)}</td>
      <td>${p.cantidad}</td>
      <td>$${subtotal.toFixed(2)}</td>
      <td><button class="remove" onclick="eliminarDelCarrito(${i})">X</button></td>
    `;
        tbody.appendChild(tr);
    });

    document.getElementById('totalCarrito').textContent = `$${total.toFixed(2)}`;
    calcularCambio();
}

document.getElementById('pago').addEventListener('input', calcularCambio);

function calcularCambio() {
    const total = parseFloat(document.getElementById('totalCarrito').textContent.replace('$', '')) || 0;
    const pago = parseFloat(document.getElementById('pago').value) || 0;
    const resultado = document.getElementById('resultado');

    if (pago === 0) {
        resultado.textContent = '';
        return;
    }

    if (pago < total) {
        resultado.textContent = `Falta: $${(total - pago).toFixed(2)}`;
        resultado.className = 'error';
    } else {
        const cambio = pago - total;
        resultado.textContent = `Cambio: $${cambio.toFixed(2)}`;
        resultado.className = 'cambio';
    }
}

function generarTicket() {
    if (carrito.length === 0) {
        alert("El carrito está vacío.");
        return;
    }

    const total = parseFloat(document.getElementById('totalCarrito').textContent.replace('$', ''));
    const pago = parseFloat(document.getElementById('pago').value) || 0;
    const cambio = Math.max(0, pago - total);

    const venta = {
        total: total,
        pago: pago,
        cambio: cambio,
        detalle: carrito
    };

    fetch('backend/agregar_venta.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(venta)
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success') {
                carrito = [];
                actualizarCarrito();
                document.getElementById('pago').value = '';
                cargarHistorial(); // Refrescar
                generarTicketVisual(venta);
                document.getElementById('ticketModal').style.display = 'flex';

                setTimeout(cerrarTicket, 5000);
                document.querySelector('.historial').scrollIntoView({ behavior: 'smooth' });
            }
        });
}

function generarTicketVisual(venta) {
    let detalle = `================================\n`;
    detalle += `       PUPUSERÍA "EL SABOR DE CASA"\n`;
    detalle += `================================\n`;
    detalle += `Fecha: ${new Date().toLocaleString()}\n`;
    detalle += `--------------------------------\n`;

    venta.detalle.forEach(p => {
        const subtotal = parseFloat(p.precio) * parseInt(p.cantidad);
        detalle += `${p.nombre.padEnd(20)} x${p.cantidad}\n`;
        detalle += `                      $${subtotal.toFixed(2)}\n`;
    });

    // ✅ Convertir strings a números con parseFloat()
    detalle += `--------------------------------\n`;
    detalle += `TOTAL:                $${parseFloat(venta.total).toFixed(2)}\n`;
    detalle += `PAGO:                 $${parseFloat(venta.pago).toFixed(2)}\n`;
    detalle += `CAMBIO:               $${parseFloat(venta.cambio).toFixed(2)}\n`;
    detalle += `================================\n`;
    detalle += `¡Gracias por su compra!\n`;

    document.getElementById('ticketTexto').textContent = detalle;
}

function verTicketHistorial(id) {
    fetch(`backend/obtener_detalle.php?id=${id}`)
        .then(res => res.json())
        .then(venta => {
            generarTicketVisual({
                detalle: venta.productos,
                total: venta.total,
                pago: venta.pago,
                cambio: venta.cambio
            });
            document.getElementById('ticketModal').style.display = 'flex';
        });
}

function editarVenta(id) {
    const nuevoPagoStr = prompt("Ingrese nuevo pago:");
    if (!nuevoPagoStr) return;

    const nuevoPago = parseFloat(nuevoPagoStr);
    if (isNaN(nuevoPago) || nuevoPago < 0) {
        alert("Pago inválido.");
        return;
    }

    const venta = historialVentas.find(v => v.id == id);
    const total = venta ? venta.total : 0;

    fetch('backend/editar_venta.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id, pago: nuevoPago, cambio: nuevoCambio })
        })
        .then(res => res.json())
        .then(() => {
            alert("Venta actualizada.");
            cargarHistorial();
        });
}

function eliminarVenta(id) {
    if (confirm("¿Eliminar esta venta?")) {
        fetch('backend/eliminar_venta.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `id=${id}`
            })
            .then(res => res.json())
            .then(() => {
                alert("Venta eliminada.");
                cargarHistorial();
            });
    }
}

function cargarHistorial() {
    fetch('backend/obtener_ventas.php')
        .then(res => res.json())
        .then(ventas => {
            historialVentas = ventas;
            const tbody = document.getElementById('historialBody');
            tbody.innerHTML = '';

            let totalVentas = 0;

            ventas.forEach((venta, index) => {
                const tr = document.createElement('tr');
                totalVentas += parseFloat(venta.total);

                tr.innerHTML = `
        <td>${index + 1}</td>
        <td>${venta.fecha}</td>
        <td>${venta.productos}</td>
        <td>$${venta.total}</td>
        <td>$${venta.pago}</td>
        <td>$${venta.cambio}</td>
        <td>
          <button onclick="verTicketHistorial(${venta.id})"><i class="fas fa-ticket-alt"></i> Ticket</button>
          <button onclick="editarVenta(${venta.id})" style="background:#f39c12;"><i class="fas fa-edit"></i> Editar</button>
          <button onclick="eliminarVenta(${venta.id})" style="background:#e74c3c;"><i class="fas fa-trash"></i> Eliminar</button>
        </td>
      `;
                tbody.appendChild(tr);
            });

            document.getElementById('totalVentas').textContent = `$${totalVentas.toFixed(2)}`;

            if ($.fn.DataTable.isDataTable('#historialTable')) {
                $('#historialTable').DataTable().destroy();
            }

            $('#historialTable').DataTable({
                dom: 'Bfrtip',
                buttons: ['excelHtml5', 'csvHtml5', 'print'],
                language: { url: "https://cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json" },
                pageLength: 10,
                order: [
                    [1, 'desc']
                ]
            });
        });
}

function imprimirTicket() {
    const printWindow = window.open('', '', 'height=600,width=400');
    printWindow.document.write('<pre>');
    printWindow.document.write(document.getElementById('ticketTexto').textContent);
    printWindow.document.write('</pre>');
    printWindow.document.close();
    printWindow.print();
}

function cerrarTicket() {
    document.getElementById('ticketModal').style.display = 'none';
}

window.onclick = function(e) {
    if (e.target === document.getElementById('ticketModal')) cerrarTicket();
};

// Cargar historial al inicio
cargarHistorial();

// Cargar menú de productos
let ultimaCarga = null;

function cargarMenu() {
    fetch('backend/obtener_productos.php')
        .then(res => res.json())
        .then(productos => {
            const contenedor = document.getElementById('menuProductos');

            // Detectar si cambió
            const productosStr = JSON.stringify(productos);
            if (ultimaCarga && ultimaCarga !== productosStr) {
                // Mostrar notificación
                const notif = document.createElement('div');
                notif.textContent = '✅ Menú actualizado';
                notif.style.cssText = `
          position: fixed;
          top: 20px;
          right: 20px;
          background: #27ae60;
          color: white;
          padding: 10px 15px;
          border-radius: 5px;
          font-size: 14px;
          z-index: 1000;
          transition: opacity 2s;
        `;
                document.body.appendChild(notif);
                setTimeout(() => { notif.style.opacity = 0; }, 2000);
                setTimeout(() => { notif.remove(); }, 3000);
            }
            ultimaCarga = productosStr;

            // Renderizar productos
            contenedor.innerHTML = '';
            productos.forEach(prod => {
                const div = document.createElement('div');
                div.className = 'producto';
                div.innerHTML = `
          <h3>${prod.nombre}</h3>
          <p>$${parseFloat(prod.precio).toFixed(2)}</p>
          <button onclick="agregarAlCarrito('${escapeHtml(prod.nombre)}', ${prod.precio})">Agregar</button>
        `;
                contenedor.appendChild(div);
            });
        })
        .catch(err => {
            console.error("Error al cargar productos:", err);
        });
}

// Función simple para evitar XSS al inyectar nombres
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

setInterval(cargarMenu, 10000); // Cada 10 segundos