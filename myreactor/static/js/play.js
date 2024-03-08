$(document).ready(function () {
    interval_id = null;
    t = 0;

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
            }
        }
    });

    $("body").keydown(function (e) {
        if (e.key == "ArrowDown") {
            $("#cool-btn").click();
        }
        else if (e.key == "ArrowUp") {
            $("#heat-btn").click();
        }
        else if (e.key == "ArrowLeft") {
            data.mdot -= data.Dmdot
            if (data.mdot < 0) {
                data.mdot = 0.0
            }
        }
        else if (e.key == "ArrowRight") {
            data.mdot += data.Dmdot
        }
    });

    $("#cool-btn").click(function () {
        if (data.Tjset > 5+273) {
            data.Tjset -= 1;
        }
    });

    $("#heat-btn").click(function () {
        if (data.Tjset < 180+273) {
            data.Tjset += 1;
        }
    });

    interval_id = setInterval(function () {
        $.ajax({
            url: $("#plots").attr("data-url"),
            type: 'post',
            data: data,
            dataType: 'json',
            success: function (newdata) {
                data = newdata;
                console.log(data)
                t += 1;

                temperatures.series[0].addPoint(data.T-273);
                temperatures.series[1].addPoint(data.Tj-273);
                temperatures.series[2].addPoint(data.Tjset-273)
                concentrations.series[0].addPoint(data.CA);
                concentrations.series[1].addPoint(data.CB);
                concentrations.series[2].addPoint(data.CC);
                concentrations.series[3].addPoint(data.CD);
                concentrations.series[4].addPoint(data.CE);
                $("#tj-display").html(
                    "T<sub>j,c</sub> = " + Number((data.Tjset-273).toFixed(2)).toString() + " °C / " +
                    '<span style="color:#069">T<sub>r</sub> = ' + Number((data.T-273).toFixed(2)).toString() + " °C"
                );
                $("#X-display").html("X = " + Number((data.X * 100).toFixed(2)).toString() + " %")
                $("#mdot-display").html("débit = " + Number((data.mdot).toFixed(2)).toString() + " g/s")

                if (data.X >= 0.95 && data.T < 168+273) {
                    // Victoire
                    clearInterval(interval_id);
                    $("#victoire").modal("show");
                    $.ajax({
                        url: $("#plots").attr("data-url") + "score/",
                        type: 'post',
                        data: {
                            "player": data.playerid,
                            "t": t,
                            "X": data.X
                        },
                        dataType: 'json',
                        success: function (data) {
                        }
                    });
                    

                }

                if (data.T > 168+273) {
                    // Boom
                    clearInterval(interval_id);
                    $("#runaway").modal("show");
                }
            }
        });
    }, 250);

});