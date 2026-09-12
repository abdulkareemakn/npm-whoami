# abdulkareem

Terminal business card. Run with:

```
npx abdulkareem
```

## Develop

```bash
npm install
npm run build   # compiles src/index.ts -> dist/index.js and makes it executable
npm start       # run locally to preview
```

## Customize

Edit the `sections` array in `src/index.ts` — each section has a `title`
(shown as a divider) and a list of `{ key, value }` fields (shown as
dotted key/value lines). Rebuild after editing.

## Publish

```bash
npm login
npm publish
```

Once published, anyone (including you) can run `npx abdulkareem` to see it.
