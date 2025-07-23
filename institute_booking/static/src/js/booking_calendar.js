import publicWidget from "@web/legacy/js/public/public_widget";


publicWidget.registry.BookingCalendar = publicWidget.Widget.extend({
    selector: '#booking_calendar',
    start: function () {
        console.log('BookingCalendar JS chargé');
        console.log('FullCalendar:', typeof FullCalendar);
        console.log('Div calendar:', this.el);
        var self = this;

        // Charger FullCalendar CSS/JS si besoin (à ajouter dans assets du manifest)
        // Initialiser FullCalendar
        var calendarEl = this.el;
        var selectedDate = null;

        var calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            locale: 'fr',
            selectable: true,
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: ''
            },
            dateClick: function(info) {
                selectedDate = info.dateStr;
                // Mettre à jour le bouton "Suivant"
                $('#booking_next').prop('disabled', false);
            },
            // Optionnel : charger les créneaux disponibles via AJAX
            // events: function(fetchInfo, successCallback, failureCallback) {
            //     ajax.jsonRpc('/booking/slots', 'call', {
            //         start: fetchInfo.startStr,
            //         end: fetchInfo.endStr,
            //     }).then(function(events){
            //         successCallback(events);
            //     });
            // },
        });

        calendar.render();

        // Désactive le bouton "Suivant" au départ
        $('#booking_next').prop('disabled', true);

        // Gestion du clic sur "Suivant"
        $('#booking_next').off('click').on('click', function () {
            if (selectedDate) {
                window.location.href = '/booking/payment?date=' + selectedDate;
            }
        });

        return this._super.apply(this, arguments);
    },
});

export default publicWidget.registry.BookingCalendar;
