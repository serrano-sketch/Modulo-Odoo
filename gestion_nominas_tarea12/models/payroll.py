# -*- coding: utf-8 -*-
# Vuelvo a dejar claro que todo este archivo usa UTF-8 para no pelearme con los acentos.
from odoo import api, fields, models, _  # Traigo las utilidades básicas de Odoo y el método de traducción.
from odoo.exceptions import ValidationError  # Importo la excepción que lanzo cuando algo no cumple mis reglas.


class Payroll(models.Model):  # Defino el modelo principal que representa cada nómina.
    _name = 'tarea12.nomina'  # Nombre técnico del modelo dentro de Odoo.
    _description = 'Nómina de empleado'  # Descripción que se muestra en la interfaz de desarrollador.
    _order = 'date desc, id desc'  # Ordeno las nóminas mostrando primero las más recientes.

    name = fields.Char(  # Este campo guarda la referencia legible de la nómina.
        string='Referencia',  # Etiqueta que verá el usuario en formularios.
        required=True,  # Obligo a que siempre tenga valor.
        default=lambda self: _('Nuevo'),  # Pongo "Nuevo" como valor inicial hasta que se genere la secuencia.
        copy=False,  # Evito que se copie la referencia cuando duplico un registro.
    )  # Cierro la definición del campo name.
    employee_id = fields.Many2one(  # Relaciono la nómina con un empleado de Recursos Humanos.
        'hr.employee',  # Este es el modelo destino de la relación.
        string='Empleado',  # Texto que muestro en pantalla.
        required=True,  # No permito nóminas sin empleado.
    )  # Cierro la definición del campo employee_id.
    company_id = fields.Many2one(  # Guardo la compañía a la que pertenece la nómina.
        'res.company',  # Enlazo con el modelo de compañías estándar.
        string='Empresa',  # Nombre del campo en la vista.
        required=True,  # Siempre debe existir una compañía asociada.
        default=lambda self: self.env.company,  # Uso la compañía del entorno como valor por defecto.
    )  # Termino el campo company_id.
    currency_id = fields.Many2one(  # Alineo la moneda con la de la compañía para mostrar importes correctamente.
        'res.currency',  # Modelo de monedas nativas de Odoo.
        string='Moneda',  # Etiqueta visible en la vista.
        related='company_id.currency_id',  # Lo dejo relacionado para no duplicar información.
        store=True,  # Lo almaceno para poder filtrar y ordenar sin recalcular.
        readonly=True,  # Evito que se cambie manualmente.
    )  # Finalizo la definición del campo currency_id.
    date = fields.Date(  # Campo para la fecha de la nómina.
        string='Fecha',  # Nombre amigable.
        required=True,  # No permito nóminas sin fecha.
        default=fields.Date.context_today,  # Uso la fecha actual como predeterminada.
    )  # Cierro el campo date.
    salary_base = fields.Monetary(  # Aquí guardo el sueldo base antes de ajustes.
        string='Sueldo base',  # Etiqueta del formulario.
        required=True,  # Necesito siempre un importe base.
        default=0.0,  # Inicio en cero por si creo la nómina sin rellenar nada todavía.
    )  # Termino salary_base.
    adjustment_ids = fields.One2many(  # Lista de bonificaciones o deducciones asociadas.
        'tarea12.nomina.ajuste',  # Modelo hijo que contiene cada ajuste.
        'payroll_id',  # Campo inverso que apunta a la nómina.
        string='Bonificaciones / Deducciones',  # Nombre que muestro en las vistas.
    )  # Fin del campo adjustment_ids.
    irpf_rate = fields.Float(  # Porcentaje de retención de IRPF que aplicaré.
        string='IRPF (%)',  # Etiqueta en formularios.
        required=True,  # Es obligatorio definirlo.
        default=15.0,  # Asigno un valor base de ejemplo del 15%.
    )  # Cierro irpf_rate.
    bonus_amount = fields.Monetary(  # Campo calculado con el total de bonificaciones.
        string='Bonificaciones totales',  # Texto visible para el usuario.
        compute='_compute_amounts',  # Función que calcula el valor automáticamente.
        store=True,  # Guardo el resultado para no recalcularlo cada vez que abro la vista.
    )  # Cierro bonus_amount.
    deduction_amount = fields.Monetary(  # Total de deducciones aplicadas.
        string='Deducciones totales',  # Etiqueta informativa.
        compute='_compute_amounts',  # Uso la misma función de cálculo general.
        store=True,  # Persiste en base de datos.
    )  # Termino deduction_amount.
    taxable_amount = fields.Monetary(  # Base imponible después de sumar bonificaciones y antes de deducciones.
        string='Base imponible IRPF',  # Nombre mostrado en la ficha.
        compute='_compute_amounts',  # Lo obtengo dentro del cómputo general.
        store=True,  # Guardo el resultado para consultas rápidas.
    )  # Cierro taxable_amount.
    irpf_amount = fields.Monetary(  # Importe del IRPF calculado según la base imponible.
        string='IRPF pagado',  # Texto que verá la persona usuaria.
        compute='_compute_amounts',  # Se calcula en el método agregado.
        store=True,  # Necesito almacenarlo para informes.
    )  # Fin de irpf_amount.
    gross_amount = fields.Monetary(  # Sueldo bruto tras ajustes.
        string='Sueldo bruto',  # Etiqueta amigable.
        compute='_compute_amounts',  # También se calcula automáticamente.
        store=True,  # Lo dejo almacenado para búsquedas.
    )  # Termina gross_amount.
    net_amount = fields.Monetary(  # Sueldo neto final tras retener el IRPF.
        string='Sueldo neto',  # Nombre mostrado al usuario.
        compute='_compute_amounts',  # Se calcula en la misma función agregada.
        store=True,  # Persiste porque es un dato importante.
    )  # Cierro net_amount.
    payment_receipt = fields.Binary(  # Archivo adjunto para el justificante de transferencia.
        string='Justificante de transferencia (PDF)',  # Explico qué tipo de archivo espero.
        attachment=True,  # Lo guardo como adjunto para aprovechar el sistema de documentos.
        filters='*.pdf',  # Sugiero que se suba únicamente un PDF.
    )  # Finalizo payment_receipt.
    state = fields.Selection(  # Campo para controlar el estado del flujo de la nómina.
        [
            ('draft', 'Redactada'),  # Estado inicial donde todavía se puede editar.
            ('confirmed', 'Confirmada'),  # Estado intermedio validado.
            ('paid', 'Pagada'),  # Estado final cuando se ha pagado al empleado.
        ],
        string='Estado',  # Etiqueta del campo.
        required=True,  # Siempre debe existir un estado vigente.
        default='draft',  # Arranco todas las nóminas en borrador.
    )  # Termino la definición de state.

    @api.model  # Indico que este método opera sobre el entorno en general al crear registros.
    def create(self, vals):  # Sobrescribo create para asignar la secuencia cuando corresponda.
        if not vals.get('name') or vals.get('name') == _('Nuevo'):  # Compruebo si el nombre sigue sin definirse.
            vals['name'] = self.env['ir.sequence'].next_by_code('tarea12.nomina') or _('Nuevo')  # Pido el siguiente número a la secuencia configurada.
        return super().create(vals)  # Llamo al create original para que continúe el flujo normal.

    def action_confirm(self):  # Acción de botón para pasar una nómina a confirmada.
        for payroll in self:  # Recorro cada registro seleccionado.
            if payroll.state == 'draft':  # Solo actúo sobre los que siguen en borrador.
                payroll.state = 'confirmed'  # Cambio el estado a confirmado.
        return True  # Devuelvo True para mantener la convención de acciones Odoo.

    def action_mark_paid(self):  # Acción que marca la nómina como pagada.
        for payroll in self:  # Itero por cada nómina afectada.
            if payroll.state in ('draft', 'confirmed'):  # Compruebo que esté en alguno de los estados previos.
                payroll.state = 'paid'  # Actualizo el estado a pagado.
        return True  # Devuelvo True para dar por terminada la acción.

    def action_reset_to_draft(self):  # Acción para volver atrás a borrador.
        for payroll in self:  # Recorro una a una las nóminas seleccionadas.
            payroll.state = 'draft'  # Pongo el estado en draft sin condiciones.
        return True  # Finalizo la acción indicando éxito.

    @api.depends('salary_base', 'irpf_rate', 'adjustment_ids.amount', 'adjustment_ids.type')  # Digo qué campos disparan el cálculo.
    def _compute_amounts(self):  # Método central que calcula todos los importes derivados.
        for payroll in self:  # Trabajo registro por registro.
            bonus = sum(line.amount for line in payroll.adjustment_ids if line.type == 'bonus')  # Sumo lo que sea bonificación.
            deduction = sum(line.amount for line in payroll.adjustment_ids if line.type == 'deduction')  # Sumo lo que sea deducción.
            taxable = payroll.salary_base + bonus  # Calculo la base imponible sumando el sueldo base y los bonus.
            gross = payroll.salary_base + bonus   # El bruto es la base más bonus.
            irpf_amount = taxable * (payroll.irpf_rate / 100.0)  # El IRPF se obtiene aplicando el porcentaje sobre la base.
            payroll.bonus_amount = bonus  # Guardo el total de bonificaciones en su campo.
            payroll.deduction_amount = deduction  # Guardo el total de deducciones.
            payroll.taxable_amount = taxable  # Almaceno la base imponible.
            payroll.irpf_amount = irpf_amount  # Registro cuánto IRPF retengo.
            payroll.gross_amount = gross  # Anoto el sueldo bruto calculado.
            payroll.net_amount = gross - irpf_amount  # El sueldo neto es el bruto menos el IRPF.

    @api.constrains('salary_base', 'irpf_rate')  # Declaro que voy a validar estos campos cuando cambien.
    def _check_salary_and_irpf(self):  # Método de validación para los importes básicos.
        for payroll in self:  # Recorro cada registro afectado.
            if payroll.salary_base < 0:  # No acepto sueldos negativos.
                raise ValidationError(_('El sueldo base debe ser mayor o igual que cero.'))  # Lanzo un error claro al usuario.
            if payroll.irpf_rate < 0 or payroll.irpf_rate > 100:  # Aseguro que el porcentaje sea lógico.
                raise ValidationError(_('El porcentaje de IRPF debe estar entre 0 y 100.'))  # Informo del rango permitido.


