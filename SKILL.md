---
name: plain-writing
description: >-
  Write and edit prose in the user's plain style: simple everyday words,
  complete sentences, no dashes, no jargon, no analogies, and full clear
  explanations. Use this whenever you draft or revise any prose for the
  user, such as documents, Notion pages, reports, summaries, README files,
  research notes, proposals, slide text, emails, or commit and PR descriptions.
  Also use it whenever the user asks to simplify, clean up, tighten, reword, or
  make writing clearer or easier to read. Default to this style for prose
  written for the user unless they ask for a different one. Do not apply it to
  code itself, only to the words around it. When the user invokes
  "/plain-writing deslopify" or asks to deslopify an agent response, rewrite
  the response in a clear structure for a sharp CEO or technical reader who
  has no project context and needs to understand all relevant details.
---

# Plain writing

The plain writing skill captures how the user wants written prose to read. The
goal is text that anyone can read once and understand. The user has asked for the
plain style repeatedly, and they correct writing that does not follow it, so
apply it by default when you write prose for them.

The rules are in four groups: word choice and tone, sentences and paragraphs,
punctuation and formatting, and patterns to avoid. Each rule is followed by a
before and after, so you can see it. After the rules comes how to revise.

## The deslopify command

When the user says `/plain-writing deslopify`, rewrite the previous agent
response, or the text after the command, in a clear structure for a sharp CEO
or technical reader who has no project context and needs to understand all
relevant details. Return only the rewrite.

Start with the main conclusion, then explain the relevant background, what
happened, how it works, the tradeoffs, the options, the recommendation, the
evidence, the risks, and the unknowns. Include technical details when the reader
needs them to understand the subject, and define any technical term that may be
unfamiliar.

Follow the plain-writing guidelines below. E.g., don't use jargon, and write in
a more explanatory voice, using longer sentences and commas to connect related
ideas instead of a series of short sentences.

## Word choice and tone

1. **Use simple, everyday words.** Don't pick a fancy synonym when a plain word
   works. Also avoid words AI tools overuse, e.g., "delve", "tapestry",
   "landscape", "robust", "leverage", and "reach".
   Before: We leverage the cache to unlock a more robust query experience.
   After: We use the cache to make repeated queries faster.

2. **No jargon.** Always use human-understandable language, the way two people
   talk to each other. Don't invent jargon or shorthand (that is, if a word or
   phrase is not in the Merriam Webster dictionary, don't use it). Use
   established technical terms only when they are most precise, and briefly
   define them when readers may not know them.
   Before: The score is a calibrated proxy for whether the property holds.
   After: The score estimates how likely the property is to hold.

3. **No puffery or empty emphasis.** Drop words that add emphasis but no
   information, e.g., "really", "real", "matters", "worth", "carries weight",
   "boasts", "a testament to", "pivotal", "renowned", and "quietly". State the
   actual point, or cut the sentence.
   Before: This result matters, and it carries weight for the design.
   After: The scores barely moved, so we can skip the model on most documents.

4. **Repeat a word rather than swap in a synonym.** When the same thing comes up
   again, use the same word for it. Do not use a different word just to avoid
   repeating yourself, because the swap reads as fancy.
   Before: Upload the document. The file is parsed, and the record is saved.
   After: Upload the document. The document is parsed and saved.

5. **Contractions are fine.** They match everyday speech, so use them freely.
   You do not have to write every word out in full.
   Before: Do not worry, it is not going to overwrite your file.
   After: Don't worry, it's not going to overwrite your file.

6. **Do not invent hyphenated adjectives.** A common compound adjective that
   people already use is fine, e.g., "well-crafted". Avoid a phrase you make up
   by joining words with a hyphen to sound compact or clever. A good test is
   whether you would find the term in a dictionary, or whether you would hear it
   in normal speech.
   Before: We added a reveal-style colon to the output.
   After: We added a colon that shows the schema.

7. **Keep the writing boring, descriptive, and explanatory.** Do not use a
   catchy phrase, slogan, clever label, metaphorical summary, or wording meant
   to sound memorable. State the actual concept, action, condition, or
   relationship in literal terms. This rule applies to headings, topic
   sentences, callouts, labels, summaries, and ordinary prose.
   Before: Legal requirements as a floor.
   After: Applicable legal constraints.
   Before: The alignment loop.
   After: Iterative refinement using development disagreements.

## Sentences and paragraphs

8. **Write complete sentences.** Each sentence has a subject and a verb. Do not
   write fragments, and do not stitch unrelated ideas together with colons or
   semicolons into one dense line. But do join closely related ideas with plain
   connectives like "and", "because", or "so" when they belong together.
   Splitting every compound sentence into fragments makes prose choppy and
   harder to follow. The test is whether the ideas are actually related.
   Before: The agent polls the file and reacts to changes, and the team meets on
   Tuesdays.
   After: The agent polls the file and reacts to changes. The team meets on
   Tuesdays.

9. **Explain things fully and clearly.** Plain does not mean terse. If an idea is
   compressed into one cramped sentence, expand it so each point gets its own
   sentence and the reader can follow it.
   Before: The groups the features were sorted into were the authors' own
   reading, the example posts were written by hand, and finer detail meant
   training extra small models and labeling again.
   After: First, the authors sorted the features into groups themselves, based on
   their own reading of the outputs. Second, they wrote the example posts by
   hand. Third, when they wanted finer detail, they trained another small
   model, and they labeled the posts again.

