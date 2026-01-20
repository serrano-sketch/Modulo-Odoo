from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    nss = fields.Char(string='Número Seguridad Social', size=12, help="Formato: 12 dígitos (2 provincia + 8 número + 2 control)")
    dni = fields.Char(string='DNI', size=9, help="Formato: 8 dígitos + letra")

    @api.constrains('nss', 'dni')
    def _check_nss_dni(self):
        for record in self:
            # NSS Validation
            if not record.nss:
                raise ValidationError("El NSS es obligatorio.")
                
            if len(record.nss) != 12 or not record.nss.isdigit():
                raise ValidationError("El NSS debe tener 12 dígitos.")
                
                # Logic: Concatenate Province + Number, then Modulo 97 should match Control
                # Standard algorithm implies: 
                # ent = int(nss[:-2])
                # rem = ent % 97
                # But sometimes logic varies for numbers < 10 million. 
                # For this exercise, simple modulo 97 of the first 10 digits usually works for standard cases.
                
                base_number = int(record.nss[:10])
                control_digit = int(record.nss[10:])
                
                # Note: In real world, if number < 10 million, logic is slightly different (add province * 10M). 
                # But simply int(full_10_digits) handles the concatenation correctly as a single number.
                
                if base_number % 97 != control_digit:
                    raise ValidationError("El NSS no es válido. Fallo en dígito de control.")

            # DNI Validation
            if not record.dni:
                raise ValidationError("El DNI es obligatorio.")

            if len(record.dni) != 9:
                raise ValidationError("El DNI debe tener 9 caracteres (8 dígitos + 1 letra).")
                
                digits_part = record.dni[:-1]
                letter_part = record.dni[-1].upper()
                
                if not digits_part.isdigit() or not letter_part.isalpha():
                    raise ValidationError("El DNI debe tener 8 dígitos seguidos de una letra.")
                
                table = "TRWAGMYFPDXBNJZSQVHLCKE"
                calculated_letter = table[int(digits_part) % 23]
                
                if calculated_letter != letter_part:
                    raise ValidationError(f"El DNI no es válido. La letra debería ser {calculated_letter}.")
