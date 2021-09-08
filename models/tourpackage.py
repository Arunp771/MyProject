from odoo import api, fields, models, _, tools
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class TravelPackage(models.Model):
    _name = "travel.package"
    _description = "Tour packages"

    responsible_id = fields.Many2one('res.partner', string='customer')
    Quotationdate = fields.Date(string='Quotation Date')
    vehicletypes = fields.Selection([
        ('bus', 'bus'),
        ('traveller', 'travellor'),
        ('van', 'van'),
        ('other', 'other')
    ], required=True, default='bus')
    # vehicletypes=fields.Many2one(comodel_name="travel.service",string="vehicle types")
    name = fields.Char(string='name')
    numberofseats = fields.Integer(string='Number of seats',
                                   default='1')
    date = fields.Date('Date', default=fields.Datetime.today())

    sourcelocation = fields.Selection([
        ('thrissur', 'thrissur'),
        ('kozikkod', 'kozikkod'),
        ('palakkad', 'palakkad'),
        ('malappuram', 'malappuram')], string='Source location')

    destinationlocation = fields.Selection([
        ('banglore', 'Banglore'),
        ('chennai', 'Chennai'),
        ('coimbatore', 'Coinbatore'),
        ('munnar', 'Munnar')], string='Destination location')

    startdate = fields.Date('Start Date', default=fields.Datetime.today())
    endtdate = fields.Date('End Date')
    ntravelers = fields.Integer('Number Of Travelers')
    facilities = fields.Many2one(comodel_name="travel.fecilities",
                                 string='fecilties')
    vehicle = fields.Many2one(comodel_name="travel.vehicle",
                                   string='vehicle')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'confirm')],
                             default="draft", sting="status")
    estimatedkm = fields.Float(string='EstimatedKM')
    warning = fields.Boolean(default=False)

    estimation_ids = fields.Many2many('travel.vehiclecharges.lines',
                                      'vehicle_id', string='Estimation')
    travel_ids = fields.One2many('travel.estimation',
                                         'service_id', string='travel charges')
    def package_request(self):
        self.state = 'confirm'
        self.vehicle.state='notavailable'
        if self.vehicle.state!="avaiable":
            raise ValidationError(_("Please enter all guest details"))

        else:
            self.vehicle.state = 'notavailable'
        vals = {
            'responsible_id': self.responsible_id.id,
        }
        travel_rec = self.env['travel.customer'].create(vals)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Travel',
            'view_mode': 'form',
            'res_model': 'travel.customer',
            'res_id': travel_rec.id,
        }

    def return_request(self):
        #self.state = 'return'
        self.vehicle.state = 'available'

    @api.onchange('vehicletypes')
    def filter_vehicle(self):
        print('rsss')
        if self.vehicletypes:
            print(self.vehicletypes)
            return {
                'domain': {'vehicle': [('vehicletypes', '=',
                                        self.vehicletypes)]}}

    # def action_add_product(self, line=line):
    #
    #     line = self.env['travel.customer'].create(
    #         {
    #             'vehiclecharges': self.vehicletypes,
    #             'service_id': self.travel_id
    #         }
    #     )


class TravelEstmation(models.Model):
    _name = "travel.estimation"
    _description = "Travel Estimasion"
    service_id = fields.Many2one(comodel_name='travel.service',
                                 string='Service')
    vehiclecharges = fields.Integer(string="Amound")
    travel_id = fields.Many2one('travel.package',string="travel")
# #     vehiclecharges = fields.Integer(string="Amound", name="vehicle_charges")
# #     estimatedkm = fields.Float(string="EstimatedKM")
# #
# #     estimation_id = fields.Many2one('travel.package',string="estimation")
# #
