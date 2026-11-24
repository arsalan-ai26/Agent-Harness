# Build an Agent Harness

A book, written in public, that builds an AI agent harness from scratch in Python, one component per chapter.

An agent is a model plus a harness: the loop, tools, context management, sessions, safety, extensions, subagents, verification and durability around the model. Each chapter explains one component from first principles, reads how four open-source harnesses built it ([eve](https://github.com/vercel/eve), [fx](https://github.com/vercel-labs/fx), [Pi and Pi Durable](https://github.com/earendil-works/pi), [nanocode](https://github.com/gakonst/nanocode)), compares them with five reference harnesses ([Codex CLI](https://github.com/openai/codex), Claude Code via the [Dive into Claude Code](https://arxiv.org/abs/2604.14228) study, and the Chinese open-source harnesses [Kimi Code](https://github.com/MoonshotAI/kimi-code), [Qwen Code](https://github.com/QwenLM/qwen-code) and [Trae Agent](https://github.com/bytedance/trae-agent)), weighs the design decisions and trade-offs, covers the research and Chinese work, and ends with what we build.

Read it on GitHub Pages: open `index.html` on the published site.

## Stages

1. **Foundations** (chapters 0 to 3): loop, model layer, tools. Gate: a working terminal coding agent.
2. **Context** (4 to 6): instructions, compaction, sessions. Gate: sessions that last hours and resume.
3. **Control** (7 to 10): safety, extensibility, subagents, evals. Gate: a governable agent.
4. **Durability and surfaces** (11 to 12). Gate: survives `kill -9` mid-task.
5. **Software factory** (13 to 15). Gate: issue in, draft pull request out.

One new chapter a week.

## Structure

```
index.html                     table of contents (generated)
chapters/<slug>.html           one page per chapter (generated)
src/<slug>.html                chapter sources
assets/                        shared CSS and JavaScript
chapters.json                  the chapter list
tools/build.py                 builds chapters/ and index.html from src/
```

No build dependencies: `python3 tools/build.py`, then open `index.html`.
