from werkzeug.exceptions import NotFound

from odoo.http import request, route
from odoo.tools import float_round, lazy
from odoo.addons.payment.controllers import portal
from odoo.addons.website_sale.contollers.main import TableCompute
from odoo.addons.website.controllers.main import QueryURL


class InstituteBooking(portal.PaymentPortal):
    @route(['/booking'], type='http', auth="public", website=True)
    def booking(self, page=0, ppg=False, search='', category=None, **post):
        if not request.website.has_ecommerce_access():
            return request.redirect('/web/login')

        Category = request.env['product.public.category']
        if category:
            category = Category.search([('id', '=', int(category))], limit=1)
            if not category or not category.can_access_from_current_website():
                raise NotFound()
        else:
            category = Category

        website = request.env['website'].get_current_website()
        if ppg:
            try:
                ppg = int(ppg)
                post['ppg'] = ppg
            except ValueError:
                ppg = False
        if not ppg:
            ppg = website.shop_ppg or 20

        gap = website.shop_gap or "16px"
        ppr = website.shop_ppr or 4

        keep = QueryURL(
            '/booking',
            {
                'search': search,
                'category': category and int(category),
            }
        )

        if search:
            post['search'] = search

        options = {
            'displayDescription': True,
            'displayDetail': True,
            'displayExtraDetail': True,
            'displayExtraLink': True,
            'displayImage': True,
            'allowFuzzy': not post.get('noFuzzy'),
            'category': str(category.id) if category else None,
            'display_currency': post.get('display_currency'),
        }

        order = post.get('order') or request.env['website'].get_current_website().shop_default_sort
        order_query = f'is_published desc, {order}, id desc'
        product_count, details, fuzzy_search_term = website._search_with_fuzzy(
            "products_only",
            search,
            limit=None,
            order=order_query,
            options=options
        )
        search_product = details[0].get('results', request.env['product.template']).with_context(bin_size=True)

        url = '/booking'
        if category:
            url += f'/category/{request.env["ir.http"]._slug(category)}' 

        pager = website.pager(url=url, total=product_count, page=page, step=ppg, scope=5, url_args=post)
        offset = pager['offset']
        products = search_product[offset:offset+ppg]
        products_prices = lazy(lambda: products._get_sales_prices(website))

        website_domain = website.website_domain()
        categs_domain = [('parent_id', '=', False)] + website_domain
        if search:
            search_categories = Category.search(
                [('product_tmpl_ids', 'in', search_product.ids)] + website_domain
            ).parents_and_self
            categs_domain.append(('id', 'in', search_categories.ids))
        else:
            search_categories = Category
        categs = lazy(lambda: Category.search(categs_domain))

        return request.render(
            "institute_booking.services",
            {
                'search': fuzzy_search_term or search,
                'original_search': fuzzy_search_term and search,
                'order': post.get('order', ''),
                'products': products,
                'search_product': search_product,
                'search_count': product_count,
                'bins': lazy(lambda: TableCompute().process(products, ppg, ppr)),
                'gap': gap,
                'category': category,
                'categories': categs,
                'keep': keep,
                'search_categories_ids': search_categories.ids,
                'products_prices': products_prices,
                'get_product_prices': lambda product: lazy(lambda: products_prices[product.id]),
                'float_round': float_round,
            }
        )
