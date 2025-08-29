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
    "name": "Sirelkhatim - Daily Inventory Consumption Report التوافق -  متوافق مع أودو 18 نسختي المجتمع والمؤسسة -  يعمل مع تطبيق المخزون القياسي -  آخر تحديث -  تقرير -  الاستهلاك -  الدوري -  لـ -  حلّل استهلاك المنتجات لأي نطاق زمني. اعرف الإجمالي، ومتوسط اليومي، والمخزون الحالي، وأيام التغطية — مع إمكانية التصفية بحسب المخازن. -  فترات مرنة -  تقارير أسبوعية أو شهرية أو بنطاق مخصص. -  تصفية بالمخازن -  تضمين موقع أو أكثر من المواقع الداخلية. -  مؤشرات عملية -  الإجمالي، المتوسط اليومي، المتاح الآن، وأيام التغطية. -  واجهات متعددة -  قائمة ومحوري ورسوم مع فلاتر وتجميعات. -  تعامل ذكي مع الحركات -  يحتسب أي حركة خارجة من مجموعة المخازن المحددة. -  قد يهمك أيضًا -  مزامنة Freshchat -  عرض -  هل تحتاج إلى مساعدة أو تخصيص؟ -  تواصل معنا للدعم أو الإضافات أو التحليلات المخصصة. -  الدعم ",
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
            "inventory_consumption_report_peridicaly/static/src/**/*",
        ],
    },

    "installable": True,
    "application": False,
    "license": "LGPL-3"
}