TAREA 13 – EXTENSIÓN DE MÓDULOS
Alumno: [Tu Nombre]

He realizado la extensión del módulo de empleados (hr.employee) creando el módulo 'hr_employee_extended'.

Funcionamiento:
He añadido dos campos nuevos en la vista de formulario de Empleados, justo debajo del campo de identificación:
- NSS (Número de Seguridad Social)
- DNI (Documento Nacional de Identidad)

Validaciones:
He programado validaciones en Python (usando @api.constrains) para asegurar que los datos son correctos:
1. NSS: Comprueba que tenga 12 dígitos. También verifica que los dos últimos dígitos de control coincidan con el cálculo del resto de los 10 primeros entre 97.
2. DNI: Comprueba que tenga 9 caracteres (8 números y 1 letra). Calcula la letra correspondiente a los números y si no coincide, da error.
3. Ambos campos son obligatorios. Si intentas guardar la ficha sin rellenarlos, no te deja.

Instalación:
Basta con instalar el módulo 'HR Employee Extension'. No hace falta configuración extra.
