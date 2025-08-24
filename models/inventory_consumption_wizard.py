# -*- coding: utf-8 -*-
from odoo import models, fields, _, api

class InventoryConsumptionWizard(models.TransientModel):
    _name = 'inventory.consumption.wizard'
    _description = 'Inventory Consumption Report Wizard'

    def _default_date_from(self):
        today = fields.Date.context_today(self)
        if isinstance(today, str):
            today = fields.Date.to_date(today)
        return today.replace(day=1)

    date_from     = fields.Date(string="From Date", required=True, default=_default_date_from)
    date_to       = fields.Date(string="To Date", required=True, default=lambda s: fields.Date.context_today(s))
    warehouse_ids = fields.Many2many('stock.warehouse', string="Warehouses",
                                     help="Leave empty to include ALL warehouses / internal locations.")
    line_ids      = fields.One2many('inventory.consumption.line', 'wizard_id', string="Lines", readonly=True)

    # -----------------------------
    # Helpers
    # -----------------------------
    def _period_days(self, d1, d2):
        return max((d2 - d1).days + 1, 1)

    # def _selected_internal_location_ids(self):
    #     """
    #     Return the set of INTERNAL location ids that belong to the selected warehouses
    #     (lot_stock_id + all its children). If no warehouses chosen, return ALL internal locations.
    #     """
    #     Loc = self.env['stock.location']
    #     if self.warehouse_ids:
    #         ids = set()
    #         for wh in self.warehouse_ids:
    #             root = wh.lot_stock_id
    #             if not root:
    #                 continue
    #             children = Loc.search([
    #                 ('parent_left', '>=', root.parent_left),
    #                 ('parent_right', '<=', root.parent_right),
    #                 ('usage', '=', 'internal'),
    #             ]).ids
    #             ids.update(children)
    #         return list(ids) or Loc.search([('usage', '=', 'internal')]).ids
    #     # no warehouses selected -> all internals
    #     return Loc.search([('usage', '=', 'internal')]).ids
    def _selected_internal_location_ids(self):
        """
        INTERNAL locations under selected warehouses (lot_stock_id + children).
        Empty selection => ALL internal locations.
        """
        Loc = self.env['stock.location']
        if self.warehouse_ids:
            loc_ids = set()
            for wh in self.warehouse_ids:
                root = wh.lot_stock_id
                if not root:
                    continue
                # 'child_of' uses parent_path; works in Odoo 18+
                children = Loc.search([('id', 'child_of', root.id), ('usage', '=', 'internal')]).ids
                loc_ids.update(children)
            return list(loc_ids) or Loc.search([('usage', '=', 'internal')]).ids
        return Loc.search([('usage', '=', 'internal')]).ids


    def _compute_consumed(self, internal_loc_ids):
        """
        Consumed = qty leaving the selected internal set:
        source IN internal_loc_ids AND destination NOT IN internal_loc_ids
        """
        cr = self.env.cr
        src_set = tuple(internal_loc_ids)
        dest_set = tuple(internal_loc_ids)

        if self._db_has_qty_done():
            cr.execute("""
                SELECT sm.product_id, SUM(COALESCE(sml.qty_done, 0)) AS qty
                FROM stock_move_line AS sml
                JOIN stock_move       AS sm   ON sml.move_id = sm.id
                JOIN stock_location   AS src  ON sml.location_id = src.id
                JOIN stock_location   AS dest ON sml.location_dest_id = dest.id
                WHERE sm.state = 'done'
                AND src.id IN %s
                AND dest.id NOT IN %s
                AND DATE(sm.date) BETWEEN %s AND %s
            GROUP BY sm.product_id
            """, (src_set, dest_set, self.date_from, self.date_to))
        else:
            cr.execute("""
                SELECT sm.product_id, SUM(COALESCE(sm.product_uom_qty, 0)) AS qty
                FROM stock_move AS sm
                JOIN stock_location src  ON sm.location_id = src.id
                JOIN stock_location dest ON sm.location_dest_id = dest.id
                WHERE sm.state = 'done'
                AND src.id IN %s
                AND dest.id NOT IN %s
                AND DATE(sm.date) BETWEEN %s AND %s
            GROUP BY sm.product_id
            """, (src_set, dest_set, self.date_from, self.date_to))

        return dict(cr.fetchall() or [])


    def _db_has_qty_done(self):
        self.env.cr.execute("""
            SELECT 1
              FROM information_schema.columns
             WHERE table_name='stock_move_line' AND column_name='qty_done'
             LIMIT 1
        """)
        return bool(self.env.cr.fetchone())

    # -----------------------------
    # Core compute
    # -----------------------------
    # def _compute_consumed(self, internal_loc_ids):
    #     """
    #     Consumed = any qty that LEAVES the selected internal locations.
    #     That is, moves where source is one of the internal_loc_ids and destination is NOT internal.
    #     Returns dict {product_id: qty_consumed} for the given period.
    #     """
    #     cr = self.env.cr
    #     params = [tuple(internal_loc_ids), self.date_from, self.date_to]

    #     if self._db_has_qty_done():
    #         # Use move lines (preferred and most accurate)
    #         cr.execute("""
    #             SELECT sm.product_id, SUM(COALESCE(sml.qty_done, 0)) AS qty
    #               FROM stock_move_line AS sml
    #               JOIN stock_move       AS sm   ON sml.move_id = sm.id
    #               JOIN stock_location   AS src  ON sml.location_id = src.id
    #               JOIN stock_location   AS dest ON sml.location_dest_id = dest.id
    #              WHERE sm.state = 'done'
    #                AND src.id IN %s
    #                AND dest.usage != 'internal'
    #                AND DATE(sm.date) BETWEEN %s AND %s
    #           GROUP BY sm.product_id
    #         """, params)
    #     else:
    #         # Fallback: use move (done) quantities
    #         cr.execute("""
    #             SELECT sm.product_id, SUM(COALESCE(sm.product_uom_qty, 0)) AS qty
    #               FROM stock_move AS sm
    #               JOIN stock_location src  ON sm.location_id = src.id
    #               JOIN stock_location dest ON sm.location_dest_id = dest.id
    #              WHERE sm.state = 'done'
    #                AND src.id IN %s
    #                AND dest.usage != 'internal'
    #                AND DATE(sm.date) BETWEEN %s AND %s
    #           GROUP BY sm.product_id
    #         """, params)

    #     return dict(cr.fetchall() or [])

    def _compute_onhand_now(self, internal_loc_ids):
        """Current on hand restricted to the same internal locations (for fair comparison)."""
        cr = self.env.cr
        cr.execute("""
            SELECT sq.product_id, COALESCE(SUM(sq.quantity), 0) AS qty
              FROM stock_quant sq
             WHERE sq.location_id IN %s
          GROUP BY sq.product_id
        """, (tuple(internal_loc_ids),))
        return dict(cr.fetchall() or [])

    # -----------------------------
    # Action
    # -----------------------------
    def action_generate(self):
        self.ensure_one()
        cr = self.env.cr

        # Clear previous lines for this wizard run
        self.line_ids.unlink()

        internal_loc_ids = self._selected_internal_location_ids()

        consumed   = self._compute_consumed(internal_loc_ids)
        onhand_now = self._compute_onhand_now(internal_loc_ids)

        product_ids = set(consumed.keys()) | set(onhand_now.keys())
        if not product_ids:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'inventory.consumption.wizard',
                'view_mode': 'form',
                'res_id': self.id,
                'target': 'new',
                'effect': {'fadeout': 'slow', 'message': _('No data for the selected filters.')},
            }

        products    = self.env['product.product'].browse(list(product_ids))
        period_days = self._period_days(self.date_from, self.date_to)

        vals_list = []
        for p in products:
            total_out = float(consumed.get(p.id, 0.0))
            avg_daily = (total_out / period_days) if period_days else 0.0
            on_hand   = float(onhand_now.get(p.id, 0.0))
            coverage  = (on_hand / avg_daily) if avg_daily else 0.0
            vals_list.append({
                'wizard_id': self.id,
                'product_id': p.id,
                'uom_id': p.uom_id.id,
                'period_days': period_days,
                'total_consumed': total_out,
                'avg_daily': avg_daily,
                'on_hand_now': on_hand,
                'coverage_days': coverage,
            })

        self.env['inventory.consumption.line'].create(vals_list)

        # return {
        #     'type': 'ir.actions.act_window',
        #     'name': _('Daily Consumption Report'),
        #     'res_model': 'inventory.consumption.line',
        #     'view_mode': 'list,pivot,graph',
        #     'domain': [('wizard_id', '=', self.id)],
        #     'context': {'search_default_groupby_product': 1},
        #     'target': 'current',
        # }
        return {
            'type': 'ir.actions.act_window',
            'name': _('Daily Consumption Report'),
            'res_model': 'inventory.consumption.line',
            'view_mode': 'list,pivot,graph',
            'views': [
                (self.env.ref('itsys_inventory_consumption_report.view_inventory_consumption_line_list').id, 'list'),
                (self.env.ref('itsys_inventory_consumption_report.view_inventory_consumption_line_pivot').id, 'pivot'),
                (self.env.ref('itsys_inventory_consumption_report.view_inventory_consumption_line_graph').id, 'graph'),
                (self.env.ref('itsys_inventory_consumption_report.view_inventory_consumption_line_search').id, 'search'),
            ],
            'domain': [('wizard_id', '=', self.id)],
            'context': {'search_default_groupby_product': 1},
            'target': 'current',
        }

