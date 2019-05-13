moment.locale('ru');  // Set the default/global locale


var app = new Vue({
    el: '#consultation',
    delimiters: ['${', '}'],
    data: {

        selectedTimeslot: {},

        timeslots: [],
        loading: false,



    },

    mounted: function () {
        this.getTimeSlots();
    },
    methods: {

         getTimeSlots: function () {
            this.loading = true;
            this.$http.get('/api/timeslots/' + document.getElementsByClassName('profile')[0].id)
                .then((response) => {
                    this.timeslots = response.data;
                    this.loading = false;
                })
                .catch((err) => {
                    this.loading = false;
                    console.log(err);
                })
        },
        slotsAggr: function (timeslots) {
            return timeslots.reduce((r, e) => {
                (r[e.date] = r[e.date] || []).push(e)
                return r;
            }, {})

        },

        selectTimeslot: function (timeslot) {
            this.selectedTimeslot = timeslot;
            console.log(timeslot)
        },


    },
    computed: {
        slotsByDate() {
            return this.timeslots.reduce((r, e) => {
                (r[e.date] = r[e.date] || []).push(e)
                return r;
            }, {})

        },

    }

});

function isEmpty(obj) {
    for (let key in obj) {
        // if the loop has started, there is a property
        return false;
    }
    return true;
}


Vue.filter('formatDate', function (value) {
    if (value) {
        return moment(String(value)).format('MM/DD/YYYY')
    }
});

Vue.filter('formatTime', function (value) {
    if (value) {
        return moment(String(value)).format('HH:mm')
    }
});

Vue.filter('formatDay', function (value) {
    if (value) {
        return moment(String(value)).format('DD MMM')
    }
});

