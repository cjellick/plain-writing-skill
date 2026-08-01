# Plain writing skill

This skill makes an AI agent write in a plain style. The full rules are in
`SKILL.md`.

The rules are plain text, so any agent can use them.

The skill also checks its own writing and removes anything that does not add
something.

## What is in here

- `SKILL.md`: the skill, with the rules and the steps.

## How to use it

`SKILL.md` is a plain markdown file with the rules. Any agent that can read a
file can follow it. The simplest way is to give `SKILL.md` to the agent as
instructions, in a rules file or the system prompt.

Some tools have a set place for skills:

- Claude Code reads skills from `~/.claude/skills`. Clone the repo into a folder
  named `plain-writing`:

```
git clone https://github.com/shreyashankar/plain-writing-skill ~/.claude/skills/plain-writing
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

The skill rewrites the agent's previous response as a one-page brief for a CTO
who is joining the project with no context. The rewrite explains the project,
the main conclusion, what changed, what it means for the business, and any
risks or open questions. It does not invent missing details.

You can also put text after the command when you want to rewrite text other than
the previous response.
