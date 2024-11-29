from odoo import fields, models, api

class TransientOffer(models.TransientModel):
    _name ="transient.model.offer"
    _description= 'Transient model'

    @api.autovacuum
    def _transient_vacuum(self):
        pass

class Property(models.Model):
    _name = 'estate.property'
    _description = 'Estate properties'

    name = fields.Char(string="Nombre", required=True)
    
    state = fields.Selection([
        ('new',"Nueva"),
        ('received',"Oferta recibida"),
        ('accepted',"Aceptado <i class='fa fa-cloud-upload fa-fw'></i>"),
        ("sold","Rechazado homs"),
        ("cancel","Cancelado :'(")
    ],default="new",string="Estatus")

    type_id = fields.Many2one("estate.property.type", string="Tipo de propiedad")
    tag_id = fields.Many2many("estate.property.tag", string="Tipo de etiqueta")
    description = fields.Text(string="Descripción")
    postcode = fields.Char(string="Codigo postal")
    date_availability = fields.Date(string="Fecha disponible")
    expected_price = fields.Float(string="Precio esperado")
    best_offer = fields.Float(string="Mejor oferta")
    selling_price = fields.Float(string="Precio de venta")
    bedrooms = fields.Integer(string="Camas")
    living_area = fields.Integer(string="Salas de estar")
    facades = fields.Integer(string="Fachadas")
    garage = fields.Boolean(string="Garaje",default=False)
    garden = fields.Boolean(string="Jardín",default=False)
    garden_area = fields.Integer(string="Área de jardín")

    garden_orientation = fields.Selection(
        [
            ('north','Norte'),
            ('south','Sur'),
            ('east','Este'),
            ('west','Oeste')
        ],string="Orientación de jardín",default="north"
    )

    offer_ids = fields.One2many('estate.property.offer','property_id',string="Ofertones")
    sales_id = fields.Many2one('res.users',string="Vendedor")
    buyer_id = fields.Many2one('res.partner',string="Comprador",domain=[('is_company','=',True)])


    # @api.depends('living_area','garden_area')
    # def _compute_total_area(self):
    #     for rec in self:
    #         rec.total_area = rec.living_area + rec.garden_area

    phone = fields.Char(string="Teléfono",related="buyer_id.phone")

    @api.onchange('living_area','garden_area')
    def _onchange_total_area(self): 
        self.total_area = self.living_area + self.garden_area

    # total_area = fields.Integer(string="Area total" compute="_compute_total_area")
    total_area = fields.Integer(string="Area total")

    def action_sold(self):
        self.state = 'sold'
    
    def action_cancel(self):
        self.state = 'cancel'

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")


    def action_property_view_offers(self):
        return {
            'type':'ir.actions.act_window',
            'name':f"{self.name - 'Ofertas chidoris'}",
            
            'domain':[('property_id','=',self.id)],
            'view_mode':'tree',
            'res_model':'state.property.offer'
        }

    
    #id, create_date, create_uid, write_date, write_uid

#Aqui estamos creando un nuevo modelo.
class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate properties type'

    name = fields.Char(string="Nombre", required=True)

class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate properties tag'

    name = fields.Char(string="Nombre", required=True)
    color = fields.Char(string="Color")