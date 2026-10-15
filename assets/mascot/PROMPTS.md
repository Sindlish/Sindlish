# Mascot variant prompts

Upload `Mascot.png` (the character sheet) as the reference in every generation. Paste the base
preamble, then the one prompt for the variant you want. Save the output with the filename given.

## Base preamble (paste this every time, before the variant prompt)

```
Use the attached character sheet as the single source of truth for the character design.
Match it exactly: same body shape and proportions, same palette, same line weight and
shading style, same eye and face design, same level of detail. Do not redesign the
character, do not add or remove any features.

Output: one character only, full body, centered, upright, facing the viewer, with
generous empty margin on all sides. Transparent background. No ground line, no shadow,
no text, no watermark, no border, no scenery.
```

If the output drifts from the sheet, upload the good result as an *additional* reference
alongside the sheet on the next attempt. Two references hold the design better than one.

## Order of work

The list is ranked by how much each variant unlocks. Do the top three first.

### 1. `mascot-standing-neutral.png`

The workhorse: hero image, footer, anywhere the mascot is simply present. Needed first
because it is the base every other pose is measured against.

```
Base preamble, then:

Standing in a calm, neutral, relaxed pose. Arms resting naturally at the sides, a
friendly closed-mouth smile, looking straight at the viewer. This is the default,
canonical pose.
```

### 2. `mascot-curious-question.png`

The charm variant: search with no results, "no docs match", empty states, 404 page.

```
Base preamble, then:

Standing with a curious, inquisitive expression: head tilted slightly, one eyebrow
raised, mouth slightly open as if asking. A single large clean question mark floats
just above and to the side of the head. The question mark is a simple bold rounded
glyph, solid colour matching the character, not stylised or hand-drawn.
```

### 3. `mascot-celebrate.png`

Paired with the Run button: code runs and passes.

```
Base preamble, then:

Standing in a small celebratory pose: both arms raised in a cheerful success gesture,
eyes closed in a happy expression, open joyful smile. Energetic but not jumping or
motion-blurred.
```

### 4. `mascot-point.png`

Points at things: callouts, admonitions, "look at this" moments.

```
Base preamble, then:

Standing and pointing outward to the side with one arm extended, the other arm relaxed.
The pointing hand is clearly readable as a pointing gesture. Confident, helpful
expression with a slight smile.
```

### 5. `mascot-thinking-error.png`

Paired with the Run button: code runs and fails. The counterpart to `celebrate`.

```
Base preamble, then:

Standing with a puzzled, slightly worried expression: brows drawn together, one hand
raised to the side of the head in a thinking gesture, mouth in a small uncertain line.
Puzzled rather than distressed. No sweat drops, no gloom, no red warning symbols.
```

### 6. `mascot-sit.png`

A companion: bottom of the docs sidebar, or the footer.

```
Base preamble, then:

Sitting down in a relaxed, comfortable pose, legs folded or tucked to one side, hands
resting in the lap, looking at the viewer with a calm content expression.
```

### 7. `mascot-wave.png`

Friendly hello: homepage hero alternative, empty-state warmth.

```
Base preamble, then:

Standing and waving with one hand raised, palm open toward the viewer, a warm open
smile. The other arm rests naturally. Cheerful and welcoming.
```

### 8. `mascot-icon.png`

The small-size problem: favicon, inline icon, tight spaces. Generate it at the same
large size as the others, then send the file to me and I will downscale and optimise it.
Do not ask the generator for a small image directly, it produces mush.

```
Base preamble, then:

A simplified, icon-like version of the character: reduced detail, bolder shapes, larger
and simpler eyes, minimal interior detail, designed to stay readable when scaled down.
Head and shoulders only, filling the frame, front facing, neutral friendly expression.
Same palette as the character sheet.
```

### 9. `mascot-silhouette.png`

Single colour, for use on tinted or coloured backgrounds where the full-colour art would
clash or lose contrast.

```
Base preamble, except replace the background and detail rules with:

Output: one character only, full body, centered, upright, facing the viewer, with
generous empty margin on all sides. Rendered as a flat, solid, single-colour silhouette
in pure black with absolutely no interior detail, no line work, and no gradient.
Transparent background. No text, no watermark, no scenery.
```

## Naming and filing

Save each as `D:\Code\Sindlish\assets\mascot\<name>.png`, using the filenames above.

When a variant exists, tell me and I will resolve
[Commission the mascot variant art set](https://github.com/Sindlish/sindlish-website/issues/27).
Three is enough to start: `standing-neutral`, `curious-question`, and `celebrate` unblock
the mascot's UI role decision on its own.