.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

========================
Account Renumber Options
========================

* New option in Account Setting Configuration, Renumber by period, this 
field will be activated by default. When it is activated, the renumber 
wizard will work as always. In the other hand if the check is not activated, 
the renumber wizard will not take into account the account move periods, 
so the renumbering will be processed only by date. 

* In the renumber wizard, the secuence assignment is the same as in the base 
process, so if the sequence is defined as "No gap" and there are gaps in 
previous moves, is possible that the final moves sequences are not concurrent 
because some moves will be used to fill the gaps.


Credits
=======

Contributors
------------
* Ainara Galdona <ainaragaldona@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>
