# Design: Modernize Frontend Architecture

## Context

The Lateral Entry Portal currently uses a vanilla JavaScript approach with 13+ HTML files, inline scripts, and CDN-based dependencies. While this works for the current scale (~45 profiles), it presents maintainability and scalability challenges:

- **Code Duplication**: Header, footer, navigation, and common functionality duplicated across all pages
- **Manual State Management**: Filter state, search queries, and theme preferences managed with global variables and localStorage
- **No Build Optimization**: All resources loaded upfront, no code splitting or tree-shaking
- **Limited Reusability**: Profile cards, stat cards, and other UI patterns implemented multiple times with inconsistencies
- **Development Friction**: No hot reload, type safety, or modern tooling

This design proposes a migration to React 18 with TypeScript, Vite, and Tailwind CSS to address these issues while maintaining all existing functionality and visual design.

## Goals / Non-Goals

### Goals
1. **Component Reusability**: Create a library of reusable UI components that can be composed
2. **Type Safety**: Add TypeScript for better developer experience and fewer runtime errors
3. **Build Optimization**: Implement code splitting, lazy loading, and production optimizations
4. **State Management**: Centralize state logic with predictable patterns
5. **Developer Experience**: Enable HMR, better debugging, and modern tooling
6. **Maintainability**: Single source of truth for components, easier to update and extend
7. **Performance**: Improve perceived performance with optimistic UI and loading states
8. **Preserve Functionality**: Maintain all existing features, routes, and visual design

### Non-Goals
1. **Backend Changes**: Flask API and database remain unchanged
2. **Data Model Changes**: No changes to SQLite schema or JSON export format
3. **Visual Redesign**: Keep existing themes and visual design (can be enhanced later)
4. **New Features**: Focus on migration first, new features come after
5. **Framework Lock-in Concerns**: React is industry standard with large ecosystem
6. **Server-Side Rendering**: Static export sufficient for current needs

## Decisions

### Decision 1: React 18 + TypeScript
**What**: Use React 18 as the UI framework with TypeScript for type safety

**Why**:
- **React**: Industry standard, large ecosystem, excellent documentation, proven at scale
- **TypeScript**: Catch errors at compile time, better IDE support, self-documenting code
- **Alternatives Considered**:
  - **Vue 3**: Simpler learning curve but smaller ecosystem, less industry adoption
  - **Svelte**: Great performance but smaller ecosystem, less mature tooling
  - **Continue with Vanilla JS**: No overhead but maintenance burden grows with complexity
- **Trade-offs**: 
  - ✅ Better DX, maintainability, ecosystem
  - ✅ Industry standard with abundant resources
  - ❌ Larger bundle size (~150KB for React alone)
  - ❌ Learning curve for team members unfamiliar with React

**Rationale**: React's maturity, ecosystem, and tooling outweigh bundle size concerns. TypeScript adds safety and documentation value with minimal overhead.

### Decision 2: Vite as Build Tool
**What**: Use Vite for development server and production builds

**Why**:
- **Fast**: ES modules in dev, fast HMR, optimized production builds
- **Simple**: Minimal configuration, sensible defaults
- **Integrated**: First-class React and TypeScript support
- **Alternatives Considered**:
  - **Create React App**: Deprecated, slower builds, more complex configuration
  - **Next.js**: Overkill for static site, adds SSR complexity we don't need
  - **Parcel**: Good but less ecosystem momentum than Vite
  - **Webpack**: Powerful but complex configuration, slower than Vite
- **Trade-offs**:
  - ✅ Fastest development experience with HMR
  - ✅ Simple configuration
  - ✅ Modern best practices out of the box
  - ❌ Relatively new (but stable and widely adopted)

**Rationale**: Vite's speed and simplicity make it ideal for modern web development without the complexity of webpack.

### Decision 3: Zustand for State Management
**What**: Use Zustand for global state (filters, search, theme) with React Query for server state

**Why**:
- **Zustand**: Minimal API, no boilerplate, works with React's concurrent features
- **React Query**: Industry standard for server state, automatic caching and refetching
- **Alternatives Considered**:
  - **Redux Toolkit**: More boilerplate, overkill for our simple state needs
  - **Jotai/Recoil**: Atomic state management, more complex than needed
  - **Context API only**: No optimization, causes unnecessary re-renders
  - **MobX**: Observable pattern, less React-idiomatic
- **Trade-offs**:
  - ✅ Minimal bundle size (~1KB for Zustand)
  - ✅ Simple API, easy to learn
  - ✅ Great TypeScript support
  - ✅ React Query handles server state complexity
  - ❌ Two libraries instead of one (but specialized for purpose)

**Rationale**: Zustand's simplicity and small size are perfect for UI state, while React Query excels at server state management.

