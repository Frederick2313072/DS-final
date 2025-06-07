import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from pathlib import Path
import os

warnings.filterwarnings('ignore')

def setup_chinese_fonts():
    try:
        plt.rcParams['font.sans-serif'] = [
            'SimHei', 
            'Noto Sans CJK SC', 
            'WenQuanYi Zen Hei',
            'Source Han Sans CN',
            'DejaVu Sans'
        ]
        plt.rcParams['axes.unicode_minus'] = False
        
        fig, ax = plt.subplots(figsize=(1, 1))
        ax.text(0.5, 0.5, '测试', fontsize=12, ha='center', va='center')
        plt.close(fig)
        print("中文字体配置成功")
        return True
    except Exception as e:
        print(f"中文字体配置失败，使用英文: {e}")
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        return False

def load_data():
    try:
        df = pd.read_csv('data/processed_imo_data_fixed.csv')
        print(f"数据加载成功，共 {len(df)} 条记录")
        return df
    except Exception as e:
        print(f"数据加载失败: {e}")
        return None

def create_data_overview(df, use_chinese=True):
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('IMO Competition Data Overview' if not use_chinese else 'IMO竞赛数据概览', 
                 fontsize=16, fontweight='bold')
    
    years = df['year'].value_counts().sort_index()
    axes[0, 0].plot(years.index, years.values, marker='o', linewidth=2, markersize=6)
    axes[0, 0].set_title('Participation Trends' if not use_chinese else '参与趋势')
    axes[0, 0].set_xlabel('Year' if not use_chinese else '年份')
    axes[0, 0].set_ylabel('Number of Participants' if not use_chinese else '参与人数')
    axes[0, 0].grid(True, alpha=0.3)
    
    axes[0, 1].hist(df['total'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    axes[0, 1].set_title('Total Score Distribution' if not use_chinese else '总分分布')
    axes[0, 1].set_xlabel('Total Score' if not use_chinese else '总分')
    axes[0, 1].set_ylabel('Frequency' if not use_chinese else '频次')
    axes[0, 1].grid(True, alpha=0.3)
    
    award_counts = df['award'].value_counts()
    colors = ['gold', 'silver', '#CD7F32', 'lightgray']
    axes[1, 0].pie(award_counts.values, labels=award_counts.index, autopct='%1.1f%%', 
                   colors=colors, startangle=90)
    axes[1, 0].set_title('Award Distribution' if not use_chinese else '奖项分布')
    
    problem_scores = [df[f'p{i}'].mean() for i in range(1, 7)]
    problem_names = [f'P{i}' for i in range(1, 7)]
    bars = axes[1, 1].bar(problem_names, problem_scores, color='lightcoral', alpha=0.8)
    axes[1, 1].set_title('Average Score by Problem' if not use_chinese else '各题平均得分')
    axes[1, 1].set_xlabel('Problem' if not use_chinese else '题目')
    axes[1, 1].set_ylabel('Average Score' if not use_chinese else '平均得分')
    axes[1, 1].set_ylim(0, 7)
    
    for bar, score in zip(bars, problem_scores):
        axes[1, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                        f'{score:.1f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('fig/data_overview.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("数据概览图已保存")

def create_country_analysis(df, use_chinese=True):
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Country Performance Analysis' if not use_chinese else '国家表现分析', 
                 fontsize=16, fontweight='bold')
    
    top_countries = df.groupby('country')['total'].mean().sort_values(ascending=False).head(15)
    bars = axes[0, 0].barh(range(len(top_countries)), top_countries.values, color='steelblue', alpha=0.8)
    axes[0, 0].set_yticks(range(len(top_countries)))
    axes[0, 0].set_yticklabels(top_countries.index)
    axes[0, 0].set_title('Top 15 Countries by Average Score' if not use_chinese else '平均分前15名国家')
    axes[0, 0].set_xlabel('Average Total Score' if not use_chinese else '平均总分')
    
    for i, (bar, score) in enumerate(zip(bars, top_countries.values)):
        axes[0, 0].text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, 
                        f'{score:.1f}', va='center', ha='left')
    
    gold_medals = df[df['award'] == 'Gold Medal'].groupby('country').size().sort_values(ascending=False).head(10)
    axes[0, 1].bar(range(len(gold_medals)), gold_medals.values, color='gold', alpha=0.8)
    axes[0, 1].set_xticks(range(len(gold_medals)))
    axes[0, 1].set_xticklabels(gold_medals.index, rotation=45, ha='right')
    axes[0, 1].set_title('Top 10 Countries by Gold Medals' if not use_chinese else '金牌数前10名国家')
    axes[0, 1].set_ylabel('Number of Gold Medals' if not use_chinese else '金牌数量')
    
    country_stats = df.groupby('country').agg({
        'total': 'mean',
        'individual_rank': 'mean'
    }).reset_index()
    
    scatter = axes[1, 0].scatter(country_stats['total'], country_stats['individual_rank'], 
                                alpha=0.6, s=50, color='purple')
    axes[1, 0].set_xlabel('Average Total Score' if not use_chinese else '平均总分')
    axes[1, 0].set_ylabel('Average Rank' if not use_chinese else '平均排名')
    axes[1, 0].set_title('Score vs Rank by Country' if not use_chinese else '国家得分与排名关系')
    axes[1, 0].invert_yaxis()
    axes[1, 0].grid(True, alpha=0.3)
    
    yearly_performance = df.groupby(['year', 'country'])['total'].mean().reset_index()
    top_5_countries = df.groupby('country')['total'].mean().sort_values(ascending=False).head(5).index
    
    for country in top_5_countries:
        country_data = yearly_performance[yearly_performance['country'] == country]
        axes[1, 1].plot(country_data['year'], country_data['total'], 
                       marker='o', label=country, linewidth=2, markersize=4)
    
    axes[1, 1].set_title('Performance Trends of Top 5 Countries' if not use_chinese else '前5名国家表现趋势')
    axes[1, 1].set_xlabel('Year' if not use_chinese else '年份')
    axes[1, 1].set_ylabel('Average Total Score' if not use_chinese else '平均总分')
    axes[1, 1].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('fig/country_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("国家分析图已保存")

def create_problem_difficulty_analysis(df, use_chinese=True):
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Problem Difficulty Analysis' if not use_chinese else '题目难度分析', 
                 fontsize=16, fontweight='bold')
    
    problem_cols = [f'p{i}' for i in range(1, 7)]
    problem_names = [f'P{i}' for i in range(1, 7)]
    problem_data = df[problem_cols].values.flatten()
    problem_labels = np.repeat(problem_names, len(df))
    
    box_data = [df[col].dropna() for col in problem_cols]
    bp = axes[0, 0].boxplot(box_data, labels=problem_names, patch_artist=True)
    colors = plt.cm.viridis(np.linspace(0, 1, 6))
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    axes[0, 0].set_title('Score Distribution by Problem' if not use_chinese else '各题得分分布')
    axes[0, 0].set_xlabel('Problem' if not use_chinese else '题目')
    axes[0, 0].set_ylabel('Score' if not use_chinese else '得分')
    axes[0, 0].grid(True, alpha=0.3)
    
    zero_rates = [df[col].eq(0).mean() * 100 for col in problem_cols]
    full_rates = [df[col].eq(7).mean() * 100 for col in problem_cols]
    
    x = np.arange(len(problem_cols))
    width = 0.35
    
    bars1 = axes[0, 1].bar(x - width/2, zero_rates, width, label='Zero Score Rate' if not use_chinese else '零分率', 
                          color='red', alpha=0.7)
    bars2 = axes[0, 1].bar(x + width/2, full_rates, width, label='Full Score Rate' if not use_chinese else '满分率', 
                          color='green', alpha=0.7)
    
    axes[0, 1].set_title('Zero Score and Full Score Rates' if not use_chinese else '零分率与满分率')
    axes[0, 1].set_xlabel('Problem' if not use_chinese else '题目')
    axes[0, 1].set_ylabel('Percentage (%)' if not use_chinese else '百分比 (%)')
    axes[0, 1].set_xticks(x)
    axes[0, 1].set_xticklabels(problem_names)
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            axes[0, 1].text(bar.get_x() + bar.get_width()/2., height + 0.5,
                           f'{height:.1f}%', ha='center', va='bottom', fontsize=8)
    
    corr_matrix = df[problem_cols].corr()
    im = axes[1, 0].imshow(corr_matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
    axes[1, 0].set_xticks(range(len(problem_cols)))
    axes[1, 0].set_yticks(range(len(problem_cols)))
    axes[1, 0].set_xticklabels(problem_names)
    axes[1, 0].set_yticklabels(problem_names)
    axes[1, 0].set_title('Problem Score Correlation' if not use_chinese else '题目得分相关性')
    
    for i in range(len(problem_cols)):
        for j in range(len(problem_cols)):
            text = axes[1, 0].text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                                  ha="center", va="center", color="black", fontsize=8)
    
    plt.colorbar(im, ax=axes[1, 0])
    
    yearly_difficulty = df.groupby('year')[problem_cols].mean()
    for i, (col, name) in enumerate(zip(problem_cols, problem_names)):
        axes[1, 1].plot(yearly_difficulty.index, yearly_difficulty[col], 
                       marker='o', label=name, linewidth=2, markersize=4)
    
    axes[1, 1].set_title('Problem Difficulty Trends Over Years' if not use_chinese else '题目难度年度趋势')
    axes[1, 1].set_xlabel('Year' if not use_chinese else '年份')
    axes[1, 1].set_ylabel('Average Score' if not use_chinese else '平均得分')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('fig/problem_difficulty.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("题目难度分析图已保存")

def create_award_analysis(df, use_chinese=True):
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Award Analysis' if not use_chinese else '奖项分析', 
                 fontsize=16, fontweight='bold')
    
    award_order = ['Gold Medal', 'Silver Medal', 'Bronze Medal', 'Honourable Mention']
    award_counts_by_year = df.groupby(['year', 'award']).size().unstack(fill_value=0)
    award_counts_by_year = award_counts_by_year.reindex(columns=award_order, fill_value=0)
    
    colors = ['gold', 'silver', '#CD7F32', 'lightgray']
    award_counts_by_year.plot(kind='bar', stacked=True, ax=axes[0, 0], color=colors, alpha=0.8)
    axes[0, 0].set_title('Award Distribution by Year' if not use_chinese else '年度奖项分布')
    axes[0, 0].set_xlabel('Year' if not use_chinese else '年份')
    axes[0, 0].set_ylabel('Number of Awards' if not use_chinese else '奖项数量')
    axes[0, 0].legend(title='Award Type' if not use_chinese else '奖项类型')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    award_proportions = df['award'].value_counts(normalize=True) * 100
    award_proportions = award_proportions.reindex(award_order, fill_value=0)
    
    yearly_proportions = []
    years = sorted(df['year'].unique())
    for year in years:
        year_data = df[df['year'] == year]
        proportions = year_data['award'].value_counts(normalize=True) * 100
        proportions = proportions.reindex(award_order, fill_value=0)
        yearly_proportions.append(proportions)
    
    yearly_proportions_df = pd.DataFrame(yearly_proportions, index=years)
    
    for i, award in enumerate(award_order):
        axes[0, 1].plot(years, yearly_proportions_df[award], 
                       marker='o', label=award, color=colors[i], linewidth=2, markersize=4)
    
    axes[0, 1].set_title('Award Proportion Trends' if not use_chinese else '奖项比例趋势')
    axes[0, 1].set_xlabel('Year' if not use_chinese else '年份')
    axes[0, 1].set_ylabel('Percentage (%)' if not use_chinese else '百分比 (%)')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    problem_cols = [f'p{i}' for i in range(1, 7)]
    problem_names = [f'P{i}' for i in range(1, 7)]
    award_problem_performance = df.groupby('award')[problem_cols].mean()
    award_problem_performance = award_problem_performance.reindex(award_order)
    
    x = np.arange(len(problem_cols))
    width = 0.2
    
    for i, award in enumerate(award_order):
        offset = (i - 1.5) * width
        bars = axes[1, 0].bar(x + offset, award_problem_performance.loc[award], 
                             width, label=award, color=colors[i], alpha=0.8)
    
    axes[1, 0].set_title('Problem Performance by Award Type' if not use_chinese else '不同奖项各题表现')
    axes[1, 0].set_xlabel('Problem' if not use_chinese else '题目')
    axes[1, 0].set_ylabel('Average Score' if not use_chinese else '平均得分')
    axes[1, 0].set_xticks(x)
    axes[1, 0].set_xticklabels(problem_names)
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    cutoff_scores = []
    years = sorted(df['year'].unique())
    
    for year in years:
        year_data = df[df['year'] == year].sort_values('total', ascending=False)
        
        gold_cutoff = year_data[year_data['award'] == 'Gold Medal']['total'].min() if len(year_data[year_data['award'] == 'Gold Medal']) > 0 else 0
        silver_cutoff = year_data[year_data['award'] == 'Silver Medal']['total'].min() if len(year_data[year_data['award'] == 'Silver Medal']) > 0 else 0
        bronze_cutoff = year_data[year_data['award'] == 'Bronze Medal']['total'].min() if len(year_data[year_data['award'] == 'Bronze Medal']) > 0 else 0
        
        cutoff_scores.append({
            'year': year,
            'Gold': gold_cutoff,
            'Silver': silver_cutoff,
            'Bronze': bronze_cutoff
        })
    
    cutoff_df = pd.DataFrame(cutoff_scores)
    
    axes[1, 1].plot(cutoff_df['year'], cutoff_df['Gold'], marker='o', label='Gold Medal', color='gold', linewidth=2)
    axes[1, 1].plot(cutoff_df['year'], cutoff_df['Silver'], marker='s', label='Silver Medal', color='silver', linewidth=2)
    axes[1, 1].plot(cutoff_df['year'], cutoff_df['Bronze'], marker='^', label='Bronze Medal', color='#CD7F32', linewidth=2)
    
    axes[1, 1].set_title('Award Cutoff Score Trends' if not use_chinese else '奖项分数线趋势')
    axes[1, 1].set_xlabel('Year' if not use_chinese else '年份')
    axes[1, 1].set_ylabel('Minimum Score' if not use_chinese else '最低分数')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('fig/award_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("奖项分析图已保存")

def generate_summary_statistics(df):
    print("\n" + "="*60)
    print("IMO数据统计摘要")
    print("="*60)
    
    print(f"数据时间范围: {df['year'].min()} - {df['year'].max()}")
    print(f"总参赛人数: {len(df):,}")
    print(f"参赛国家数: {df['country'].nunique()}")
    print(f"平均总分: {df['total'].mean():.2f}")
    print(f"总分标准差: {df['total'].std():.2f}")
    
    print("\n奖项分布:")
    award_counts = df['award'].value_counts()
    for award, count in award_counts.items():
        percentage = count / len(df) * 100
        print(f"  {award}: {count:,} ({percentage:.1f}%)")
    
    print("\n各题平均得分:")
    for i in range(1, 7):
        avg_score = df[f'p{i}'].mean()
        print(f"  P{i}: {avg_score:.2f}")
    
    print("\n表现最佳的国家 (按平均分):")
    top_countries = df.groupby('country')['total'].mean().sort_values(ascending=False).head(10)
    for i, (country, avg_score) in enumerate(top_countries.items(), 1):
        print(f"  {i:2d}. {country}: {avg_score:.2f}")
    
    print("="*60)

def main():
    print("开始IMO数据综合分析...")
    
    os.makedirs('fig', exist_ok=True)
    
    use_chinese = setup_chinese_fonts()
    
    df = load_data()
    if df is None:
        print("无法加载数据，程序退出")
        return
    
    print(f"使用{'中文' if use_chinese else '英文'}标签")
    
    print("生成数据概览图...")
    create_data_overview(df, use_chinese)
    
    print("生成国家分析图...")
    create_country_analysis(df, use_chinese)
    
    print("生成题目难度分析图...")
    create_problem_difficulty_analysis(df, use_chinese)
    
    print("生成奖项分析图...")
    create_award_analysis(df, use_chinese)
    
    print("生成地区分析图...")
    import subprocess
    subprocess.run(['python', 'src/regional_analysis.py'], check=False)
    
    generate_summary_statistics(df)
    
    print("\n所有分析图表已生成完成！")
    print("图表保存位置:")
    print("  - fig/data_overview.png")
    print("  - fig/country_analysis.png") 
    print("  - fig/problem_difficulty.png")
    print("  - fig/award_analysis.png")
    print("  - fig/regional_analysis.png")

if __name__ == "__main__":
    main() 