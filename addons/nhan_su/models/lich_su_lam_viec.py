from odoo import models, fields, api


class LichSuLamViec(models.Model):
    _name = 'lich_su_lam_viec'
    _description = 'Bảng chứa thông tin lịch sử làm việc'

    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True)
