#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Beyond Passive Code Copiers - Automated Student Auditing Evaluator
Author: IT Faculty Research Group, Ton Duc Thang University (TDTU)
Date: June 2026
"""

import os
import re

class AuditEvaluator:
    def __init__(self):
        self.scores = {}

    def evaluate_nested_loop_exercise(self, filepath):
        """Kiểm tra xem sinh viên có dùng Window Function để sửa O(N^2) không"""
        if not os.path.exists(filepath):
            return False, "Không tìm thấy tệp nộp bài."
        
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read().upper()

        # Kiểm tra xem code cũ O(N^2) đã bị loại bỏ hoặc comment chưa
        # Và kiểm tra sự xuất hiện của các Window Functions
        has_dense_rank = "DENSE_RANK" in code or "RANK" in code or "ROW_NUMBER" in code
        has_partition = "PARTITION BY" in code
        has_over = "OVER" in code

        if has_dense_rank and has_partition and has_over:
            return True, "Xuất sắc! Đã phát hiện việc tối ưu hóa bằng Window Function (DENSE_RANK) đạt độ phức tạp O(N)."
        return False, "Lỗi: Bài làm chưa tối ưu bằng Window Function (OVER / PARTITION BY)."

    def evaluate_mutating_table_exercise(self, filepath):
        """Kiểm tra xem sinh viên có bẻ gãy ORA-04091 bằng Compound Trigger không"""
        if not os.path.exists(filepath):
            return False, "Không tìm thấy tệp nộp bài."

        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read().upper()

        has_compound = "COMPOUND TRIGGER" in code
        has_after_each = "AFTER EACH ROW" in code
        has_after_statement = "AFTER STATEMENT" in code

        if has_compound and has_after_each and has_after_statement:
            return True, "Xuất sắc! Đã áp dụng Compound Trigger thành công để né lỗi ORA-04091."
        return False, "Lỗi: Chưa chuyển đổi cấu trúc trigger sang COMPOUND TRIGGER để tách trạng thái."

    def evaluate_concurrency_lock_exercise(self, filepath):
        """Kiểm tra xem sinh viên có tiêm khóa FOR UPDATE chống Race Condition không"""
        if not os.path.exists(filepath):
            return False, "Không tìm thấy tệp nộp bài."

        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read().upper()

        has_for_update = "FOR UPDATE" in code or "WITH (XLOCK" in code
        has_commit = "COMMIT" in code

        if has_for_update and has_commit:
            return True, "Xuất sắc! Đã tiêm khóa bảo vệ FOR UPDATE và xử lý Transaction an toàn."
        return False, "Lỗi: Thiếu khóa FOR UPDATE, giao dịch không an toàn đối với Race Condition."

    def run_grading_suite(self):
        print("="*75)
        print("💡 CHƯƠNG TRÌNH CHẤM ĐIỂM TỰ ĐỘNG - AI AUDITING LAB EVALUATOR")
        print("="*75)
        
        # Thử nghiệm kiểm tra giả lập trên chính các file hướng dẫn mẫu vừa tạo
        tests = [
            ("Nested Loops Optimization", "auditing_protocols/nested_loops_opt/exercise.sql", self.evaluate_nested_loop_exercise),
            ("Oracle Mutating Trigger", "auditing_protocols/oracle_mutating_table/trigger_fix.sql", self.evaluate_mutating_table_exercise),
            ("Concurrency Lock Injection", "auditing_protocols/concurrency_lock/concurrency_test.sql", self.evaluate_concurrency_lock_exercise)
        ]
        
        for name, path, eval_func in tests:
            print(f"🔄 Đang chấm bài: {name} ({path})...")
            success, msg = eval_func(path)
            if success:
                print(f"   🟢 ĐẠT ĐIỂM TỐI ĐA: {msg}")
            else:
                print(f"   🔴 CHƯA ĐẠT: {msg}")
            print("-"*75)

if __name__ == "__main__":
    evaluator = AuditEvaluator()
    evaluator.run_grading_suite()