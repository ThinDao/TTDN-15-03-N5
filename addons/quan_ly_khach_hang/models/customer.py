from odoo import models, fields, api

class Customer(models.Model):
    _name = 'customer'
    _description = 'Bảng chứa thông tin khách hàng'

    # Các trường cơ bản
    customer_id = fields.Char("Mã khách hàng", required=True, index=True, copy=False)
    customer_name = fields.Char("Tên khách hàng", required=True)
    email = fields.Char("Email")
    phone = fields.Char("Số điện thoại")
    address = fields.Text("Địa chỉ")
    gender = fields.Selection([
        ('male', 'Nam'),
        ('female', 'Nữ'),
        ('other', 'Khác')
    ], string="Giới tính")
    date_of_birth = fields.Date("Ngày sinh")
    age = fields.Integer("Tuổi", compute="_compute_age", store=True)
    company_name = fields.Char("Tên công ty")
    tax_code = fields.Char("Mã số thuế")
    customer_type = fields.Selection([
        ('individual', 'Cá nhân'),
        ('company', 'Công ty')
    ], string="Loại khách hàng", default="individual")
    active = fields.Boolean("Active", default=True)
    notes = fields.Text("Ghi chú")

    # Trường liên kết với các model khác
    sale_order_ids = fields.One2many('sale_order', inverse_name='customer_id', string="Đơn hàng")
    interact_ids = fields.One2many('crm_interact', inverse_name='customer_id', string="Tương tác")
    contract_ids = fields.One2many('contract', inverse_name='customer_id', string="Hợp đồng")
    lead_ids = fields.One2many('crm_lead', inverse_name='customer_id', string="Cơ hội")
    feedback_ids = fields.One2many('feedback', inverse_name='customer_id', string="Phản hồi")
    task_ids = fields.One2many('project_task', inverse_name='customer_id', string="Nhiệm vụ dự án")
    note_ids = fields.One2many('note', inverse_name='customer_id', string="Ghi chú")

    # Trường tính toán (computed field)
    @api.depends('date_of_birth')
    def _compute_age(self):
        today = fields.Date.today()
        for record in self:
            if record.date_of_birth:
                delta = today - record.date_of_birth
                record.age = delta.days // 365
            else:
                record.age = 0

    # Tạo mã khách hàng tự động
    @api.model
    def create(self, vals):
        if vals.get('customer_id', 'New') == 'New':
            vals['customer_id'] = self.env['ir.sequence'].next_by_code('customer.sequence') or 'New'
        return super(Customer, self).create(vals)

    # Đặt tên hiển thị cho bản ghi
    def name_get(self):
        result = []
        for record in self:
            name = f"[{record.customer_id}] {record.customer_name}"
            result.append((record.id, name))
        return result