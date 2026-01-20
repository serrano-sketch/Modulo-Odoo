TAREA 13 – EXTENSIÓN DE MÓDULOS
Alumno: [Tu Nombre]

He realizado la extensión del módulo de empleados (hr.employee) creando el módulo 'hr_employee_extended'.

Funcionamiento:
He añadido dos campos nuevos en la vista de formulario de Empleados. Para que sean más visibles y accesibles, los he colocado en la sección de "Información General", junto al teléfono y otros datos de contacto, en lugar de en pestañas secundarias.
- NSS (Número de Seguridad Social)
- DNI (Documento Nacional de Identidad)

Validaciones:
He programado validaciones en Python (usando @api.constrains) para asegurar que los datos son correctos y que no se queden vacíos:
1. NSS: Comprueba que tenga 12 dígitos. También verifica que los dos últimos dígitos de control coincidan con el cálculo del resto (algoritmo estándar).
2. DNI: Comprueba que tenga 9 caracteres (8 números y 1 letra). Calcula la letra correcta y comprueba que coincida.
3. Ambos campos son obligatorios. Si intentas guardar la ficha sin rellenarlos, no te deja.

Instalación:
Basta con instalar el módulo 'HR Employee Extension'. No hace falta configuración extra.
