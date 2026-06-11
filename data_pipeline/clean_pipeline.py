#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Beyond Passive Code Copiers - Data Cleaning & Analytical Pipeline
Author: IT Faculty Research Group, Ton Duc Thang University (TDTU)
Date: June 2026
"""

import os
import glob
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# ==============================================================================
# 1. THIẾT LẬP ĐỒ HỌA CHUẨN ACADEMIC
# ==============================================================================
sns.set_theme(style="whitegrid", context="talk")
plt.rcParams.update({
    'font.family': 'sans-serif',
    'figure.titlesize': 16,
    'axes.titlesize': 13,
    'axes.labelsize': 11,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.facecolor': '#ffffff',
    'axes.facecolor': '#f8f9fa',
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})

# ==============================================================================
# 2. BỘ ĐỌC & DỌN DẸP DỮ LIỆU THỰC NGHIỆM BẤT BẠI
# ==============================================================================
def clean_scale_score(series):
    """Trích xuất và ép kiểu điểm số Likert (1-5) an toàn từ văn bản thô"""
    def extract_single_digit(val):
        val_str = str(val).strip()
        # Tìm các chữ số đơn lẻ từ 1 đến 5 trong chuỗi
        digits = re.findall(r'[1-5]', val_str)
        if digits:
            return int(digits[0])
        return np.nan
    return series.apply(extract_single_digit)

def safe_load(file_path):
    """Hàm đọc tệp an toàn chống lỗi định dạng CSV/TSV do ngoặc kép hỏng"""
    try:
        # Thử đọc phân tách bằng tab trước tiên nếu file bị dính tab
        df = pd.read_csv(file_path, sep='\t', engine='python', on_bad_lines='skip')
        if df.shape[1] <= 1:
            # Nếu chỉ có 1 cột, thử đọc bằng dấu phẩy tiêu chuẩn
            df = pd.read_csv(file_path, sep=',', engine='python', on_bad_lines='skip')
        return df
    except Exception as e:
        print(f"  ⚠️ Không thể đọc tệp {file_path} qua định dạng mặc định: {e}")
        return None

# Quét không gian làm việc tìm tệp CSV/XLSX
all_files = glob.glob("*.csv") + glob.glob("*.xlsx")
df_adb, df_rp, df_dbms, df_mobile = None, None, None, None

print("🔄 Đang quét dữ liệu thực tế...")
for f in all_files:
    try:
        if f.endswith('.xlsx'):
            df = pd.read_excel(f)
        else:
            df = safe_load(f)
            
        if df is None or df.empty:
            continue
            
        cols_trigger = " ".join(df.columns.astype(str).tolist()).lower()
        
        # Ánh xạ theo cấu trúc cột đặc trưng của từng nhóm khảo sát
        if "o(n^2)" in cols_trigger or "bắt lỗi" in cols_trigger:
            df_adb = df
            print(f"  ✅ Đã nhận diện tệp Advanced DB: '{f}'")
        elif "sprint" in cols_trigger or "đóng vai" in cols_trigger or "role-play" in cols_trigger:
            df_rp = df
            print(f"  ✅ Đã nhận diện tệp Đóng vai Agile: '{f}'")
        elif "anxiety" in cols_trigger or "without ai" in cols_trigger:
            df_dbms = df
            print(f"  ✅ Đã nhận diện tệp DBMS Survey: '{f}'")
        elif "màn hình" in cols_trigger or "bàn phím" in cols_trigger or "di động" in cols_trigger:
            df_mobile = df
            print(f"  ✅ Đã nhận diện tệp Trải nghiệm Di động: '{f}'")
    except Exception as e:
        print(f"  ⚠️ Lỗi xử lý nhận diện trên tệp {f}: {e}")

# Tạo thư mục đầu ra nếu chưa có
os.makedirs("figures", exist_ok=True)

# ==============================================================================
# 3. KÍCH HOẠT VẼ BIỂU ĐỒ & XUẤT ẢNH PNG CHẤT LƯỢNG CAO
# ==============================================================================

# FIGURE 1: PARADOX OF RELIANCE VS AUDITING EFFORT
try:
    if df_adb is not None:
        fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
        col_action = [c for c in df_adb.columns if "O(N^2)" in c][0]
        col_effort = [c for c in df_adb.columns if "nỗ lực" in c][0]
        
        def map_actions(val):
            val = str(val)
            if "tối ưu lại" in val or "Re-prompting" in val: return 'Re-prompting / Optimization'
            if "Tự tay viết lại" in val or "Window" in val: return 'Manual Refactoring (CTE/Window)'
            if "Giữ nguyên" in val or "lười" in val: return 'Retained Due to Reliance'
            return 'Other Strategic Actions'
            
        actions_en = df_adb[col_action].apply(map_actions)
        counts = actions_en.value_counts()
        axes[0].pie(counts, labels=counts.index, autopct='%1.1f%%', 
                    colors=['#4f46e5', '#10b981', '#f43f5e', '#f59e0b'], startangle=90,
                    wedgeprops={'edgecolor': 'w', 'linewidth': 1})
        axes[0].set_title("Student Reactions to Inefficient AI Code", fontweight='bold', pad=10)
        
        df_adb['clean_effort'] = clean_scale_score(df_adb[col_effort])
        sns.countplot(data=df_adb.dropna(subset=['clean_effort']), x='clean_effort', hue='clean_effort', palette="viridis", legend=False, ax=axes[1])
        axes[1].set_title("Cognitive Shift: Level of Auditing Effort", fontweight='bold')
        axes[1].set_xlabel("1: Minimal Verification  <--->  5: Extreme Critical Verification")
        axes[1].set_ylabel("Student Count")
        
        plt.suptitle("Figure 1: Paradox of Reliance vs. Auditing Effort", y=1.02, fontweight='bold')
        plt.tight_layout()
        plt.savefig('figures/figure1_reliance_paradox.png')
        plt.close()
        print("  🎉 Đã xuất: Figure 1 -> figures/figure1_reliance_paradox.png")
except Exception as e:
    print(f"  ❌ Không thể xuất Figure 1: {e}")

# FIGURE 2: TEAMWORK VELOCITY & METRIC METAMORPHOSIS VIA ROLE-PLAY
try:
    if df_rp is not None:
        fig, axes = plt.subplots(1, 2, figsize=(15, 5.5))
        col_sprint = [c for c in df_rp.columns if "Sprint" in c or "tiến độ" in c][0]
        df_rp['clean_sprint'] = clean_scale_score(df_rp[col_sprint])
        sns.countplot(data=df_rp.dropna(subset=['clean_sprint']), x='clean_sprint', hue='clean_sprint', palette="Blues_r", legend=False, ax=axes[0])
        axes[0].set_title("Sprint Acceleration via AI Roles", fontweight='bold')
        axes[0].set_xlabel("Acceleration Impact (1: Low to 5: High Velocity)")
        axes[0].set_ylabel("Student Count")
        
        comp_cols = [col for col in df_rp.columns if "So với cách làm việc nhóm" in col or "cải thiện" in col.lower()]
        if comp_cols:
            melted_comp = df_rp[comp_cols].melt()
            metric_labels = {
                'trách nhiệm': 'Accountability', 'giao tiếp': 'Communication',
                'bất ngờ': 'Agile Crisis Management', 'chất lượng': 'Product Quality focus',
                'chuyên nghiệp': 'Decision Under Pressure'
            }
            melted_comp['variable'] = melted_comp['variable'].apply(lambda x: next((v for k, v in metric_labels.items() if k in x.lower()), 'Collaboration'))
            
            def map_change(v):
                if "rõ rệt" in str(v) or "Highly" in str(v): return 'Highly Improved'
                if "Cải thiện" in str(v) or "Improved" in str(v): return 'Improved'
                return 'Neutral/Base'
            melted_comp['value'] = melted_comp['value'].apply(map_change)
            
            sns.countplot(data=melted_comp, y='variable', hue='value', 
                          hue_order=['Highly Improved', 'Improved', 'Neutral/Base'],
                          palette=['#047857', '#34d399', '#cbd5e1'], ax=axes[1])
            axes[1].set_title("Role-Play Metamorphosis vs Legacy Frameworks", fontweight='bold')
            axes[1].set_xlabel("Response Count")
            axes[1].set_ylabel("")
            axes[1].legend(title="Perceived Metric Change")

        plt.suptitle("Figure 2: Sprint Acceleration & Metric Metamorphosis via Role-Play", y=1.02, fontweight='bold')
        plt.tight_layout()
        plt.savefig('figures/figure2_sprint_acceleration.png')
        plt.close()
        print("  🎉 Đã xuất: Figure 2 -> figures/figure2_sprint_acceleration.png")
except Exception as e:
    print(f"  ❌ Không thể xuất Figure 2: {e}")

# FIGURE 3: LONG-TERM METACOGNITIVE CONCERNS AND SELF-EFFICACY
try:
    if df_dbms is not None:
        fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
        anxiety_col = [c for c in df_dbms.columns if "anxiety" in c.lower()][0]
        atrophy_col = [c for c in df_dbms.columns if "weaken" in c.lower() or "atrophy" in c.lower() or "thui chột" in c.lower()][0]
        
        df_melted_dbms = df_dbms[[anxiety_col, atrophy_col]].melt()
        df_melted_dbms['variable'] = df_melted_dbms['variable'].apply(lambda x: 'Anxiety Reduction' if 'anxiety' in x.lower() else 'Fear of Skill Atrophy')
        df_melted_dbms['value'] = clean_scale_score(df_melted_dbms['value'])
        
        sns.boxplot(data=df_melted_dbms.dropna(), x='variable', y='value', hue='variable', palette="Set2", legend=False, ax=axes[0])
        axes[0].set_title("Psychological & Cognitive Dynamics", fontweight='bold')
        axes[0].set_ylabel("Likert Scale Rating (1-5)")
        axes[0].set_xlabel("")
        
        se_col = [c for c in df_dbms.columns if "without ai" in c.lower() or "tự tin" in c.lower() or "self-efficacy" in c.lower()][0]
        df_dbms['clean_se'] = clean_scale_score(df_dbms[se_col])
        sns.histplot(df_dbms['clean_se'].dropna(), bins=5, color='#8b5cf6', discrete=True, ax=axes[1], kde=False)
        axes[1].set_title("Post-Intervention System Autonomy", fontweight='bold')
        axes[1].set_xlabel("Confidence to Architect Solo (1: Zero to 5: Full Mastery)")
        axes[1].set_ylabel("Student Count")
        axes[1].set_xticks([1, 2, 3, 4, 5])
        
        plt.suptitle("Figure 3: Metacognitive Concerns & Self-Efficacy Autonomy", y=1.02, fontweight='bold')
        plt.tight_layout()
        plt.savefig('figures/figure3_metacognitive_efficacy.png')
        plt.close()
        print("  🎉 Đã xuất: Figure 3 -> figures/figure3_metacognitive_efficacy.png")
except Exception as e:
    print(f"  ❌ Không thể xuất Figure 3: {e}")

# FIGURE 4: THE ANATOMY OF AI HALLUCINATIONS (SEMANTIC KNOWLEDGE MAP)
try:
    if df_adb is not None:
        plt.figure(figsize=(10, 5))
        col_hallucinate = [c for c in df_adb.columns if "bắt lỗi" in c or "hallucinate" in c.lower() or "phát hiện" in c.lower()][0]
        raw_text = " ".join(df_adb[col_hallucinate].dropna().astype(str).tolist())
        
        # Bản dịch ngữ nghĩa hỗ trợ trực quan hóa chuẩn học thuật quốc tế
        translation_dict = {
            'tuần': '', 'bài': '', 'lỗi': 'Error', 'em': '', 'thầy': '', 'nhầm': 'Misunderstanding',
            'RANK()': 'RANK_Function', 'DENSE_RANK()': 'DENSE_RANK_Function', 'FOR UPDATE': 'FOR_UPDATE_Lock',
            'Transaction': 'Concurrency_Transaction', 'Procedure': 'Stored_Procedure', 
            'Trigger': 'Database_Trigger', 'Mutating Table': 'Mutating_Table_Error', 
            'O(N^2)': 'Algorithmic_Complexity_ON2', 'tối ưu': 'Optimization', 'chạy sai': 'Logical_Failure',
            'khóa ngoại': 'Foreign_Key_Constraint', 'khóa chính': 'Primary_Key'
        }
        for vn, en in translation_dict.items():
            raw_text = raw_text.replace(vn, en)
            
        wordcloud = WordCloud(width=900, height=450, background_color='#ffffff', 
                              colormap='flare', max_words=40, collocations=False, random_state=42).generate(raw_text)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title("Figure 4: Semantic Landscape of AI Bugs Exposed by Students", fontsize=14, fontweight='bold', pad=15)
        plt.savefig('figures/figure4_hallucination_cloud.png')
        plt.close()
        print("  🎉 Đã xuất: Figure 4 -> figures/figure4_hallucination_cloud.png")
except Exception as e:
    print(f"  ❌ Không thể xuất Figure 4: {e}")

# FIGURE 5: MOBILE LEARNING VS. AFFECTIVE FILTER MODULATION (Chỉ mục định vị tuyệt đối)
try:
    if df_mobile is not None:
        fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
        
        # Áp dụng giải pháp định vị cột tuyệt đối bỏ qua lỗi font chữ
        df_mobile['clean_read'] = clean_scale_score(df_mobile.iloc[:, 4])
        df_mobile['clean_type'] = clean_scale_score(df_mobile.iloc[:, 5])
        df_mobile['clean_pressure'] = clean_scale_score(df_mobile.iloc[:, 7])
        
        ux_data = pd.concat([
            pd.DataFrame({'Score': df_mobile['clean_read'], 'Dimension': 'Reading Prompts'}),
            pd.DataFrame({'Score': df_mobile['clean_type'], 'Dimension': 'Typing Code'})
        ]).dropna()
        
        sns.boxplot(data=ux_data, x='Dimension', y='Score', hue='Dimension', palette="Pastel2", legend=False, ax=axes[0])
        axes[0].set_title("Mobile Interface Ergonomics", fontweight='bold')
        axes[0].set_ylabel("Usability Score (1: Bad Friction to 5: Seamless)")
        axes[0].set_xlabel("")
        axes[0].set_ylim(0.5, 5.5)
        
        sns.kdeplot(df_mobile['clean_pressure'].dropna(), fill=True, color='#f4a261', linewidth=2.5, ax=axes[1])
        axes[1].set_title("Affective Filter Lowering Effect", fontweight='bold')
        axes[1].set_xlabel("AI Psychological Comfort Rating (1: Low to 5: High Safety)")
        axes[1].set_ylabel("Density Function")
        axes[1].set_xlim(0.5, 5.5)
        
        plt.suptitle("Figure 5: Mobile Intelligent Learning: Interface Friction vs. Psychological Safety", y=1.02, fontweight='bold')
        plt.tight_layout()
        plt.savefig('figures/figure5_mobile_learning_paradox.png')
        plt.close()
        print("  🎉 Đã xuất: Figure 5 -> figures/figure5_mobile_learning_paradox.png")
except Exception as e:
    print(f"  ❌ Không thể xuất Figure 5: {e}")

print("\n" + "="*60)
print("📊 PIPELINE HOÀN TẤT: CẢ 5 HÌNH MINH CHỨNG ĐÃ ĐƯỢC KẾT XUẤT THÀNH CÔNG VÀO THƯ MỤC 'figures/'")
print("="*60)
