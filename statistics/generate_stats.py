#!/usr/bin/env python3
"""
Baekjoon 문제 풀이 통계 생성 스크립트
- 언어별 분포 통계
- 난이도별 분포 통계
- Solved.ac 프로필 정보
- 그래프 이미지 생성
"""

import os
import json
import re
import requests
from pathlib import Path
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 한글 폰트 설정 (macOS)
try:
    fm.fontManager.addfont('/System/Library/Fonts/AppleSDGothicNeo.ttc')
    plt.rcParams['font.sans-serif'] = ['Apple SD Gothic Neo']
except:
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']

# 색상 팔레트 (연보라색 중심)
PURPLE_PALETTE = {
    'dark_purple': '#5a3a7a',      # 진 보라
    'medium_purple': '#7d5ba8',    # 중간 보라
    'light_purple': '#9b7ebd',     # 연 보라
    'lighter_purple': '#b8a5d1',   # 더 연한 보라
    'lightest_purple': '#d4c5e2',  # 가장 연한 보라
}

# 언어별 색상
LANGUAGE_COLORS = {
    'C#': PURPLE_PALETTE['dark_purple'],
    'Python': PURPLE_PALETTE['medium_purple'],
    'C': PURPLE_PALETTE['light_purple'],
    'C++': PURPLE_PALETTE['lighter_purple'],
}

# 난이도별 색상
TIER_COLORS = {
    'Bronze': PURPLE_PALETTE['lightest_purple'],
    'Silver': PURPLE_PALETTE['lighter_purple'],
    'Gold': PURPLE_PALETTE['light_purple'],
    'Platinum': PURPLE_PALETTE['medium_purple'],
    'Diamond': PURPLE_PALETTE['dark_purple'],
}