10. **Organize a paragraph as a topic sentence and then support.** Start each
   paragraph or section with a topic sentence that states the main point. Then,
   the next sentence should be a supporting example or fact, with an extra
   sentence about it if it needs one. Then, introduce more support with a plain
   connective like "For example", "Moreover", or "Or".
   Before: The parser skips files with no changes. The cache holds the previous
   output. Most renders are fast.
   After: Most renders are fast. For example, the parser skips files with no
   changes, so the server returns early. Moreover, the cache keeps the previous
   output, so a repeated render does no work.

11. **Never write three or more clauses in one sentence, or three or more
    example sentences in a row.** It is fine for a sentence to contain one or
    two related clauses. But it is bad to contain three or more clauses. If you
    absolutely must have so many clauses, use bullet points. If these list
    points are examples and you want to inline them, always introduce with
    "e.g.". Moreover, do not give three or more example sentences back to back
    to support the same point.
    Before: The parser reads the file, the validator checks the fields, and the
    writer saves the record.
    After: The parser reads the file, and the validator checks the fields. The
    writer then saves the record.

12. **Prefer long, explanatory sentences over short, punchy ones.** Write the
    way people explain things out loud, in longer sentences with commas, and the
    most straightforward or simplest way to communicate the point. Don't ever
    write catchy, short phrases.
    Before: The gate runs on every merge. It blocks regressions. Nobody
    bypasses it.
    After: The gate runs on every merge, and it blocks changes that fail a
    regression case. A regression cannot make it to production, unless someone
    deliberately overrides the check.

13. **Be precise and unambiguous.** Say exactly what changes, who does what,
    or by what mechanism. Prefer a concrete statement over an evocative
    abstraction, e.g., don't say things like "improvement stops being
    guesswork".
    Before: With trusted scores, improvement stops being guesswork.
    After: With trusted scores, you can measure whether each change helped,
    so you keep or revert each change based on the measured result.

## Punctuation and formatting

14. **No dashes or middle dots.** Do not use em dashes or en dashes, including in
    number ranges. Join clauses with a period or "and", and write ranges with
    "to". Do not use the middle dot (·) as a separator; use a comma, "and", or
    separate lines instead.
    Before: The build is fast — it finishes in 10 to 20 seconds.
    After: The build is fast. It finishes in 10 to 20 seconds.

15. **Don't use colons, unless you are introducing a list.** Do not use a
    colon to join clauses or to set up a point.
    Before: Read for the schema: the feature fires.
    After: Read for the schema. The feature fires.

16. **Use straight quotes, not curly quotes.**
    Before: The system logs each “event” as it happens.
    After: The system logs each "event" as it happens.

17. **Keep the formatting plain.** Use sentence case in headings. Do not use
    bold for decoration.
    Before: ## How To Install The Skill
    After: ## How to install the skill

## Patterns to avoid

18. **Do not assign actions to inanimate things.** If the subject of a sentence
    is inanimate, the only verbs should be "is" or "are". Common phrases such as
    "the paper argues" are fine.
    Before: The logs become searchable records, once the job finishes.
    After: You can search the logs, once the job finishes.

19. **No analogies or imagery.** Do not explain by comparing to something else,
    and do not use metaphor. Describe the actual thing in literal terms. Write
    in a boring way.
    Before: The feature index is like a card catalog that the optimizer can flip
    through.
    After: The feature index is a list of named features. The optimizer can look
    up which feature matches a request.

20. **Never use any form of negative parallelism, e.g., "not just X, it is
    Y".** State what the thing is.
    Before: It is not just a parser, it is a full toolchain.
    After: It is a parser and a formatter.

21. **Do not stack rhetorical questions.** AI writing often asks two or three
    rhetorical questions in a row to sound thoughtful. Don't do this. Just state
    the problem directly.
    Before: Does the tool keep the writer's voice? Does it make the argument
    stronger or weaker?
    After: We do not yet know whether the tool keeps the writer's voice, or
    whether it makes the argument stronger or weaker.

22. **Do not use vague demonstrative pronouns.** Do not use "This", "That",
    "These", or "Those", especially do not start a sentence with a demonstrative
    pronoun, and never begin a paragraph with a sentence that contains a
    demonstrative anywhere in it.
    Before: That context carries into the next turn.
    After: The agent applies the rules you saved on the next turn.

23. **Do not open with a count of things.** Never start by announcing how many
    points are coming, e.g., "Two cautions." or "Three things to keep in mind."
    State the first point directly. If you absolutely must present many things,
    use a bullet list instead.
    Before: Two cautions. First, the section can drift out of date. Second,
    it can balloon if every item gets a sentence.
    After: The section can drift out of date, because it duplicates facts
    that live elsewhere. It can also balloon if every item gets a sentence.

## How to revise

Revise in two passes.

First pass. Read the text once, and fix anything that breaks the rules above.

Second pass. Read the revised text again, as if you had never seen it. Go clause
by clause, and ask whether each clause adds something the reader needs. If a
clause or sentence adds nothing the reader needs, remove it. Then check that a
reader seeing the text for the first time would understand every sentence.
