from odoo import fields, models, api, _
import requests # Importar requests
from odoo.exceptions import UserError
import base64

class CharacterWizard(models.TransientModel):
    _name = 'character.wizard'
    _description = 'Character Wizard'

    character_name = fields.Char(string="Character Name", readonly=True)
    character_status = fields.Char(string="Status", readonly=True)
    character_species = fields.Char(string="Species", readonly=True)
    character_gender = fields.Char(string="Gender", readonly=True)
    # character_image = fields.Char(string="Image URL", readonly=True)
    character_image = fields.Binary(string="Character Image", readonly=True)

    def fetch_image(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return base64.b64encode(response.content)
        return False



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
    api_url = fields.Char(string="API URL") # Nuevo campo para la URL de la API

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
    
    def _get_report_base_filename(self):
        self.ensure_one()
        return 'Estate Property - %s' % self.name


    # Campos para almacenar los datos del personaje de Rick and Morty temporalmente
    character_name = fields.Char(string="Nombre del personje", readonly=True)
    character_status = fields.Char(string="Estatus", readonly=True)
    character_species = fields.Char(string="Especie", readonly=True)
    character_gender = fields.Char(string="Genero", readonly=True)
    character_image = fields.Char(string="URL de la imagen", readonly=True)



    @api.model
    @api.returns('self', lambda value: value.id)
    def _retry_operation(self, operation, *args, **kwargs):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                return operation(*args, **kwargs)
            except Exception as e:
                if attempt < max_retries - 1:
                    continue
                else:
                    raise UserError(_("Max retries exceeded. Operation failed."))



    def call_api(self):
        url = self.api_url  # Usar la URL ingresada por el usuario
        if not url:
            raise UserError(_("Please provide a valid API URL."))
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            image_data = base64.b64encode(requests.get(data['image']).content)
            wizard = self.env['character.wizard'].create({
                'character_name': data['name'],
                'character_status': data['status'],
                'character_species': data['species'],
                'character_gender': data['gender'],
                'character_image': image_data,
            })
            return {
                'type': 'ir.actions.act_window',
                'name': 'Character Data',
                'res_model': 'character.wizard',
                'view_mode': 'form',
                'target': 'new',
                'res_id': wizard.id,
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'API Call Failed',
                    'message': f"Failed to connect to API: {response.status_code}",
                    'type': 'danger',
                    'sticky': False,
                }
            }



    # def call_api(self):
    #     response = requests.get("https://rickandmortyapi.com/api/character/564")
    #     if response.status_code == 200:
    #         data = response.json()
    #         image_data = base64.b64encode(requests.get(data['image']).content)
    #         wizard = self.env['character.wizard'].create({
    #             'character_name': data['name'],
    #             'character_status': data['status'],
    #             'character_species': data['species'],
    #             'character_gender': data['gender'],
    #             'character_image': image_data,
    #         })
    #         return {
    #             'type': 'ir.actions.act_window',
    #             'name': 'Character Data',
    #             'res_model': 'character.wizard',
    #             'view_mode': 'form',
    #             'target': 'new',
    #             'res_id': wizard.id,
    #         }
    #     else:
    #         return {
    #             'type': 'ir.actions.client',
    #             'tag': 'display_notification',
    #             'params': {
    #                 'title': 'API Call Failed',
    #                 'message': f"Failed to connect to API: {response.status_code}",
    #                 'type': 'danger',
    #                 'sticky': False,
    #             }
    #         }

    # def call_api(self):
    #     # response = requests.get("https://rickandmortyapi.com/api/character/564")
    #     response = requests.get("https://rickandmortyapi.com/api/character/72")
    #     if response.status_code == 200:
    #         data = response.json()
    #         wizard = self.env['character.wizard'].create({
    #             'character_name': data['name'],
    #             'character_status': data['status'],
    #             'character_species': data['species'],
    #             'character_gender': data['gender'],
    #             'character_image': data['image'],
    #         })
    #         return {
    #             'type': 'ir.actions.act_window',
    #             'name': 'Character Data',
    #             'res_model': 'character.wizard',
    #             'view_mode': 'form',
    #             'target': 'new',
    #             'res_id': wizard.id,
    #         }
    #     else:
    #         return {
    #             'type': 'ir.actions.client',
    #             'tag': 'display_notification',
    #             'params': {
    #                 'title': 'API Call Failed',
    #                 'message': f"Failed to connect to API: {response.status_code}",
    #                 'type': 'danger',
    #                 'sticky': False,
    #             }
    #         }


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
    character_name = fields.Char(string="Character Name", readonly=True)
    character_status = fields.Char(string="Status", readonly=True)
    character_species = fields.Char(string="Species", readonly=True)
    character_gender = fields.Char(string="Gender", readonly=True)
    character_image = fields.Char(string="Image URL", readonly=True)

    def call_api(self):
        for record in self:
            response = requests.get(record.api_url)
            if response.status_code == 200:
                data = response.json()
                record.character_name = data['name']
                record.character_status = data['status']
                record.character_species = data['species']
                record.character_gender = data['gender']
                record.character_image = data['image']
            else:
                raise Exception(f"Failed to connect to API: {response.status_code}")


