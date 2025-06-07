#!/usr/bin/env python3
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

def create_continent_mapping():
    continent_map = {
        'China': '亚洲',
        'Japan': '亚洲',
        'South Korea': '亚洲',
        'North Korea': '亚洲',
        'Taiwan': '亚洲',
        'Hong Kong': '亚洲',
        'Singapore': '亚洲',
        'Thailand': '亚洲',
        'Vietnam': '亚洲',
        'India': '亚洲',
        'Iran': '亚洲',
        'Kazakhstan': '亚洲',
        'Mongolia': '亚洲',
        'Indonesia': '亚洲',
        'Philippines': '亚洲',
        'Malaysia': '亚洲',
        'Bangladesh': '亚洲',
        'Sri Lanka': '亚洲',
        'Myanmar': '亚洲',
        'Uzbekistan': '亚洲',
        'Kyrgyzstan': '亚洲',
        'Tajikistan': '亚洲',
        'Turkmenistan': '亚洲',
        'Afghanistan': '亚洲',
        'Pakistan': '亚洲',
        'Nepal': '亚洲',
        'Bhutan': '亚洲',
        'Maldives': '亚洲',
        'Brunei': '亚洲',
        'Cambodia': '亚洲',
        'Laos': '亚洲',
        'Macau': '亚洲',
        
        'United States': '北美洲',
        'Canada': '北美洲',
        'Mexico': '北美洲',
        'Guatemala': '北美洲',
        'Costa Rica': '北美洲',
        'El Salvador': '北美洲',
        'Honduras': '北美洲',
        'Nicaragua': '北美洲',
        'Panama': '北美洲',
        'Belize': '北美洲',
        'Jamaica': '北美洲',
        'Cuba': '北美洲',
        'Dominican Republic': '北美洲',
        'Haiti': '北美洲',
        'Trinidad and Tobago': '北美洲',
        'Barbados': '北美洲',
        
        'Brazil': '南美洲',
        'Argentina': '南美洲',
        'Chile': '南美洲',
        'Peru': '南美洲',
        'Colombia': '南美洲',
        'Venezuela': '南美洲',
        'Ecuador': '南美洲',
        'Bolivia': '南美洲',
        'Uruguay': '南美洲',
        'Paraguay': '南美洲',
        'Guyana': '南美洲',
        'Suriname': '南美洲',
        
        'Russia': '欧洲',
        'Germany': '欧洲',
        'France': '欧洲',
        'United Kingdom': '欧洲',
        'Italy': '欧洲',
        'Spain': '欧洲',
        'Poland': '欧洲',
        'Romania': '欧洲',
        'Netherlands': '欧洲',
        'Belgium': '欧洲',
        'Czech Republic': '欧洲',
        'Greece': '欧洲',
        'Portugal': '欧洲',
        'Sweden': '欧洲',
        'Hungary': '欧洲',
        'Austria': '欧洲',
        'Belarus': '欧洲',
        'Switzerland': '欧洲',
        'Bulgaria': '欧洲',
        'Serbia': '欧洲',
        'Croatia': '欧洲',
        'Slovakia': '欧洲',
        'Slovenia': '欧洲',
        'Lithuania': '欧洲',
        'Latvia': '欧洲',
        'Estonia': '欧洲',
        'Denmark': '欧洲',
        'Finland': '欧洲',
        'Norway': '欧洲',
        'Iceland': '欧洲',
        'Ireland': '欧洲',
        'Luxembourg': '欧洲',
        'Malta': '欧洲',
        'Cyprus': '欧洲',
        'Moldova': '欧洲',
        'Ukraine': '欧洲',
        'Bosnia and Herzegovina': '欧洲',
        'Montenegro': '欧洲',
        'North Macedonia': '欧洲',
        'Albania': '欧洲',
        'Kosovo': '欧洲',
        'Georgia': '欧洲',
        'Armenia': '欧洲',
        'Azerbaijan': '欧洲',
        'Turkey': '欧洲',
        
        'Australia': '大洋洲',
        'New Zealand': '大洋洲',
        'Fiji': '大洋洲',
        'Papua New Guinea': '大洋洲',
        'Solomon Islands': '大洋洲',
        'Vanuatu': '大洋洲',
        'Samoa': '大洋洲',
        'Tonga': '大洋洲',
        'Palau': '大洋洲',
        'Marshall Islands': '大洋洲',
        'Micronesia': '大洋洲',
        'Kiribati': '大洋洲',
        'Nauru': '大洋洲',
        'Tuvalu': '大洋洲',
        
        'South Africa': '非洲',
        'Egypt': '非洲',
        'Nigeria': '非洲',
        'Kenya': '非洲',
        'Morocco': '非洲',
        'Tunisia': '非洲',
        'Algeria': '非洲',
        'Libya': '非洲',
        'Ethiopia': '非洲',
        'Ghana': '非洲',
        'Uganda': '非洲',
        'Tanzania': '非洲',
        'Zimbabwe': '非洲',
        'Zambia': '非洲',
        'Botswana': '非洲',
        'Namibia': '非洲',
        'Mozambique': '非洲',
        'Madagascar': '非洲',
        'Mauritius': '非洲',
        'Seychelles': '非洲',
        'Cameroon': '非洲',
        'Ivory Coast': '非洲',
        'Senegal': '非洲',
        'Mali': '非洲',
        'Burkina Faso': '非洲',
        'Niger': '非洲',
        'Chad': '非洲',
        'Sudan': '非洲',
        'South Sudan': '非洲',
        'Central African Republic': '非洲',
        'Democratic Republic of the Congo': '非洲',
        'Republic of the Congo': '非洲',
        'Gabon': '非洲',
        'Equatorial Guinea': '非洲',
        'Sao Tome and Principe': '非洲',
        'Angola': '非洲',
        'Rwanda': '非洲',
        'Burundi': '非洲',
        'Djibouti': '非洲',
        'Eritrea': '非洲',
        'Somalia': '非洲',
        'Comoros': '非洲',
        'Cape Verde': '非洲',
        'Guinea': '非洲',
        'Guinea-Bissau': '非洲',
        'Liberia': '非洲',
        'Sierra Leone': '非洲',
        'Gambia': '非洲',
        'Mauritania': '非洲',
        'Benin': '非洲',
        'Togo': '非洲',
        'Lesotho': '非洲',
        'Swaziland': '非洲',
        'Malawi': '非洲'
    }
    return continent_map

