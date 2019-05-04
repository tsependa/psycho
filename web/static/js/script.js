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


var app = new Vue({
    el: '#app',
    delimiters: ['${', '}'],
    data: {
        themes: [],
        specialists: [],
        timeslots: [],
        loading: false,
        selectedTheme: {},
        selectedSpecialist: {},
        selectedTimeslot: {},
        message: null,
        showSuccess: false,
        step: 0,
        promos: [
            {img: 'img/svg/1.svg', text: 'Хотите изменить отношения с любимым человеком'},
            {img: 'img/svg/2.svg', text: 'Найти спутника жизни'},
            {img: 'img/svg/3.svg', text: 'Страдаете от низкой самооценки'},
            {img: 'img/svg/4.svg', text: 'Потеряли интерес к жизни'},
            {img: 'img/svg/5.svg', text: 'Должны принять сложное решение, но вы не знаете, как поступить'},
            {img: 'img/svg/6.svg', text: 'Испытываете страх или тревогу'},
            {img: 'img/svg/7.svg', text: 'Тяжело переживаете развод или разрыв отношений'},
            {img: 'img/svg/8.svg', text: 'Потеряли близкого человека'},
            {img: 'img/svg/9.svg', text: 'Находитесь в состоянии депрессии'},
            {img: 'img/svg/10.svg', text: 'Устали от стресса на работе'},
            {img: 'img/svg/11.svg', text: 'Воспитываете ребенка'}
        ],
        consult: [
            {img: ['img/svg/busy.svg'], text: '1 час длится консультация'},
            {img: ['img/svg/tablet.svg'], text: 'Подключение по телефону, планшету или компьютеру'},
            {img: ['img/svg/debit-card.svg'], text: 'Оплата онлайн с помощью карты'},
            {img: ['img/svg/distance.svg'], text: '5-6 консультаций длится средняя терапия'},
            {img: ['img/svg/Shield.svg'], text: '100% конфиденциально'},
            {img: ['img/svg/ruble.svg'], text: 'Стоимость 3 400'},

        ],
        features: [
            {
                img: ['img/logo/logo_ps.svg', 'img/svg/moscow.svg'],
                title: '',
                text: 'Все специалисты нашего сервиса являются сотрудниками Московской службы психологической помощи населению Департамента труда и социальной защиты населения города Москвы  \n'
            },
            {img: ['img/svg/map.svg'], title: '', text: '23 очных отделения в Москве и МО'},
            {
                img: ['img/svg/psychologist.svg'],
                title: '',
                text: 'Более <b class=\"font-weight-bold\">1000</b> консультаций в день'
            },
            {
                img: ['img/svg/search.svg'],
                title: 'Решение за Вами',
                text: "Выберите психолога сами"
            },
            {
                img: ['img/svg/gears.svg'],
                title: 'Все автоматизировано',
                text: 'Общение только с психологом',
            },
            {img: ['img/svg/online.svg'], title: 'Онлайн', text: 'В удобное время <br> В удобном месте'},
            {
                img: ['img/svg/employee.svg'],
                title: '',
                text: 'Все <b class=\"font-weight-bold\">специалисты</b> регулярно проходят <b class=\"font-weight-bold\">супервизии</b>'
            },
            {
                img: ['img/svg/goal.svg'],
                title: '',
                text: "Нацелены на <b class=\"font-weight-bold\">результат</b>, а не просто выслушать"
            },

        ],


    },
    mounted: function () {

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

        selectTheme: function (event) {
            this.step = 2;
            this.selectedSpecialist = {};

        },

        selectSpecialist: function (event) {
            this.step = 2;
            this.selectedSpecialist = {};

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

        magicPayment: function () {
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

        }
    }

});


/*const cleaveCreditCard = new Cleave('.input-card', {
    creditCard: true
});*/

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

var csrftoken = readCookie('csrftoken');



