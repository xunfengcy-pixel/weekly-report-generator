' Weekly Report Generator Launcher
' Double-click to start the Streamlit app

Set WshShell = CreateObject("WScript.Shell")

' Get current script directory using WScript object
strPath = WScript.ScriptFullName
strDir = Left(strPath, InStrRev(strPath, "\") - 1)

' Change to project directory and start Streamlit
WshShell.Run "cmd /c cd /d """ & strDir & """ && streamlit run app.py", 0, False

' Show startup message
MsgBox "Weekly Report Generator is starting..." & vbCrLf & vbCrLf & "Please wait a moment, browser will open automatically." & vbCrLf & vbCrLf & "URL: http://localhost:8501", vbInformation, "Weekly Report Generator"

Set WshShell = Nothing
