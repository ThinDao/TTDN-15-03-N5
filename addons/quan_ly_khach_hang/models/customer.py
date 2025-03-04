from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Customer(models.Model):
    _name = 'customer'
    _description = 'Bảng chứa thông tin khách hàng'
    _sql_constraints = [
        ('customer_id_unique', 'unique(customer_id)', 'Mã khách hàng phải là duy nhất!'),
    ]

    # Các trường cơ bản
    customer_id = fields.Char("Mã khách hàng", required=True, index=True, copy=False)
    customer_name = fields.Char("Tên khách hàng", required=True)
    email = fields.Char("Email")
    phone = fields.Char("Số điện thoại")
    address = fields.Char("Địa chỉ")
    gender = fields.Selection([
        ('male', 'Nam'),
        ('female', 'Nữ'),
        ('other', 'Khác')
    ], string="Giới tính")
    date_of_birth = fields.Date("Ngày sinh")
    age = fields.Integer("Tuổi", compute="_compute_age", store=True)
    income_level = fields.Selection([
        ('0-20tr', '0-20 triệu/tháng'),
        ('20-50tr', '20-50 triệu/tháng'),
        ('50-70tr', '50-70 triệu/tháng'),
        ('70-100tr', '70-100 triệu/tháng'),
        ('100tr+', '100 triệu trở lên')
    ], string="Mức thu nhập")
    image = fields.Binary("Ảnh", attachment=True)
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

    # Trường tính toán (computed fields)
    total_customers = fields.Integer("Tổng số khách hàng", compute="_compute_total_customers", store=True)
    total_contracts = fields.Integer("Tổng số hợp đồng", compute="_compute_total_contracts", store=True)
    total_interactions = fields.Integer("Tổng số tương tác", compute="_compute_total_interactions", store=True)
    total_sale_orders = fields.Integer("Tổng số đơn hàng", compute="_compute_total_sale_orders", store=True)

    # Tính toán tổng số khách hàng
    @api.depends()
    def _compute_total_customers(self):
        total = self.search_count([])
        for record in self:
            record.total_customers = total

    # Tính toán tổng số hợp đồng
    @api.depends('contract_ids')
    def _compute_total_contracts(self):
        for record in self:
            record.total_contracts = len(record.contract_ids)

    # Tính toán tổng số tương tác
    @api.depends('interact_ids')
    def _compute_total_interactions(self):
        for record in self:
            record.total_interactions = len(record.interact_ids)

    # Tính toán tổng số đơn hàng
    @api.depends('sale_order_ids')
    def _compute_total_sale_orders(self):
        for record in self:
            record.total_sale_orders = len(record.sale_order_ids)

    # Tính toán tuổi
    @api.depends('date_of_birth')
    def _compute_age(self):
        today = fields.Date.today()
        for record in self:
            if record.date_of_birth:
                if record.date_of_birth > today:
                    raise ValidationError("Ngày sinh không thể lớn hơn ngày hiện tại!")
                delta = today - record.date_of_birth
                record.age = delta.days // 365
            else:
                record.age = 0

    # Đặt tên hiển thị cho bản ghi
    def name_get(self):
        result = []
        for record in self:
            name = f"[{record.customer_id}] {record.customer_name}"
            result.append((record.id, name))
        return result