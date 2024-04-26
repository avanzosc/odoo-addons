from odoo import models, fields, api

class SurveyUserInputLine(models.Model):
    _inherit = 'survey.user_input.line'

    # Define el campo calculado
    calculated_matrix_question_id = fields.Many2one(
        'survey.question.answer', 
        string='Matrix Question ID',
        compute='_compute_matrix_question_id',
        store=True  # Almacenar el valor calculado en la base de datos
    )
    
    # Define el campo calculado
    calculated_suggested_answer_question_id = fields.Many2one(
        'survey.question.answer', 
        string='Suggested Answer ID',
        compute='_compute_suggested_answer_id',
        store=True  # Almacenar el valor calculado en la base de datos
    )


    # Método de cálculo para el campo calculado
    @api.depends('matrix_row_id')
    def _compute_matrix_question_id(self):
        for line in self:
            if line.matrix_row_id:
                line.calculated_matrix_question_id = line.matrix_row_id.matrix_question_id.id
            else:
                line.calculated_matrix_question_id = False


    # Método de cálculo para el campo calculado
    @api.depends('suggested_answer_id')
    def _compute_suggested_answer_id(self):
        for line in self:
            if line.question_id:
                line.calculated_suggested_answer_question_id = line.suggested_answer_id.question_id.id
            else:
                line.calculated_suggested_answer_question_id = False
