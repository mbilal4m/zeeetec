from odoo import models, fields, api, _ 


class AccountMove(models.Model):
    _inherit = 'account.move'

    ref_number = fields.Char(string="Reference#")
    remark = fields.Char(string="Remarks")
    credit_period = fields.Integer(string="Credit Period")
    total_item = fields.Integer(string="Total Item", compute="_compute_total_vals")
    total_qty = fields.Integer(string="Total Qty/Wt", compute="_compute_total_vals")
    total_disc_amnt = fields.Integer(string="Total Disc.Amnt", compute="_compute_total_vals")

    @api.onchange('order_line')
    def _compute_total_vals(self):
        for rec in self:
            lines = rec.invoice_line_ids.filtered(lambda x: not x.display_type)
            rec.total_item = len(lines)
            rec.total_qty = sum(lines.mapped('quantity'))
            rec.total_disc_amnt = sum(lines.mapped('dis_amount'))


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'


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

    @api.onchange('quantity', 'discount', 'price_unit', 'tax_ids', 'dis_amount')
    def _onchange_price_subtotal(self):
        for line in self:
            if not line.move_id.is_invoice(include_receipts=True):
                continue

            line.update(line._get_price_total_and_subtotal())
            line.update(line._get_fields_onchange_subtotal())

    @api.model
    def _get_price_total_and_subtotal_model(self, price_unit, quantity, discount, currency, product, partner, taxes, move_type):
        ''' This method is used to compute 'price_total' & 'price_subtotal'.

        :param price_unit:  The current price unit.
        :param quantity:    The current quantity.
        :param discount:    The current discount.
        :param currency:    The line's currency.
        :param product:     The line's product.
        :param partner:     The line's partner.
        :param taxes:       The applied taxes.
        :param move_type:   The type of the move.
        :return:            A dictionary containing 'price_subtotal' & 'price_total'.
        '''
        res = {}

        # Compute 'price_subtotal'.
        line_discount_price_unit = price_unit * (1 - (discount / 100.0))
        if self.dis_amount:
            line_discount_price_unit = price_unit - self.dis_amount
        subtotal = quantity * line_discount_price_unit

        # Compute 'price_total'.
        if taxes:
            taxes_res = taxes._origin.with_context(force_sign=1).compute_all(line_discount_price_unit,
                quantity=quantity, currency=currency, product=product, partner=partner, is_refund=move_type in ('out_refund', 'in_refund'))
            res['price_subtotal'] = taxes_res['total_excluded']
            res['price_total'] = taxes_res['total_included']
        else:
            res['price_total'] = res['price_subtotal'] = subtotal
        #In case of multi currency, round before it's use for computing debit credit
        if currency:
            res = {k: currency.round(v) for k, v in res.items()}
        return res