.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

========================
Stock Split Quant By Lot
========================

* New wizard for stock moves to split its internal quants by lot.
* This wizard will load all internal quants for the origin move.
* You can split quants using a text box or a csv file.
* When you want to split a quant by text. You must check "By Text" in the
  wizard. Then you must fill the text box with lot numbers and after that 
  you must define the delimiter character.
* When you want to split by file. You must check "By File" in the wizard.
  Then you must select a file from your computer in the File field. The file
  must have csv format and at least lot_name column, it also can have qty column
  to define the quantity for each lot. If there is not lot_name column the
  system will raise an error. You also can redefine the delimiter.
* If you don't define qty column in the file or you are intending to split by
  text. The quantity for each lot will be 1.
* Once the header in the wizard is filled, you must push "Load Lines" button.
  It will create new lines above. There you can see the lots and it quantitys.
  You can change these lines if you want, but take into account that the other
  lines are not going to update automatically. When you apply the modifications
  the quants information in the movement will be the same as you are seeing in
  the wizard.
* Internally it creates an inventory for that product/lots with the same values
  as defined in the wizard lines.

Credits
=======

Contributors
------------
* Ainara Galdona <ainaragaldona@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>
