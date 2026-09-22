.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

========================================
Previsión de tesorería: colores en pivot
========================================

CLM15016. Añade formato condicional por signo a las vistas pivot del módulo
``treasury_forecast``: valores positivos en verde, negativos en rojo, ceros
y celdas vacías sin color.

**Features**

- Colorea por signo todas las celdas numéricas del pivot (medidas, totales y subtotales).
- Usa las clases semánticas de Bootstrap ``text-success`` y ``text-danger``, las mismas que el core de Odoo emplea para las variaciones del modo comparación, por lo que el modo oscuro funciona automáticamente sin SCSS propio.
- El modo *comparación de periodos* del core se mantiene intacto: las variaciones (``o_variation`` con ``o_positive`` / ``o_negative`` / ``o_null``) siguen comportándose igual.
- El efecto se acota mediante ``js_class`` en las vistas pivot del módulo base — sin tocar el módulo base ni afectar al resto de pivots del sistema.

**Vistas afectadas**

- ``treasury_forecast.view_treasury_forecast_pivot`` (modelo ``treasury.forecast``).
- ``treasury_forecast.view_treasury_forecast_report_pivot`` (modelo ``treasury.forecast.report``).

**Cómo está implementado**

- Se registra una entrada propia en el registry de vistas (``treasury_forecast_pivot_color``) que reutiliza ``pivotView`` por *spread* y sustituye únicamente el ``Renderer`` por una subclase de ``PivotRenderer``.
- La subclase usa un template QWeb (``treasury_forecast_pivot_color.PivotRenderer``) que hereda ``web.PivotRenderer`` en modo ``primary`` y añade vía ``xpath`` un ``t-att-class`` dinámico sobre el div numérico (``div.o_value`` con ``t-esc='getFormattedValue(cell)'``).
- Los assets se declaran en ``web.assets_backend_lazy``, no en ``web.assets_backend``, porque el módulo ``web`` mueve ``views/pivot/**`` al bundle lazy en Odoo 18 (code-splitting).

**Usage**

- Instala el módulo desde Apps.
- Abre los pivots de previsión de tesorería: *Accounting > Previsión de Tesorería*.
- Los valores positivos se ven en verde y los negativos en rojo automáticamente.

**Personalización futura**

En ``static/src/pivot/treasury_forecast_pivot_renderer.xml`` hay un comentario indicando dónde se cambiaría la condición si en el futuro se pide:

- Colorear sólo una medida concreta: añadir ``cell.measure === '<campo>'`` a la condición.
- Rangos / semáforo: sustituir las comparaciones ``> 0`` / ``< 0`` por los umbrales adecuados.

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

* Ana Juaristi <anajuaristi@avanzosc.es>
* Aner Arregi <aneravanzosc@gmail.es>

For specific questions regarding this module, please contact the contributors. For support, please use the official issue tracker.

License
=======

This project is licensed under the AGPL-3 License. For more details, refer to the LICENSE file or visit <https://opensource.org/licenses/AGPL-3.0>.
