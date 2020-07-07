from app.util.validaciones.ValidacioCadenas import ValidacionCadenas
from . import BaseTestClass


class ValidacioncadenasTest(BaseTestClass):

    def test_validar_tamano_parametro_largo(self):
        tamano_maximo = 12
        tamano_minimo = 5
        codigo_error_esperado = "nombre_demasiado_largo"
        error = ValidacionCadenas.validar_tamano_parametro("12345678910111213", "nombre", tamano_minimo,
                                                           tamano_maximo)
        self.assertEqual(codigo_error_esperado, error['error'])

    def test_validar_tamano_parametro_corto(self):
        tamano_maximo = 12
        tamano_minimo = 5
        codigo_error_esperado = "nombre_demasiado_corto"
        error = ValidacionCadenas.validar_tamano_parametro("123", "nombre", tamano_minimo,
                                                           tamano_maximo)
        self.assertEqual(codigo_error_esperado, error['error'])

    def test_validar_tamano_correcto(self):
        tamano_maximo = 12
        tamano_minimo = 5
        esperado = None
        error = ValidacionCadenas.validar_tamano_parametro("1234567", "nombre", tamano_minimo,
                                                           tamano_maximo)
        self.assertEqual(esperado, error)

    def test_validar_cadena_tiene_caracteres_especiales(self):
        cadena = "asdfA56. !#"
        contiene_caracteres_especiales = ValidacionCadenas.validar_cadena_sin_caracteres_especiales(cadena)
        self.assertEqual(False, contiene_caracteres_especiales)

    def test_validar_cadena_no_tiene_caracteres_especiales(self):
        cadena = "asdfgADGHGF12852"
        contiene_caracteres_especiales = ValidacionCadenas.validar_cadena_sin_caracteres_especiales(cadena)
        self.assertEqual(True, contiene_caracteres_especiales)

    def test_validar_contrasena_correcta(self):
        contrasena = "Estas2525.-!"
        contrasena_valida = ValidacionCadenas.validar_contrasena(contrasena)
        self.assertEqual(True, contrasena_valida)

    def test_validar_contrasena_incorrecta(self):
        contrasena = "HolaComoEstas2525.-!"
        contrasena_valida = ValidacionCadenas.validar_contrasena(contrasena)
        self.assertEqual(False, contrasena_valida)

    def test_validar_numero_telefono_valido(self):
        numero_telefono = "+521231231230"
        esperado = None
        numero_valido = ValidacionCadenas.validar_numero_telefono(numero_telefono)
        self.assertEqual(esperado, numero_valido)

    def test_validar_numero_telefono_invalido(self):
        numero_telefono = "+521231231230123"
        esperado = "telefono_no_valido"
        numero_valido = ValidacionCadenas.validar_numero_telefono(numero_telefono)
        self.assertEqual(esperado, numero_valido['error'])

    def test_validar_correo_electronico_valido(self):
        correo_electronico = "asdfg.--sff78@ghjkl.uv.mx"
        correo_electronico_valido = ValidacionCadenas.validar_email(correo_electronico)
        self.assertEqual(None, correo_electronico_valido)

    def test_validar_correo_electronico_invalido(self):
        correo_electronico = "sdfdg@asdf"
        esperado = None
        correo_electronico_valido = ValidacionCadenas.validar_email(correo_electronico)
        self.assertEqual(esperado, correo_electronico_valido)
