.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===================================
AEAT modelo 303 - Navarra (F66/F69)
===================================

Este módulo añade a la declaración del modelo 303 las casillas y los cálculos
específicos de la Hacienda Foral de Navarra (modelo F66/F69), sin alterar la
exportación oficial estatal del 303.

Descripción
-----------

El modelo 303 de OCA sigue siendo la declaración estatal. Sobre él se incorpora
una pestaña **Navarra (F66/F69)** que se muestra únicamente cuando la compañía
tiene configurada la Hacienda Foral de Navarra como agencia tributaria, y que
incluye las siguientes casillas:

- **[55] Cifra relativa**: porcentaje definitivo de cifra relativa.
- **[50] IVA deducible**: total del IVA deducible del periodo.
- **[61] Cuota resultante**: (IVA devengado - IVA deducible) × cifra relativa.
- **[62] Cuota a compensar de periodos anteriores**.
- **[63] Resultado final**: casilla 61 - casilla 62 + regularización anual.
- **[69] Regularización anual** (mapeada sobre la casilla 68 del 303).
- **Modo de pago** de Navarra.
- **[93] Sin actividad**.
- **[164]/[165] Resumen anual de operaciones**.
- **[264]/[265] Operaciones exentas sin derecho a deducción**.

Además, el módulo genera el fichero de presentación **F66** (mensual) o
**F69** (trimestral) con el formato oficial de 250 caracteres por registro,
incluyendo la relación de casillas, el resumen anual y los datos de contacto.

Configuración
-------------

Para utilizar las casillas navarras:

1. Instale el módulo.
2. En la compañía, configure la **Hacienda Foral de Navarra**
   (`l10n_es_aeat.aeat_tax_agency_navarra`) como agencia tributaria.

Uso
---

1. Cree o abra una declaración del modelo 303.
2. Acceda a la pestaña **Navarra (F66/F69)**.
3. Calcule la declaración para obtener las casillas 50, 61, 62 y 63.
4. Informe la **cifra relativa** (casilla 55):

   - En los tres primeros trimestres se toma el porcentaje definitivo del año
     anterior y no puede modificarse.
   - En el cuarto trimestre se informa el porcentaje definitivo del propio año.

5. Si el resultado de la casilla 63 es negativo y se desea compensar con
   Navarra, marque **Dejar el resultado negativo para compensar**. La casilla
   62 de la siguiente declaración recogerá automáticamente ese saldo.
6. Seleccione el **modo de pago** cuando el resultado final sea positivo.
7. En el cuarto trimestre (o en el periodo de cese) informe las casillas
   164/165 del resumen anual.
8. Marque la casilla 264 o la 265 de operaciones exentas sin derecho a
   deducción.
9. Pulse **Generar fichero F66/F69** para descargar el fichero de presentación.
   El nombre del fichero incluye el modelo, el NIF, el ejercicio y el periodo.

Tests
-----

El módulo incluye pruebas automáticas que cubren el cálculo de las casillas
navarras, la compensación de saldos negativos, la cifra relativa de los tres
primeros trimestres, el modo de pago, el resumen anual, las operaciones
exentas y la generación de los ficheros F66/F69.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/odoo-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us smash it by providing detailed and welcomed feedback.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Contributors
------------

* AvanzOSC

Maintainer
----------

This module is maintained by AvanzOSC.

This module is part of the `AvanzOSC/odoo-addons
<https://github.com/avanzosc/odoo-addons>`_ project on GitHub.

You are welcome to contribute. To learn how please visit
https://github.com/avanzosc/odoo-addons.
