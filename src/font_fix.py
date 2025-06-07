#!/usr/bin/env python3
import os
import subprocess
import urllib.request
import shutil
import matplotlib.pyplot as plt
from pathlib import Path
import warnings

def run_command(cmd):
    """执行系统命令"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=False)
        return result.returncode == 0
    except Exception:
        return False

def test_chinese_font():
    """测试中文字体是否可用"""
    try:
        chinese_fonts = ['SimHei', 'Noto Sans CJK SC', 'WenQuanYi Zen Hei']
        
        for font in chinese_fonts:
            plt.rcParams['font.sans-serif'] = [font]
            plt.rcParams['axes.unicode_minus'] = False
            
            fig, ax = plt.subplots(figsize=(1, 1))
            ax.text(0.5, 0.5, '测试', ha='center', va='center')
            
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                plt.savefig('/tmp/test.png', dpi=50)
                plt.close(fig)
                
                if not any('font' in str(warning.message).lower() for warning in w):
                    os.remove('/tmp/test.png')
                    return True, font
                    
        return False, None
    except Exception:
        return False, None

def install_fonts():
    """安装中文字体"""
    print("安装系统中文字体...")
    commands = [
        "sudo apt update -qq",
        "sudo apt install -y fonts-noto-cjk fonts-wqy-zenhei fontconfig"
    ]
    
    for cmd in commands:
        run_command(cmd)

def download_and_install_simhei():
    """下载并安装SimHei字体"""
    font_url = "https://github.com/jiaxiaochu/font/raw/master/simhei.ttf"
    font_path = "/tmp/simhei.ttf"
    
    try:
        if not os.path.exists(font_path):
            print("下载SimHei字体...")
            urllib.request.urlretrieve(font_url, font_path)
        
        # 安装到用户目录
        user_fonts_dir = Path.home() / ".fonts"
        user_fonts_dir.mkdir(exist_ok=True)
        
        user_font_path = user_fonts_dir / "simhei.ttf"
        if not user_font_path.exists():
            shutil.copy2(font_path, user_font_path)
        
        # 更新字体缓存
        run_command("fc-cache -f")
        return True
    except Exception as e:
        print(f"SimHei安装失败: {e}")
        return False

def configure_matplotlib():
    """配置matplotlib"""
    config_dir = Path.home() / ".matplotlib"
    config_dir.mkdir(exist_ok=True)
    
    config_file = config_dir / "matplotlibrc"
    config_content = """font.family: sans-serif
font.sans-serif: SimHei, Noto Sans CJK SC, WenQuanYi Zen Hei, DejaVu Sans
axes.unicode_minus: False"""
    
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        # 清除matplotlib缓存
        cache_dir = Path.home() / ".cache" / "matplotlib"
        if cache_dir.exists():
            shutil.rmtree(cache_dir)
        
        return True
    except Exception as e:
        print(f"配置失败: {e}")
        return False

def create_test_plot():
    """创建测试图表"""
    try:
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Noto Sans CJK SC', 'WenQuanYi Zen Hei']
        plt.rcParams['axes.unicode_minus'] = False
        
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot([1, 2, 3], [1, 4, 2], 'o-', label='测试数据')
        ax.set_title('中文字体测试')
        ax.set_xlabel('X轴')
        ax.set_ylabel('Y轴')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        os.makedirs('fig', exist_ok=True)
        plt.savefig('fig/font_test.png', dpi=150, bbox_inches='tight')
        plt.close()
        
        print("测试图表已保存: fig/font_test.png")
        return True
    except Exception as e:
        print(f"测试图表创建失败: {e}")
        return False

def main():
    print("=" * 50)
    print("matplotlib 中文字体修复工具")
    print("=" * 50)
    
    # 检测当前字体支持
    supported, current_font = test_chinese_font()
    
    if supported:
        print(f"✓ 中文字体已支持，当前使用: {current_font}")
        create_test_plot()
        print("无需修复！")
        return
    
    print("✗ 检测到中文字体问题，开始修复...")
    
    # 安装字体
    install_fonts()
    download_and_install_simhei()
    
    # 配置matplotlib
    configure_matplotlib()
    
    # 验证修复结果
    supported, current_font = test_chinese_font()
    
    if supported:
        print(f"✓ 修复成功！当前使用: {current_font}")
        create_test_plot()
    else:
        print("✗ 修复未完全成功，请重启Python环境后重试")
    
    print("=" * 50)

if __name__ == "__main__":
    main() 