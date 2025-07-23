from odoo.http import request, route
from odoo.addons.payment.controllers import portal

import logging
_logger = logging.getLogger(__name__)

class InstituteBooking(portal.PaymentPortal):
    @route('/booking', type='http', auth='public', website=True)
    def booking_page(self, **kw):
        categories = request.env['product.product'].sudo().search([
            ('type', '=', 'service'), 
            ('website_published', '=', True)
        ])
        _logger.info("Available services: %s", categories.mapped('name'))
        return request.render('institute_booking.services', {
            'services': categories,
        })
