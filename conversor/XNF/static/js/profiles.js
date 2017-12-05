/**
 * Created by leosamu on 31/3/15.
 */
function updateprofile(){
$.post('../updateprofile/', $('#profileform').serialize(),function(){
    alert('perfil actualizado');
})

}

function createnewuser(){
$.post('../createnewuser/', $('#profileform').serialize(),function(){
    alert('perfil creado');
    //clean
}).done(function(){
    $("form")[0].reset()
});

}