from odoo import api, fields, models, _, tools
from datetime import datetime, timedelta


class TravelService(models.Model):
    _name = "travel.service"
    _description = "Travel service"
    name = fields.Char(string='name')


    servicetypes = fields.Selection([
        ('field', 'field'),
        ('flight', 'flight'),
        ('train', 'train'),
        ('bus', 'bus')
    ], required=True, default='bus')
    eperiod = fields.Integer(string='Expiration period')

class TravelFecilities(models.Model):
    _name = "travel.fecilities"
    _description = "Travel fecilities"
    name = fields.Char(string='Name')



class TravelVehicle(models.Model):
    _name = "travel.vehicle"
    _description = "Travel vehicle"

    RegistrationNo = fields.Char(string='Registration Number')
    vehicletypes = fields.Selection([
        ('bus', 'bus'),
        ('traveller', 'travellor'),
        ('van', 'van'),
        ('other', 'other')
        ], required=True, default='bus')
    name = fields.Char(string='name')
    numberofseats = fields.Integer(string='Number of seats',
                                        default='1')
    date = fields.Date('Date', default=fields.Datetime.today())

    facilities_ids = fields.Many2many(comodel_name='travel.fecilities' , string='facilities')
    state = fields.Selection([('available', 'available'), ('notavailable', 'notavailable')],
                             default="available", sting="status")
    # vehiclecharges = fields.Integer(string="Amound", name="vehicle_charges")
    # service_id = fields.Many2one(comodel_name='travel.service',
    #                              string='Service')
    # quantity = fields.Integer(string="Quantity", default="1",readonly=True,)
    # unit = fields.Integer(string="Unit")
    vehiclecharges_ids = fields.One2many('travel.vehiclecharges.lines', 'vehicle_id', string='vehicle charges')

    @api.onchange('RegistrationNo','vehicletypes')
    def change_name(self):
        if self.RegistrationNo and self.vehicletypes:
            self.name = self.RegistrationNo + self.vehicletypes
        else:
            self.RegistrationNo= False

class TravelVehiclecharges(models.Model):
        _name = "travel.vehiclecharges.lines"
        _description = "travel vehiclecharges lines"
        vehiclecharges = fields.Integer(string="Amound", name="vehicle_charges")
        service_id = fields.Many2one(comodel_name='travel.service',
                                     string='Service')
        quantity = fields.Integer(string="Quantity", default="1")
        unit = fields.Integer(string="Unit")
        subtotal=fields.Integer(string='Subtotal',compute='_compute_subtotal')
        vehicle_id = fields.Many2one('travel.vehicle',string="vehicle")

        @api.depends('quantity', 'vehiclecharges')
        def _compute_subtotal(self):
            for rec in self:
             rec.subtotal = rec.quantity * rec.vehiclecharges
