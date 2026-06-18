#!/bin/bash
ollama serve &
sleep 5
ollama pull qwen3:0.6b
ollama run qwen3:0.6b
wait