# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Registro(models.Model):
    _name = 'mi_modulo_personalizado.registro'
    _description = 'Registro del Módulo Personalizado'

    name = fields.Char(string='Nombre', required=True)
    descripcion = fields.Text(string='Descripción')
    fecha = fields.Date(string='Fecha', default=fields.Date.today)
    activo = fields.Boolean(string='Activo', default=True)
    usuario_id = fields.Many2one('res.users', string='Usuario Responsable', default=lambda self: self.env.user)
