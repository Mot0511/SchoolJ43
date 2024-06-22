let begin = ''
let end = ''

const get_monday_date = (date) => {
    const weekday = moment().day()
    date.subtract(weekday - 1, 'd')
    return date
}

const init = () => {
    const url = new URL(window.location.href).searchParams

    const date = url.has('date') ? moment(url.get('date'), 'DD.MM.YYYY') : get_monday_date(moment())

    begin = date.format('DD.MM.YYYY')
    end = date.add(6, 'd').format('DD.MM.YYYY')

    document.getElementById('date').innerHTML = `${begin} - ${end}`

    console.log(moment().day())
}



const nextWeek = () => {
    const date = moment(end, 'DD.MM.YYYY')
    const next_date = date.add(1, 'd').format('DD.MM.YYYY')

    window.location.replace(`/diary?date=${next_date}`);
}

const lastWeek = () => {
    const date = moment(begin, 'DD.MM.YYYY')
    const last_date = date.subtract(7, 'd').format('DD.MM.YYYY')

    window.location.replace(`/diary?date=${last_date}`);
}

init()