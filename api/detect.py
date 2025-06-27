from http.server import BaseHTTPRequestHandler
import json
import traceback
from urllib.parse import urlparse

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # 处理预检请求
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
    def do_POST(self):
        try:
            # 读取请求数据
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # 验证输入
            if 'url' not in data or not data['url']:
                self.send_error_response(400, "缺少URL参数")
                return
                
            # 验证URL格式
            url = data['url'].strip()
            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                self.send_error_response(400, "无效的URL格式")
                return
            
            # ========================================
            # 在这里添加你的检测逻辑
            # ========================================
            # from your_detector import detect_function
            # result = detect_function(url)
            
            # 示例检测逻辑（替换为你的实际代码）
            result = {
                "success": True,
                "url": url,
                "detected_options": {
                    "has_size_selector": True,
                    "has_color_selector": True,
                    "has_quantity_selector": True,
                    "options": ["Size: M", "Color: Black", "Qty: 1"]
                },
                "platform": "示例电商平台",
                "timestamp": str(datetime.now())
            }
            
            # 返回成功响应
            self.send_success_response(result)
            
        except json.JSONDecodeError:
            self.send_error_response(400, "无效的JSON格式")
        except Exception as e:
            # 记录详细错误信息用于调试
            error_details = {
                "error": str(e),
                "type": type(e).__name__,
                "traceback": traceback.format_exc()
            }
            print(f"Error: {error_details}")  # Vercel日志中可见
            self.send_error_response(500, f"服务器错误: {str(e)}")
    
    def send_success_response(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = {
            "success": True,
            "data": data
        }
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def send_error_response(self, code, message):
        self.send_response(code)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = {
            "success": False,
            "error": {
                "code": code,
                "message": message
            }
        }
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

# 导入需要的库
from datetime import datetime

# ========================================
# 在下面粘贴你的检测函数
# ========================================
# def detect_function(url):
#     # 你的检测逻辑
#     return result
