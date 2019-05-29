moment.locale('ru');  // Set the default/global locale


var app = new Vue({
    el: '#select_app',
    delimiters: ['${', '}'],
    data: {
        selectedTheme: {},
        selectedExps: {value: 'от 5 лет', start: 0, checked: 'checked'},
        selectedGender: "",
        selectedSpecialist: {},
        selectedTimeslot: {},


        themes: [],
        specialists: [],
        timeslots: [],
        methods: [],
        loading: false,

        message: null,
        showSuccess: false,
        showPopup: false,


    },

    mounted: function () {
/*        this.getThemes();
        this.getSpecialists();*/

        /*this.getMethods();*/


    },
    methods: {
        getThemes: function () {
            this.loading = true;
            this.$http.get('/api/theme/')
                .then((response) => {
                    this.themes = response.data;
                    this.loading = false;
                })
                .catch((err) => {
                    this.loading = false;
                    console.log(err);
                })
        },

        getSpecialists: function () {
            this.loading = true;
            this.$http.get('/api/specialist/')
                .then((response) => {
                    this.specialists = response.data;
                    this.loading = false;
                })
                .catch((err) => {
                    this.loading = false;
                    console.log(err);
                })
        },

        getMethods: function () {
            this.loading = true;
            this.$http.get('/api/method/')
                .then((response) => {
                    this.methods = response.data;
                    this.loading = false;
                })
                .catch((err) => {
                    this.loading = false;
                    console.log(err);
                })
        },


        selectSpecialist: function (specialist) {
            this.selectedSpecialist = specialist;
            /*  #$('#modalSpecialistForm').modal('show');*/


        },

        getTimeSlots: function () {
            this.loading = true;
            this.$http.get('/api/readTimeSlot/')
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

        filteredSpecialists() {
            let filteredThemeSpecialists = this.specialists.filter((specialist) => {
                    if (isEmpty(this.selectedTheme)) {
                        return true;
                    } else {
                        return specialist.themes.map(theme => theme.id).includes(this.selectedTheme.id);

                    }
                }
            );

            let filteredExpSpecialists = filteredThemeSpecialists.filter((specialist) => {
                return specialist.experience > this.selectedExps.start;
            });

            let filteredGenderSpecialists = filteredExpSpecialists.filter((specialist) => {
                if (isEmpty(this.selectedGender)) {
                    return true;
                } else {
                    return specialist.gender === this.selectedGender;
                }
            });


            return filteredGenderSpecialists;
        },

        experienceList() {
            return [
                {value: 'от 5 лет', start: 5, checked: 'checked'},
                {value: 'от 10 лет', start: 10,},
                {value: 'от 15 лет', start: 15,},
                {value: 'более 20 лет', start: 20,},

            ]
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

Vue.filter('formatDayPretty', function (value) {
    if (value) {
        return moment(String(value)).format('DD MMM HH:mm')
    }
});
