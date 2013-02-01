# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
#    Copyright (C) 2004-2010 AvanzOSC (http://avanzosc.es). All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from osv import osv
from osv import fields

class training_antiguas_recibos(osv.osv):
    _name = 'training.antiguas.recibos'
    _description = 'antiguos recibos de ucav'

    _columns = {
            'num_alum': fields.char('Num.Alumno', size=10),
            'nombre_apellido': fields.char('Nombre y Apellido', size=150),
            'dni': fields.char('dni', size=10),
            'ano_academico': fields.char('Año Academico', size=10),
            'num_recibo': fields.integer('Numero de recibo'),
            'concepto': fields.char('Concepto', size=30),
            'estado': fields.char('Estado', size=10),
            'importe': fields.float('Importe'),
            'forma_pago': fields.char('Forma de Pago', size=10),
            'fecha': fields.date('fecha'),
            'asiento': fields.char('Asiento', size=10),
            'banco': fields.char('Banco', size=10),
            'observaciones': fields.text('Observaciones'),
        }
training_antiguas_recibos()

class training_antiguas_matriculas(osv.osv):
    _name = 'training.antiguas.matriculas'
    _description = 'antiguas matriculas de ucav'
    
    _columns = {
            'secuencia': fields.char('Secuencia', size=10),
            'ano_academico': fields.char('Año Academico', size=10),
            'titulacion': fields.char('Titulacion', size=150),
            'nombre_apellido': fields.char('Nombre y Apellido', size=150),
            'num_alum': fields.char('Num.Alumno',size=10),
            'dni': fields.char('dni', size=10),
            'forma_pago': fields.char('Forma de Pago',size=10),
            'asig_matri': fields.text('Asignaturas Matriculadas'),
            'concepto_pago': fields.text('Concepto Pago'),
            'importe_pago_inicial':fields.float('Importe pago inicial'),
            'importe_total_matricula':fields.float('Importe total matricula'),
            'importe_resto':fields.float('Importe resto'),
            'fecha': fields.date('Fecha'),
        }
training_antiguas_matriculas()

class training_antiguas_actas(osv.osv):
    _name = 'training.antiguas.actas'
    _description = 'antiguas actas de ucav'
    
    _columns = {
                'titulacion': fields.char('Titulacion',size=150),
                'asignatura': fields.char('Asignatura', size=150),
                'cod_asig': fields.char('Código de Asignatura', size=10),
                'creditos': fields.float('Creditos'),
                'curso_academico': fields.char('Curso academico', size=10),
                'nom_apell_prof': fields.char('Nombre y apellido Profe', size=150),
                'convocatoria': fields.char('Convocatoria', size=10),
                'gracia': fields.boolean('Conv.gracia'),
                'compensatoria': fields.boolean('Conv.compensatoria'),
                'fecha': fields.date('Fecha'),
                'firmas': fields.text('Firmas'),
                'notas': fields.text('Notas'),   
        }
training_antiguas_actas()

class training_antiguas_actas_proyectos(osv.osv):
    _name = 'training.antiguas.actas.proyectos'
    _description = 'antiguas actas de proyectos de ucav'
    
    _columns = {
                'titulacion': fields.char('Titulacion', size=150),
                'cod_asig': fields.char('Código de Asignatura', size=10),
                'creditos': fields.float('Creditos'),
                'convocatoria': fields.char('Convocatoria', size=10),
                'tribunal': fields.text('Tribunal'),
                'nombre_alumn': fields.char('Asignatura', size=150),
                'dni': fields.char('dni', size=10),
                'num_alumn': fields.integer('Num.Alumno'),
                'titulo_proyecto': fields.char('', size=128),
                'nombre_dicector': fields.char('Nombre director', size=128),
                'nombre_codirector': fields.char('Nombre codirector', size=128),
                'calif_cuali': fields.char('Calificación cualitativa', size=10),
                'calif_cuanti': fields.char('Calificación cuantitativa', size=128),
                'fecha': fields.date('Fecha'),
               }
training_antiguas_actas_proyectos()

class training_antiguas_actacompensatoria(osv.osv):
    _name = 'training.antiguas.actacompensatoria'
    _description = 'antiguas actas compensatorias'
    
    _columns = {
                'titulacion': fields.char('Titulacion', size=150),
                'cod_asig': fields.char('Código de Asignatura', size=10),
                'asignatura': fields.char('Asignatura', size=150),
                'creditos': fields.float('Creditos'),
                'convocatoria': fields.char('Convocatoria', size=10),
                'convocatoria_efect': fields.char('Convocatoria efectiva', size=10),
                'cod_alumn': fields.char('Código Alumno', size=10),
                'nombre_alumn': fields.char('Asignatura', size=150),
                'profesores': fields.text('Profesores'),
                'creditos': fields.float('Creditos'),
                'fecha': fields.date('Fecha'),
               }
training_antiguas_actacompensatoria()