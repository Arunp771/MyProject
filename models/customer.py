from odoo import api, fields, models, _, tools
from odoo import api, fields, models, _
from datetime import datetime
from datetime import timedelta


class TravelCustomers(models.Model):
    _name = "travel.customer"
    _inherit = ["mail.thread", 'mail.activity.mixin']
    _description = "Travel customer"
    _rec_name = 'reference'

    name = fields.Char(string='name', )
    reference = fields.Char(string='Booking Reference', required=True,
                            copy=False, readonly=True,
                            default=lambda self: _('New'))
    vehicle = fields.Many2one(comodel_name="travel.vehicle",
                              string='vehicle')
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
    date = fields.Date('Booking Date', default=fields.Datetime.today())
    numberofpassengers = fields.Integer(string='Number of passengers',
                                        default='1')
    service_id = fields.Many2one(comodel_name='travel.service',
                                 string='Service')

    note = fields.Text(string='Address')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'confirm'),
                              ('done', 'done'), ('expire', 'expired')],
                             default="draft", sting="status")
    responsible_id = fields.Many2one('res.partner', string='Name')
    note = fields.Char(string='Address', related='responsible_id.street')
    expiration_date = fields.Date(string='Expiration Date',
                                  compute='_compute_expiration_date',
                                  default=fields.Datetime.today())
    estimation_ids = fields.Many2many('travel.estimation',
                                      'service_id', string='Estimation Amount')
    travel_id=fields.Many2many('travel.vehiclecharges.lines', string='esrtttt')

    exe_id = fields.Integer(related='service_id.eperiod')


    @api.depends('exe_id', 'date')
    def _compute_expiration_date(self):
        for rec in self:

            if rec.date == False:
                rec.expiration_date = False
            else:
                rec.expiration_date = fields.Datetime.from_string(rec.date) \
                                      + timedelta(days=int(rec.exe_id))

    def check_expiry(self):
        today = fields.Datetime.today()
        travel_customer = self.env['travel.customer'].search([])
        for customer in travel_customer:
            if customer.state == 'draft' and customer.expiration_date < toady:
                customer.state = 'expire'

    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code(
                'travel.order') or _('New')
            res = super(TravelCustomers, self).create(vals)
            return res

    def customer_request(self):
        self.state = 'confirm'

    @api.onchange('service_id')
    def _onchange_product_id(self):
        temp=self.env['travel.vehiclecharges.lines'].search([('service_id.id','=',self.service_id.id)])
        list=[]
        for i in temp:
            val={
                'service_id':i.service_id.id,
                'vehiclecharges':i.vehiclecharges

            }
            list.append([0, 0, val])

        self.travel_id=list
            # print(i.service_id.name)
            # print(i.vehiclecharges)
