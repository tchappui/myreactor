$(document).ready(function () {

    function getRandomInteger(min, max) {
        return Math.floor(Math.random() * (max - min + 1) ) + min;
      }

    interval_id = null;
    t = 0;

    U0 = data.U;

    t_failure_start = getRandomInteger(30, 300); 
    t_failure_stop = t_failure_start + 10 + getRandomInteger(10, 50);

    console.log(t_failure_start);
    console.log(t_failure_stop);

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
        if (e.key == "ArrowDown" || e.key == "ArrowLeft") {
            $("#cool-btn").click();
        }
        else if (e.key == "ArrowUp" || e.key == "ArrowRight") {
            $("#heat-btn").click();
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
                t += 1;

                // Simulating of failure of the temperature control system
                if (t > t_failure_start && t < t_failure_stop) {
                    data.U = 0;
                    $("#failure").show();
                }
                else {
                    $("#failure").hide(); 
                    data.U = U0;
                }

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

                if (data.X > 1) {
                    // Victoire
                    clearInterval(interval_id);
                    $("#victoire").text(t);
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

                if (data.T > 250+273) {
                    // Boom
                    clearInterval(interval_id);
                    $("#runaway").modal("show");
                }
            }
        });
    }, 200);

});