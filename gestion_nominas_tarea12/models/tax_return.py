# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, date


class IncomeTaxReturn(models.Model):
    _name = 'tarea12.declaracion.renta'
    _description = 'Declaración de la renta anual'
    _order = 'year desc, id desc'

    name = fields.Char(
        string='Referencia',
        required=True,
        default=lambda self: _('Nuevo'),
        copy=False,
    )
    year = fields.Integer(
        string='Año',
        required=True,
        default=lambda self: datetime.now().year,
    )
    employee_id = fields.Many2one(
        'hr.employee',
        string='Empleado',
        required=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Empresa',
        required=True,
        default=lambda self: self.env.company,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Moneda',
        related='company_id.currency_id',
        store=True,
        readonly=True,
    )
    payroll_ids = fields.Many2many(
        'tarea12.nomina',
        'tarea12_nomina_declaracion_rel',
        'declaracion_id',
        'nomina_id',
        string='Nóminas',
    )
    date_from = fields.Date(
        string='Fecha desde',
        compute='_compute_year_limits',
        store=True,
    )
    date_to = fields.Date(
        string='Fecha hasta',
        compute='_compute_year_limits',
        store=True,
    )
    salary_total = fields.Monetary(
        string='Sueldo bruto total',
        compute='_compute_totals',
        store=True,
    )
    irpf_total = fields.Monetary(
        string='IRPF pagado',
        compute='_compute_totals',
        store=True,
    )
    payroll_count = fields.Integer(
        string='Número de nóminas',
        compute='_compute_totals',
        store=True,
    )

    @api.model
    def create(self, vals):
        if not vals.get('name') or vals.get('name') == _('Nuevo'):
            vals['name'] = self.env['ir.sequence'].next_by_code('tarea12.declaracion.renta') or _('Nuevo')
        return super().create(vals)

    @api.depends('payroll_ids', 'payroll_ids.gross_amount', 'payroll_ids.irpf_amount')
    def _compute_totals(self):
        for record in self:
            salary_total = sum(record.payroll_ids.mapped('gross_amount'))
            irpf_total = sum(record.payroll_ids.mapped('irpf_amount'))
            record.salary_total = salary_total
            record.irpf_total = irpf_total
            record.payroll_count = len(record.payroll_ids)

    @api.depends('year')
    def _compute_year_limits(self):
        for record in self:
            if record.year:
                record.date_from = date(record.year, 1, 1)
                record.date_to = date(record.year, 12, 31)
            else:
                record.date_from = False
                record.date_to = False

    @api.constrains('payroll_ids', 'employee_id', 'year')
    def _check_payrolls(self):
        for record in self:
            payroll_count = len(record.payroll_ids)
            if payroll_count > 14:
                raise ValidationError(_('Una declaración no puede incluir más de 14 nóminas.'))
            for payroll in record.payroll_ids:
                if payroll.employee_id != record.employee_id:
                    raise ValidationError(_('Todas las nóminas seleccionadas deben pertenecer al mismo empleado.'))
                if not payroll.date:
                    raise ValidationError(_('Las nóminas deben tener fecha para generar la declaración.'))
                payroll_date = fields.Date.to_date(payroll.date)
                if payroll_date.year != record.year:
                    raise ValidationError(_('Todas las nóminas deben pertenecer al año %s.') % record.year)
