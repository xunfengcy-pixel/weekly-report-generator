' 周报生成器一键启动脚本
' 双击此文件即可启动 Streamlit 应用

Set WshShell = CreateObject("WScript.Shell")

' 获取当前脚本所在目录
strPath = WshShell.ScriptFullName
strDir = Left(strPath, InStrRev(strPath, "\") - 1)

' 切换到项目目录并启动 Streamlit
' 使用 /k 参数保持窗口运行，方便查看日志
WshShell.Run "cmd /c cd /d """ & strDir & """ && streamlit run app.py", 0, False

' 显示提示
MsgBox "周报生成器正在启动..." & vbCrLf & vbCrLf & "请稍等片刻，浏览器将自动打开。" & vbCrLf & vbCrLf & "地址：http://localhost:8501", vbInformation, "周报生成器"

Set WshShell = Nothing
