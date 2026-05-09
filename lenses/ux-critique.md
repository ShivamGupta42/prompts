# UX critique lens

Apply this lens to evaluate **user experience** — interface, copy, hierarchy, accessibility, and the path from intent to outcome. Use it on user-facing plans (UI work, new flows, redesigns). Skip for pure backend, infra, or developer-facing changes.

If a screenshot or live URL is available, look at it. Otherwise reason from the design spec, mockup, or implementation plan.

This lens has two parts: **critique** (find what's wrong) and **friction-to-fix** (propose a specific change for the highest-impact issue).

---

## Part A — Critique

Walk through these eight categories. For each, surface 0–3 concrete issues. **If a category has no real issues, say "nothing found" with a one-line note on what you checked — don't fabricate.**

### 1. First impression (3 seconds)

What feels off in the first three seconds? Alignment, spacing, visual weight, color choices. The reader's eye should land somewhere meaningful. Where does it land here?

### 2. Hierarchy

Is the most important action obvious? Does the eye flow logically from primary → secondary → tertiary? What competes for attention and shouldn't?

### 3. Consistency with the system

Does this match product patterns — colors, typography, spacing, component usage? What breaks the system, and is the break intentional or accidental? Accidental breaks are P0; intentional breaks need a stated reason.

### 4. Information completeness

Is content complete, correct, logically ordered? What's missing? What's confusing? What does the user have to infer that we should state directly?

### 5. Copy check

Is the text human-simple? Flag jargon, assumed knowledge, unclear labels, robotic phrasing. Users shouldn't need expertise to understand what's in front of them. "Verify your identity" beats "OAuth re-authentication required." Quote the bad lines and propose replacements.

### 6. Mobile fit

- Touch targets ≥44pt?
- Primary actions thumb-reachable (lower 2/3 of screen)?
- Layout responsive without horizontal scroll at 375px?
- Feels native, or like a desktop layout shrunk down?

### 7. Accessibility

- Color contrast at WCAG AA minimum (4.5:1 for body text, 3:1 for large text and UI components)
- Tiny text (under 16px for body)
- Unclear focus states for keyboard nav
- Missing labels or descriptions for screen readers
- Tap targets too close together
- Animation that ignores `prefers-reduced-motion`

### 8. Errors and edge states

What happens at empty / loading / error / offline states? Are they designed, or does the user see a blank screen and a console error? When something fails, does the user know what to do next, or are they stuck?

---

## Part B — Friction → Fix

Pick the **single highest-impact friction** from Part A (or from the user job context if a JTBD lens already ran). Walk through:

### 1. Top friction

Where do users pause, retry, or abandon? Be specific to a moment in the flow — name the screen, button, copy line, or interaction.

### 2. Root cause

Why does this friction exist? UI clarity, missing feedback, cognitive load, poor defaults, confusing copy, hidden affordance, mismatch with mental model?

### 3. Design fix

Propose a concrete fix. Be specific: *"Change button text from 'Continue' to 'Save and continue'"* beats *"improve clarity."* Cover layout, copy, interaction, or flow changes as needed.

### 4. Hypothesis

State as: *"If we [fix], users will [behavior change], measured by [metric]."* Make the metric something you'd actually observe in analytics or user testing.

### 5. Side effects

What else changes? Other screens affected, edge cases now in scope, empty/error states needing rework, copy that ripples elsewhere?

### 6. Smallest version

What's the minimum viable version of this fix that could ship today? Save the gold-plated version for v2. The smallest version teaches you whether the hypothesis was right at the lowest cost.

### 7. Confidence

Rate (1–10) confidence this fix moves the needle:

- 1–3: guessing
- 4–6: informed but unverified
- 7–8: verified via user evidence
- 9–10: verified with data or A/B testing

What would lift confidence to 9+?

---

## Output format

- **Part A**: 5–10 issues max, grouped by P0 (blocks usability) / P1 (noticeable friction) / P2 (polish). For each P0 and P1: what's wrong + specific fix.
- **Part B**: one friction-to-fix walkthrough. If multiple high-impact frictions exist, name the others as P1 follow-ups but only walk through the top one in full.

## Rules for this lens

- Concrete beats abstract. Name the button, the screen, the copy line, the contrast ratio.
- Don't fabricate issues to fill categories. Empty categories are fine; lying isn't.
- Skip the lens entirely (with a one-line reason) if the work has no user-visible surface. A backend job-queue refactor doesn't need a UX critique.
- Quote real copy. Use real measurements (px, pt, contrast ratios) not vague modifiers ("too small").
