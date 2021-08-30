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