### Decision 4: Tailwind CSS with Build-Time Configuration
**What**: Move from CDN Tailwind to build-time Tailwind with custom configuration and JIT mode

**Why**:
- **Build-time**: Purge unused styles, custom configuration, better performance
- **JIT Mode**: Generate styles on-demand during development, faster builds
- **Custom Config**: Define theme colors, extend utilities, maintain design system
- **Alternatives Considered**:
  - **Keep CDN Tailwind**: Simple but no customization, larger bundle, no purging
  - **CSS Modules**: More verbose, lose utility-first benefits
  - **Styled Components**: Runtime overhead, larger bundle
  - **Plain CSS**: Maximum control but loses Tailwind's consistency
- **Trade-offs**:
  - ✅ Smaller production CSS bundle (only used styles)
  - ✅ Custom configuration and design tokens
  - ✅ Better autocomplete in IDE
  - ❌ Requires build step (already needed for React)

**Rationale**: Build-time Tailwind provides better performance and customization with no additional complexity since we already need a build step.

### Decision 5: Client-Side Routing with React Router v6
**What**: Use React Router for navigation with hash routing mode for deployment compatibility

**Why**:
- **React Router**: Industry standard, excellent DX, v6 is data-focused
- **Hash Routing**: Works with subdirectory deployment without server configuration
- **Alternatives Considered**:
  - **TanStack Router**: Newer, type-safe, but less mature ecosystem
  - **Wouter**: Minimal but lacks features (data loading, lazy loading)
  - **Server-side routing**: Requires backend, complicates static deployment
- **Trade-offs**:
  - ✅ No server configuration needed for subdirectory deployment
  - ✅ Client-side navigation is instant
  - ✅ Lazy loading routes for code splitting
  - ❌ Hash in URLs (`/#/profiles`) less clean but necessary for static hosting

**Rationale**: React Router v6 is the proven solution with hash mode ensuring deployment compatibility without server configuration.

### Decision 6: Component Architecture Pattern
**What**: Implement atomic design principles with components, layouts, and pages

**Structure**:
```
src/
├── components/          # Reusable UI components
│   ├── ui/             # Basic building blocks (Button, Badge, Card)
│   ├── profiles/       # Profile-specific (ProfileCard, ProfileModal)
│   ├── search/         # Search-related (SearchBar, FilterChips)
│   ├── navigation/     # Navigation (Header, Footer, MobileNav)
│   └── theme/          # Theme-related (ThemeSwitcher)
├── layouts/            # Layout components (MainLayout, PageLayout)
├── pages/              # Page components (Home, Profiles, Analytics)
├── hooks/              # Custom React hooks
├── stores/             # Zustand stores
├── lib/                # Utilities (API client, formatters)
├── types/              # TypeScript type definitions
└── App.tsx             # Root component with router
```

**Why**:
- Clear separation of concerns
- Easy to locate and modify components
- Encourages reusability
- Scales well as project grows

## Risks / Trade-offs

### Risk 1: Bundle Size Increase
- **Impact**: Initial bundle ~280KB gzipped vs current ~30KB
- **Likelihood**: Certain
- **Mitigation**: 
  - Code splitting by route reduces initial load
  - React Query caching reduces subsequent requests
  - Modern browsers cache vendor chunks aggressively
  - Better perceived performance offsets size increase
- **Acceptance**: Modern web apps typically 300-500KB; our ~280KB is reasonable

### Risk 2: Breaking Changes During Migration
- **Impact**: Features might break or behave differently during migration
- **Likelihood**: High
- **Mitigation**:
  - Parallel development in separate branch
  - Comprehensive testing checklist
  - Page-by-page migration with validation
  - Keep old version available for rollback
  - User acceptance testing before final deployment
- **Acceptance**: Thorough testing required but risk is manageable

### Risk 3: Development Complexity
- **Impact**: New build system and tooling adds complexity
- **Likelihood**: Medium
- **Mitigation**:
  - Document setup and development workflow
  - Use conventional patterns and minimal configuration
  - Leverage Vite's sensible defaults
  - Create npm scripts for common tasks
- **Acceptance**: Modern tooling is industry standard; one-time setup cost

### Risk 4: Deployment Configuration
- **Impact**: Build output structure might not work with current deployment
- **Likelihood**: Low
- **Mitigation**:
  - Configure Vite base path for subdirectory deployment
  - Test production build locally before deployment
  - Maintain static export capability
  - Document deployment process
- **Acceptance**: Vite handles subdirectory deployment well with proper configuration

### Trade-off 1: Bundle Size vs Developer Experience
- **Choice**: Larger bundle for better DX and maintainability
- **Justification**: One-time download cost, cached aggressively, benefits compound over time
- **Impact**: ~250KB additional initial download, negligible on modern connections

