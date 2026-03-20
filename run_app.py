#!/usr/bin/env python3
"""
周报生成器启动入口
支持打包为独立可执行文件
"""
import os
import sys
import subprocess
import webbrowser
import time
import signal
import threading
import socket
import urllib.request

def get_resource_path(relative_path):
    """获取资源文件路径（支持打包后的路径）"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

def check_port_available(port):
    """检查端口是否可用"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result != 0

def check_server_running(port):
    """检查服务是否真的在运行"""
    try:
        url = f'http://127.0.0.1:{port}/_stcore/health'
        req = urllib.request.Request(url, method='GET', timeout=2)
        with urllib.request.urlopen(req) as response:
            return response.status == 200
    except:
        return False

def wait_for_server(port, timeout=60):
    """等待服务启动"""
    start_time = time.time()
    url = f'http://127.0.0.1:{port}'
    
    print(f"⏳ 等待服务启动...")
    
    while time.time() - start_time < timeout:
        if check_server_running(port):
            print("")
            return True
        time.sleep(0.5)
        print(".", end='', flush=True)
    
    print("")
    return False

def main():
    """主函数"""
    # 设置工作目录
    if hasattr(sys, '_MEIPASS'):
        os.chdir(sys._MEIPASS)
    else:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("=" * 50)
    print("🚀 周报生成器启动中...")
    print("=" * 50)
    
    # 检查端口 8501 是否被占用
    port = 8501
    
    if not check_port_available(port):
        # 端口被占用，检查是否已有服务在运行
        print(f"📡 端口 {port} 被占用，检查是否有服务在运行...")
        
        if check_server_running(port):
            print("✅ 发现已有服务在运行！")
            print(f"🌐 正在打开浏览器: http://localhost:{port}")
            
            # 打开浏览器
            try:
                if sys.platform == 'darwin':
                    subprocess.Popen(['open', f'http://localhost:{port}'])
                else:
                    webbrowser.open(f'http://localhost:{port}', new=2)
            except:
                print(f"⚠️ 请手动访问: http://localhost:{port}")
            
            input("按回车键退出...")
            return
        else:
            # 端口被占用但服务没响应，可能是僵尸进程
            print(f"⚠️ 端口 {port} 被占用但无响应，尝试使用其他端口...")
            port = 8502
            while port <= 8510:
                if check_port_available(port):
                    break
                port += 1
            
            if port > 8510:
                print("❌ 无法找到可用端口")
                input("按回车键退出...")
                return
    
    print(f"📡 使用端口: {port}")
    
    # 设置环境变量
    env = os.environ.copy()
    env['STREAMLIT_SERVER_HEADLESS'] = 'true'
    env['STREAMLIT_SERVER_PORT'] = str(port)
    env['STREAMLIT_SERVER_ADDRESS'] = '127.0.0.1'
    env['STREAMLIT_BROWSER_GATHERUSAGESTATS'] = 'false'
    
    # 启动 Streamlit
    try:
        print("🔥 正在启动 Streamlit 服务...")
        process = subprocess.Popen(
            [sys.executable, '-m', 'streamlit', 'run', 'app.py',
             f'--server.port={port}',
             '--server.address=127.0.0.1',
             '--browser.gatherUsageStats=false',
             '--server.headless=true'],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        input("按回车键退出...")
        return
    
    # 读取输出的线程
    def read_output():
        try:
            for line in process.stdout:
                print(line, end='')
        except:
            pass
    
    output_thread = threading.Thread(target=read_output, daemon=True)
    output_thread.start()
    
    # 等待服务启动
    if not wait_for_server(port, timeout=60):
        print("")
        print("❌ 服务启动超时")
        print("请检查上面的错误信息")
        process.terminate()
        input("按回车键退出...")
        return
    
    print(f"✅ 服务已启动！")
    
    # 打开浏览器
    url = f'http://localhost:{port}'
    print(f"🌐 正在打开浏览器: {url}")
    
    try:
        if sys.platform == 'darwin':
            subprocess.Popen(['open', url])
        else:
            webbrowser.open(url, new=2)
    except Exception as e:
        print(f"⚠️ 无法自动打开浏览器，请手动访问: {url}")
    
    print("")
    print("=" * 50)
    print("✅ 周报生成器运行中！")
    print(f"🌐 访问地址: {url}")
    print("")
    print("⚠️ 请不要关闭此窗口")
    print("🛑 关闭此窗口将停止服务")
    print("=" * 50)
    print("")
    
    # 处理退出信号
    def signal_handler(sig, frame):
        print("\n🛑 正在关闭服务...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except:
            process.kill()
        print("✅ 服务已停止")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 等待进程结束
    try:
        process.wait()
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == '__main__':
    main()
