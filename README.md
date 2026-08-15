# Plain writing skill

This skill makes an AI agent write in a plain style. The full rules are in
`SKILL.md`.

The rules are plain text, so any agent can use them.

The skill also checks its own writing and removes anything that does not add
something.

## What is in here

- `SKILL.md`: the skill, with the rules and the steps.
- `evals/`: optional. Only needed if you want to measure the skill.

## How to use it

`SKILL.md` is a plain markdown file with the rules. Any agent that can read a
file can follow it. The simplest way is to give `SKILL.md` to the agent as
instructions, in a rules file or the system prompt.

Some tools have a set place for skills:

- Claude Code reads skills from `~/.claude/skills`. Install only the skill
  file, not the evals:

```
mkdir -p ~/.claude/skills/plain-writing
curl -fsSL https://raw.githubusercontent.com/shreyashankar/plain-writing-skill/main/SKILL.md \
  -o ~/.claude/skills/plain-writing/SKILL.md
```

If you want a git checkout of just the skill files, use a sparse clone. That
skips the `evals/` folder:

```
git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/shreyashankar/plain-writing-skill \
  ~/.claude/skills/plain-writing
```

- Other agents, e.g., Codex or pi, can use the rules too. Paste the rules from
  `SKILL.md` into whatever instructions that agent reads.

Then ask the agent to write or revise some text. It applies the rules on its
own.

## Deslopify an agent response

Use the command below when an agent response assumes too much context, uses
unexplained technical terms, or does not make the main point clear.

```
/plain-writing deslopify
```

The skill rewrites the agent's previous response in a clear structure for a
sharp CEO or technical reader who has no project context and needs to understand
all relevant details. The rewrite follows the plain-writing guidelines in the
skill.

You can also put text after the command when you want to rewrite text other than
the previous response.

## Evals

A skill install does not need the evals. If you want to run them, clone the
repo as usual, or add the folder to a sparse checkout:

```
git sparse-checkout add evals
```

Then see `evals/README.md`.
