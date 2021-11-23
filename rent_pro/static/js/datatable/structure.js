function drawDataTable(dateCol, expArr, responseArrCols, records, tableId) {

    var table;
    let initialDateCol = dateCol;

    table = $(tableId).DataTable({
        data: records,
        deferRender: true,
        columns: responseArrCols,
        columnDefs: [{
            "defaultContent": "-",
            "targets": "_all"
        }],
        "order": [
            [1, "asc"]
        ],
        select: {
            style: 'multi'
        },
        dom: 'lBfrtip',
        buttons: [{
                extend: 'copy',
                exportOptions: {
                    columns: expArr
                }
            },
            {
                extend: 'excel',
                exportOptions: {
                    columns: expArr
                }
            },
            {
                extend: 'csv',
                exportOptions: {
                    columns: expArr
                }
            },
            {
                extend: 'print',
                exportOptions: {
                    columns: expArr
                }
            }
        ],
        initComplete: function() {
            let $buttons = $('.dt-buttons').hide();
            $('#exportLink').on('change', function() {
                let btnClass = $(this).find(":selected")[0].id ?
                    '.buttons-' + $(this).find(":selected")[0].id :
                    null;
                if (btnClass) $buttons.find(btnClass).click();
            })
        }
    });

    $("#date-cols").on("change", function() {
        dateCol = this.value;

        if (dateCol == "hide") {
            dateCol = initialDateCol;
            $('#datepicker_from').val('').attr('type', 'date');
            $('#datepicker_to').val('').attr('type', 'date');
            $("#date_filter").hide()
        } else {
            $('#datepicker_from').val('').attr('type', 'date');
            $('#datepicker_to').val('').attr('type', 'date');
            $("#date_filter").show();
        }
        table.draw();
    })

    $('#datepicker_from').change(function() {
        let fromMin = document.getElementById('datepicker_from').value;
        fromMin = dateToStrDt(fromMin);
        document.getElementById("datepicker_to").setAttribute("min", fromMin);
        table.draw();
    });

    $('#datepicker_to').change(function() {
        table.draw();
    });

    $(".loader").hide()
    $(".options").hide()
    $(".toggle-options").on("click", function() {
        $(".options").slideToggle(500, "linear");
    })
    $("tr").on("click", function() {
        console.log(table.row(this).data());
    })

    $('.dataTables_filter input').unbind().keyup(function(e) {
        var value = $(this).val();
        if (value.length > 3) {
            table.search(value).draw();
        } else {
            //optional, reset the search if the phrase 
            //is less then 3 characters long
            table.search('').draw();
        }
    });

    $.fn.dataTable.moment = function(format, locale) {
        var types = $.fn.dataTable.ext.type;

        // Add type detection
        types.detect.unshift(function(d) {
            return moment(d, format, locale, true).isValid() ?
                'moment-' + format :
                null;
        });

        // Add sorting method - use an integer for the sorting
        types.order['moment-' + format + '-pre'] = function(d) {
            return moment(d, format, locale, true).unix();
        };
    };

    $.fn.dataTableExt.afnFiltering.push(
        function(oSettings, aData, iDataIndex) {
            var iFini = document.getElementById('datepicker_from').value;
            var iFfin = document.getElementById('datepicker_to').value;

            var iStartDateCol = parseInt(dateCol);

            if (iFini != "" && iFfin == "") {
                iFini = new Date(iFini);
                iFini = new Date(iFini.setHours(iFini.getHours() + 4));
            } else if (iFini == "" && iFfin != "") {
                iFfin = new Date(iFfin);
                iFfin = new Date(iFfin.setHours(iFfin.getHours() + 5));
                iFfin = new Date(iFfin.setHours(iFfin.getHours() + 5));
            } else if (iFini != "" && iFfin != "") {
                iFini = new Date(iFini);
                iFfin = new Date(iFfin);
                iFfin = new Date(iFfin.setHours(iFfin.getHours() + 5));

                iFini = new Date(iFini.setHours(iFini.getHours() + 4));
                iFfin = new Date(iFfin.setHours(iFfin.getHours() + 5));
            }


            var datofini = aData[iStartDateCol].substring(0, 2) + "-" + aData[iStartDateCol].substring(3, 5) + "-" + aData[iStartDateCol].substring(6, 10);
            datofini = moment(datofini, "MM DD YYYY").toDate();
            if (datofini == "Invalid Date") {
                return false;
            }
            if (iFini && !isNaN(iFini)) {
                if (datofini < iFini) {
                    return false;
                }
            }

            if (iFfin && !isNaN(iFfin)) {
                if (datofini > iFfin) {
                    return false;
                }
            }
            return true;
        }
    );
}