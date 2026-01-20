# -*- coding: utf-8 -*-
{
    'name': 'Gestión Nóminas Tarea 12',
    'version': '18.0.1.0.0',
    'summary': 'Tarea 12 DAM - Nóminas, bonificaciones, deducciones e IRPF',
    'description': """
Implementación guiada por la TAREA 12 (2ºDAM – SGE). Permite registrar nóminas con
bonificaciones/deducciones, controlar el IRPF y generar la declaración anual respetando
el límite de 14 nóminas por año y empleado.
    """,
    'author': 'Joaquin Carrasco',
    'website': 'https://github.com/JoaquinCarrasco',
    'category': 'Human Resources/Payroll',
    'depends': ['base', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/tax_return_views.xml',
        'views/payroll_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
