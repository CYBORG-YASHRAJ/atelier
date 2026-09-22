---
name: web-3d
description: Live 3D for the web — Spline embeds (@splinetool/runtime), three.js / React Three Fiber / Threlte, Theatre.js sequencing, 3D icons, PeachWeb, and the performance laws that keep 3D premium. Load for ANY 3D request — 3D hero, 3D icons, product viewer, WebGL, Spline scene, scroll-driven 3D.
---

# Web 3D

## The gate — design-law still rules

Live 3D is a HERO MOMENT: at most ONE per page, serving the story, obeying
the project's tokens (palette, lighting mood, restraint). A gratuitous
spinning cube is anti-slop. `prefers-reduced-motion`, low-end mobile, and
loading states all get a static webp poster — always ship the fallback.

## Choose the tool (ladder — stop at the first rung that holds)

| Need | Use |
|------|-----|
| 3D **icons** / decorative marks | pre-rendered assets first: 3dicons.co, Shapefest, IconScout 3D (all in registry) — or generate on the image ladder, then `assets.py cut` → transparent webp. Zero runtime cost; the default. |
| Designed interactive scene, fastest path | **Spline** (spline.design) — design visually, embed via runtime (below) |
| Full code control in React | **React Three Fiber** — `npm i three @react-three/fiber @react-three/drei` |
| Svelte project | **Threlte** (threlte.xyz) — `npm i three @threlte/core @threlte/extras` |
| Vanilla / any other framework | **three.js** directly |
| Keyframe / scroll-driven cinematic sequencing | **Theatre.js** — `@theatre/core` (runtime) + `@theatre/studio` (DEV ONLY — never in the prod bundle) + `@theatre/r3f` bridge |
| Photoreal scroll narrative from rendered frames | **asset-pipeline frame sequence** — canvas scrub with chunked decode; cheaper and more predictable than live 3D |
| Client wants a no-code 3D site | **PeachWeb** (peachweb.io) — paid visual builder, exports embeds for any platform |

## Spline embed (the fast path — this IS the integration; ignore "Spline MCP" servers, Spline has no public API)

React/Next.js: `npm i @splinetool/react-spline @splinetool/runtime`

```tsx
import { lazy, Suspense } from 'react';
const Spline = lazy(() => import('@splinetool/react-spline'));
// inside the hero, below an IntersectionObserver or next/dynamic ssr:false:
<Suspense fallback={<img src="/poster.webp" alt="" />}>
  <Spline scene="https://prod.spline.design/<id>/scene.splinecode"
          onLoad={(app) => appRef.current = app} />
</Suspense>
```

Vanilla: `new Application(canvas).load(url)` from `@splinetool/runtime`.
Control at runtime: `app.findObjectByName('Cube')` (then mutate
`.position/.rotation/.scale`), `app.emitEvent('mouseHover', 'Cube')`,
`app.setVariable(name, value)`. Scene URL comes from the Spline editor →
Export → Code Export. Community scenes: study technique, never copy paid assets.

## R3F skeleton (the laws are in the props)

```tsx
<Canvas dpr={[1, 2]} frameloop="demand" gl={{ antialias: true }}>
  <Environment preset="studio" />
  <MyModel /> {/* useGLTF('/model.glb') — drei caches + disposes */}
  <OrbitControls enableZoom={false} />
</Canvas>
```

`frameloop="demand"` for scenes that only move on interaction; drop it only
for continuous animation. Threlte mirrors this: `<Canvas>` from
`@threlte/core`, helpers from `@threlte/extras` (`<GLTF>`, `<OrbitControls>`).

## Performance laws (non-negotiable)

- Lazy-load ALL 3D: dynamic import behind IntersectionObserver — never in the initial bundle.
- Clamp `dpr` to `[1, 2]`; one WebGL context per page.
- GLB budget < 2 MB: compress with `npx gltf-transform optimize in.glb out.glb` (draco + prune + resize).
- Dispose on unmount (drei/Threlte handle it; raw three.js: `geometry.dispose()`, `material.dispose()`, `renderer.dispose()`).
- Poster fallback (webp via asset-pipeline) for reduced-motion, mobile, and load — the page must read perfectly with 3D absent.

## Scroll narrative composition

Use three depth planes at most: a slow atmospheric backdrop, the primary frame
sequence or 3D subject, and crisp semantic copy/chrome. Map all planes to one
normalized scroll progress; vary distance and easing instead of adding unrelated
animations. Pin only while the scene advances, then return to normal document
flow. Avoid scroll hijacking, wheel interception, and fake smooth-scroll latency.

Choose rendered frames for photoreal materials, fluid simulation, cinematic
lighting, or model-heavy scenes that do not need object interaction. Choose live
3D only when the user must rotate, select, configure, or inspect the object.
Never run live WebGL behind a full frame sequence. On mobile, reduce parallax,
serve a deliberate crop, and shorten the pinned distance. Follow the detailed
loading, poster, accessibility, and SEO contract in asset-pipeline.

## Live-scene debugging (optional MCP companion)

Register `npx threejs-devtools-mcp` with the current host's MCP setup — inspects
and edits a RUNNING three.js/R3F scene (59 tools, MIT) through a WebSocket
bridge; needs the project dev server up. Offer with yes/no confirmation per
bootstrap — useful only in 3D-heavy projects.
Host integration: read [the runtime contract](../../references/runtime.md) for plugin/project paths, host command names and capabilities. Explicit user instructions and repository conventions take precedence over these defaults.
