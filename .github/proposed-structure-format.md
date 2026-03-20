# Proposed Structure Format

This file defines the expected format of `outputs/proposed_structure.json`.

## Goals

1. Keep the Step 2 proposal fully detailed.
2. Make the proposal directly machine-readable without duplicating the same information in markdown and JSON.
3. Allow tools such as the dependency graph generator to consume the proposal reliably.

## File Format

The proposed structure output should be a single JSON object.

Required top-level keys:

- `inputs_reviewed`
- `user_preferences_applied`
- `pages`
- `proposed_missing_prerequisites`
- `omitted_source_sections`
- `tag_review`
- `checkpoint_review`

## Schema

```json
{
  "inputs_reviewed": [
    {
      "path": "inputs/example.md",
      "role": "existing platform content"
    }
  ],
  "user_preferences_applied": [
    "Language-agnostic foundations first before Python-specific pages."
  ],
  "pages": [
    {
      "slug": "programming-recursive-functions",
      "title": "Programming: Recursive Functions",
      "learning_objective": "Understand recursion, base cases, and recursive step design.",
      "description": "Language-agnostic conceptual treatment of recursion and termination.",
      "prerequisites": [
        "programming-defining-functions",
        "programming-calling-functions"
      ],
      "related_content": [
        "example-python-factorial-recursive"
      ],
      "proposed_tags": [
        "programming"
      ],
      "status": "new"
    }
  ],
  "proposed_missing_prerequisites": [
    {
      "slug": "python-defining-functions",
      "why": "Needed as a Python-specific syntax prerequisite.",
      "suggested_minimal_scope": "Python syntax for function definition, arguments, and return values.",
      "suggested_prerequisites": [
        "programming-defining-functions"
      ],
      "suggested_tags": [
        "python"
      ]
    }
  ],
  "omitted_source_sections": [
    {
      "section": "Calling a Function",
      "reason": "Covered by existing content already in the platform."
    }
  ],
  "tag_review": {
    "new_tags_required": [],
    "existing_tags_used": [
      "programming",
      "python",
      "exercise",
      "sample-solution"
    ],
    "notes": "All proposed pages use existing tags only."
  },
  "checkpoint_review": {
    "language_agnostic_foundations_first": "Applied for recursion and default arguments.",
    "single_learning_objective": "Each page has one focused objective.",
    "concrete_exercises": "Exercises are extracted from the source notebook.",
    "exercise_naming_conventions": "Uses exercise-<language>-<topic> and sample-solution-<language>-<topic>.",
    "tagging_conventions": "Programming for language-agnostic pages, python for Python pages."
  }
}
```

## Required Page Fields

Each entry in `pages` must include:

- `slug`
- `title`
- `learning_objective`
- `description`
- `prerequisites`
- `related_content`
- `proposed_tags`
- `status`

## Notes For Tooling

- The dependency graph tool reads `pages[*].slug`, `pages[*].prerequisites`, and `proposed_missing_prerequisites[*].slug`.
- All other fields are preserved so the JSON file can be used directly for review and later content generation steps.
- Keep slugs and tags as plain strings.
- Use valid JSON only: double quotes, no trailing commas, no markdown fencing.

## Backward Compatibility

The graph script still accepts older markdown proposals if explicitly passed, but `outputs/proposed_structure.json` is now the canonical Step 2 output format.
