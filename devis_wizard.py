# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class fast_alu_wiz(models.TransientModel):
    _name = 'fast.devis.wizard'


    # champ fenêtre/porte en ALU
    # currency_id = fields.Many2one('res.currency', string='Devise', default=1)
    largeur = fields.Integer()
    hauteur = fields.Integer()
    article = fields.Many2one('product.template', 'Article', domain="[('type_FAST', '=', 'alu')]")
    #variant_test = fields.Many2one('product.attribute.value','Variant')#, related='article.attribute_line_ids.attribute_id.name')
    quantity = fields.Integer(default=1)
    reduction = fields.Float(default=0.0)

    poignee_clef = fields.Boolean(string="Poignée à clef")
    poignee = fields.Boolean(string="Poignée")
    paumelle = fields.Boolean(string="Paumelles")
    compas = fields.Boolean(string="Compas")
    mecanisme = fields.Boolean(string="Mécanisme")
    lames = fields.Boolean(string="Lames")
    division = fields.Boolean(string="Divisions")
    serrure_auto = fields.Boolean(string="Serrure auto")
    montant_liaison = fields.Boolean(string="Montant de liaison")

    def get_accessoire(self):
        self.recompute()
        accessoire=[]
        if self.poignee_clef:
            accessoire.append('Poignée à clef')
        if self.poignee:
            accessoire.append('Poignée')
        if self.paumelle:
            accessoire.append('Paumelles')
        if self.compas:
            accessoire.append('Compas')
        if self.mecanisme:
            accessoire.append('Mécanisme')
        if self.lames:
            accessoire.append('Lames')
        if self.division:
            accessoire.append('Divisions')
        if self.serrure_auto:
            accessoire.append('Serrure auto')
        if self.montant_liaison:
            accessoire.append('Montant de liaison')
        return accessoire

    prix = fields.Float()  # Monetary(currency_field='currency_id', readonly=True)
    prix_unitaire = fields.Float()  # Monetary(currency_field='currency_id', readonly=True)

    @api.onchange('article')
    def onchange_article1(self):
        self.couleur_radioD = False
        self.vitre_radioD = False
        self.epaisseur_radioD = False
        if not self.article:
            self.prix = 0.0


    couleur_radioD = fields.Many2one('product.template.attribute.value', string="Couleur")
    vitre_radioD = fields.Many2one('product.template.attribute.value', string="Vitrage")
    epaisseur_radioD = fields.Many2one('product.template.attribute.value', string="Épaisseur")

    accesory_list_art = fields.Many2many('product.product', related='article.accessory_ids_fast', ondelete='restrict', readonly=False)



    def add_action(self):
        self.action_show_warning()
        order_id = self._context.get('active_id')
        prix_total = self.quantity * self.prix_unitaire

        if order_id:
            order = self.env['sale.order'].browse(order_id)

            self.recompute()
            order_line = self.env['sale.order.line'].create({
                'order_id': order.id,
                'product_id': self.article.product_variant_id.id,
                #'product_template_id': self.article.id,
                'name':
                        'Accessoires: ' + str(self.get_accessoire()) + ', \n'
                        'Vitre: ' + str(self.vitre_radioD.name) +
                        ' ' + str(self.epaisseur_radioD.name) + ', '                                           
                        'Couleur:' + str(self.couleur_radioD.name) + ', \n'
                        'Largeur: ' + str(self.largeur) + ', '
                        'Hauteur: ' + str(self.hauteur) + ', \n'
                        'Prix de base: ' + str(self.prix),



                'discount': self.reduction,
                'price_unit': self.prix_unitaire,
                'product_uom_qty': self.quantity,
                'price_subtotal': prix_total,

            })
        return {'type': 'ir.actions.act_window_close'}

    def _compute_prix_unitaire(self):
        self.prix_unitaire = self.largeur/1000 * self.hauteur/1000 * self.prix

    def _compute_calculateur_prix_base(self):
        articl = self.article.name
        if (articl).endswith("plein bardage en ALU") or (articl).endswith("Métallique"):
            designation_article = self.env['product.pricelist.item'].search([('name', '=', self.article)])
            for val in designation_article:
                texte = 'Variante : ' + self.article.name + ' (' + str(self.couleur_radioD.name)
                if (val.name).startswith(texte):
                    self.prix = val.fixed_price
        else:
          designation_article = self.env['product.pricelist.item'].search([('name', '=', self.article)])
          for val in designation_article:
            texte = 'Variante : ' + self.article.name + ' (' + str(self.couleur_radioD.name) + ', ' + str(self.vitre_radioD.name)
            if (val.name).startswith(texte):
                self.prix = val.fixed_price

    def action_show_warning(self):
        if (len(self.article) == 0):
            raise UserError('Il faut choisir un article')
        articl = self.article.name
        if (articl).endswith("plein bardage en ALU") or (articl).endswith("Métallique"):
          if (len(self.couleur_radioD) == 0):
             raise UserError('La selection des variants vitrage et/ou couleur et/ou épaisseur est obligatoire')
          elif (self.hauteur == 0) or (self.largeur == 0):
            raise UserError('Les dimensions ne peuvent pas être nulles')
          elif self.reduction > 100:
            raise UserError('Désolé, la remise ne peut pas être supérieur à 100')
          elif not(self.poignee_clef or self.poignee or self.paumelle or self.compas or self.mecanisme or self.lames or self.division or self.serrure_auto or self.montant_liaison):
            raise UserError('Il faut choisir au moins un accesoire ! ')
        else:
            if (len(self.couleur_radioD) == 0) or (len(self.vitre_radioD) == 0) or (len(self.epaisseur_radioD) == 0):
                raise UserError('La selection des variants vitrage et/ou couleur et/ou épaisseur est obligatoire')
            elif (self.hauteur == 0) or (self.largeur == 0):
                raise UserError('Les dimensions ne peuvent pas être nulles')
            elif self.reduction > 100:
                raise UserError('Désolé, la remise ne peut pas être supérieur à 100')
            elif not (
                    self.poignee_clef or self.poignee or self.paumelle or self.compas or self.mecanisme or self.lames or self.division or self.serrure_auto or self.montant_liaison):
                raise UserError('Il faut choisir au moins un accesoire ! ')


    # @api.onchange('vitre')
    @api.onchange('article')
    def on_change_article(self):
        if self.article:
            self.recompute()
            self._compute_calculateur_prix_base()
            self._compute_prix_unitaire()

        else:
            self.prix = 0.0

    @api.onchange('couleur_radioD')
    def on_change_couleur(self):
        if self.article:
            self._compute_calculateur_prix_base()
            self._compute_prix_unitaire()
        else:
            self.prix = 0.0

    @api.onchange('vitre_radioD')
    def on_change_vitre(self):
        if self.article:
            self._compute_calculateur_prix_base()
            self._compute_prix_unitaire()
        else:
            self.prix = 0.0

    @api.onchange('largeur')
    def on_change_largeur(self):
        if self.largeur > 0:
            self._compute_prix_unitaire()
        else:
            self.prix_unitaire = 0.0

    @api.onchange('hauteur')
    def on_change_hauteur(self):
        if self.hauteur > 0:
            self._compute_prix_unitaire()
        else:
            self.prix_unitaire = 0.0

