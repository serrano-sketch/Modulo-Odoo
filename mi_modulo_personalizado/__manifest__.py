# -*- coding: utf-8 -*-
{
    'name': 'Gestion de Equipos',
    'version': '1.1',
    'category': 'Administration/IT Assets',
    'summary': 'Control de ordenadores, componentes, incidencias y usuarios.',
    'description': """
        Registro de ordenadores de la empresa, sus componentes, incidencias,
        usuario asignado, tags de sistema operativo y control de seguridad.
    """,
    'author': 'Tu Nombre',
    'depends': ['base'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/component_views.xml',
        'views/computer_views.xml',
        'views/os_tag_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
