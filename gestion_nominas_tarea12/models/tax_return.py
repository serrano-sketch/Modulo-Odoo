# -*- coding: utf-8 -*-
# Igual que en los otros archivos, mantengo UTF-8 para poder escribir descripciones en español.
from odoo import api, fields, models, _  # Traigo las clases base y helpers de Odoo.
from odoo.exceptions import ValidationError  # Necesito validar que las declaraciones se armen con sentido.
from datetime import datetime, date  # Uso datetime para valores por defecto y date para los límites del año.


class IncomeTaxReturn(models.Model):  # Modelo que representa la declaración anual de la renta.
    _name = 'tarea12.declaracion.renta'  # Nombre técnico del modelo.
    _description = 'Declaración de la renta anual'  # Breve explicación de lo que guarda este modelo.
    _order = 'year desc, id desc'  # Ordeno mostrando primero las declaraciones más recientes.

    name = fields.Char(  # Referencia legible de cada declaración.
        string='Referencia',  # Etiqueta que verá el usuario.
        required=True,  # Siempre debe tener un nombre asignado.
        default=lambda self: _('Nuevo'),  # Inicializo con "Nuevo" hasta que genere la secuencia.
        copy=False,  # Evito duplicar la referencia al copiar registros.
    )  # Termino la definición de name.
    year = fields.Integer(  # Año fiscal de la declaración.
        string='Año',  # Texto mostrado en formularios.
        required=True,  # Es obligatorio indicar el año.
        default=lambda self: datetime.now().year,  # Uso el año actual al crear la declaración.
    )  # Cierro el campo year.
    employee_id = fields.Many2one(  # Empleado al que pertenece la declaración.
        'hr.employee',  # Modelo destino.
        string='Empleado',  # Etiqueta visible.
        required=True,  # No se puede dejar la declaración sin empleado.
    )  # Fin de employee_id.
    company_id = fields.Many2one(  # Compañía propietaria de la declaración.
        'res.company',  # Modelo de compañías.
        string='Empresa',  # Título que aparece en la vista.
        required=True,  # Siempre necesito asociarla a una compañía.
        default=lambda self: self.env.company,  # Uso la compañía actual como valor por defecto.
    )  # Cierro company_id.
    currency_id = fields.Many2one(  # Moneda usada para mostrar los importes totales.
        'res.currency',  # Modelo de monedas estándar.
        string='Moneda',  # Etiqueta visible.
        related='company_id.currency_id',  # La heredo de la compañía para mantener coherencia.
        store=True,  # La guardo para no recalcularla siempre.
        readonly=True,  # Evito que se pueda editar manualmente.
    )  # Termino currency_id.
    payroll_ids = fields.Many2many(  # Relación con las nóminas incluidas en la declaración.
        'tarea12.nomina',  # Modelo relacionado.
        'tarea12_nomina_declaracion_rel',  # Tabla relacional que uso como puente.
        'declaracion_id',  # Nombre de la columna que apunta a la declaración.
        'nomina_id',  # Nombre de la columna que apunta a la nómina.
        string='Nóminas',  # Etiqueta que se verá en la vista.
    )  # Fin del campo payroll_ids.
    date_from = fields.Date(  # Fecha inicial del periodo fiscal.
        string='Fecha desde',  # Etiqueta visible.
        compute='_compute_year_limits',  # Se calcula automáticamente según el año.
        store=True,  # Guardo el resultado para filtros posteriores.
    )  # Cierro date_from.
    date_to = fields.Date(  # Fecha final del periodo fiscal.
        string='Fecha hasta',  # Texto mostrado en el formulario.
        compute='_compute_year_limits',  # Se recalcula cuando cambia el año.
        store=True,  # Persisto el resultado para mejorar el rendimiento.
    )  # Cierro date_to.
    salary_total = fields.Monetary(  # Suma de todos los sueldos brutos seleccionados.
        string='Sueldo bruto total',  # Nombre del campo.
        compute='_compute_totals',  # Se calcula automáticamente en base a las nóminas.
        store=True,  # Almaceno el valor para consultas.
    )  # Cierro salary_total.
    irpf_total = fields.Monetary(  # Total del IRPF retenido en las nóminas asociadas.
        string='IRPF pagado',  # Etiqueta en la vista.
        compute='_compute_totals',  # Se recalcula cada vez que cambian las nóminas.
        store=True,  # Persiste para búsquedas y reportes.
    )  # Fin de irpf_total.
    payroll_count = fields.Integer(  # Cuenta cuántas nóminas están vinculadas.
        string='Número de nóminas',  # Texto mostrado.
        compute='_compute_totals',  # Lo calculo en el mismo método que los totales.
        store=True,  # Lo guardo porque lo muestro mucho.
    )  # Cierro payroll_count.

    @api.model  # Indico que este método trabaja a nivel del modelo completo al crear registros.
    def create(self, vals):  # Sobrescribo create para asegurar la referencia automática.
        if not vals.get('name') or vals.get('name') == _('Nuevo'):  # Verifico si hace falta generar un nombre.
            vals['name'] = self.env['ir.sequence'].next_by_code('tarea12.declaracion.renta') or _('Nuevo')  # Obtengo el siguiente valor de la secuencia configurada.
        return super().create(vals)  # Llamo al create estándar para seguir con la creación normal.

    @api.depends('payroll_ids', 'payroll_ids.gross_amount', 'payroll_ids.irpf_amount')  # Especifico los campos que disparan los recálculos.
    def _compute_totals(self):  # Método que calcula los importes agregados de la declaración.
        for record in self:  # Recorro cada declaración afectada.
            salary_total = sum(record.payroll_ids.mapped('gross_amount'))  # Sumo los importes brutos de cada nómina.
            irpf_total = sum(record.payroll_ids.mapped('irpf_amount'))  # Sumo el IRPF pagado en todas ellas.
            record.salary_total = salary_total  # Guardo la suma de sueldos.
            record.irpf_total = irpf_total  # Guardo la suma de IRPF.
            record.payroll_count = len(record.payroll_ids)  # Actualizo el contador de nóminas enlazadas.

    @api.depends('year')  # Este cálculo depende únicamente del año seleccionado.
    def _compute_year_limits(self):  # Método para establecer las fechas inicial y final del ejercicio.
        for record in self:  # Trabajo con cada declaración.
            if record.year:  # Solo si tengo un año definido.
                record.date_from = date(record.year, 1, 1)  # Pongo el primer día del año como inicio.
                record.date_to = date(record.year, 12, 31)  # Y el último día del año como final.
            else:  # Si no hay año todavía.
                record.date_from = False  # Limpio la fecha desde.
                record.date_to = False  # Limpio la fecha hasta.

    @api.constrains('payroll_ids', 'employee_id', 'year')  # Valido cada vez que cambian las nóminas, el empleado o el año.
    def _check_payrolls(self):  # Compruebo que la declaración cumpla las reglas exigidas.
        for record in self:  # Itero por cada declaración.
            payroll_count = len(record.payroll_ids)  # Calculo el número de nóminas asociadas.
            if payroll_count > 14:  # No permito más de 14 nóminas en un año.
                raise ValidationError(_('Una declaración no puede incluir más de 14 nóminas.'))  # Informo del límite máximo permitido.
            for payroll in record.payroll_ids:  # Reviso una por una las nóminas enlazadas.
                if payroll.employee_id != record.employee_id:  # Deben pertenecer al mismo empleado.
                    raise ValidationError(_('Todas las nóminas seleccionadas deben pertenecer al mismo empleado.'))  # Aclaro el motivo del rechazo.
                if not payroll.date:  # Cada nómina debe tener fecha.
                    raise ValidationError(_('Las nóminas deben tener fecha para generar la declaración.'))  # Aviso del requisito.
                payroll_date = fields.Date.to_date(payroll.date)  # Convierto la fecha en objeto date para comparar.
                if payroll_date.year != record.year:  # Verifico que la nómina sea del mismo año.
                    raise ValidationError(_('Todas las nóminas deben pertenecer al año %s.') % record.year)  # Muestro el año esperado.
