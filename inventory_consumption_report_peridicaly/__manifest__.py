# -*- coding: utf-8 -*-
################################################################################
#
#    Sirelkhatim Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Sirelkhatim Technologies(<https://www.Sirelkhatim.uk>).
#    Author: Ammu Raj (odoo@Sirelkhatim.uk)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.#
################################################################################
{
    "name": "Sirelkhatim - Daily Inventory Consumption Report |  سرالختم - تقرير الاستهلاك الدوري للمخزون",
    "version": "18.0.1.0.0",
    "summary": "Analyze daily average consumption per product (with stock & coverage days) | تحليل متوسط الاستهلاك اليومي لكل منتج (مع المخزون وأيام التغطية)",
    "author": "Sirelkhatim Technologies",
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

    "description": """
Daily Inventory Consumption Report | تقرير الاستهلاك الدوري للمخزون
==================================================================

**Compatibility | التوافق**
- ✅ Compatible with Odoo 18 Community & Enterprise  
- ✅ Works with the standard Inventory application  

**Features | المزايا**
- 📊 Analyze product consumption for any time range.  
  حلّل استهلاك المنتجات لأي نطاق زمني.  
- 📈 See totals, daily averages, current stock, and coverage days.  
  اعرف الإجمالي، المتوسط اليومي، المخزون الحالي، وأيام التغطية.  
- ⏳ Flexible periods (weekly, monthly, custom ranges).  
  فترات مرنة (أسبوعية، شهرية أو بنطاق مخصص).  
- 🏷 Filter by warehouses or multiple internal locations.  
  تصفية حسب المخازن أو عدة مواقع داخلية.  
- 🔎 Smart handling of outgoing moves from selected warehouses.  
  التعامل الذكي مع الحركات الخارجة من المخازن المحددة.  
- 📑 Multiple report views: list, pivot, charts with filters/groupings.  
  واجهات متعددة: قائمة، محوري، رسوم بيانية مع فلاتر وتجميعات.  

**Extra | إضافات**
- 🔄 Synchronization-ready and extendable.  
  قابل للتزامن والتوسعة.  
- 🤝 Need help or customization? Contact us for support or tailored analytics.  
  هل تحتاج إلى مساعدة أو تخصيص؟ تواصل معنا للدعم أو التحليلات المخصصة.  
    """,

    "installable": True,
    "application": False,
}
