    # -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    @api.model_create_multi
    def create(self, vals_list):
        order = super(SaleOrder, self).create(vals_list)

        for vals in vals_list:
            order_name = vals['name']
            order_lines = vals['order_line']
            #amout_total = vals['amount_total'] #can not get amount_total directly,
            amount_total = 0  #therefore need to calculate as below. Check why! Here set initial value to 0
            for order_line in order_lines:
                price_unit =order_line[2]['price_unit']
                tax_ids = order_line[2]['tax_id']
                tax_total = 0
                for tax_id in tax_ids:
                    tax = self.env['account.tax'].search([('id', '=', tax_id[2])]).amount * 0.01
                    tax_total += ((price_unit* tax))
                amount_total += price_unit+tax_total
        message = 'New Quatation: %s has been Created, Sum: %d.'%(order_name,amount_total)
        
        if order.partner_id:
            order.partner_id.message_post(body=message, subject='Quotation Created')
        return order