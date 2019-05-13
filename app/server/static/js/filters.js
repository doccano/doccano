export const toPercent = (val) => {
    return parseFloat(val * 100).toFixed(2)
}

export const parseDate = (date) => {
    const dateParsed = new Date(date)
    return dateParsed.getFullYear() + "/" + (dateParsed.getMonth() + 1) + "/" + dateParsed.getDate() + " " + dateParsed.getHours() + ":" + dateParsed.getMinutes() + ":" + dateParsed.getSeconds() 
}