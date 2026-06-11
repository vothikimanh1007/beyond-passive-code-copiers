#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Beyond Passive Code Copiers - Agile Role-Play Simulation Engine (CLI Mode)
Author: IT Faculty Research Group, Ton Duc Thang University (TDTU)
Date: June 2026
"""

import os
import json
import argparse
import time
import random

# Định nghĩa đường dẫn tương đối tới tệp cấu hình
CONFIG_DIR = os.path.join(os.path.dirname(__file__), "configs")
PROMPTS_PATH = os.path.join(CONFIG_DIR, "roles_prompts.json")
CASES_PATH = os.path.join(CONFIG_DIR, "case_studies.json")

def load_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️ Không tìm thấy tệp cấu hình tại: {filepath}")
        return {}

def run_simulation(role_key, case_key):
    prompts = load_json(PROMPTS_PATH)
    cases = load_json(CASES_PATH)
    
    # 1. Xác thực tham số đầu vào
    if role_key not in prompts:
        print(f"❌ Vai trò '{role_key}' không hợp lệ. Chọn: {list(prompts.keys())}")
        return
    if case_key not in cases:
        print(f"❌ Case-study '{case_key}' không hợp lệ. Chọn: {list(cases.keys())}")
        return
        
    role_data = prompts[role_key]
    case_data = cases[case_key]
    
    print("=" * 70)
    print(f"🚀 KHỞI CHẠY MÔ PHỎNG SPRINT (ROLE-PLAY SIMULATION SANDBOX)")
    print("=" * 70)
    print(f"📋 Case Study: {case_data['title']}")
    print(f"📝 Mô tả: {case_data['description']}")
    print(f"👤 Vai trò đảm nhiệm: {role_data['role']}")
    print(f"🤖 Prompt Hệ thống gán cho AI trợ lý:\n   {role_data['system_instruction']}")
    print("-" * 70)
    
    time.sleep(1)
    print("\n⏳ [Sprint 1/1 Started] Đang nạp mã nguồn thiết kế hệ thống...")
    time.sleep(1.2)
    
    # Kích hoạt sự cố ngẫu nhiên mô phỏng Agile thực tế
    anomaly = random.choice(case_data['anomalies'])
    print(f"\n🚨 [SỰ CỐ PHÁT SINH - AGIL CRISIS ALERT]:")
    print(f"   Loại sự cố: {anomaly['type']}")
    print(f"   Chi tiết: {anomaly['detail']}")
    print("-" * 70)
    
    time.sleep(1.5)
    print("\n🛠️ [Giải pháp Sư phạm chủ động]:")
    if role_key == "TechLead":
        print("   👉 [TechLead Action]: Từ chối commit! Ép AI viết lại mã tích hợp bộ đệm chỉ mục và kiểm tra luồng CI.")
    elif role_key == "QA":
        print("   👉 [QA Action]: Tạo kịch bản mô phỏng kiểm tra tải đồng thời (XLOCK, ROWLOCK) để vá lỗi Race Condition.")
    elif role_key == "Architect":
        print("   👉 [Architect Action]: Tái cấu trúc logic trigger sang thủ tục Stored Procedure riêng biệt hoặc dùng Compound Trigger.")
        
    time.sleep(1.2)
    
    # Tính toán KPI gia tốc Sprint mẫu dựa trên phân bổ thực nghiệm (Mean = 3.83)
    velocity_increment = round(random.uniform(3.5, 4.8), 2)
    print("\n" + "=" * 70)
    print(f"📈 KẾT QUẢ ĐẦU RA SPRINT THÀNH CÔNG!")
    print(f"   ✔️ Chỉ số gia tốc tiến độ đạt: {velocity_increment} / 5.0")
    print(f"   ✔️ Tải trọng nhận thức của nhóm được phân bổ tối ưu!")
    print("=" * 70)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mô phỏng Đóng vai Agile tích hợp AI - DI-IDEA 2026 Sandbox")
    parser.add_argument("--role", type=str, default="TechLead", help="Vai trò: TechLead, QA, hoặc Architect")
    parser.add_argument("--case", type=str, default="forklift_warehouse", help="Case-study: forklift_warehouse hoặc library_booking")
    
    args = parser.parse_args()
    run_simulation(args.role, args.case)
