# ===============================
# PBU Setup Script (Windows Safe)
# ===============================

function Read-Plain([securestring]$sec) {
  if (-not $sec) { return "" }
  return [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($sec)
  )
}

function Ask([string]$label, [string]$default = "") {
  if ($default -and $default.Trim() -ne "") {
    $answer = Read-Host "${label} (default: ${default})"
    if ([string]::IsNullOrWhiteSpace($answer)) { return $default } else { return $answer }
  } else {
    return (Read-Host "${label}")
  }
}

function Ask-Secret([string]$label, [string]$default = "") {
  if ($default -and $default.Trim() -ne "") {
    $prompt = "${label} (Enter to keep default)"
  } else {
    $prompt = $label
  }
  $val = Read-Host -AsSecureString $prompt
  $plain = Read-Plain $val
  if ([string]::IsNullOrWhiteSpace($plain)) { return $default } else { return $plain }
}

# -------------------
# Collect Input
# -------------------
$PUBLIC_BASE_URL = Ask "Public site base URL" "https://pbu-web.onrender.com"
$API_BASE_URL    = Ask "API base URL" "https://pbu-api.onrender.com"

$NEXT_PUBLIC_PRIMARY_COLOR   = Ask "Primary color" "#2E8B57"
$NEXT_PUBLIC_SECONDARY_COLOR = Ask "Secondary color" "#FFD700"
$NEXT_PUBLIC_CTA_COLOR       = Ask "CTA color" "#FF4500"

$NEXT_PUBLIC_SUPABASE_URL    = Ask "Supabase URL" ""
$NEXT_PUBLIC_SUPABASE_ANON_KEY = Ask-Secret "Supabase ANON Key"
$SUPABASE_SERVICE_ROLE_KEY   = Ask-Secret "Supabase Service Role Key"

$TWILIO_AUTH_TOKEN = Ask-Secret "Twilio Auth Token"
$TWILIO_FROM       = Ask "Twilio From number (e.g., +15551234567)" ""

$PRINTFUL_API_KEY  = Ask-Secret "Printful API Key"
$PRINTFUL_STORE_ID = Ask "Printful Store ID" "794628"

$NODE_VERSION = Ask "Node.js version" "18.20.4"

# -------------------
# Write .env
# -------------------
$webEnv = @"
PUBLIC_BASE_URL=$PUBLIC_BASE_URL
API_BASE_URL=$API_BASE_URL

NEXT_PUBLIC_PRIMARY_COLOR=$NEXT_PUBLIC_PRIMARY_COLOR
NEXT_PUBLIC_SECONDARY_COLOR=$NEXT_PUBLIC_SECONDARY_COLOR
NEXT_PUBLIC_CTA_COLOR=$NEXT_PUBLIC_CTA_COLOR

NEXT_PUBLIC_SUPABASE_URL=$NEXT_PUBLIC_SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY=$NEXT_PUBLIC_SUPABASE_ANON_KEY

NODE_VERSION=$NODE_VERSION
NEXT_TELEMETRY_DISABLED=1
"@

$apiEnv = @"
PUBLIC_BASE_URL=$PUBLIC_BASE_URL
API_BASE_URL=$API_BASE_URL

SUPABASE_SERVICE_ROLE_KEY=$SUPABASE_SERVICE_ROLE_KEY

TWILIO_AUTH_TOKEN=$TWILIO_AUTH_TOKEN
TWILIO_FROM=$TWILIO_FROM

PRINTFUL_API_KEY=$PRINTFUL_API_KEY
PRINTFUL_STORE_ID=$PRINTFUL_STORE_ID
"@

# -------------------
# Save Files
# -------------------
$webPath = "apps\web\.env"
$apiPath = "apps\api\.env"

New-Item -ItemType Directory -Force -Path (Split-Path $webPath) | Out-Null
New-Item -ItemType Directory -Force -Path (Split-Path $apiPath) | Out-Null

$webEnv | Out-File -Encoding UTF8 -FilePath $webPath
$apiEnv | Out-File -Encoding UTF8 -FilePath $apiPath

Write-Host "✔ Created $webPath" -ForegroundColor Green
Write-Host "✔ Created $apiPath" -ForegroundColor Green
