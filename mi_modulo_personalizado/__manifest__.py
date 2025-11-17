# -*- coding: utf-8 -*-
{
    'name': 'Mi Módulo Personalizado',
    'version': '1.0',
    'category': 'Administration/Records',
    'summary': 'Módulo personalizado para gestión de registros',
    'description': """
        Módulo personalizado creado para la tarea 8.
        Incluye gestión de seguridad con diferentes niveles de acceso.
    """,
    'author': 'Serra',
    'depends': ['base'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/test_model_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
