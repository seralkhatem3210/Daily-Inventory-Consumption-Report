# -*- coding: utf-8 -*-
################################################################################
#
#    Sirelkhatim Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Sirelkhatim Technologies(<https://www.Sirelkhatim.uk>).
#    Author: Ammu Raj (odoo@Sirelkhatim.uk)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
{
    "name": "Daily Inventory Consumption Report",
    "version": "18.0.1.0.0",
    "summary": "Average daily consumption per product over a selected period, with on‑hand and coverage days",
    "author": "Sirelkhatim",
    "license": "LGPL-3",
    "website": "https://sirelkhatim.uk",
    "category": "Inventory/Reporting",
    "depends": ["stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/inventory_consumption_views.xml"
    ],
    "images": [
        "static/description/banner.png",
        "static/description/icon.png"
    ],
    "assets": {
        "web.assets_backend": [
            "freshsales_sync/static/src/**/*",
        ],
    },

    "installable": True,
    "application": False,
    "license": "LGPL-3"
}