##champ porte/fenêtre en PVC
    largeurP = fields.Integer()
    hauteurP = fields.Integer()
    articleP = fields.Many2one('product.template', 'Article', domain="[('type_FAST', '=', 'pvc')]")

    quantityP = fields.Integer(default=1)
    reductionP = fields.Float(default=0.0)

    prixP = fields.Float()
    prix_unitaireP = fields.Float()

    poignee_clefP = fields.Boolean(string="Poignée à clef")
    poigneeP = fields.Boolean(string="Poignée")
    paumelleP = fields.Boolean(string="Paumelles")
    compasP = fields.Boolean(string="Compas")
    mecanismeP = fields.Boolean(string="Mécanisme")
    lamesP = fields.Boolean(string="Lames")
    divisionP = fields.Boolean(string="Divisions")
    serrure_autoP = fields.Boolean(string="Serrure auto")
    montant_liaisonP = fields.Boolean(string="Montant de liaison")

    def get_accessoireP(self):
     self.recompute()
     accessoire = []
     if self.poignee_clefP:
         accessoire.append('Poignée à clef')
     if self.poigneeP:
         accessoire.append('Poignée')
     if self.paumelleP:
        accessoire.append('Paumelles')
     if self.compasP:
        accessoire.append('Compas')
     if self.mecanismeP:
        accessoire.append('Mécanisme')
     if self.lamesP:
        accessoire.append('Lames')
     if self.divisionP:
        accessoire.append('Divisions')
     if self.serrure_autoP:
        accessoire.append('Serrure auto')
     if self.montant_liaisonP:
        accessoire.append('Montant de liaison')
     return accessoire





    @api.onchange('articleP')
    def onchange_articleP(self):
         self.couleurP_radioD = False
         self.vitreP_radioD = False
         self.epaisseurP_radioD = False
         if not self.articleP:
          self.prixP = 0.0


    couleurP_radioD = fields.Many2one('product.template.attribute.value', string="Couleur")
    vitreP_radioD = fields.Many2one('product.template.attribute.value', string="Vitrage")
    epaisseurP_radioD = fields.Many2one('product.template.attribute.value', string="Épaisseur")

    accesoryP_list_art = fields.Many2many('product.product', related='articleP.accessory_ids_fast', ondelete='restrict', readonly=False)


    def add_actionP(self):
      self.action_show_warningP()
      order_id = self._context.get('active_id')
      prix_total = self.quantityP * self.prix_unitaireP

      if order_id:
        order = self.env['sale.order'].browse(order_id)

        self.recompute()
        order_line = self.env['sale.order.line'].create({
            'order_id': order.id,
            'product_id': self.articleP.product_variant_id.id,

            'name':
                'Accessoires: ' + str(self.get_accessoireP()) + ', \n'
                'Vitre: ' + str(self.vitreP_radioD.name) +
                ' ' + str(self.epaisseurP_radioD.name) + ', '
                'Couleur: Blanc, \n'
                'Largeur: ' + str(self.largeurP) + ', '
                'Hauteur: ' + str(self.hauteurP) + ', \n'
                'Prix de base: ' + str(self.prixP),

            'discount': self.reductionP,
            'price_unit': self.prix_unitaireP,
            'product_uom_qty': self.quantityP,
            'price_subtotal': prix_total,

        })
      return {'type': 'ir.actions.act_window_close'}


    def _compute_prix_unitaireP(self):
      self.prix_unitaireP = self.largeurP / 1000 * self.hauteurP / 1000 * self.prixP


    def _compute_calculateur_prix_baseP(self):
      articl = self.articleP.name
      if (articl).endswith("plein bardage en PVC"):
        self.prixP = self.articleP.list_price
      else:
        designation_article = self.env['product.pricelist.item'].search([('name', '=', self.articleP)])

        for val in designation_article:
          texte = 'Variante : ' + self.articleP.name + ' (' + str(self.vitreP_radioD.name)

          if (val.name).startswith(texte):
            self.prixP = val.fixed_price


    def action_show_warningP(self):
        if (len(self.articleP) == 0):
            raise UserError('Il faut choisir un article')
        articl = self.articleP.name
        if (articl).endswith("plein bardage en PVC"):
            if (self.hauteurP == 0) or (self.largeurP == 0):
               raise UserError('Les dimensions ne peuvent pas être nulles')
            elif self.reductionP > 100:
               raise UserError('Désolé, la remise ne peut pas être supérieur à 100')
            elif not (self.poignee_clefP or self.poigneeP or self.paumelleP or self.compasP
                  or self.mecanismeP or self.lamesP or self.divisionP or self.serrure_autoP or self.montant_liaisonP):
               raise UserError('Il faut choisir au moins un accesoire ! ')
        else:
            if (len(self.vitreP_radioD) == 0) or (len(self.epaisseurP_radioD) == 0):
              raise UserError('La selection des variants vitrage et/ou couleur et/ou épaisseur est obligatoire')
            elif (self.hauteurP == 0) or (self.largeurP == 0):
              raise UserError('Les dimensions ne peuvent pas être nulles')
            elif self.reductionP > 100:
              raise UserError('Désolé, la remise ne peut pas être supérieur à 100')
            elif not (self.poignee_clefP or self.poigneeP or self.paumelleP or self.compasP
                or self.mecanismeP or self.lamesP or self.divisionP or self.serrure_autoP or self.montant_liaisonP):
              raise UserError('Il faut choisir au moins un accesoire ! ')


    @api.onchange('articleP')
    def on_change_articleP(self):
     if self.articleP:
        self.recompute()
        self._compute_calculateur_prix_baseP()
        self._compute_prix_unitaireP()

     else:
        self.prixP = 0.0


    @api.onchange('vitreP_radioD')
    def on_change_vitreP(self):
     if self.articleP:
        self._compute_calculateur_prix_baseP()
        self._compute_prix_unitaireP()
     else:
        self.prixP = 0.0


    @api.onchange('largeurP')
    def on_change_largeurP(self):
     if self.largeurP > 0:
        self._compute_prix_unitaireP()
     else:
        self.prix_unitaireP = 0.0


    @api.onchange('hauteurP')
    def on_change_hauteurP(self):
      if self.hauteurP > 0:
        self._compute_prix_unitaireP()
      else:
        self.prix_unitaireP = 0.0


    # is_vitr_empty = fields.Boolean(True)
    # def is_radio_empty(self):
    #    # nbr_atr = self.articleP.search_count([('attribute_id.name', '=', 'vitrage')])
    #    if len(self.vitreP_radioD.name) > 0:
    #        self.is_vitr_empty = False
    #
    #    else:
    #        self.is_vitr_empty = True






