from odoo import models, fields, api

class ProjectTask(models.Model):
    _name = 'project_task'
    _description = 'Bảng chứa thông tin nhiệm vụ'

    project_task_id = fields.Char("Mã nhiệm vụ", required=True)
    customer_id = fields.Many2one('customer', string="Khách hàng", required=True, ondelete='cascade')
    name = fields.Char("Tên nhiệm vụ", required=True)
    deadline = fields.Date("Hạn chót", required=True)

    # Đặt tên hiển thị cho bản ghi
    def name_get(self):
        result = []
        for record in self:
            name = f"[{record.project_task_id}] {record.name}"
            result.append((record.id, name))
        return result
