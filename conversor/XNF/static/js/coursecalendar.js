/**
 * Created by leosamu on 10/9/15.
 */
var source = [];
var toggle = true;

$(document).ready(function() {



        $('#calendar').fullCalendar({
                header: {
                    left: 'prev,next today',
                    center: 'title',
                    right: ''
                },
                editable: false,
                draggable: false,
                droppable: false, // this allows things to be dropped onto the calendar
                drop: function() {
                    // is the "remove after drop" checkbox checked?
                    if ($('#drop-remove').is(':checked')) {
                        // if so, remove the element from the "Draggable Events" list
                        $(this).remove();
                    }
                },
                eventSources: [source]
            });

         $.getJSON("../coursesdates/", function(data){
             source=data;
             $('#calendar').fullCalendar('addEventSource', source);
             $('#calendar').fullCalendar( 'refetchEvents' );
         })

            $('.i-checks').iCheck({
                checkboxClass: 'icheckbox_square-green',
                radioClass: 'iradio_square-green',
            });

        /* initialize the external events
         -----------------------------------------------------------------*/


        $('#external-events div.external-event').each(function() {

            // store data so the calendar knows to render an event upon drop
            $(this).data('event', {
                title: $.trim($(this).text()), // use the element's text as the event title
                stick: true // maintain when user navigates (see docs on the renderEvent method)
            });

            // make the event draggable using jQuery UI
            $(this).draggable({
                zIndex: 1111999,
                revert: true,      // will cause the event to go back to its
                revertDuration: 0  //  original position after the drag
            });

        });


        /* initialize the calendar
         -----------------------------------------------------------------*/





    });

function hideselfpaced()
{
    console.log("test");
    $('#calendar').fullCalendar('removeEvents');
    toggle = !toggle;
    $.getJSON("../coursesdates/?selfpaced=" + toggle, function(data){
            source=data;
            $('#calendar').fullCalendar('addEventSource', source);
            $('#calendar').fullCalendar( 'refetchEvents' );
         });
}

function dataToCSV()
{
patata="";
source.forEach(function(element){
    patata = patata + '\n' + element.title + ',' + element.url + ',' + element.start + ',' + element.end;
});


}