# -*- coding: utf-8 -*-
# from odoo import http


# class KsEquipment(http.Controller):
#     @http.route('/ks_equipment/ks_equipment', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ks_equipment/ks_equipment/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ks_equipment.listing', {
#             'root': '/ks_equipment/ks_equipment',
#             'objects': http.request.env['ks_equipment.ks_equipment'].search([]),
#         })

#     @http.route('/ks_equipment/ks_equipment/objects/<model("ks_equipment.ks_equipment"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ks_equipment.object', {
#             'object': obj
#         })
