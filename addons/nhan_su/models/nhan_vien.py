from odoo import models, fields, api
from datetime import date


class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    _rec_name = 'ho_ten'

    ma_dinh_danh = fields.Char("Mã định danh", required=True)
    ngay_sinh = fields.Integer("Ngày sinh")
    que_quan = fields.Char("Quê quán")
    email = fields.Char("Email")
    so_dien_thoai = fields.Char("Số điện thoại")
    lich_su_lam_viec_ids = fields.One2many('lich_su_lam_viec', inverse_name='nhan_vien_id', string="Danh sách LSLV")
    gioi_tinh = fields.Selection([
        ('male', 'Nam'),
        ('female', 'Nữ'),
        ('other', 'Khác')
    ], string="Giới tính")

    ho_ten = fields.Char("Họ tên", compute='_tinh_ho_va_ten', store=True)
    ho_ten_dem = fields.Char("Họ tên đệm")
    ten = fields.Char("Tên")
    tuoi = fields.Integer(string='Tuổi', compute='_tinh_tuoi', store=True)

    @api.depends("ngay_sinh","tuoi")
    def _tinh_tuoi(self):
        for record in self:
            if record.ngay_sinh:
                current_year = date.today().year
                record.tuoi= current_year - record.ngay_sinh
            else:
                record.tuoi = 0

    @api.depends("ho_ten_dem","ten")
    def _tinh_ho_va_ten(self):
        for record in self:
            if record.ho_ten_dem and record.ten:
                record.ho_ten = record.ho_ten_dem + '' + record.ten

    @api.onchange("ho_ten_dem","ten")
    def _tinh_thay_doi(self):
        for record in self:
            if record.ho_ten_dem and record.ten:
                record.ma_dinh_danh = record.ten