def create_regional_analysis(df, use_chinese=True):
    continent_map = create_continent_mapping()
    
    if use_chinese:
        df['continent'] = df['country'].map(continent_map)
    else:
        english_map = {k: v.replace('亚洲', 'Asia').replace('欧洲', 'Europe')
                      .replace('北美洲', 'North America').replace('南美洲', 'South America')
                      .replace('非洲', 'Africa').replace('大洋洲', 'Oceania') 
                      for k, v in continent_map.items()}
        df['continent'] = df['country'].map(english_map)
    
    df_with_continent = df[df['continent'].notna()].copy()
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Regional Performance Analysis' if not use_chinese else '地区表现分析', 
                 fontsize=16, fontweight='bold')
    
    continent_stats = df_with_continent.groupby('continent').agg({
        'total': 'mean',
        'contestant': 'count'
    }).round(2)
    continent_stats.columns = ['Average Score' if not use_chinese else '平均分', 
                              'Participants' if not use_chinese else '参与人数']
    continent_stats = continent_stats.sort_values('Average Score' if not use_chinese else '平均分', ascending=False)
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(continent_stats)))
    bars = axes[0, 0].bar(range(len(continent_stats)), 
                         continent_stats['Average Score' if not use_chinese else '平均分'], 
                         color=colors, alpha=0.8)
    axes[0, 0].set_xticks(range(len(continent_stats)))
    axes[0, 0].set_xticklabels(continent_stats.index, rotation=45, ha='right')
    axes[0, 0].set_title('Average Score by Region' if not use_chinese else '各地区平均分')
    axes[0, 0].set_ylabel('Average Score' if not use_chinese else '平均分')
    axes[0, 0].grid(True, alpha=0.3)
    
    for bar, score in zip(bars, continent_stats['Average Score' if not use_chinese else '平均分']):
        axes[0, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                       f'{score:.1f}', ha='center', va='bottom')
    
    medal_by_continent = df_with_continent.groupby(['continent', 'award']).size().unstack(fill_value=0)
    medal_order = ['Gold Medal', 'Silver Medal', 'Bronze Medal', 'Honourable Mention']
    medal_by_continent = medal_by_continent.reindex(columns=medal_order, fill_value=0)
    medal_colors = ['gold', 'silver', '#CD7F32', 'lightgray']
    
    medal_by_continent.plot(kind='bar', stacked=True, ax=axes[0, 1], 
                           color=medal_colors, alpha=0.8)
    axes[0, 1].set_title('Medal Distribution by Region' if not use_chinese else '各地区奖项分布')
    axes[0, 1].set_xlabel('Region' if not use_chinese else '地区')
    axes[0, 1].set_ylabel('Number of Medals' if not use_chinese else '奖项数量')
    axes[0, 1].legend(title='Award Type' if not use_chinese else '奖项类型', 
                     bbox_to_anchor=(1.05, 1), loc='upper left')
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    participation_by_continent = df_with_continent.groupby('continent')['contestant'].count().sort_values(ascending=False)
    
    wedges, texts, autotexts = axes[1, 0].pie(participation_by_continent.values, 
                                             labels=participation_by_continent.index,
                                             autopct='%1.1f%%', startangle=90,
                                             colors=colors)
    axes[1, 0].set_title('Participation Distribution by Region' if not use_chinese else '各地区参与分布')
    
    yearly_regional = df_with_continent.groupby(['year', 'continent'])['total'].mean().reset_index()
    
    for continent in continent_stats.index:
        continent_data = yearly_regional[yearly_regional['continent'] == continent]
        if len(continent_data) > 1:
            axes[1, 1].plot(continent_data['year'], continent_data['total'], 
                           marker='o', label=continent, linewidth=2, markersize=4)
    
    axes[1, 1].set_title('Regional Performance Trends' if not use_chinese else '地区表现趋势')
    axes[1, 1].set_xlabel('Year' if not use_chinese else '年份')
    axes[1, 1].set_ylabel('Average Score' if not use_chinese else '平均分')
    axes[1, 1].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('fig/regional_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("地区分析图已保存")
    
    print("\n地区统计摘要:")
    print("="*50)
    for continent in continent_stats.index:
        avg_score = continent_stats.loc[continent, 'Average Score' if not use_chinese else '平均分']
        participants = continent_stats.loc[continent, 'Participants' if not use_chinese else '参与人数']
        gold_medals = medal_by_continent.loc[continent, 'Gold Medal'] if continent in medal_by_continent.index else 0
        print(f"{continent}: 平均分 {avg_score:.2f}, 参与人数 {participants}, 金牌数 {gold_medals}")

def main():
    print("开始地区分析...")
    
    os.makedirs('fig', exist_ok=True)
    
    use_chinese = setup_chinese_fonts()
    
    try:
        df = pd.read_csv('data/processed_imo_data_fixed.csv')
        print(f"数据加载成功，共 {len(df)} 条记录")
    except Exception as e:
        print(f"数据加载失败: {e}")
        return
    
    print(f"使用{'中文' if use_chinese else '英文'}标签")
    
    create_regional_analysis(df, use_chinese)
    
    print("地区分析完成！")

if __name__ == "__main__":
    main() 