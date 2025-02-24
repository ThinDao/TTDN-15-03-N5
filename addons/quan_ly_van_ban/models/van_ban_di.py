from odoo import models, fields, api


class VanBanDi(models.Model):
    _name = 'van_ban_di'
    _description = 'Bảng chứa thông tin văn bản'

    ma_dinh_danh = fields.Char("Tên văn bản", required=True)

