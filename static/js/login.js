$(function () {
    $("#id_formulario").formValidation({
        message: 'Este valor no es valido',
        fields:{
            username:{
                validators:{
                    noEmpty:{},
                    stringLength: { min:3, max:15}
                }
            },
            password:{
                validators:{
                    noEmpty:{},
                    stringLength: { min:3, max:15}
                }
            }
        }
    });
});