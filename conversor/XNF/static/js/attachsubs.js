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

    var coursestxt = JSON.parse(atob($("#courses")[0].value));

    for (i=0;i<coursestxt.length;i++)
    {
        if (coursestxt[i].server==element.value)
        {
            select
             .append($("<option></option>")
             .attr("value",coursestxt[i].id)
             .text(coursestxt[i].id));
        }
    }
};

function courseselect(element){

    console.log("patata");
    var capitulos = $(".capitulos",$(element).parent().parent().parent());
    var server = $(".serverselect",$(element).parent().parent().parent())[0].value;
    $(capitulos).empty();

    $($("#addsubcourse")[0]).attr({'course':element.value,'server':server,'chapter':""});

    var coursestxt = JSON.parse(atob($("#courses")[0].value));
    for (i=0;i<coursestxt.length;i++)
    {
        if (coursestxt[i].id==element.value && coursestxt[i].server== server)
        {
           for(j=0;j<coursestxt[i].chapters.length;j++)
           {
               if (coursestxt[i].chapters[j].linked==false){
                   coursestxt[i].chapters[j].displayname = '<strike>' + coursestxt[i].chapters[j].displayname + '</strike>'
               }

               if ($(element).hasClass("origen"))
               {
                   capitulos
                .append($('<div class="input-group fadeInDown col-md-11">' +
                                '<span class="form-control">' + coursestxt[i].chapters[j].displayname + '</span>' +
                            '</div>'))
               }
               else if ($(element).hasClass("destino"))
               {
                   capitulos
                .append($('<div class="input-group">' +
                                '<span class="input-group-btn fadeInDown">' +
                                    '<button type="button" class="btn btn-default" server="' + coursestxt[i].server +'" course="' + coursestxt[i].id +'" chapter="' + coursestxt[i].chapters[j].name +'" onclick="addsubs(this)"> <i class="fa fa-language"></i> </button>' +
                                '</span>' +
                                '<span class="form-control">' + coursestxt[i].chapters[j].displayname + '</span>' +
                            '</div>'))
               }

           }
        }
    }

};

function addsubs(element){
    console.log("patata");
    //displayName = $("span.form-control",$(element).parent().parent())[0].innerText;
    //capitulos = $(".capitulos").not($(".capitulos",$(element).parent().parent().parent().parent().parent()));
    chapter = $(element).attr("chapter");
    server = $(element).attr("server");
    course = $(element).attr("course");
    lang = {'es':$($("input[name='language']")[0]).is(':checked'),'en':$($("input[name='language']")[1]).is(':checked')}
    strLang = JSON.stringify(lang);
    /*toastr.options.positionClass="toast-top-full-width";
    toastr.options.progressBar=true;*/
    toastr.success('Puede cerrar esta página o realizar otras tareas, recibirá una alerta al finalizar de enlazar los subtitulos al curso','Subtitulos solicitados para enlazar');
     $.get('/XNF/addsubs/', {srvOrigen:server,courseOrigen:course,chapter_name: chapter,language : strLang}, function(newChapterName){
              $('button').prop('disabled', false);
              $('select').prop('disabled', false);
              console.log(newChapterName);
           });
};

function clicklanguageselector(){
   $("#addsubcourse").attr("disabled", !$("input[type='checkbox']").is(":checked"));
}