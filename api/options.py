"""
Shopify Product Options App Detector
检测Shopify商店使用的产品选项应用
"""
import requests
from bs4 import BeautifulSoup
import re
import json
from typing import Dict, List, Tuple
import argparse
from urllib.parse import urlparse, urljoin

class ShopifyAppDetector:
    def __init__(self, url: str):
        self.url = self._normalize_url(url)
        self.soup = None
        self.page_content = None
        self.detected_apps = []
        self.confidence_scores = {}
        
    def _normalize_url(self, url: str) -> str:
        """规范化URL"""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url.rstrip('/')
    
    def fetch_page(self) -> bool:
        """获取页面内容"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(self.url, headers=headers, timeout=10)
            response.raise_for_status()
            
            self.page_content = response.text
            self.soup = BeautifulSoup(self.page_content, 'html.parser')
            return True
        except Exception as e:
            print(f"Error fetching page: {e}")
            return False
    
    def is_shopify_store(self) -> bool:
        """检测是否为Shopify商店"""
        shopify_indicators = [
            lambda: self.soup.find('script', src=re.compile(r'cdn\.shopify\.com')),
            lambda: self.soup.find('script', src=re.compile(r'shopifycdn\.com')),
            lambda: 'Shopify' in self.page_content,
            lambda: self.soup.find('meta', {'name': 'shopify-checkout-api-token'}),
            lambda: '.myshopify.com' in self.url
        ]
        
        return any(indicator() for indicator in shopify_indicators)
    
    def detect_zepto(self) -> Tuple[bool, int]:
        """检测Zepto Product Personalizer"""
        score = 0
        checks = {
            'pplr_custom_cart_track': 30,
            'zepto-personalizer-container': 25,
            'shopify://apps/zepto-product-personalizer': 30,
            '_zepto_design_id': 15
        }
        
        for pattern, points in checks.items():
            if pattern in self.page_content:
                score += points
        
        return score > 0, score
    
    def detect_bold_options(self) -> Tuple[bool, int]:
        """检测Bold Options"""
        score = 0
        
        # CSS类检测
        bold_classes = ['bold_options', 'bold_option_set', 'bold_option', 
                       'bold_option_title', 'bold_option_value']
        for class_name in bold_classes:
            if self.soup.find(class_=class_name):
                score += 15
        
        # Script检测
        if self.soup.find('script', src=re.compile(r'boldapps\.net')):
            score += 30
        
        # JS对象检测
        if 'BoldOptions' in self.page_content or 'window.Bold' in self.page_content:
            score += 25
        
        return score > 0, score
    
    def detect_kickflip(self) -> Tuple[bool, int]:
        """检测Kickflip"""
        score = 0
        
        # 检测mczr相关元素
        mczr_patterns = [
            r'class="[^"]*mczr[^"]*"',
            r'id="[^"]*mczr[^"]*"',
            r'data-mczr=',
            '#mczr-modal',
            'mczrAddToCart'
        ]
        
        for pattern in mczr_patterns:
            if re.search(pattern, self.page_content):
                score += 15
        
        # 检测iframe
        if self.soup.find('iframe', src=re.compile(r'gokickflip\.com')):
            score += 40
        
        return score > 0, score
    
    def detect_customily(self) -> Tuple[bool, int]:
        """检测Customily"""
        score = 0
        
        patterns = {
            'window.engraver': 35,
            'engraver.init': 30,
            'customily.com': 25,
            'preview-canvas': 10
        }
        
        for pattern, points in patterns.items():
            if pattern in self.page_content:
                score += points
        
        return score > 0, score
    
    def detect_shoppad_infinite_options(self) -> Tuple[bool, int]:
        """检测Shoppad Infinite Options"""
        score = 0
        
        patterns = {
            'Shoppad.apps.infiniteoptions': 40,
            'infiniteoptions-container': 30,
            'infinite_options': 20,
            'window.Shoppad': 10
        }
        
        for pattern, points in patterns.items():
            if pattern in self.page_content:
                score += points
        
        return score > 0, score
    
    def detect_hulk(self) -> Tuple[bool, int]:
        """检测Hulk Product Options"""
        score = 0
        
        patterns = {
            'HulkProductOptions': 35,
            'hulk-product-options': 30,
            'hulkapps.com': 25,
            'hulk_po': 10
        }
        
        for pattern, points in patterns.items():
            if pattern in self.page_content:
                score += points
        
        return score > 0, score
    
    def detect_tepo(self) -> Tuple[bool, int]:
        """检测Tepo Product Options"""
        score = 0
        
        patterns = {
            'tepo-options': 30,
            'TepoOptions': 30,
            'class="tepo-': 25,
            'window.tepo': 15
        }
        
        for pattern, points in patterns.items():
            if pattern in self.page_content:
                score += points
        
        return score > 0, score
    
    def detect_apo(self) -> Tuple[bool, int]:
        """检测APO (Advanced Product Options)"""
        score = 0
        
        patterns = {
            'mwProductOptionsObjects': 40,
            'mw-product-options': 30,
            'mageworx': 20,
            '_mw_option_relation': 10
        }
        
        for pattern, points in patterns.items():
            if pattern in self.page_content:
                score += points
        
        return score > 0, score
    
    def detect_teeinblue(self) -> Tuple[bool, int]:
        """检测Teeinblue"""
        score = 0
        
        patterns = {
            'Teeinblue': 30,
            'teeinblue-form': 30,
            'teeinblue.com': 25,
            'window.TIB': 15
        }
        
        for pattern, points in patterns.items():
            if pattern in self.page_content:
                score += points
        
        return score > 0, score
    
    def detect_zakeke(self) -> Tuple[bool, int]:
        """检测Zakeke"""
        score = 0
        
        patterns = {
            'zakekeDesigner': 35,
            'zakeke-container': 30,
            'zakeke.com': 25,
            'zakeke-button': 10
        }
        
        for pattern, points in patterns.items():
            if pattern in self.page_content:
                score += points
        
        return score > 0, score
    
    def detect_sc_options(self) -> Tuple[bool, int]:
        """检测SC Product Options"""
        score = 0
        
        patterns = {
            'SCProductOptions': 35,
            'sc-product-options': 30,
            'data-sc-option': 20,
            'shopcircle': 15
        }
        
        for pattern, points in patterns.items():
            if pattern in self.page_content:
                score += points
        
        return score > 0, score
    
    def detect_lpo(self) -> Tuple[bool, int]:
        """检测LPO (Live Product Options)"""
        score = 0
        
        patterns = {
            'liveProductOptions': 35,
            'lpo-options': 30,
            'cloudlift': 25,
            'window.LPO': 10
        }
        
        for pattern, points in patterns.items():
            if pattern in self.page_content:
                score += points
        
        return score > 0, score
    
    def detect_avis(self) -> Tuple[bool, int]:
        """检测Avis Product Options"""
        score = 0
        
        patterns = {
            'AvisOptions': 35,
            'avis-options': 30,
            'avisplus-product-options': 25,
            'data-avis-option': 10
        }
        
        for pattern, points in patterns.items():
            if pattern in self.page_content:
                score += points
        
        return score > 0, score
    
    def detect_globo(self) -> Tuple[bool, int]:
        """检测Globo Product Options"""
        score = 0
        
        patterns = {
            'GloboProductOptions': 35,
            'globo-options': 30,
            'globo.io': 25,
            'globosoftware': 15
        }
        
        for pattern, points in patterns.items():
            if pattern in self.page_content:
                score += points
        
        return score > 0, score
    
    def detect_easily(self) -> Tuple[bool, int]:
        """检测Easily Product Options"""
        score = 0
        
        patterns = {
            'EasilyOptions': 35,
            'easily-options': 30,
            'data-easily': 20,
            'easily_product_options': 15
        }
        
        for pattern, points in patterns.items():
            if pattern in self.page_content:
                score += points
        
        return score > 0, score
    
    def detect_shopaw(self) -> Tuple[bool, int]:
        """检测Shopaw Product Options"""
        score = 0
        
        patterns = {
            'ShopawOptions': 35,
            'shopaw-options': 30,
            'shopaw-product-builder': 25,
            'data-shopaw': 10
        }
        
        for pattern, points in patterns.items():
            if pattern in self.page_content:
                score += points
        
        return score > 0, score
    
    def run_detection(self):
        """运行所有检测"""
        if not self.fetch_page():
            return False
        
        if not self.is_shopify_store():
            print("Warning: This may not be a Shopify store")
        
        detectors = {
            'Zepto Product Personalizer': self.detect_zepto,
            'Bold Product Options': self.detect_bold_options,
            'Kickflip': self.detect_kickflip,
            'Customily': self.detect_customily,
            'Shoppad Infinite Options': self.detect_shoppad_infinite_options,
            'Hulk Product Options': self.detect_hulk,
            'Tepo Product Options': self.detect_tepo,
            'APO (Advanced Product Options)': self.detect_apo,
            'Teeinblue': self.detect_teeinblue,
            'Zakeke': self.detect_zakeke,
            'SC Product Options': self.detect_sc_options,
            'LPO (Live Product Options)': self.detect_lpo,
            'Avis Product Options': self.detect_avis,
            'Globo Product Options': self.detect_globo,
            'Easily Product Options': self.detect_easily,
            'Shopaw Product Options': self.detect_shopaw
        }
        
        for app_name, detector in detectors.items():
            detected, score = detector()
            if detected:
                self.detected_apps.append(app_name)
                self.confidence_scores[app_name] = score
        
        return True
    
    def print_results(self):
        """打印检测结果"""
        print(f"\n{'='*60}")
        print(f"Shopify App Detection Results for: {self.url}")
        print(f"{'='*60}\n")
        
        if not self.detected_apps:
            print("No product options apps detected")
            return
        
        print(f"Detected {len(self.detected_apps)} app(s):\n")
        
        # 按置信度排序
        sorted_apps = sorted(self.detected_apps, 
                           key=lambda x: self.confidence_scores[x], 
                           reverse=True)
        
        for app in sorted_apps:
            score = self.confidence_scores[app]
            confidence = self._get_confidence_level(score)
            print(f"✓ {app}")
            print(f"  Confidence: {confidence} (Score: {score})")
            print()
    
    def _get_confidence_level(self, score: int) -> str:
        """根据分数返回置信度级别"""
        if score >= 70:
            return "High"
        elif score >= 40:
            return "Medium"
        else:
            return "Low"

def main():
    parser = argparse.ArgumentParser(
        description='Detect Shopify product options apps'
    )
    parser.add_argument('url', help='Shopify store URL or product page URL')
    parser.add_argument('--json', action='store_true', 
                       help='Output results as JSON')
    
    args = parser.parse_args()
    
    detector = ShopifyAppDetector(args.url)
    
    if detector.run_detection():
        if args.json:
            result = {
                'url': detector.url,
                'detected_apps': detector.detected_apps,
                'confidence_scores': detector.confidence_scores
            }
            print(json.dumps(result, indent=2))
        else:
            detector.print_results()
    else:
        print("Detection failed")

if __name__ == '__main__':
    main()
