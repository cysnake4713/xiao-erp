# -*- coding: utf-8 -*-
# author: cysnake4713
#

from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class RenumberWizard(models.Model):
    _inherit = 'wizard.renumber'

    _defaults = {
        'is_draft': True,
    }
