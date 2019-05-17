Vue.filter('formatDate', function (value) {
    if (value) {
        return moment(String(value)).format('MM/DD/YYYY')
    }
});

Vue.filter('formatTime', function (value) {
    if (value) {
        return moment(String(value)).locale('ru').format('HH:mm')
    }
});

Vue.filter('dayOfWeek', function (value) {
    if (value) {
        return moment(String(value)).locale('ru').format('dd')
    }
});

Vue.filter('day', function (value) {
    if (value) {
        return moment(String(value)).locale('ru').format('DD')
    }
});

Vue.filter('month', function (value) {
    if (value) {
        return moment(String(value)).locale('ru').format('MMM')
    }
});

Vue.filter('formatDiff', function (value) {
    if (value) {
        return moment(String(value)).locale('ru').fromNow();
    }
});


const app2 = new Vue({
        el: '#adm_app',
        delimiters: ['${', '}'],
        data: {
            user_enrolls: [],
            specialist_enrolls: [],
            timeslots: [],
            specialist_id: null,
            slotsByDateMap: [],
            editSlot: {},

        },
        methods: {
            getUserEnrolls: function () {
                this.loading = true;
                this.$http.get('/api/enroll/')
                    .then((response) => {
                        this.user_enrolls = response.data;
                        this.loading = false;
                    })
                    .catch((err) => {
                        this.loading = false;
                        console.log(err);
                    })
            },

            getSpecialistEnrolls: function () {
                this.loading = true;
                this.$http.get('/api/enrollspec/')
                    .then((response) => {
                        this.specialist_enrolls = response.data;
                        this.loading = false;
                    })
                    .catch((err) => {
                        this.loading = false;
                        console.log(err);
                    })
            },


            getSpecialistTimeslots: function () {
                this.loading = true;
                this.$http.get('/api/timeslots/' + readCookie('specialist_id') + '/')
                    .then((response) => {
                        this.timeslots = response.data;
                        this.loading = false;
                    })
                    .catch((err) => {
                        this.loading = false;
                        console.log(err);
                    })
            },

            getSlotsByDateMap: function () {
                this.loading = true;
                this.slotsByDateMap = [];
                for (var day = 0; day < 15; day++) {
                    var today = new Date();
                    today.setHours(0, 0, 0, 0);
                    today.setDate(today.getDate() + day);
                    for (var hour = 9; hour < 23; hour++) {
                        cur_time = new Date(today.getFullYear(), today.getMonth(), today.getDate(), hour, 0, 0);

                        var existingSlot = this.timeslots.find(o => {
                            return moment(o.start_time).format('MM/DD/YYYY HH') === moment(cur_time).format('MM/DD/YYYY HH')
                        });

                        if (typeof existingSlot !== "undefined") {
                            existingSlot.date = moment(existingSlot.start_time).format('MM/DD/YYYY');
                            existingSlot.time = moment(existingSlot.start_time).format('HH:mm');
                            this.slotsByDateMap.push(existingSlot)
                        } else {

                            var curTimeSlot = {
                                date: moment(cur_time).format('MM/DD/YYYY'),
                                time: moment(cur_time).format('HH:mm'),
                                duration: 60,
                                start_time: cur_time.toISOString().split('.')[0] + "Z",
                                /* id: existingSlot.id,*/
                            };

                            this.slotsByDateMap.push(curTimeSlot)
                        }
                    }


                }
                this.loading = false;

            },

            xxxTimeSlot: function (timeslot) {
                this.editSlot = timeslot;
                $("#editTimeSlotModal").modal('show');
            },

            editTimeSlot: function (timeslot) {
                this.editSlot = timeslot;
                this.loading = true;

                if (this.editSlot.id === undefined) {
                    this.$http.post('/api/timeslot/', {
                        "specialist": s_id,
                        "start_time": this.editSlot.start_time,
                    }, {
                        headers:
                            {"X-CSRFToken": csrftoken}
                    },)
                        .then((response) => {

                            this.timeslots.push(response.data);
                            this.loading = false;
                        })
                        .catch((err) => {
                            this.loading = false;
                            console.log(err);
                        })
                } else {
                    this.$http.delete('/api/timeslot/' + this.editSlot.id, {
                        headers:
                            {"X-CSRFToken": csrftoken}
                    },).then((response) => {
                        var index = this.timeslots.indexOf(this.editSlot);
                        this.timeslots.splice(index, 1);
                        this.loading = false;
                    })
                        .catch((err) => {
                            this.loading = false;
                            console.log(err);
                        })
                }

            },
            setEditSlot: function () {

            }
        },
        mounted: function () {
            this.specialist_id = s_id;
            this.getUserEnrolls();
            this.getSpecialistTimeslots();
            this.getSpecialistEnrolls();


        },

        computed: {
            slotsByDate() {
                this.getSlotsByDateMap();
                return this.slotsByDateMap.reduce((r, e) => {
                    (r[e.date] = r[e.date] || []).push(e)
                    return r;
                }, {})

            },
        }

    })
;



function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

var s_id = readCookie('specialist_id');

var csrftoken = readCookie('csrftoken');
