# -*- coding: utf-8 -*-

import logging
from odoo.exceptions import UserError, Warning
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange('order_line')
    def onchange_product_id(self):
        self.ensure_one()
        existing_products = []
        warning = {}
        if self.order_line:
            existing_products = [line.product_id for line in self.order_line]
            for line in self.order_line:
                count_product = existing_products.count(line.product_id)
                if line.product_id in existing_products and count_product > 1:
                    title = _("Alerte pour l'article: %s", line.product_id.name)
                    message = _("Vous avez ajouté cet article (%s) fois" % count_product)
                    warning = {
                        'title': title,
                        'message': message
                    }
                    return {'warning': warning}
                existing_products.append(line.product_id)
