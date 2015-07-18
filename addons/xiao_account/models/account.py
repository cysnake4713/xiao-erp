# -*- coding: utf-8 -*-
# author: cysnake4713
#

from openerp import tools, exceptions
from openerp import models, fields, api
from openerp.tools.translate import _


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def create(self, vals):
        move = super(AccountMove, self).create(vals)
        if move.journal_id and move.journal_id.sequence_id:
            context = dict(self.env.context)
            context.update({'fiscalyear_id': move.period_id.fiscalyear_id.id})
            move.name = self.pool.get('ir.sequence').next_by_id(self.env.cr, self.env.uid, move.journal_id.sequence_id.id, context)
        else:
            raise exceptions.ValidationError(_('Error!'), _('Please define a sequence on the journal.'))
        return move
