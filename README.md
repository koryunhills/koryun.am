# Koryun | UX/UI Design Agency

A static website for Koryun, built with Astro and deployable to Cloudflare Pages for free.

## Pages

- **/** – Home (hero, work, services preview, contact)
- **/services** – Full services, design process, how we help
- **/about** – Team, approach, why choose us
- **/naviguide** – Case study: Naviguide
- **/gouter** – Case study: Gouter
- **/torn** – Case study: Torn

## Local development

```bash
npm install
npm run dev
```

Open [http://localhost:4321](http://localhost:4321).

## Build

```bash
npm run build
```

Output is in `dist/`.

## Deploy to Cloudflare Pages (free)

### Option 1: Connect Git repository

1. Push this project to GitHub/GitLab.
2. Go to [Cloudflare Dashboard](https://dash.cloudflare.com) → Pages → Create project → Connect to Git.
3. Select project and configure:
   - **Build command:** `npm run build`
   - **Build output directory:** `dist`
4. Deploy.

### Option 2: Deploy via Wrangler CLI

```bash
npm install -g wrangler
npx wrangler pages deploy dist --project-name=koryun-am
```

### Option 3: Direct upload

1. Run `npm run build`.
2. In Cloudflare Dashboard → Pages → Create project → Direct upload.
3. Upload the `dist` folder.

## Custom domain

In Cloudflare Pages → Custom domains → Add `koryun.am` and follow DNS setup.
