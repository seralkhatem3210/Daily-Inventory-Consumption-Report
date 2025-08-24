# -*- coding: utf-8 -*-
from odoo import models, fields

class InventoryConsumptionLine(models.TransientModel):
    _name = 'inventory.consumption.line'
    _description = 'Inventory Consumption Report Line'
    _transient_max_hours = 72

    wizard_id = fields.Many2one('inventory.consumption.wizard', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Product", required=True)
    uom_id = fields.Many2one('uom.uom', string="UoM", readonly=True)

    period_days = fields.Integer(string="Days in Period", readonly=True)
    total_consumed = fields.Float(string="Total Consumed", digits='Product Unit of Measure', readonly=True)
    avg_daily = fields.Float(string="Avg Daily Consumption", digits='Product Unit of Measure', readonly=True)
    on_hand_now = fields.Float(string="On Hand (Now)", digits='Product Unit of Measure', readonly=True)
    coverage_days = fields.Float(string="Coverage (days @ avg)", readonly=True)

        # أضف هذا الحقل:
    categ_id = fields.Many2one(
        'product.category',
        string="Category",
        related='product_id.categ_id',
        store=False,  # لا داعي للتخزين لأنه transient
        readonly=True,
    )