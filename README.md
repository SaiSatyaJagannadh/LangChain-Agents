<div align="center">

# 🔗 LangChain Agents — Local & Cloud LLM Chains

### Prompt templates and LCEL chains that run the same task on OpenAI or a local open-weight model via Ollama.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1.0-1C3C3C?style=flat-square&logo=langchain&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-gpt--oss:20b_·_gemma3-000000?style=flat-square)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white)
![uv](https://img.shields.io/badge/uv-DE5FE9?style=flat-square)

</div>

---

## ✨ What it shows

- **`PromptTemplate` → LLM** composed with LCEL (`prompt | llm`)
- **Provider swap in one line** — `ChatOpenAI` (o3-mini) ↔ `ChatOllama` (`gpt-oss:20b`, `gemma3:270m`)
- A summarisation chain: give it a bio, get a short summary + two interesting facts
- Fully **offline** option — no API key needed when running on Ollama

```python
chain = summary_prompt_template | ChatOllama(model="gpt-oss:20b", temperature=0)
print(chain.invoke({"information": bio}).content)
```

## 🚀 Run it

```bash
git clone https://github.com/SaiSatyaJagannadh/LangChain-Agents.git && cd LangChain-Agents
uv sync
ollama pull gpt-oss:20b          # or set OPENAI_API_KEY in .env and switch to ChatOpenAI
uv run main.py
```

---

<div align="center">

**Built by [Sai Satya Jagannadh Doddipatla (DJ)](https://saisatyajagannadh.github.io/PersonalPortfolio/)** · ⭐ Star the repo if it helped

</div>
