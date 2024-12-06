from odoo import fields, models, api, _


class Property(models.Model):
    _name = 'estate.property'
    _description = 'Propiedades inmobiliarias'

    name = fields.Char(string="Nombre", required=True)
    color = fields.Integer(string="Color")
    
    state = fields.Selection([
        ('new',"Nuevo"),
        ('received',"Oferta recibida"),
        ('accepted',"Aceptado"),
        ("sold","Vendido"),
        ("cancel","Cancelado")
    ],default="new",string="Estatus")

    type_id = fields.Many2one("estate.property.type", string="Tipo de propiedad")
    tag_id = fields.Many2many("estate.property.tag", string="Tipo de etiqueta")
    description = fields.Text(string="Descripción")
    postcode = fields.Char(string="Codigo postal")
    date_availability = fields.Date(string="Fecha disponible")
    expected_price = fields.Float(string="Precio esperado")
    best_offer = fields.Float(string="Mejor oferta",compute="_compute_best_price")
    selling_price = fields.Float(string="Precio de venta",readonly=True)
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

    def action_accept_offer(self):
        self.state = 'accepted'
    

    def action_decline_offer(self):
        self.state = 'decline'
    
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
            'name':f"{self.name} - Ofertones",
            'domain':[('property_id','=',self.id)],
            'view_mode':'tree',
            'res_model':'estate.property.offer'
        }

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for rec in self:
            if rec.offer_ids:
                rec.best_offer = max(rec.offer_ids.mapped('price'))
            else:
                rec.best_offer = 0

    def action_client_action(self):
        return {
            'type':'ir.actions.client',
            'tag':'display_notification',
            'params':{
                'title': _('Testing Client'),
                'type':'success',
                'sticky':False
            }
        }
    
    #id, create_date, create_uid, write_date, write_uid


    def action_url_action(self):
        return {
            'type':'ir.actions.act_url',
            'url':"https://odoo.com",
            'target':'new',
        }



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




class APIConnector(models.Model):
    _name = 'api.connector'
    _description = 'API Connector'

    name = fields.Char(string="Name")
    api_url = fields.Char(string="API URL", required=True)

    def call_api(self):
        for record in self:
            response = requests.get(record.api_url)
            if response.status_code == 200:
                data = response.json()
                self.env['api.connector.character'].create({
                    'name': data['name'],
                    'status': data['status'],
                    'species': data['species'],
                    'gender': data['gender'],
                    'image': data['image']
                })
            else:
                raise Exception(f"Failed to connect to API: {response.status_code}")

class Character(models.Model):
    _name = 'api.connector.character'
    _description = 'Rick and Morty Character'

    name = fields.Char(string="Name")
    status = fields.Char(string="Status")
    species = fields.Char(string="Species")
    gender = fields.Char(string="Gender")
    image = fields.Binary(string="Image")

