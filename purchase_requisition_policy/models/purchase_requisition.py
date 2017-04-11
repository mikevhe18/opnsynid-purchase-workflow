# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields, SUPERUSER_ID


class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    @api.multi
    @api.depends(
        "state",
        "order_type.sent_supplier_group_ids",
        "order_type.open_bid_group_ids",
        "order_type.tender_reset_group_ids",
        "order_type.open_product_group_ids",
        "order_type.generate_po_group_ids",
        "order_type.cancel_requisition_group_ids"
    )
    def _compute_policy(self):
        obj_purchase_order_type = self.env["purchase.order.type"]
        for requisition in self:
            if self.env.user.id == SUPERUSER_ID:
                requisition.sent_supplier_ok = True
                requisition.open_bid_ok = True
                requisition.tender_reset_ok = True
                requisition.open_product_ok = True
                requisition.generate_po_ok = True
                requisition.cancel_requisition_ok = True
                continue

            order_type_id = requisition.order_type.id

            if not order_type_id:
                requisition.sent_supplier_ok = True
                requisition.open_bid_ok = True
                requisition.tender_reset_ok = True
                requisition.open_product_ok = True
                requisition.generate_po_ok = True
                requisition.cancel_requisition_ok = True
                continue

            order_type =\
                obj_purchase_order_type.browse([order_type_id])[0]
            requisition.sent_supplier_ok =\
                self._button_policy(order_type, 'sent_supplier')
            requisition.open_bid_ok =\
                self._button_policy(order_type, 'open_bid')
            requisition.tender_reset_ok =\
                self._button_policy(order_type, 'tender_reset')
            requisition.open_product_ok =\
                self._button_policy(order_type, 'open_product')
            requisition.generate_po_ok =\
                self._button_policy(order_type, 'generate_po')
            requisition.cancel_requisition_ok =\
                self._button_policy(order_type, 'cancel_requisition')

    @api.model
    def _button_policy(self, order_type, button_type):
        result = False
        user = self.env.user
        group_ids = user.groups_id.ids

        if button_type == 'sent_supplier':
            button_group_ids = order_type.sent_supplier_group_ids.ids
        elif button_type == 'open_bid':
            button_group_ids = order_type.open_bid_group_ids.ids
        elif button_type == 'tender_reset':
            button_group_ids = order_type.tender_reset_group_ids.ids
        elif button_type == 'open_product':
            button_group_ids = order_type.open_product_group_ids.ids
        elif button_type == 'generate_po':
            button_group_ids = order_type.generate_po_group_ids.ids
        elif button_type == 'cancel_requisition':
            button_group_ids = order_type.cancel_requisition_group_ids.ids

        if not button_group_ids:
            result = True
        else:
            if (set(button_group_ids) & set(group_ids)):
                result = True
        return result

    sent_supplier_ok = fields.Boolean(
        string="Can Confirm Call",
        compute="_compute_policy",
        store=False,
    )
    open_bid_ok = fields.Boolean(
        string="Can Close Call for Bids",
        compute="_compute_policy",
        store=False,
    )
    tender_reset_ok = fields.Boolean(
        string="Can Reset to Draft",
        compute="_compute_policy",
        store=False,
    )
    open_product_ok = fields.Boolean(
        string="Can Choose product lines",
        compute="_compute_policy",
        store=False,
    )
    generate_po_ok = fields.Boolean(
        string="Can Done",
        compute="_compute_policy",
        store=False,
    )
    cancel_requisition_ok = fields.Boolean(
        string="Can Cancel Call",
        compute="_compute_policy",
        store=False,
    )
