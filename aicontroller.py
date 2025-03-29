from flask import Flask, request, jsonify
import requests
import time
import uuid
import json
import os
import sys


OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

def send_openrouter(prompt: str, for_check: bool) -> str:
    """Отправка запроса к API OpenRouter."""
    api_key = load_key("openrouter")
    if not api_key:
        return "Ошибка: API-ключ для OpenRouter не найден."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "localhost:1234",
        "X-Title": "Local API Proxy",
    }
    payload = {
        "model": load_model(),
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000,
    }
    if for_check:
        payload = {
            "model": "nvidia/llama-3.1-nemotron-70b-instruct:free",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000,
        }

    try:
        response = requests.post(OPENROUTER_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        api_response = response.json()
        return api_response["choices"][0]["message"]["content"]
    except requests.RequestException as e:
        print(f"Ошибка при запросе к OpenRouter API: {str(e)}")
        return f"Ошибка API: {str(e)}"

def load_key() -> str | None:
    return "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"

def load_model() -> str:
    return "nvidia/llama-3.1-nemotron-70b-instruct:free"