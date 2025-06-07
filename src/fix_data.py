import pandas as pd
import numpy as np
import re

def fix_country_data():
    """修复数据中的异常国家代码"""
    print("正在修复数据...")
    
    # 读取原始数据
    df = pd.read_csv('data/processed_imo_data.csv')
    print(f"原始数据: {len(df)} 条记录")
    
    # 查找异常的国家代码（C开头的数字代码）
    abnormal_pattern = r'^C\d+$'
    abnormal_countries = df[df['country'].str.match(abnormal_pattern, na=False)]
    print(f"发现异常国家代码: {len(abnormal_countries)} 条记录")
    print("异常代码:", abnormal_countries['country'].unique())
    
    # 删除这些异常记录
    df_clean = df[~df['country'].str.match(abnormal_pattern, na=False)]
    print(f"清理后数据: {len(df_clean)} 条记录")
    
    # 标准化一些国家名称
    country_mapping = {
        'People\'s Republic of China': 'China',
        'United States of America': 'United States',
        'Republic of Korea': 'South Korea',
        'Democratic People\'s Republic of Korea': 'North Korea',
        'Russian Federation': 'Russia',
        'Union of Soviet Socialist Republics': 'Soviet Union',
        'Federal Republic of Germany': 'Germany',
        'German Democratic Republic': 'Germany',
        'Czechoslovakia': 'Czech Republic',
        'Yugoslavia': 'Serbia',
    }
    
    df_clean['country'] = df_clean['country'].replace(country_mapping)
    
    # 添加地区分类
    region_mapping = {
        # 亚洲
        'China': 'Asia', 'Japan': 'Asia', 'South Korea': 'Asia', 'North Korea': 'Asia',
        'India': 'Asia', 'Singapore': 'Asia', 'Thailand': 'Asia', 'Vietnam': 'Asia',
        'Indonesia': 'Asia', 'Malaysia': 'Asia', 'Philippines': 'Asia', 'Taiwan': 'Asia',
        'Hong Kong': 'Asia', 'Mongolia': 'Asia', 'Kazakhstan': 'Asia', 'Uzbekistan': 'Asia',
        'Iran': 'Asia', 'Iraq': 'Asia', 'Turkey': 'Asia', 'Türkiye': 'Asia',
        'Israel': 'Asia', 'Saudi Arabia': 'Asia', 'Pakistan': 'Asia', 'Bangladesh': 'Asia',
        'Myanmar': 'Asia', 'Cambodia': 'Asia', 'Laos': 'Asia', 'Nepal': 'Asia',
        'Sri Lanka': 'Asia', 'Afghanistan': 'Asia', 'Syria': 'Asia', 'Lebanon': 'Asia',
        'Jordan': 'Asia', 'Kuwait': 'Asia', 'Qatar': 'Asia', 'United Arab Emirates': 'Asia',
        'Oman': 'Asia', 'Yemen': 'Asia', 'Bahrain': 'Asia', 'Cyprus': 'Asia',
        'Georgia': 'Asia', 'Armenia': 'Asia', 'Azerbaijan': 'Asia',
        
        # 欧洲
        'United Kingdom': 'Europe', 'Germany': 'Europe', 'France': 'Europe', 'Italy': 'Europe',
        'Spain': 'Europe', 'Poland': 'Europe', 'Romania': 'Europe', 'Netherlands': 'Europe',
        'Belgium': 'Europe', 'Switzerland': 'Europe', 'Austria': 'Europe', 'Sweden': 'Europe',
        'Norway': 'Europe', 'Denmark': 'Europe', 'Finland': 'Europe', 'Iceland': 'Europe',
        'Ireland': 'Europe', 'Portugal': 'Europe', 'Greece': 'Europe', 'Hungary': 'Europe',
        'Czech Republic': 'Europe', 'Slovakia': 'Europe', 'Slovenia': 'Europe', 'Croatia': 'Europe',
        'Serbia': 'Europe', 'Bosnia and Herzegovina': 'Europe', 'Montenegro': 'Europe',
        'North Macedonia': 'Europe', 'Albania': 'Europe', 'Bulgaria': 'Europe', 'Moldova': 'Europe',
        'Ukraine': 'Europe', 'Belarus': 'Europe', 'Lithuania': 'Europe', 'Latvia': 'Europe',
        'Estonia': 'Europe', 'Russia': 'Europe', 'Soviet Union': 'Europe', 'Luxembourg': 'Europe',
        
        # 北美洲
        'United States': 'North America', 'Canada': 'North America', 'Mexico': 'North America',
        'Guatemala': 'North America', 'Cuba': 'North America', 'Jamaica': 'North America',
        'Haiti': 'North America', 'Dominican Republic': 'North America', 'Trinidad and Tobago': 'North America',
        'Costa Rica': 'North America', 'Panama': 'North America', 'El Salvador': 'North America',
        'Honduras': 'North America', 'Nicaragua': 'North America', 'Belize': 'North America',
        
        # 南美洲
        'Brazil': 'South America', 'Argentina': 'South America', 'Chile': 'South America',
        'Peru': 'South America', 'Colombia': 'South America', 'Venezuela': 'South America',
        'Ecuador': 'South America', 'Bolivia': 'South America', 'Paraguay': 'South America',
        'Uruguay': 'South America', 'Guyana': 'South America', 'Suriname': 'South America',
        
        # 大洋洲
        'Australia': 'Oceania', 'New Zealand': 'Oceania', 'Papua New Guinea': 'Oceania',
        'Fiji': 'Oceania', 'Solomon Islands': 'Oceania', 'Vanuatu': 'Oceania',
        
        # 非洲
        'South Africa': 'Africa', 'Egypt': 'Africa', 'Morocco': 'Africa', 'Tunisia': 'Africa',
        'Algeria': 'Africa', 'Libya': 'Africa', 'Sudan': 'Africa', 'Ethiopia': 'Africa',
        'Kenya': 'Africa', 'Tanzania': 'Africa', 'Uganda': 'Africa', 'Nigeria': 'Africa',
        'Ghana': 'Africa', 'Madagascar': 'Africa', 'Mauritius': 'Africa', 'Zimbabwe': 'Africa',
        'Botswana': 'Africa', 'Namibia': 'Africa', 'Mozambique': 'Africa', 'Angola': 'Africa',
        'Zambia': 'Africa', 'Malawi': 'Africa', 'Rwanda': 'Africa', 'Burundi': 'Africa',
    }
    
    # 添加地区列
    df_clean['region'] = df_clean['country'].map(region_mapping)
    
    # 处理未匹配的国家
    unmapped_countries = df_clean[df_clean['region'].isna()]['country'].unique()
    if len(unmapped_countries) > 0:
        print(f"未映射到地区的国家: {unmapped_countries}")
        df_clean['region'] = df_clean['region'].fillna('Other')
    
    # 确保奖项列的一致性
    award_mapping = {
        'Gold medal': 'Gold Medal',
        'Silver medal': 'Silver Medal', 
        'Bronze medal': 'Bronze Medal',
        'Honourable mention': 'Honourable Mention'
    }
    df_clean['award'] = df_clean['award'].replace(award_mapping)
    
    # 保存修复后的数据
    df_clean.to_csv('data/processed_imo_data_fixed.csv', index=False)
    print(f"修复后的数据已保存")
    print(f"最终记录数: {len(df_clean)}")
    print(f"国家数: {df_clean['country'].nunique()}")
    print(f"地区分布: {df_clean['region'].value_counts()}")
    
    return df_clean

if __name__ == "__main__":
    fix_country_data() 