from odoo import fields, models


class ProductSeries(models.Model):
    _name = "product.series"
    _description = "Product Series"

    name = fields.Char(string="Series", required=True)


class ProductModel(models.Model):
    _name = "product.model"
    _description = "Product Model"

    name = fields.Char(string="Model", required=True)


class ProductApplication(models.Model):
    _name = "product.application"
    _description = "Product Application"

    name = fields.Char(string="Application", required=True)


class ProductFamily(models.Model):
    _name = "product.family"
    _description = "Product Family"

    name = fields.Char(string="Family", required=True)


class ProductColor(models.Model):
    _name = "product.color"
    _description = "Product Color"

    name = fields.Char(string="Color", required=True)
