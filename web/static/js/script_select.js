var app = new Vue({
    el: '#select_app',
    delimiters: ['${', '}'],
    data: {
        selectedThemes: [],
        selectedExps: {value: 'от 5 лет', start: 6, checked: 'checked'},
        selectedMethods: [],
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
        this.getThemes();
        this.getSpecialists();
        this.getMethods();
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
            this.$http.get('/api/timeslot/' + this.selectedSpecialist.id)
                .then((response) => {
                    this.timeslots = response.data;
                    this.loading = false;
                })
                .catch((err) => {
                    this.loading = false;
                    console.log(err);
                })
        },

        registerUser: function () {
            this.$http.post('/api/user/', {
                    username: 'tsependa_s1@mail.ru',
                    email: 'tsependa_s1@mail.ru',
                    password: '123456',
                }, {
                    headers:
                        {"X-CSRFToken": csrftoken}
                },
                {emulateJSON: true})
                .then((response) => {
                    console.log(response.data);
                });
            window.location = "/office";
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
                return this.selectedThemes.every(i => specialist.themes.includes(i))
            });

            let filteredExpSpecialists = filteredThemeSpecialists.filter((specialist) => {

                return specialist.experience > this.selectedExps.start;
            });
            return filteredExpSpecialists;
        },

        experienceList() {
            return [
                {value: 'от 5 лет', start: 6, checked: 'checked'},
                {value: 'от 10 лет', start: 11,},
                {value: 'от 15 лет', start: 16,},
                {value: 'более 20 лет', start: 21,},

            ]
        },

    }

});



