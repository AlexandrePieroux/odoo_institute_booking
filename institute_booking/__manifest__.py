{
    'name': 'Institute Booking System',
    'category': 'Website/Website',
    'sequence': 50,
    'summary': 'Allow clients to book for services appointment',
    'version': '1.0',
    'depends': [
        'website_sale',
        'calendar'
    ],
    'data': [
        'data/data.xml',
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'web.public.bundle',
            'https://cdn.jsdelivr.net/npm/fullcalendar@6.1.18/index.global.min.js',
            'institute_booking/static/src/js/booking_calendar.js',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}