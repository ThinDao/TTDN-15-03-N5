from odoo import models, fields, api


class KhachHang(models.Model):
    _name = 'khach_hang'
    _description = 'Bảng chứa thông tin khách hàng'

    ma_khach_hang = fields.Char("Mã khách hàng", required=True)
    ten_khach_hang = fields.Char("Tên khách hàng")