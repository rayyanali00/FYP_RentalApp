function hideLoader() {
    $(".spinner-border").hide();
}

function dateToStrDt(date) {
    let newDate = new Date(date);
    newDate.setDate(newDate.getDate() + 1);

    let month = newDate.getMonth() + 1;
    month = month.toString();

    let day = newDate.getDate();
    day = day.toString();

    if (month.length == 1) {
        month = "0" + month;
    }
    if (day.length == 1) {
        day = "0" + day;
    }

    let dateStr = newDate.getFullYear() + "-" + month + "-" + day;
    return dateStr;
}

function loadRecordsInDataTable(dateCol, expArr, apiUrl, responseArrCols, tableId) {
    let records;
    const request = new XMLHttpRequest();
    request.addEventListener('readystatechange', () => {
        if (request.readyState === 4 && request.status === 200) {
            records = JSON.parse(request.responseText);
            console.log(records[0]);
            hideLoader();
            drawDataTable(dateCol, expArr, responseArrCols, records, tableId);
        }
    })
    request.open('GET', apiUrl);
    request.send();
}