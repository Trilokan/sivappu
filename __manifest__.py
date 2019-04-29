# -*- coding: utf-8 -GPK*-

{
    "name": "Sivappu",
    "version": "1.0",
    "author": "La Mars",
    "website": "http://",
    "category": "Sivappu",
    "sequence": 1,
    "summary": "Hospital Management System",
    "description": """

    Hospital Management System

    Patient Management
    Employee Management
    Purchase Management
    Pharmacy Management
    Assert Management
    Accounts Management

    """,
    "depends": ["base", "mail"],
    "data": [

        "view/assert_backend.xml",

        "sequence/account.xml",
        "sequence/hr.xml",
        "sequence/inventory.xml",
        "sequence/register.xml",

        # Hospitality
        "view/hospitality/admission.xml",
        "view/hospitality/discharge.xml",
        "view/hospitality/ambulance.xml",
        "view/hospitality/admission_reason.xml",
        "view/hospitality/discharge_reason.xml",

        # Operation
        "view/operation/operation.xml",
        "view/operation/operation_theater.xml",
        "view/operation/patient_operation.xml",

        # Base
        "view/base/company.xml",
        "view/base/user.xml",

        # Register
        "view/register/person.xml",
        "view/register/employee.xml",
        "view/register/patient.xml",
        
        # General
        "view/general/language.xml",
        "view/general/religion.xml",
        "view/general/employee_identity.xml",
        "view/general/patient_identity.xml",
        "view/general/employee_qualification.xml",

        # Contact
        "view/contact/contact.xml",
        "view/contact/doctor.xml",
        "view/contact/driver.xml",
        "view/contact/nurse.xml",
        "view/contact/staff.xml",
        "view/contact/patient.xml",
        "view/contact/supplier.xml",
        "view/contact/service.xml",

        # Human Resources
        "view/hr/employee_card.xml",
        "view/hr/department.xml",
        "view/hr/designation.xml",
        "view/hr/experience.xml",
        "view/hr/category.xml",
        "view/hr/address.xml",

        # Recruitment
        "view/recruitment/resume_bank.xml",
        "view/recruitment/vacancy_position.xml",
        "view/recruitment/appointment_order.xml",

        # Time Management
        "view/time_management/shift.xml",
        "view/time_management/month_attendance.xml",
        "view/time_management/month_attendance_wiz.xml",
        "view/time_management/week_schedule.xml",
        "view/time_management/daily_attendance.xml",
        "view/time_management/work_sheet.xml",
        "view/time_management/time_sheet.xml",
        "view/time_management/time_sheet_application.xml",
        "view/time_management/add_employee.xml",
        "view/time_management/holiday_change.xml",
        "view/time_management/shift_change.xml",
        "view/time_management/time_config.xml",

        # Leave Management
        "view/leave_management/leave_application.xml",
        "view/leave_management/permission.xml",
        "view/leave_management/on_duty.xml",
        "view/leave_management/comp_off.xml",
        "view/leave_management/leave_level.xml",
        "view/leave_management/leave_type.xml",
        "view/leave_management/leave_availability.xml",
        "view/leave_management/leave_config.xml",

        # Payroll
        "view/payroll/hr_pay_update_wiz.xml",
        "view/payroll/hr_pay.xml",
        "view/payroll/payroll_generation.xml",
        "view/payroll/payslip.xml",
        "view/payroll/salary_structure.xml",
        "view/payroll/salary_rule.xml",
        "view/payroll/salary_rule_code.xml",
        "view/payroll/salary_rule_slab.xml",

        # Doctor
        "view/doctor/doctor_availability.xml",
        "view/doctor/doctor_timing.xml",

        # Appointment
        "view/appointment/appointment.xml",
        "view/appointment/my_appointment.xml",
        "view/appointment/opt.xml",
        "view/appointment/ot.xml",
        "view/appointment/meeting.xml",
        "view/appointment/appointment_reason.xml",

        # Notes
        "view/notes/notes.xml",
        "view/notes/reminder.xml",

        # Notice Board
        "view/notice_board/notice.xml",
        "view/notice_board/events.xml",

        # Product
        "view/product/product.xml",
        "view/product/product_group.xml",
        "view/product/product_sub_group.xml",
        "view/product/product_category.xml",
        "view/product/uom.xml",
        "view/product/tax.xml",
        "view/product/location.xml",
        "view/product/warehouse.xml",
        
        # Store
        "view/store/stock_adjustment.xml",
        "view/store/store_request.xml",
        "view/store/store_issue.xml",
        "view/store/store_return.xml",
        "view/store/store_accept.xml",
        "view/store/material_receipt.xml",
        "view/store/stock_move.xml",
        "view/store/store_config.xml",
        
        # Asserts
        "view/asserts/asserts_capitalisation.xml",
        "view/asserts/asserts.xml",
        "view/asserts/asserts_maintenance.xml",
        "view/asserts/asserts_reminder.xml",

        # Purchase
        "view/purchase/purchase_indent.xml",
        "view/purchase/indent_approval.xml",
        "view/purchase/vendor_selection.xml",
        "view/purchase/quotation.xml",
        "view/purchase/purchase_order.xml",
        "view/purchase/invoice.xml",

        # Purchase Return
        "view/purchase_return/po_return.xml",
        "view/purchase_return/invoice.xml",

        # Sales
        "view/sale/sale_order.xml",
        "view/sale/invoice.xml",

        # Sale Return
        "view/sale_return/so_return.xml",
        "view/sale_return/invoice.xml",

        # Account
        "view/account/account.xml",
        "view/account/journal.xml",
        "view/account/journal_entry.xml",
        "view/account/journal_detail.xml",

        # Menu
        "view/menu/menu.xml",
        "view/menu/sub_menu.xml",

    ],
    "demo": [

    ],
    "qweb": [

    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}