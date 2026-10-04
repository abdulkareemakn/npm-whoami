# AGENTS.md

## Commands

- `pnpm build` — compile `src/index.ts` to `dist/index.js`
- `pnpm start` — run the card locally

## Terminal colors

- Never hardcode colors (hex, `rgb()`, etc.) in terminal output. Use chalk's
  named colors so output adapts to the user's light or dark terminal theme; a
  fixed color is legible against one background only.
- Don't combine `bold` with a color. Terminals render that as the bright color
  variant, which is low-contrast on light backgrounds.
- Leave body text on the terminal's default foreground. It is the only color
  guaranteed to contrast with the theme's background.
