# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ks_equipment(models.Model):
     _name = 'ks_equipment.ks_equipment'
     _inherit = 'mail.thread',
     _description = 'ks_equipment.ks_equipment'

     reference = fields.Char('REfErence')
     employee_id = fields.Many2one('hr.employee','Employee',track_visibility='always')
     materiel_id = fields.Many2one('product.template','MatEriel',track_visibility='always')
     Date_dElivrance = fields.Date('Date de dElivrance')
     NumSerie = fields.Char('NumEro de SErie',track_visibility='always')
     Valeur = fields.Float('Valeur du matEriel')
     Category_id = fields.Many2one('product.category','CatEgorie du matEriel')
     note = fields.Text('Note')
     attribuE_par_id = fields.Many2one('res.users','AttribuE par')
     state = fields.Selection([('nouveau','Nouveau'), ('attribuE','AttribuE'), ('retournE','RetournE'), ('perdu','Perdu'), ('cassE','CassE'), ('remboursE','RemboursE'), ('annulE','AnnulE')], default='nouveau')


#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

     #@api.multi
     def attribuer(self):
           if self.state == 'nouveau':
                return self.write({'state': 'attribuE'})

     #@api.mul
     def retourner(self):
           if self.state == 'attribuE':
                return self.write({'state': 'retournE'})


     def annuler(self):
           if self.state == 'attribuE':
                return self.write({'state': 'annulE'})

     def perdu(self):
          if self.state == 'attribuE':
               return self.write({'state': 'perdu'})

     def cassE(self):
          if self.state == 'attribuE':
               return self.write({'state': 'cassE'})




