# 启动后端服务
# 使用: PowerShell 中运行 .\scripts\start-backend.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  启动 LeBron Stats 后端服务" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$BackendPort = 3000

# 获取项目根目录
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$BackendPath = Join-Path $ProjectRoot "backend"

# 检查后端目录
if (-not (Test-Path $BackendPath)) {
    Write-Host "❌ 后端目录不存在: $BackendPath" -ForegroundColor Red
    exit 1
}

# 检查 Python
$PythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $PythonCmd) {
    $PythonCmd = Get-Command python3 -ErrorAction SilentlyContinue
}

if (-not $PythonCmd) {
    Write-Host "❌ 未找到 Python，请安装 Python 3.8+" -ForegroundColor Red
    Write-Host "   下载地址: https://www.python.org/downloads/" -ForegroundColor Gray
    exit 1
}

Write-Host "✅ Python: $($PythonCmd.Source)" -ForegroundColor Green

# 检查虚拟环境
$VenvPath = Join-Path $BackendPath "venv"
$VenvPython = Join-Path $VenvPath "Scripts\python.exe"

if (Test-Path $VenvPython) {
    Write-Host "✅ 使用虚拟环境: $VenvPath" -ForegroundColor Green
    $PythonExe = $VenvPython
} else {
    Write-Host "⚠️  使用系统 Python" -ForegroundColor Yellow
    Write-Host "   建议创建虚拟环境: python -m venv venv" -ForegroundColor Gray
    $PythonExe = $PythonCmd.Source
}

# 检查依赖
Write-Host ""
Write-Host "📦 检查依赖..." -ForegroundColor Yellow

# 尝试导入 fastapi
$CheckResult = & $PythonExe -c "import fastapi; import nba_api; print('OK')" 2>&1
if ($CheckResult -notlike "*OK*") {
    Write-Host "⚠️  依赖未安装，正在安装..." -ForegroundColor Yellow
    Set-Location $BackendPath
    & $PythonExe -m pip install -r requirements.txt
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 依赖安装失败" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✅ 依赖安装完成" -ForegroundColor Green
} else {
    Write-Host "✅ 依赖已安装" -ForegroundColor Green
}

Write-Host ""
Write-Host "🚀 启动后端服务..." -ForegroundColor Green
Write-Host "   端口: $BackendPort" -ForegroundColor Gray
Write-Host "   地址: http://localhost:$BackendPort" -ForegroundColor Gray
Write-Host ""

# 启动后端
Set-Location $BackendPath
& $PythonExe main.py
