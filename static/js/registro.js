$(function () {

   $("#id_formulario").formValidation({
       message: 'This value is not valid',
        fields: {
            correo: {
                validators: {
                    notEmpty: {},
                    remote:{
                        message: 'Este correo ya esta en uso',
                        url: '/registro/datoValidacion/',
                        data: function(validator, $field, value) {
                            return {
                                correo: validator.getFieldElements('correo').val(),
                                tipo : 'correo'
                            };
                            },
                            type: 'POST'
                    }
                }
            },
            usuario: {
                validators: {
                    noEmpty: {},
                    remote: {
                        message: 'este usuario no esta disponible',
                        url: '/registro/datoValidacion/',
                        data: function(validator, $field, value) {
                            return {
                                usuario: validator.getFieldElements('usuario').val(),
                                tipo : 'usuario'
                            };
                            },
                            type: 'POST'
                    }
                }
            }
        }
    });
});
