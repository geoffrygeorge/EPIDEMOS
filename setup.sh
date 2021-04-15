mkdir -p ~/.streamlit/

echo "[server]
headless = true
port = $PORT
enableCORS = false

[theme]
primaryColor = "#ff0000"
backgroundColor = "#d6eaf8"
secondaryBackgroundColor = "#ffffff"
textColor = "#002d80"
font = "sans serif"
" > ~/.streamlit/config.toml