class BaekjoonStats:
    def __init__(self, repo_path):
        self.repo_path = Path(repo_path)
        self.baekjoon_path = self.repo_path / "백준"
        self.stats_path = self.repo_path / "statistics"
        self.stats_path.mkdir(exist_ok=True)
        
        self.language_count = defaultdict(int)
        self.tier_count = defaultdict(int)
        self.total_problems = 0
        self.profile_info = {}
        
    def count_files(self):
        """백준 폴더의 모든 파일을 스캔하여 언어별, 난이도별로 분류"""
        if not self.baekjoon_path.exists():
            print("❌ 백준 폴더를 찾을 수 없습니다.")
            return False
        
        for root, dirs, files in os.walk(self.baekjoon_path):
            for file in files:
                # 파일 확장자로 언어 판단
                if file.endswith('.cs'):
                    language = 'C#'
                elif file.endswith('.py'):
                    language = 'Python'
                elif file.endswith('.c') and not file.endswith('.cpp'):
                    language = 'C'
                elif file.endswith('.cpp'):
                    language = 'C++'
                else:
                    continue
                
                # 난이도 추출 (폴더 구조: 백준/Bronze/... 또는 백준/Silver/... 등)
                rel_path = Path(root).relative_to(self.baekjoon_path)
                tier = rel_path.parts[0] if rel_path.parts else "Unknown"
                
                self.language_count[language] += 1
                self.tier_count[tier] += 1
                self.total_problems += 1
        
        return self.total_problems > 0
    
    def fetch_profile_info(self, username):
        """Solved.ac에서 프로필 정보 조회"""
        try:
            url = f"https://solved.ac/api/v3/user/show?handle={username}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            self.profile_info = {
                'username': data.get('handle'),
                'tier': data.get('tier'),
                'rating': data.get('rating'),
                'rank': data.get('rank'),
                'solved': data.get('solvedCount'),
            }
            return True
        except Exception as e:
            print(f"⚠️ Solved.ac 프로필 조회 실패: {e}")
            return False
    
    def save_stats_json(self):
        """통계를 JSON으로 저장"""
        stats = {
            'total_problems': self.total_problems,
            'language': dict(self.language_count),
            'tier': dict(self.tier_count),
            'profile': self.profile_info,
            'timestamp': __import__('datetime').datetime.now().isoformat(),
        }
        
        json_path = self.stats_path / "stats.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 통계 저장: {json_path}")
        return stats
    
    def generate_language_pie_chart(self):
        """언어별 분포 파이 차트 생성"""
        if not self.language_count:
            return
        
        fig, ax = plt.subplots(figsize=(10, 8), facecolor='white')
        
        languages = list(self.language_count.keys())
        counts = list(self.language_count.values())
        colors = [LANGUAGE_COLORS.get(lang, PURPLE_PALETTE['light_purple']) 
                 for lang in languages]
        
        # 파이 차트
        wedges, texts, autotexts = ax.pie(
            counts,
            labels=languages,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 12, 'weight': 'bold'},
            explode=[0.05] * len(languages),
        )
        
        # 자동 텍스트 스타일 (퍼센트)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(11)
            autotext.set_weight('bold')
        
        ax.set_title('프로그래밍 언어별 분포', fontsize=16, weight='bold', pad=20)
        
        plt.tight_layout()
        output_path = self.stats_path / "language_distribution.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"✅ 언어 차트 생성: {output_path}")
    
    def generate_tier_pie_chart(self):
        """난이도별 분포 파이 차트 생성"""
        if not self.tier_count:
            return
        
        # 난이도 순서 정렬
        tier_order = ['Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond']
        sorted_tiers = [t for t in tier_order if t in self.tier_count]
        counts = [self.tier_count[t] for t in sorted_tiers]
        colors = [TIER_COLORS.get(tier, PURPLE_PALETTE['light_purple']) 
                 for tier in sorted_tiers]
        
        fig, ax = plt.subplots(figsize=(10, 8), facecolor='white')
        
        # 파이 차트
        wedges, texts, autotexts = ax.pie(
            counts,
            labels=sorted_tiers,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 12, 'weight': 'bold'},
            explode=[0.05] * len(sorted_tiers),
        )
        
        # 자동 텍스트 스타일 (퍼센트)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(11)
            autotext.set_weight('bold')
        
        ax.set_title('난이도별 분포', fontsize=16, weight='bold', pad=20)
        
        plt.tight_layout()
        output_path = self.stats_path / "tier_distribution.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"✅ 난이도 차트 생성: {output_path}")
    
    def update_readme(self):
        """README.md의 통계 섹션을 자동으로 업데이트"""
        readme_path = self.repo_path / "README.md"
        
        if not readme_path.exists():
            print("⚠️ README.md를 찾을 수 없습니다.")
            return False
        
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Tier 이름 매핑
        tier_names = {
            1: "Bronze V", 2: "Bronze IV", 3: "Bronze III", 4: "Bronze II", 5: "Bronze I",
            6: "Silver V", 7: "Silver IV", 8: "Silver III", 9: "Silver II", 10: "Silver I",
            11: "Gold V", 12: "Gold IV", 13: "Gold III", 14: "Gold II", 15: "Gold I",
            16: "Platinum V", 17: "Platinum IV", 18: "Platinum III", 19: "Platinum II", 20: "Platinum I",
            21: "Diamond V", 22: "Diamond IV", 23: "Diamond III", 24: "Diamond II", 25: "Diamond I",
        }
        
        tier_num = self.profile_info.get('tier', 0)
        tier_name = tier_names.get(tier_num, "Unknown")
        rank = self.profile_info.get('rank', 0)
        username = self.profile_info.get('username', 'sernn')
        solved = self.profile_info.get('solved', 'N/A')
        rating = self.profile_info.get('rating', 'N/A')
        
        # 통계 섹션 생성
        stats_section = f"""## 📌 요약 정보

### 📊 총 풀이 문제 수

| 통계 | 값 |
|------|-----|
| **이 레포지토리의 풀이** | {self.total_problems}개 |
| **Solved.ac 전체 풀이** | {solved}개 |

### 🏆 Solved.ac 프로필 정보

| 항목 | 정보 |
|------|------|
| **아이디** | {username} |
| **레이팅** | {rating} |
| **티어** | {tier_num} ({tier_name}) |
| **순위** | {rank:,}위 |

**🔗 [Solved.ac 프로필 바로가기](https://solved.ac/profile/{username})**
"""
        
        # 기존 통계 섹션 찾아서 교체
        pattern = r"## 📌 요약 정보\n\n(?:.*?\n)*?(?=---|\Z)"
        content = re.sub(pattern, stats_section.rstrip() + "\n\n---\n", content, flags=re.DOTALL)
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ README 업데이트: {readme_path}")
        return True
    
    def run(self, username='sernn'):
        """전체 통계 생성 프로세스 실행"""
        print("🚀 Baekjoon 통계 생성 시작...\n")
        
        # 1. 파일 카운트
        if self.count_files():
            print(f"✅ 파일 스캔 완료: 총 {self.total_problems}개 문제")
            print(f"   언어: {dict(self.language_count)}")
            print(f"   난이도: {dict(self.tier_count)}\n")
        else:
            print("❌ 파일을 찾을 수 없습니다.")
            return False
        
        # 2. Solved.ac 프로필 정보
        print("📡 Solved.ac 프로필 정보 조회 중...")
        self.fetch_profile_info(username)
        if self.profile_info:
            print(f"✅ 프로필 조회 완료: {self.profile_info}\n")
        
        # 3. JSON 저장
        self.save_stats_json()
        
        # 4. 그래프 생성
        print("\n📊 그래프 생성 중...")
        self.generate_language_pie_chart()
        self.generate_tier_pie_chart()
        
        # 5. README 업데이트
        print("\n📝 README 업데이트 중...")
        self.update_readme()
        
        print("\n✨ 모든 통계 생성 완료!")
        return True

if __name__ == "__main__":
    # 스크립트 위치의 부모 폴더를 레포지토리로 인식
    repo_path = Path(__file__).parent.parent
    
    stats = BaekjoonStats(repo_path)
    stats.run(username='sernn')
