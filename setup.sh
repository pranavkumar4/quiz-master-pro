#!/bin/bash

mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
enableXsrfProtection = true\n\
\n\
[theme]\n\
primaryColor = '#6366f1'\n\
backgroundColor = '#ffffff'\n\
secondaryBackgroundColor = '#f3f4f6'\n\
textColor = '#1f2937'\n\
font = 'sans serif'\n\
" > ~/.streamlit/config.toml
