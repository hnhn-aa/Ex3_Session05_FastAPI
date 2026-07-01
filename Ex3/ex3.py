from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List

# ==========================================
# DỮ LIỆU MOCKUP (Giữ nguyên từ đề bài)
# ==========================================
students = [
    {"id": 1, "name": "Nguyen Van A"},
    {"id": 2, "name": "Tran Thi B"},
    {"id": 3, "name": "Le Van C"}
]

courses = [
    {"id": 1, "name": "FastAPI Basic", "capacity": 2},
    {"id": 2, "name": "Python OOP", "capacity": 2}
]

registrations = [
    {"id": 1, "student_id": 1, "course_id": 1},
    {"id": 2, "student_id": 2, "course_id": 1}
]

# ==========================================
# PYDANTIC MODEL (Validate dữ liệu đầu vào)
# ==========================================
class CreateRegistration(BaseModel):
    student_id: int
    course_id: int

app = FastAPI()

# ==========================================
# API CREATE PHIẾU ĐĂNG KÝ
# ==========================================
@app.post("/registrations")
def create_registration(new_reg: CreateRegistration):
    # 1. Kiểm tra student_id có tồn tại không
    student_exists = False
    for student in students:
        if student["id"] == new_reg.student_id:
            student_exists = True
            break
            
    if not student_exists:
        return {
            "message": "Student not found",
            "data": None
        }

    # 2. Kiểm tra course_id có tồn tại không và lấy thông tin khóa học
    target_course = None
    for course in courses:
        if course["id"] == new_reg.course_id:
            target_course = course
            break
            
    if not target_course:
        return {
            "message": "Course not found",
            "data": None
        }

    # 3. BẪY 1: Kiểm tra học viên đã đăng ký trùng khóa này chưa
    for reg in registrations:
        if reg["student_id"] == new_reg.student_id and reg["course_id"] == new_reg.course_id:
            return {
                "detail": "Student already registered this course"
            }

    # 4. BẪY 2: Kiểm tra sĩ số khóa học (Capacity)
    current_enrolled = 0
    for reg in registrations:
        if reg["course_id"] == new_reg.course_id:
            current_enrolled += 1
            
    if current_enrolled >= target_course["capacity"]:
        return {
            "detail": "Course is full"
        }

    # 5. Tạo id mới (tự động tăng dựa trên phần tử cuối cùng)
    new_id = registrations[-1]["id"] + 1 if registrations else 1

    # 6. Thêm phiếu đăng ký mới vào hệ thống
    new_record = {
        "id": new_id,
        "student_id": new_reg.student_id,
        "course_id": new_reg.course_id
    }
    registrations.append(new_record)

    # 7. Trả về kết quả thành công
    return {
        "message": "Đăng ký khóa học thành công",
        "data": new_record
    }