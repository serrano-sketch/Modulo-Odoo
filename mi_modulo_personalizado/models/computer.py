# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PcComputer(models.Model):
    _name = 'pc.computer'
    _description = 'Ordenador de empresa'

    number = fields.Char(string='Numero de equipo', required=True)
    user_id = fields.Many2one('res.users', string='Usuario')
    component_ids = fields.Many2many(
        'pc.component',
        'pc_computer_component_rel',
        'computer_id',
        'component_id',
        string='Componentes',
    )
    last_mod_date = fields.Date(string='Ultima modificacion')
    price_total = fields.Monetary(
        string='Precio total',
        compute='_compute_total',
        currency_field='currency_id',
        store=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Moneda',
        default=lambda self: self.env.company.currency_id.id,
    )
    incidents = fields.Text(string='Incidencias')
    os_tag_ids = fields.Many2many(
        'pc.os.tag',
        string='Sistemas operativos',
    )

    @api.constrains('last_mod_date')
    def _check_last_mod_date(self):
        for record in self:
            if record.last_mod_date and record.last_mod_date > fields.Date.today():
                raise ValidationError('La fecha no puede ser futura')

    @api.depends('component_ids.price')
    def _compute_total(self):
        for record in self:
            total = sum(record.component_ids.mapped('price'))
            record.price_total = total
