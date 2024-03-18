========================
 Control access to Apps
========================

Installation
============

* `Install <https://odoo-development.readthedocs.io/en/latest/odoo/usage/install-module.html>`__ this module in a usual way

Configuration
=============

After the installation of this module by default no one has access to installing modules.
To control such permission follow the steps below.


* Open menu ``[[ Settings ]] >> Users & Companies >> Users``, select the user you want to grant the access to
* On ``Access Rights`` tab, ``Application Accesses`` settings group there is an ``Apps access`` security category

 * Select ``Allow installing apps`` - to allow apps installation from everywhere
 * Select ``Allow installing apps only from settings`` - to allow apps installation only from other module's ``Configuration >> Settings`` menu, there is no ``[[ Apps ]]`` menu available
 * Select blank line - to restrict application installation

Usage
=====

* Be sure that you don't test the functionality under the ``Administrator`` (superuser with id=1) user - he is immune to any access restriction except of hiding menus or buttons in UI
* If you don't select anything in ``Apps access``: there is no ``[[ Apps ]]`` menu - even if your user is in ``Administration: Settings`` security group. Also note that you
  have no ability to include yourself in groups allowing to installing apps - this is what ``access_restricted`` module does (``access_apps`` depends on it)
* If you have ``Allow installing apps`` selected: there is ``[[ Apps ]]`` menu
* If you have ``Allow installing apps only from settings``: from other module's ``Configuration >> Settings`` menu, e.g. from ``[[ Website ]] >> Configuration >> Settings`` (this menu is available after the *Website app* installation) see that
  you have the ability to check the ``Digital Content`` checkbox that actually installs the ``website_sale_digital`` module after clicking on ``[Apply]`` button.
