$(function () {

   $("#id_formulario").formValidation({
       message: 'This value is not valid',
        fields: {
            new_password1: {
                validators: {
                    identical: {
                        field: 'new_password2',
                        message: 'Las contraseñas no son iguales'
                    }
                }
            },
            new_password2: {
                validators: {
                    identical: {
                        field: 'new_password1',
                         message: 'Las contraseñas no son iguales'
                    }
                }
            }
            }
    });
});
