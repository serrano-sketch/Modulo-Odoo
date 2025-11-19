# -*- coding: utf-8 -*-

from odoo import fields, models


class PcComponent(models.Model):
    """Modelo que almacena los componentes reutilizables disponibles."""

    _name = 'pc.component'
    _description = 'Componente de ordenador'

    name = fields.Char(string='Nombre tecnico', required=True)
    specs = fields.Text(string='Especificaciones')
    price = fields.Monetary(
        string='Precio',
        currency_field='currency_id',
        help='Coste de adquisición del componente.',
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Moneda',
        default=lambda self: self.env.company.currency_id.id,
    )
