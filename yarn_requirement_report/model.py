#-*- coding:utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 OpenERP SA (<http://openerp.com>). All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api

class YarnRequirementReport(models.AbstractModel):
    _name = 'report.yarn_requirement_report.yarn_requirement'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('yarn_requirement_report.yarn_requirement')
        records = self.env['yarn.requirement'].browse(docids)

        entries = []
        for x in records.tree_link:
            if x.product not in entries:
                entries.append(x.product)

        def getrate(prod):
            element = ' '
            for x in records.tree_link:
                if x.product == prod:
                    if x.appr_rate.name:
                        element = '(' + x.appr_rate.name + ')'
                    if x.appr_rate.rate:
                        element = element + ' ' + str(x.appr_rate.rate)
                    return element

        def getbags(prod):
            bags = 0
            for x in records.tree_link:
                if x.product == prod:
                    if x.nob:
                        bags = bags + x.nob

            return bags

        def getworkorders(prod):
            workorder = []
            workorders = ' '
            for x in records.tree_link:
                if x.product == prod:
                    if x.won.name not in workorder:
                        if x.won.name:
                            workorder.append(x.won.name)

            for x in workorder:
                workorders = workorders + str(x) + ", "

            return workorders

        def getbuyers(prod):
            buyer = []
            buyers = ' '
            for x in records.tree_link:
                if x.product == prod:
                    if x.buyer.name not in buyer:
                        if x.buyer.name:
                            buyer.append(x.buyer.name)

            for x in buyer:
                buyers = buyers + str(x) + ", "

            return buyers

        def getprodtype(prod):
            prodtype = []
            prodtypes = ' '

            for x in records.tree_link:
                if x.product == prod:
                    if x.prod_type.name not in prodtype:
                        if x.prod_type.name:
                            prodtype.append(x.prod_type.name)

            for x in prodtype:
                prodtypes = prodtypes + str(x) + ", "

            return prodtypes

        def getdate(prod):
            dates = []
            delivery = ' '

            for x in records.tree_link:
                if x.product == prod:
                    if x.delv_date not in dates:
                        dates.append(x.delv_date)

            for x in dates:
                delivery = delivery + str(x) + ', '

            return delivery

        docargs = {
            'doc_ids': docids,
            'doc_model': 'yarn.requirement',
            'docs': records,
            'data': data,
            'entries': entries,
            'getrate': getrate,
            'getbags': getbags,
            'getworkorders': getworkorders,
            'getbuyers': getbuyers,
            'getprodtype': getprodtype,
            'getdate': getdate
            }

        return report_obj.render('yarn_requirement_report.yarn_requirement', docargs)