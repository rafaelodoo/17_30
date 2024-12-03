from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import ValidationError

# Comentado en el video 30
# class TransientOffer(models.TransientModel):
#     _name ="transient.model.offer"
#     _description= 'Transient model'

#     @api.autovacuum
#     def _transient_vacuum(self):
#         pass



class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Oferta inmobiliaria'

    


 
    @api.depends('property_id','partner_id')
    def _compute_name(self):
        for rec in self:
            if rec.property_id and rec.partner_id:
                rec.name = f"Propiedad:{rec.property_id.name} - Nombre del contacto:{rec.partner_id.name}"
            else:
                return False


    name = fields.Char(string="Description", compute="_compute_name")


    price= fields.Float(string="Precio")
    status = fields.Selection(
        [
            ('accepted','Aceptado'),
            ('refused','Rechazado')
        ],string="Estado",default="accepted"
    )

    partner_id = fields.Many2one('res.partner', string="Cliente")
    property_id = fields.Many2one('estate.property', string="Propiedad")
    validity = fields.Integer(string="Validez", default="")
    # deadline = fields.Integer(string="Deadline",compute="_compute_total_area",inverse="_inverse_deadline")
    deadline = fields.Integer(string="Deadline",compute="_compute_total_area")

    # _sql_constraints = [
    #     ('check_validity','check(validity > 0)','Deadline cannot be before creation date')
    # ]
    
    @api.model
    def _set_create_date(self):
        return fields.Date.to_string(date.today())
    
    creation_date = fields.Date(string="Fecha de creación", default="_set_create_date")
    # creation_date = fields.Date(string="Fecha de creación")


    # @api.depends_context('uid')
    @api.depends('validity','creation_date')
    def _compute_total_area(self):
        # print(self.env_context)
        # print(self._context)
        for rec in self:
            if rec.creation_date and rec.validity:
                rec.deadline = rec.creation_date + timedelta(days=rec.validity)
            else:
                rec.deadline = False

    def _inverse_deadline(self):
        for rec in self:
            if rec.deadline and rec.creation_date:
                rec.validity = (rec.deadline - rec.creation_date).days
            
            else:
                rec.validity = False

    # @api.autovacuum
    # def _clean_offers(self):
    #     self.search(['estatus','=','refused']).unlink()


    # @api.model_create_multi
    # def create(self,vals):
    #     for rec in vals:
    #         if not rec.get('creation_date'):
    #             rec['creation_date'] = fields.Date.today()
    #
    #     return super(PropertyOffer, self).create(vals)
    
    
    def action_accept_offer(self):
        self.status = 'accepted'

    def action_decline_offer(self):
        self.status = 'declined'


    # @api.constrains('validity')
    # def _check_validity(self):
    #     for rec in self:
    #         if rec.deadline <= rec.creation_date:
    #             raise ValidationError()

    # def write(self,vals):
    #     res_partner_ids = self.env['res.partner'].search([
    #         ('is_company',"=",True),
    #     ])
    #     return super(PropertyOffer,self).write(vals)
    
    # def write(self,vals):
    #     print(vals)
    #     self.env['res.partner'].browse(1)
    #     return super(PropertyOffer,self).write(vals)



    # def write(self,vals):
    #     print(vals)
    #     # self.env['res.partner'].brower(1) ==> # res.partner(1)
    #     res_partner_ids = self.env['res.partner'].search(
    #         [('is_company','=',True),
    #         ('name','=',vals.get('name'))
    #     ], limit=1, order='name desc'
    #     )
    #     print(res_partner_ids)

    #     return super(PropertyOffer,self).write(vals)


    # def write(self,vals):
    #     print(vals)
        
    #     res_partner_ids = self.env['res.partner'].search([
    #         ('is_company','=',True)
    #     ]).filtered(lambda x: x.phone == '2411002566')
                
    #     print(res_partner_ids)

    #     return super(PropertyOffer,self).write(vals)