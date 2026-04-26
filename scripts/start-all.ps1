# 一键启动脚本 - 启动前后端服务
# 使用: PowerShell 中运行 .\scripts\start-all.ps1

param(
    [switch]$BackendOnly,
    [switch]$FrontendOnly
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  LeBron Stats - 全栈项目启动器" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$BackendPort = 3000
$FrontendPort = 5173

# 获取项目根目录
$ProjectRoot = Split-Path -Parent $PSScriptRoot

# 检查端口是否被占用
function Test-Port {
    param($Port)
    $connection = Test-NetConnection -ComputerName localhost -Port $Port -WarningAction SilentlyContinue
    return $connection.TcpTestSucceeded
}

# 检查后端端口
if (Test-Port $BackendPort) {
    Write-Host "⚠️  端口 $BackendPort 已被占用，后端可能已在运行" -ForegroundColor Yellow
} else {
    Write-Host "✅ 端口 $BackendPort 可用" -ForegroundColor Green
}

# 检查前端端口
if (Test-Port $FrontendPort) {
    Write-Host "⚠️  端口 $FrontendPort 已被占用，前端可能已在运行" -ForegroundColor Yellow
} else {
    Write-Host "✅ 端口 $FrontendPort 可用" -ForegroundColor Green
}

Write-Host ""

# 启动后端
if (-not $FrontendOnly) {
    Write-Host "🚀 正在启动后端服务..." -ForegroundColor Green
    
    $BackendPath = Join-Path $ProjectRoot "backend"
    
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
        exit 1
    }
    
    Write-Host "   Python: $($PythonCmd.Source)" -ForegroundColor Gray
    
    # 检查虚拟环境
    $VenvPath = Join-Path $BackendPath "venv"
    $VenvPython = Join-Path $VenvPath "Scripts\python.exe"
    
    if (Test-Path $VenvPython) {
        Write-Host "   使用虚拟环境" -ForegroundColor Gray
        $PythonExe = $VenvPython
    } else {
        Write-Host "   使用系统 Python（建议创建虚拟环境）" -ForegroundColor Yellow
        $PythonExe = $PythonCmd.Source
    }
    
    # 启动后端（后台运行）
    $BackendJob = Start-Job -ScriptBlock {
        param($Python, $Path)
        Set-Location $Path
        & $Python main.py
    } -ArgumentList $PythonExe, $BackendPath
    
    Write-Host "   后端服务启动中..." -ForegroundColor Gray
    Start-Sleep -Seconds 3
    
    # 检查后端是否启动成功
    $Retries = 0
    $MaxRetries = 10
    while ($Retries -lt $MaxRetries) {
        if (Test-Port $BackendPort) {
            Write-Host "   ✅ 后端服务已启动: http://localhost:$BackendPort" -ForegroundColor Green
            break
        }
        Start-Sleep -Seconds 1
        $Retries++
    }
    
    if ($Retries -eq $MaxRetries) {
        Write-Host "   ❌ 后端服务启动失败" -ForegroundColor Red
        Receive-Job $BackendJob
        exit 1
    }
    
    Write-Host ""
}

# 启动前端
if (-not $BackendOnly) {
    Write-Host "🚀 正在启动前端服务..." -ForegroundColor Green
    
    $FrontendPath = Join-Path $ProjectRoot "frontend"
    
    if (-not (Test-Path $FrontendPath)) {
        Write-Host "❌ 前端目录不存在: $FrontendPath" -ForegroundColor Red
        exit 1
    }
    
    # 检查 Node.js
    $NodeCmd = Get-Command node -ErrorAction SilentlyContinue
    if (-not $NodeCmd) {
        Write-Host "❌ 未找到 Node.js，请安装 Node.js 20+" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "   Node.js: $($NodeCmd.Source)" -ForegroundColor Gray
    
    # 检查 npm
    $NpmCmd = Get-Command npm -ErrorAction SilentlyContinue
    if (-not $NpmCmd) {
        Write-Host "❌ 未找到 npm" -ForegroundColor Red
        exit 1
    }
    
    # 检查 node_modules
    $NodeModulesPath = Join-Path $FrontendPath "node_modules"
    if (-not (Test-Path $NodeModulesPath)) {
        Write-Host "   安装前端依赖..." -ForegroundColor Yellow
        Set-Location $FrontendPath
        & $NpmCmd.Source install
    }
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  🎉 所有服务已启动！" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  📊 后端 API: http://localhost:$BackendPort" -ForegroundColor White
    Write-Host "  🎨 前端页面: http://localhost:$FrontendPort" -ForegroundColor White
    Write-Host ""
    Write-Host "  API 接口:" -ForegroundColor Gray
    Write-Host "    - GET http://localhost:$BackendPort/api/today-game" -ForegroundColor Gray
    Write-Host "    - GET http://localhost:$BackendPort/api/career-stats" -ForegroundColor Gray
    Write-Host "    - GET http://localhost:$BackendPort/api/all-stats" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  按 Ctrl+C 停止服务" -ForegroundColor Yellow
    Write-Host ""
    
    # 启动前端（前台运行）
    Set-Location $FrontendPath
    & $NpmCmd.Source run dev
}

# 如果是仅后端模式，保持运行
if ($BackendOnly) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  ✅ 后端服务已启动！" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  📊 后端 API: http://localhost:$BackendPort" -ForegroundColor White
    Write-Host ""
    Write-Host "  按 Ctrl+C 停止服务" -ForegroundColor Yellow
    Write-Host ""
    
    # 等待用户输入
    while ($true) {
        Start-Sleep -Seconds 1
    }
}
