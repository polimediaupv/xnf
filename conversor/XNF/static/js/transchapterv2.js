/**
 * Created by leosamu on 19/11/14.
 */

/* on server select we need to clear courses dropdown set it to default element and load the dropdown
   * with the courses of the selected server */
function serverselect(element){
    //parent->select
    //parent.parent->row
    var capitulos = $(".capitulos",$(element).parent().parent().parent());
    $(capitulos).empty();

    var select = $(".courseselect",$(element).parent().parent());
    var select2 = $(".courseselect2",$(element).parent().parent());
    $(select).empty();
    select
        .append($("<option></option>")
        .text('Seleccione un curso de origen...'));
    console.log("adfadñaddfjkñl")
    $.get( "../transchapterv2listcourse?serverid="+ element.value, function( data ) {

        }).done(function(data) {
            courses = JSON.parse(data);
            $.each( courses, function( key, val ) {
                select
                 .append($("<option></option>")
                 .attr("value",val['data-course-key'])
                 .text(val['course-name']));
            });
    });
};

function courseselect(element){
    var capitulos = $(".capitulos",$(element).parent().parent().parent());
    var server = $(".serverselect",$(element).parent().parent().parent())[0].value;
    $(capitulos).empty();
    $.get( "../transchapterv2listchapters?serverid="+ encodeURIComponent(server) + '&courseid=' + encodeURIComponent(element.value), function( data ) {

        }).done(function(data) {
            courses = JSON.parse(data);
            $.each( courses, function( key, val ) {
                console.log(val);
                if ($(element).hasClass("origen"))
                   {
                       capitulos
                    .append($('<div class="input-group fadeInDown">' +
                                    '<span class="form-control">' + val['display_name'] + '</span>' +
                                    '<span class="input-group-btn">' +
                                        '<button type="button" class="origencopy btn btn-default" server="' + server +'" course="' + element.value +'" chapter="' + val['id'] +'" onclick="copychapter(this)"> &gt; </button>' +
                                    '</span>' +
                                '</div>'))
                   }
                   else if ($(element).hasClass("destino"))
                   {
                       capitulos
                    .append($('<div class="input-group">' +
                                    '<span class="input-group-btn fadeInDown">' +
                                        '<button type="button" class="btn btn-default" server="' + server +'" course="' + element.value  +'" chapter="' + val['id'] +'" onclick="copychapter(this)"> &lt; </button>' +
                                    '</span>' +
                                    '<span class="form-control">' + val['display_name'] + '</span>' +
                                '</div>'))
                   }
            });
    });
};

function copychapter(element){
    console.log("patata");
    displayName = $("span.form-control",$(element).parent().parent())[0].innerText;
    capitulos = $(".capitulos").not($(".capitulos",$(element).parent().parent().parent().parent().parent()));
    chapter = $(element).attr("chapter");
    server = $(element).attr("server");
    course = $(element).attr("course");
    serverend= $(".serverselect").not($(".serverselect",$(element).parent().parent().parent().parent().parent()))[0].value;
    courseend= $(".courseselect").not($(".courseselect",$(element).parent().parent().parent().parent().parent()))[0].value;
    $('button').prop('disabled', true);
    $('select').prop('disabled', true);

     $.get('../transchapterv2copychapter/', {serversrc:server,coursesrc:course,chaptersrc: chapter,serverdst:serverend,coursedst:courseend}, function(newChapterName){
              $('button').prop('disabled', false);
              $('select').prop('disabled', false);
              console.log(newChapterName);
              if ($(capitulos).hasClass("origen"))
               {
                   capitulos
                .append($('<div class="input-group fadeInRight">' +
                                '<span class="form-control">' + displayName + '</span>' +
                                '<span class="input-group-btn">' +
                                    '<button type="button" class="origencopy btn btn-default" server="' + serverend +'" course="' + courseend +'" chapter="' + newChapterName +'" onclick="copychapter(this)"> &gt; </button>' +
                                '</span>' +
                            '</div>'))
               }
               else if ($(capitulos).hasClass("destino"))
               {
                   capitulos
                .append($('<div class="input-group fadeInLeft">' +
                                '<span class="input-group-btn">' +
                                    '<button type="button" class="btn btn-default" server="' + serverend +'" course="' + courseend +'" chapter="' + newChapterName +'" onclick="copychapter(this)"> &lt; </button>' +
                                '</span>' +
                                '<span class="form-control">' + displayName + '</span>' +
                            '</div>'))
               }
           });
};