## Autres produits
    largeurA = fields.Integer(default=1000)
    longueurA = fields.Integer()
    articleA = fields.Many2one('product.template', 'Article', domain="['|', ('type_FAST', '=', 'inox'), ('type_FAST', '=', 'granite, placo')] ")

    quantityA = fields.Integer(default=1)
    reductionA = fields.Float(default=0.0)

    prixA = fields.Float()
    prix_unitaireA = fields.Float()

    is_inox = fields.Boolean(default=False)

    accesoryA_list_art = fields.Many2many('product.product', related='articleA.accessory_ids_fast', ondelete='restrict', readonly=False)

    def add_actionA(self):
        self.action_show_warningA()
        order_id = self._context.get('active_id')
        prix_total = self.quantityA * self.prix_unitaireA

        if not(self.is_inox):
          if order_id:
            order = self.env['sale.order'].browse(order_id)

            self.recompute()
            order_line = self.env['sale.order.line'].create({
                'order_id': order.id,
                'product_id': self.articleA.product_variant_id.id,

                'name':
                    'Largeur: ' + str(self.largeurA) + ', '
                    'Longueur: ' + str(self.longueurA) + ', \n'
                    'Prix de base: ' + str(self.prixA),

                'discount': self.reductionA,
                'price_unit': self.prix_unitaireA,
                'product_uom_qty': self.quantityA,
                'price_subtotal': prix_total,

            })
          return {'type': 'ir.actions.act_window_close'}
        else:
            if order_id:
                order = self.env['sale.order'].browse(order_id)

                self.recompute()
                order_line = self.env['sale.order.line'].create({
                    'order_id': order.id,
                    'product_id': self.articleA.product_variant_id.id,

                    'name':
                         'Longueur: ' + str(self.longueurA) + ', \n'
                         'Prix de base: ' + str(self.prixA),
                    'discount': self.reductionA,
                    'price_unit': self.prix_unitaireA,
                    'product_uom_qty': self.quantityA,
                    'price_subtotal': prix_total,

                })
            return {'type': 'ir.actions.act_window_close'}

    def action_show_warningA(self):
            if (len(self.articleA) == 0):
              raise UserError('Il faut choisir un article')

            if (self.longueurA == 0):
               raise UserError('Les dimensions ne peuvent pas être nulles')
            elif self.reductionA > 100:
               raise UserError('Désolé, la remise ne peut pas être supérieur à 100')

    @api.onchange('articleA')
    def on_change_articleA(self):
     if self.articleA:
        #self.recompute()
        self._compute_calculateur_prix_baseA()
        self._compute_prix_unitaireA()
        self.inox_or_not()
        #self.recompute()

    def _compute_prix_unitaireA(self):
      self.prix_unitaireA = (self.largeurA / 1000) * (self.longueurA / 1000) * self.prixA


    def _compute_calculateur_prix_baseA(self):
        self.prixA = self.articleA.list_price

    @api.onchange('largeurA')
    def on_change_largeurA(self):
     if self.largeurA > 0:
        self._compute_prix_unitaireA()
     else:
        self.prix_unitaireA = 0.0


    @api.onchange('longueurA')
    def on_change_longueurA(self):
      if self.longueurA > 0:
        self._compute_prix_unitaireA()
      else:
        self.prix_unitaireA = 0.0




    #Category_id = fields.Many2one('product.category', 'Catégorie du matériel', related='articleA.categ_id')

    def inox_or_not(self):
        if (self.articleA.type_FAST == 'inox'):

            self.is_inox = True

        elif (self.articleA.type_FAST == 'granite, placo'):
            self.is_inox = False


