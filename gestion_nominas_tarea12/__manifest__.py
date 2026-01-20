# -*- coding: utf-8 -*-
# Mantengo la codificación en UTF-8 porque en este manifiesto también uso tildes.
{
    'name': 'Gestión Nóminas Tarea 12',  # Este es el nombre que verá el usuario en la lista de apps.
    'version': '18.0.1.0.0',  # Aquí reflejo la versión que me inventé para esta entrega.
    'summary': 'Tarea 12 DAM - Nóminas, bonificaciones, deducciones e IRPF',  # Resumen corto para el listado.
    'description': (  # Con esta clave doy un texto más largo que explique el módulo.
        "Implementación guiada por la TAREA 12 (2ºDAM – SGE). Permite registrar nóminas con\n"
        "bonificaciones/deducciones, controlar el IRPF y generar la declaración anual respetando\n"
        "el límite de 14 nóminas por año y empleado.\n"
    ),
    'author': 'Joaquin Carrasco',  # Firmo con mi nombre para dejar claro que yo lo hice.
    'website': 'https://github.com/JoaquinCarrasco',  # Apunto a mi GitHub personal por si miran quién soy.
    'category': 'Human Resources/Payroll',  # Clasifico el módulo dentro del menú de Recursos Humanos.
    'depends': ['base', 'hr'],  # Declaro que necesito los módulos base y hr para que todo funcione.
    'data': [  # En esta lista indico los archivos de datos y vistas que debe cargar Odoo.
        'security/ir.model.access.xml',  # Primero cargo los permisos para no tener problemas de acceso.
        'data/sequence_data.xml',  # Luego activo las secuencias para nóminas y declaraciones.
        'views/tax_return_views.xml',  # Registro las vistas de declaraciones para que se vean en el cliente.
        'views/payroll_views.xml',  # Añado las vistas de nóminas tanto en árbol como en formulario.
        'views/menu_views.xml',  # Finalmente doy de alta el menú que enlaza con mis acciones.
    ],
    'installable': True,  # Marco que se puede instalar porque está listo para usarse.
    'application': True,  # Indico que es una app completa para que salga en el lanzador principal.
    'license': 'LGPL-3',  # Declaro la licencia libre que estoy usando.
}  # Cierro el diccionario del manifiesto.
