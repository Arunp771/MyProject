from odoo import api, fields, models, _, tools
from odoo import api, fields, models, _
from datetime import datetime
from datetime import timedelta


class TravelCustomers(models.Model):
    _name = "travel.customer"
    _inherit = ["mail.thread", 'mail.activity.mixin']
    _description = "Travel customer"

    name = fields.Char(string='name', )
    reference = fields.Char(string='Booking Reference', required=True,
                            copy=False, readonly=True,
                            default=lambda self: _('New'))
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
                                  compute='_compute_expiration_date')

    exe_id = fields.Integer(related='service_id.eperiod')

    @api.depends('exe_id', 'date')
    def _compute_expiration_date(self):
        for rec in self:
            print("test3")
            print(self.env['travel.customer'].search([]))
            rec.expiration_date = fields.Datetime.from_string(rec.date) \
                                   + timedelta(days=int(rec.exe_id))

    def check_expiry(self):
        today = fields.Date.today()
        travel_customer = self.env['travel.customer'].search([])
        for customer in travel_customer:
            print("test1")
            if customer.state == 'draft' and customer.expiration_date < today:
                print("test2")
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