### Trade-off 2: Hash Routing vs Clean URLs
- **Choice**: Hash routing (`/#/profiles`) for deployment simplicity
- **Justification**: No server configuration needed, works everywhere
- **Impact**: Slightly less aesthetic URLs, but functional and SEO not a concern (public data portal)

### Trade-off 3: React vs Continue Vanilla JS
- **Choice**: React for long-term maintainability
- **Justification**: Current approach doesn't scale; React investment pays off
- **Impact**: Migration effort upfront, but easier maintenance and feature development afterward

## Migration Plan

### Phase 1: Project Setup (Day 1-2)
1. Initialize Vite project with React and TypeScript
2. Configure Tailwind CSS with custom theme colors
3. Set up ESLint, Prettier, and TypeScript strict mode
4. Configure build output for subdirectory deployment (`/lateral-entry/`)
5. Copy existing assets (images, JSON files) to `public/`
6. Port CSS variables from `themes.css` to Tailwind config

### Phase 2: Core Infrastructure (Day 3-5)
1. Create API client with JSON fallback logic
2. Implement theme system with Zustand store
3. Create layout components (Header, Footer, MobileNav)
4. Build basic UI components (Button, Badge, Card, Loading, Error)
5. Set up React Router with hash routing
6. Implement base page layout structure

### Phase 3: Component Library (Day 6-10)
1. Build ProfileCard component with all variants
2. Create BatchCard, StatCard components
3. Implement SearchBar with debouncing
4. Build FilterChips with active state
5. Create ThemeSwitcher component
6. Build ProfileModal for detail views
7. Implement loading skeletons and error boundaries

### Phase 4: Page Migration (Day 11-20)
1. **Simple Pages First** (Day 11-13):
   - FAQ page
   - History page
   - Citations page
2. **Data Pages** (Day 14-17):
   - Home page with stats and recent profiles
   - Analytics page with charts
   - 2024 Cancellation page
3. **Complex Pages** (Day 18-20):
   - All Profiles page with search/filter
   - Batch detail pages (2019, 2021, 2023)
   - Profile detail page

### Phase 5: State Management (Day 21-23)
1. Implement profiles store with Zustand
2. Add search store with debouncing
3. Create filters store with active filters
4. Set up React Query for API data fetching
5. Add loading and error states globally
6. Implement optimistic UI updates

### Phase 6: Testing & Refinement (Day 24-28)
1. Cross-browser testing (Chrome, Firefox, Safari, Edge)
2. Mobile device testing (iOS, Android)
3. Theme testing (all 4 themes on all pages)
4. Search and filter testing
5. Navigation and routing testing
6. Performance testing (Lighthouse, bundle analysis)
7. Accessibility testing (keyboard nav, screen readers)
8. Fix bugs and refine UX

### Phase 7: Production Build & Deployment (Day 29-30)
1. Optimize production build configuration
2. Test production build locally with `npm run preview`
3. Verify subdirectory deployment works
4. Create deployment documentation
5. Deploy to staging environment for final testing
6. Deploy to production
7. Monitor for issues
8. Archive old HTML files to `backups/`

### Rollback Strategy
If critical issues arise post-deployment:
1. Revert to old HTML files from backups
2. Update deployment to serve old files
3. Investigate and fix issues in development
4. Redeploy when ready

## Open Questions

### Q1: Should we use hash routing or browser routing?
**Answer**: Hash routing (`/#/`) for deployment simplicity since we're deploying to a subdirectory without server control. Can migrate to browser routing later if server configuration becomes available.

### Q2: Do we need TypeScript strict mode?
**Answer**: Yes. Strict mode catches more errors and enforces better practices. Initial setup takes longer but prevents bugs later.

### Q3: Should we migrate all pages at once or incrementally?
**Answer**: All at once in a separate branch, then deploy together. Incremental (serving some pages from React, some from HTML) adds complexity and confusion.

### Q4: How do we handle the API fallback to static JSON?
**Answer**: Port existing logic from `main.js` into API client utility. React Query handles caching and error states elegantly.

### Q5: Should we add tests during migration?
**Answer**: Not initially. Focus on feature parity first. Add tests incrementally after migration is complete and stable.

### Q6: How do we handle images and static assets?
**Answer**: Move to `public/` directory, reference with `/` prefix. Vite serves these at build time and copies to dist.

### Q7: What about SEO?
**Answer**: Not a primary concern since this is a data portal, not marketing content. Hash routing is acceptable. Could add meta tags for social sharing.

### Q8: Should we use a UI library (MUI, Chakra, etc.)?
**Answer**: No. Current design is already implemented with Tailwind. Continue with custom components using Tailwind for consistency and smaller bundle.