class PayrollAdjustment(models.Model):  # Modelo hijo para manejar bonificaciones y deducciones.
    _name = 'tarea12.nomina.ajuste'  # Nombre técnico del modelo de ajustes.
    _description = 'Bonificación o deducción'  # Texto descriptivo que veré en herramientas técnicas.
    _order = 'payroll_id, id'  # Ordeno los registros dentro de cada nómina en orden de creación.

    payroll_id = fields.Many2one(  # Relación hacia la nómina propietaria.
        'tarea12.nomina',  # Modelo objetivo de la relación.
        string='Nómina',  # Etiqueta que aparece en la vista.
        required=True,  # Siempre debo asociarlo a una nómina.
        ondelete='cascade',  # Si elimino la nómina quiero borrar también sus ajustes.
    )  # Cierro payroll_id.
    company_id = fields.Many2one(  # Compañía a la que pertenece el ajuste.
        'res.company',  # Uso el modelo estándar de compañías.
        string='Empresa',  # Nombre del campo.
        related='payroll_id.company_id',  # Heredo el valor de la nómina para mantener coherencia.
        store=True,  # Almaceno la relación para poder filtrar directamente.
        readonly=True,  # Evito modificaciones manuales.
    )  # Termino company_id.
    currency_id = fields.Many2one(  # Moneda utilizada en el ajuste.
        'res.currency',  # Modelo de monedas.
        string='Moneda',  # Etiqueta visible.
        related='payroll_id.currency_id',  # Reutilizo la moneda de la nómina.
        store=True,  # Persisto el valor para evitar recalcular.
        readonly=True,  # No permito cambiarlo manualmente.
    )  # Finalizo currency_id.
    type = fields.Selection(  # Indico si el ajuste suma o resta.
        [
            ('bonus', 'Bonificación'),  # Opción para sumar dinero.
            ('deduction', 'Deducción'),  # Opción para restar dinero.
        ],
        required=True,  # Siempre debo especificar de qué tipo es.
        default='bonus',  # Arranco suponiendo que será una bonificación.
    )  # Cierro type.
    name = fields.Char(  # Texto que describe la bonificación o deducción.
        string='Concepto',  # Etiqueta mostrada al usuario.
        required=True,  # Obligo a escribir un concepto.
    )  # Termino name.
    amount = fields.Monetary(  # Importe específico del ajuste.
        string='Importe',  # Nombre en pantalla.
        required=True,  # Debe existir siempre.
        default=0.0,  # Empiezo en cero hasta que lo rellenen.
    )  # Cierro amount.

    @api.constrains('amount')  # Declaro la restricción sobre el importe.
    def _check_amount(self):  # Función encargada de validar los montos.
        for line in self:  # Recorro cada ajuste editado.
            if line.amount <= 0:  # No acepto importes nulos o negativos.
                raise ValidationError(_('El importe debe ser mayor que cero.'))  # Informo al usuario del error.
