# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Payroll(models.Model):
    _name = 'tarea12.nomina'
    _description = 'Nómina de empleado'
    _order = 'date desc, id desc'

    name = fields.Char(
        string='Referencia',
        required=True,
        default=lambda self: _('Nuevo'), #Esto sirve para que al crear un nuevo registro aparezca "Nuevo" en lugar de estar vacío ademas el _ es para traducción de odoo
        copy=False,
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
    date = fields.Date(
        string='Fecha',
        required=True,
        default=fields.Date.context_today,
    )
    salary_base = fields.Monetary(
        string='Sueldo base',
        required=True,
        default=0.0,
    )
    adjustment_ids = fields.One2many(
        'tarea12.nomina.ajuste',
        'payroll_id',
        string='Bonificaciones / Deducciones',
    )
    irpf_rate = fields.Float(
        string='IRPF (%)',
        required=True,
        default=15.0,
    )
    bonus_amount = fields.Monetary(
        string='Bonificaciones totales',
        compute='_compute_amounts',
        store=True,
    )
    deduction_amount = fields.Monetary(
        string='Deducciones totales',
        compute='_compute_amounts',
        store=True,
    )
    taxable_amount = fields.Monetary(
        string='Base imponible IRPF',
        compute='_compute_amounts',
        store=True,
    )
    irpf_amount = fields.Monetary(
        string='IRPF pagado',
        compute='_compute_amounts',
        store=True,
    )
    gross_amount = fields.Monetary(
        string='Sueldo bruto',
        compute='_compute_amounts',
        store=True,
    )
    net_amount = fields.Monetary(
        string='Sueldo neto',
        compute='_compute_amounts',
        store=True,
    )
    payment_receipt = fields.Binary(
        string='Justificante de transferencia (PDF)',
        attachment=True,
        filters='*.pdf',
    )
    state = fields.Selection(
        [
            ('draft', 'Redactada'),
            ('confirmed', 'Confirmada'),
            ('paid', 'Pagada'),
        ],
        string='Estado',
        required=True,
        default='draft',
    )

    @api.model
    def create(self, vals):
        if not vals.get('name') or vals.get('name') == _('Nuevo'):
            vals['name'] = self.env['ir.sequence'].next_by_code('tarea12.nomina') or _('Nuevo')
        return super().create(vals)

    def action_confirm(self):
        for payroll in self:
            if payroll.state == 'draft':
                payroll.state = 'confirmed'
        return True

    def action_mark_paid(self):
        for payroll in self:
            if payroll.state in ('draft', 'confirmed'):
                payroll.state = 'paid'
        return True

    def action_reset_to_draft(self):
        for payroll in self:
            payroll.state = 'draft'
        return True

    @api.depends('salary_base', 'irpf_rate', 'adjustment_ids.amount', 'adjustment_ids.type')
    def _compute_amounts(self):
        for payroll in self:
            bonus = sum(line.amount for line in payroll.adjustment_ids if line.type == 'bonus')
            deduction = sum(line.amount for line in payroll.adjustment_ids if line.type == 'deduction')
            taxable = payroll.salary_base + bonus
            gross = payroll.salary_base + bonus - deduction
            irpf_amount = taxable * (payroll.irpf_rate / 100.0)
            payroll.bonus_amount = bonus
            payroll.deduction_amount = deduction
            payroll.taxable_amount = taxable
            payroll.irpf_amount = irpf_amount
            payroll.gross_amount = gross
            payroll.net_amount = gross - irpf_amount

    @api.constrains('salary_base', 'irpf_rate')
    def _check_salary_and_irpf(self):
        for payroll in self:
            if payroll.salary_base < 0:
                raise ValidationError(_('El sueldo base debe ser mayor o igual que cero.'))
            if payroll.irpf_rate < 0 or payroll.irpf_rate > 100:
                raise ValidationError(_('El porcentaje de IRPF debe estar entre 0 y 100.'))


class PayrollAdjustment(models.Model):
    _name = 'tarea12.nomina.ajuste'
    _description = 'Bonificación o deducción'
    _order = 'payroll_id, id'

    payroll_id = fields.Many2one(
        'tarea12.nomina',
        string='Nómina',
        required=True,
        ondelete='cascade',
    )
    company_id = fields.Many2one(
        'res.company',
        string='Empresa',
        related='payroll_id.company_id',
        store=True,
        readonly=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Moneda',
        related='payroll_id.currency_id',
        store=True,
        readonly=True,
    )
    type = fields.Selection(
        [
            ('bonus', 'Bonificación'),
            ('deduction', 'Deducción'),
        ],
        required=True,
        default='bonus',
    )
    name = fields.Char(
        string='Concepto',
        required=True,
    )
    amount = fields.Monetary(
        string='Importe',
        required=True,
        default=0.0,
    )

    @api.constrains('amount')
    def _check_amount(self):
        for line in self:
            if line.amount <= 0:
                raise ValidationError(_('El importe debe ser mayor que cero.'))
