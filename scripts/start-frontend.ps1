# 启动前端服务
# 使用: PowerShell 中运行 .\scripts\start-frontend.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  启动 LeBron Stats 前端服务" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$FrontendPort = 5173

# 获取项目根目录
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$FrontendPath = Join-Path $ProjectRoot "frontend"

# 检查前端目录
if (-not (Test-Path $FrontendPath)) {
    Write-Host "❌ 前端目录不存在: $FrontendPath" -ForegroundColor Red
    exit 1
}

# 检查 Node.js
$NodeCmd = Get-Command node -ErrorAction SilentlyContinue
if (-not $NodeCmd) {
    Write-Host "❌ 未找到 Node.js，请安装 Node.js 20+" -ForegroundColor Red
    Write-Host "   下载地址: https://nodejs.org/" -ForegroundColor Gray
    exit 1
}

Write-Host "✅ Node.js: $($NodeCmd.Source)" -ForegroundColor Green
Write-Host "   版本: $(& $NodeCmd.Source --version)" -ForegroundColor Gray

# 检查 npm
$NpmCmd = Get-Command npm -ErrorAction SilentlyContinue
if (-not $NpmCmd) {
    Write-Host "❌ 未找到 npm" -ForegroundColor Red
    exit 1
}

Write-Host "✅ npm: $($NpmCmd.Source)" -ForegroundColor Green

# 检查 node_modules
$NodeModulesPath = Join-Path $FrontendPath "node_modules"
if (-not (Test-Path $NodeModulesPath)) {
    Write-Host ""
    Write-Host "📦 安装前端依赖..." -ForegroundColor Yellow
    Set-Location $FrontendPath
    & $NpmCmd.Source install
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 依赖安装失败" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✅ 依赖安装完成" -ForegroundColor Green
} else {
    Write-Host "✅ 依赖已安装" -ForegroundColor Green
}

Write-Host ""
Write-Host "🚀 启动前端服务..." -ForegroundColor Green
Write-Host "   端口: $FrontendPort" -ForegroundColor Gray
Write-Host "   地址: http://localhost:$FrontendPort" -ForegroundColor Gray
Write-Host ""

# 检查 .env 配置
$EnvFile = Join-Path $FrontendPath ".env"
if (Test-Path $EnvFile) {
    $EnvContent = Get-Content $EnvFile
    if ($EnvContent -match "VITE_USE_MOCK=true") {
        Write-Host "⚠️  注意: 当前使用 Mock 数据" -ForegroundColor Yellow
        Write-Host "   如需使用真实 API，请修改 .env 文件:" -ForegroundColor Gray
        Write-Host "   VITE_USE_MOCK=false" -ForegroundColor Gray
    } else {
        Write-Host "✅ 使用真实 API 数据" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  🎨 前端服务已启动！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  访问地址: http://localhost:$FrontendPort" -ForegroundColor White
Write-Host ""
Write-Host "  按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host ""

# 启动前端
Set-Location $FrontendPath
& $NpmCmd.Source run dev
