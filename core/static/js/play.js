$(document).ready(function () {

    function getRandomInteger(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    interval_id = null;

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
        beforeSend: function (xhr, settings) {
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
        if (data.Tjset > 5 + 273) {
            data.Tjset -= 1;
        }
    });

    $("#heat-btn").click(function () {
        if (data.Tjset < 180 + 273) {
            data.Tjset += 1;
        }
    });

    $("#slider1").on("change", function () {
        const value = $('#slider1');
        data.slider1 = value.val();
    });

    $("#slider2").on("input change", function () {
        const value = $('#slider2');
        data.slider2 = value.val();
    });

    $("#slider3").on("input change", function () {
        const value = $('#slider3');
        data.slider3 = value.val();
    });

    $("#slider4").on("input change", function () {
        const value = $('#slider4');
        data.slider4 = value.val();
    });

    $("#slider5").on("input change", function () {
        const value = $('#slider5');
        data.slider5 = value.val();
    });

    $("#slider6").on("input change", function () {
        const value = $('#slider6');
        data.slider6 = value.val();
    });

    $("#slider7").on("input change", function () {
        const value = $('#slider7');
        data.slider7 = value.val();
    });

    $("#slider8").on("input change", function () {
        const value = $('#slider8');
        data.slider8 = value.val();
    });

    $("#slider9").on("input change", function () {
        const value = $('#slider9');
        data.slider9 = value.val();
    });

    interval_id = setInterval(function () {
        $.ajax({
            url: $("#plots").attr("data-url"),
            type: 'post',
            data: data,
            dataType: 'json',
            success: function (newdata) {
                data = newdata;

                temperatures.series[0].addPoint(data.T - 273);
                temperatures.series[1].addPoint(data.Tj - 273);
                temperatures.series[2].addPoint(data.Tjset - 273)
                concentrations.series[0].addPoint(data.CA);
                concentrations.series[1].addPoint(data.CB);
                concentrations.series[2].addPoint(data.CC);
                concentrations.series[3].addPoint(data.CD);
                concentrations.series[4].addPoint(data.CE);
                $("#tj-display").html(
                    "T<sub>j,c</sub> = " + Number((data.Tjset - 273).toFixed(2)).toString() + " °C / " +
                    '<span style="color:#069">T<sub>r</sub> = ' + Number((data.T - 273).toFixed(2)).toString() + " °C"
                );
                $("#X-display").html("X = " + Number((data.X * 100).toFixed(2)).toString() + " %")

                if (data.X >= 0.95 && data.T < 220 + 273) {
                    // Victoire
                    clearInterval(interval_id);
                    //$("#victoire").text(t);
                    $("#victoire").modal("show");

                    $.ajax({
                        url: $("#plots").attr("data-url") + "score/",
                        type: 'post',
                        data: {
                            "player": data.playerid,
                            "t": data.t,
                            "X": data.X
                        },
                        dataType: 'json',
                        success: function (data) {
                        }
                    });


                }

                if (data.T > 220 + 273) {
                    // Boom
                    clearInterval(interval_id);
                    $("#runaway").modal("show");
                }
            }
        });
    }, 250);

});