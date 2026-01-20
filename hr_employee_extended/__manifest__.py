{
    'name': 'HR Employee Extension',
    'version': '1.0',
    'summary': 'Extends HR Employee with NSS and DNI fields',
    'description': """
        Extends the HR Employee module to include:
        - NSS (Social Security Number) with validation
        - DNI (National Identity Document) with validation
    """,
    'author': 'Antigravity',
    'category': 'Human Resources',
    'depends': ['hr'],
    'data': [
        'views/hr_employee_view.xml',
    ],
    'installable': True,
    'application': False,
}
