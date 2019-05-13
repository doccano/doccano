export const toPercent = (val) => {
    return parseFloat(val * 100).toFixed(2) + '%'
}

const addZero = (str) => {
    return ('0'+str).substr(-2)
}

export const parseDate = (date) => {
    const dateParsed = new Date(date)
    return dateParsed.getFullYear() + "/" + (dateParsed.getMonth() + 1) + "/" + dateParsed.getDate() + " " + addZero(dateParsed.getHours()) + ":" + addZero(dateParsed.getMinutes()) + ":" + addZero(dateParsed.getSeconds()) 
}