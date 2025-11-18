# -*- coding: utf-8 -*-

from odoo import fields, models


class PcOsTag(models.Model):
    _name = 'pc.os.tag'
    _description = 'Etiqueta de sistema operativo'

    name = fields.Char(string='Sistema operativo', required=True)
