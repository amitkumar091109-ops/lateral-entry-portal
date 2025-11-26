# Build System Specification

## ADDED Requirements

### Requirement: Vite Build Configuration
The system SHALL use Vite as the build tool with optimized configuration for development and production environments.

#### Scenario: Development server starts with HMR
- **WHEN** a developer runs `npm run dev`
- **THEN** Vite starts a development server on port 5173
- **AND** Hot Module Replacement (HMR) is enabled
- **AND** changes to source files trigger instant browser updates
- **AND** React Fast Refresh preserves component state during updates

#### Scenario: Production build creates optimized bundle
- **WHEN** a developer runs `npm run build`
- **THEN** Vite compiles TypeScript to JavaScript
- **AND** it bundles all modules with Rollup
- **AND** it minifies JavaScript and CSS
- **AND** it tree-shakes unused code
- **AND** it generates a `dist/` directory with optimized assets
- **AND** the build includes source maps for debugging

#### Scenario: Base path configured for subdirectory deployment
- **WHEN** the production build is created
- **THEN** all asset paths are prefixed with `/lateral-entry/`
- **AND** the router base path is set to `/lateral-entry/`
- **AND** the built application works correctly when deployed to prabhu.app/lateral-entry/

### Requirement: TypeScript Configuration
The system SHALL use TypeScript in strict mode with path aliases and React JSX support.

#### Scenario: TypeScript compiles with strict mode
- **WHEN** TypeScript files are compiled
- **THEN** strict mode is enabled catching more errors
- **AND** it enforces explicit types for function parameters and return values
- **AND** it disallows implicit any types
- **AND** it enables strict null checks

#### Scenario: Path aliases simplify imports
- **WHEN** a developer imports from `@/components`
- **THEN** TypeScript resolves it to `src/components/`
- **WHEN** importing from `@/lib`
- **THEN** TypeScript resolves it to `src/lib/`
- **AND** this works in both dev and production builds

### Requirement: Tailwind CSS Build Integration
The system SHALL configure Tailwind CSS to process styles at build time with JIT mode and purging.

#### Scenario: Tailwind processes styles during build
- **WHEN** the application is built
- **THEN** Tailwind scans all JSX files for class names
- **AND** it generates only the CSS for used utilities
- **AND** it purges unused styles from the output
- **AND** the final CSS bundle is under 30KB gzipped

#### Scenario: Custom theme colors are configured
- **WHEN** Tailwind is configured
- **THEN** theme colors from `themes.css` are added to Tailwind config
- **AND** utilities like `bg-theme-primary`, `text-theme-accent` are available
- **AND** CSS custom properties are used for dynamic theming

#### Scenario: JIT mode generates styles on-demand
- **WHEN** a developer uses an arbitrary value like `w-[375px]`
- **THEN** Tailwind generates the utility on-demand
- **AND** it's included in the development build
- **AND** it's included in production if used in the code

### Requirement: Code Splitting
The system SHALL implement route-based code splitting to reduce initial bundle size.

#### Scenario: Routes are lazy loaded
- **WHEN** the application is built
- **THEN** each page component is split into a separate chunk
- **AND** chunks are loaded on-demand when routes are accessed
- **WHEN** a user navigates to the Profiles page
- **THEN** only the Profiles chunk is downloaded
- **AND** subsequent navigation to that page uses cached chunk

#### Scenario: Vendor code is split separately
- **WHEN** the production build is created
- **THEN** React, React DOM, and other vendor libraries are in a separate vendor chunk
- **AND** the vendor chunk is cached aggressively by browsers
- **AND** application code changes don't invalidate vendor cache

### Requirement: Asset Optimization
The system SHALL optimize static assets including images, fonts, and JSON files.

#### Scenario: Static assets are copied to dist
- **WHEN** the application is built
- **THEN** files in `public/` directory are copied to `dist/`
- **AND** JSON data files are included
- **AND** analytics PNG images are included
- **AND** all assets are accessible at runtime

#### Scenario: Asset URLs are hashed for cache busting
- **WHEN** JavaScript and CSS files are built
- **THEN** filenames include content hashes (e.g., `main.a3b2c1d4.js`)
- **WHEN** code changes
- **THEN** the hash changes forcing browsers to fetch new versions
- **WHEN** code doesn't change
- **THEN** the hash remains the same allowing cache reuse

### Requirement: Development Experience
The system SHALL provide excellent developer experience with fast builds, clear errors, and helpful tooling.

#### Scenario: Errors display in browser and terminal
- **WHEN** a TypeScript error occurs
- **THEN** it's displayed in the terminal with file location
- **AND** it's displayed as an overlay in the browser
- **AND** the error message includes helpful context

#### Scenario: ESLint catches code quality issues
- **WHEN** a developer writes code that violates ESLint rules
- **THEN** the IDE shows inline warnings
- **AND** `npm run lint` displays all issues
- **AND** common issues are auto-fixed with `npm run lint:fix`

#### Scenario: Prettier formats code consistently
- **WHEN** a developer runs `npm run format`
- **THEN** Prettier formats all source files
- **AND** it enforces consistent style (quotes, semicolons, indentation)
- **AND** it can be configured to run on save in IDEs

### Requirement: Environment Configuration
The system SHALL support environment variables for different deployment targets.

#### Scenario: Environment variables are typed
- **WHEN** environment variables are accessed in code
- **THEN** they use the `import.meta.env` API
- **AND** TypeScript provides autocomplete for defined variables
- **AND** attempting to access undefined variables causes a type error

#### Scenario: API base URL is configurable
- **WHEN** `VITE_API_BASE_URL` is set in environment
- **THEN** the API client uses that URL
- **WHEN** the variable is not set
- **THEN** it defaults to the appropriate value based on environment (dev vs production)

### Requirement: Deployment Package
The system SHALL generate a deployment-ready package that can be uploaded to the production server.

#### Scenario: Dist directory is production-ready
- **WHEN** `npm run build` completes
- **THEN** the `dist/` directory contains all necessary files
- **AND** `index.html` is at the root
- **AND** assets are in `assets/` subdirectory
- **AND** JSON data files are in `data/` subdirectory
- **AND** the entire directory can be uploaded to `/lateral-entry/` on the server

#### Scenario: Preview command tests production build locally
- **WHEN** a developer runs `npm run preview`
- **THEN** Vite serves the production build locally
- **AND** it's accessible at `http://localhost:4173`
- **AND** it behaves exactly like the production deployment
- **AND** developers can test before deploying

### Requirement: Build Performance
The system SHALL complete builds quickly for rapid iteration and deployment.

#### Scenario: Development server starts in under 2 seconds
- **WHEN** a developer runs `npm run dev`
- **THEN** the dev server is ready in under 2 seconds
- **AND** HMR updates apply in under 100ms

#### Scenario: Production build completes in under 30 seconds
- **WHEN** a production build is triggered
- **THEN** it completes in under 30 seconds on a modern machine
- **AND** the terminal displays build time and bundle sizes

### Requirement: Dependency Management
The system SHALL manage dependencies explicitly with lockfiles and version pinning.

#### Scenario: Dependencies are locked with package-lock.json
- **WHEN** dependencies are installed
- **THEN** exact versions are recorded in `package-lock.json`
- **AND** subsequent installs use the same versions
- **AND** this ensures reproducible builds

#### Scenario: Security vulnerabilities are auditable
- **WHEN** a developer runs `npm audit`
- **THEN** it scans for known vulnerabilities
- **AND** reports severity levels
- **AND** suggests fixes with `npm audit fix`
