from odoo import models, fields, api, _ 


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    ref_number = fields.Char(string="Reference#")
    remark = fields.Char(string="Remarks")
    credit_period = fields.Integer(string="Credit Period")
    total_item = fields.Integer(string="Total Item", compute="_compute_total_vals")
    total_qty = fields.Integer(string="Total Qty/Wt", compute="_compute_total_vals")
    total_disc_amnt = fields.Integer(string="Total Disc.Amnt", compute="_compute_total_vals")

    @api.onchange('order_line')
    def _compute_total_vals(self):
        for rec in self:
            lines = rec.order_line.filtered(lambda x: not x.display_type)
            rec.total_item = len(lines)
            rec.total_qty = sum(lines.mapped('product_uom_qty'))
            rec.total_disc_amnt = sum(lines.mapped('dis_amount'))

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update({
            'ref_number': self.ref_number,
            'remark': self.remark,
            'credit_period': self.credit_period,
        })
        return invoice_vals

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    dis_amount = fields.Float(string="Disc. Amnt")

    @api.onchange('discount')
    def onchange_disc(self):
        for rec in self:
            if rec.discount != 0:
                rec.dis_amount = 0

    @api.onchange('dis_amount')
    def onchange_disc_amont(self):
        for rec in self:
            if rec.dis_amount != 0:
                rec.discount = 0


    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'dis_amount')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            if line.dis_amount:
                price = line.price_unit - line.dis_amount

            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups('account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])
        



    def _prepare_invoice_line(self, **optional_values):
        res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
        res.update({
            'dis_amount': self.dis_amount,
        })
        return res