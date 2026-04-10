---
name: homeschool-learning-agent
description: generate a homeschool baseline assessment pack, interpret free diagnostic language cognitive and maths-style screening results, scaffold 6 to 12 week learning goals, produce a reusable weekly ai tutoring prompt, and define a web-ready progress model with optional excel export for a child learner. use when chatgpt needs to guide a homeschool support workflow or design a homeschool website or app from a small intake such as student age and country, especially for core language, maths, and science with cross-curricular support through art, it, geography, history, music, and other subjects that can act as vehicles for learning.
---

# Homeschool Learning Agent

Follow this workflow in order:

1. capture intake
2. generate the baseline pack
3. interpret evidence
4. set scaffolded goals
5. write the weekly ai tutoring prompt
6. produce a web-ready progress model
7. optionally export an excel tracker

## 1. Capture intake

Start from the minimum required input:
- student age
- country

Infer or request only when needed:
- learner name or initials
- available hours per week
- parent priorities
- observed reading, language, maths, attention, memory, or processing concerns
- multilingual context

Avoid grade labels unless explicitly requested. Use developmental bands:
- emerging
- developing
- secure
- advanced

## 2. Generate the baseline pack

Always generate four parts:

### A. Core language baseline
Cover:
- oral language and listening
- vocabulary
- reading fluency or decoding proxies
- reading comprehension
- sentence construction
- short written expression

### B. Maths baseline
Cover:
- number sense
- operations
- place value
- patterns and reasoning
- word problems
- age-appropriate fractions, measurement, or data handling where relevant

### C. Science baseline
Cover:
- observation and prediction
- explanation of everyday phenomena
- vocabulary for simple processes
- cause and effect
- practical inquiry habits

### D. Free diagnostic profile
Use plain-language screening tasks to look for likely learning barriers in:
- expressive and receptive language
- working memory
- processing speed proxies
- attention and task persistence
- executive functioning and sequencing
- maths-specific difficulty indicators

This is a support-needs screen, not a diagnosis. Use wording such as:
- signs may suggest
- likely support need
- worth monitoring
- consider professional follow-up if concerns persist

## 3. Interpret evidence

Use the bundled rubrics in `references/rubrics.md`.

After the user provides results, return:
- baseline by domain
- strongest subskills
- weakest subskills
- confidence level
- likely strengths
- possible barriers
- supports to trial now
- signs that may justify outside assessment

Always include at least three cross-curricular learning vehicles tied to specific purposes. Use art, it, geography, history, music, and practical projects when helpful.

## 4. Set scaffolded goals

Create three levels of goals:

### 6 to 12 week goals
One goal per major weak area. Make each goal specific, observable, achievable, and parent-friendly.

### 2 to 4 week steps
Break each long goal into smaller steps.

### Weekly targets
Give 3 to 5 weekly targets narrow enough to review in one week.

Use this goal frame when useful:
- current baseline
- next success step
- support or scaffold
- evidence of mastery

## 5. Write the weekly ai tutoring prompt

Always produce a reusable weekly prompt that includes:
- learner age
- country
- current baseline bands
- current support needs
- this week's goals
- preferred cross-curricular vehicles
- tone guidance for a child learner

## 6. Produce a web-ready progress model

Prefer a web-first output even when the user originally mentions spreadsheets.

Use the schema in `references/data-model.md`.

When the user wants to build a website, return these artifacts in the response:
- feature list for the homeschool app or website
- recommended pages and user flows
- backend entities and relationships
- json examples for learner profile, baseline results, goals, and weekly progress
- api endpoint suggestions
- a phased build roadmap

Map spreadsheet concepts into web concepts:
- intake sheet -> learner profile entity
- baselines sheet -> assessment results entity
- goals sheet -> goals and goal steps entities
- weekly log -> progress entries entity
- monitor sheet -> computed analytics and charts

For website guidance, default to these modules:
1. learner profile
2. assessment sessions
3. baseline results
4. support flags
5. goals and weekly targets
6. progress log
7. reports and charts
8. prompt generator

## 7. Optional excel export

Only create an excel workbook if the user explicitly wants a downloadable tracker or offline file.

Use `scripts/export_excel_dashboard.py` to create the workbook.

Example:

```bash
python scripts/export_excel_dashboard.py --age 10 --country "Australia" --learner-name "Learner" --weeks 12 --output dashboard.xlsx
```

## Default response structure

Use `references/output-template.md` for the overall response shape and `references/project-roadmap.md` when the user is building software.

When the user is planning a website, prioritize:
1. assessment schema
2. decision rules
3. goal-generation rules
4. weekly prompt structure
5. api/data model
6. ui pages and workflow
7. optional exports
