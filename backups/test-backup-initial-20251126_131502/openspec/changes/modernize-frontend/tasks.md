# Implementation Tasks

## 1. Project Setup & Infrastructure
- [ ] 1.1 Initialize Vite project with React and TypeScript template
- [ ] 1.2 Install dependencies: react-router-dom, zustand, @tanstack/react-query, tailwindcss
- [ ] 1.3 Configure Tailwind CSS with custom theme colors from existing themes.css
- [ ] 1.4 Set up TypeScript with strict mode and path aliases
- [ ] 1.5 Configure ESLint with React and TypeScript presets
- [ ] 1.6 Configure Prettier for consistent code formatting
- [ ] 1.7 Set up Vite config for subdirectory base path (`/lateral-entry/`)
- [ ] 1.8 Copy static assets (JSON files, images, analytics) to `public/` directory
- [ ] 1.9 Create project structure (`src/components/`, `src/pages/`, `src/hooks/`, etc.)
- [ ] 1.10 Set up development and build npm scripts

## 2. Core Infrastructure & Utilities
- [ ] 2.1 Create API client utility with fetch wrapper and error handling
- [ ] 2.2 Implement JSON fallback logic for static deployment
- [ ] 2.3 Create base path detection utility for subdirectory deployment
- [ ] 2.4 Implement date formatting utilities (formatDate, formatNumber)
- [ ] 2.5 Create TypeScript types for entrants, batches, stats, ministries
- [ ] 2.6 Set up React Query client with default options
- [ ] 2.7 Create error boundary component for graceful error handling
- [ ] 2.8 Implement loading skeleton components

## 3. Theme System
- [ ] 3.1 Create Zustand store for theme state (regular, vintage, cyberpunk, minimalist)
- [ ] 3.2 Implement theme persistence to localStorage
- [ ] 3.3 Convert CSS custom properties to Tailwind config theme extension
- [ ] 3.4 Create ThemeProvider component to apply theme classes
- [ ] 3.5 Build ThemeSwitcher component with floating button and menu
- [ ] 3.6 Port theme-specific CSS enhancements to Tailwind @layer directives
- [ ] 3.7 Test theme switching across all themes

## 4. Layout Components
- [ ] 4.1 Create MainLayout component with Header, Footer, and outlet
- [ ] 4.2 Build Header component with logo, title, and desktop navigation
- [ ] 4.3 Build MobileNav component with fixed bottom navigation
- [ ] 4.4 Create Footer component with links and information
- [ ] 4.5 Implement PageLayout component for consistent page structure
- [ ] 4.6 Add responsive breakpoint handling for mobile/desktop views

## 5. Basic UI Components
- [ ] 5.1 Create Button component with variants (primary, secondary)
- [ ] 5.2 Build Badge components (batch badges, position badges, filter chips)
- [ ] 5.3 Create Card component with hover effects and theme support
- [ ] 5.4 Build Loading spinner component
- [ ] 5.5 Create Error message component
- [ ] 5.6 Implement Icon wrapper component for Font Awesome icons
- [ ] 5.7 Build SearchBar component with clear button and debouncing
- [ ] 5.8 Create FilterChips component with active state management

## 6. Profile Components
- [ ] 6.1 Create ProfileCard component with all profile data display
- [ ] 6.2 Implement position badge rendering logic (JS, Director, DS)
- [ ] 6.3 Build ministry/department display with conditional rendering
- [ ] 6.4 Add appointment date formatting to ProfileCard
- [ ] 6.5 Create ProfileModal component for detailed profile view
- [ ] 6.6 Implement modal open/close animations
- [ ] 6.7 Add profile link generation based on current route

## 7. Statistics & Analytics Components
- [ ] 7.1 Create StatCard component for displaying statistics
- [ ] 7.2 Build BatchCard component for batch overview display
- [ ] 7.3 Implement HeroStats component for homepage statistics
- [ ] 7.4 Create analytics chart placeholders (preserve existing PNG images)
- [ ] 7.5 Add loading states for statistics

## 8. State Management
- [ ] 8.1 Create profiles Zustand store with search, filter, and sort logic
- [ ] 8.2 Implement useProfiles custom hook with React Query
- [ ] 8.3 Create useSearch hook with debounced search input
- [ ] 8.4 Build useFilters hook for batch, position, and ministry filters
- [ ] 8.5 Implement useStats hook for statistics data
- [ ] 8.6 Create useBatch hook for batch detail data
- [ ] 8.7 Add cache invalidation and refetch logic

## 9. Routing & Navigation
- [ ] 9.1 Set up React Router with HashRouter for compatibility
- [ ] 9.2 Define routes for all pages (/, /profiles, /analytics, /history, etc.)
- [ ] 9.3 Implement route-based code splitting with React.lazy
- [ ] 9.4 Create navigation utilities (active link detection)
- [ ] 9.5 Add breadcrumb navigation for nested pages
- [ ] 9.6 Implement 404 Not Found page

## 10. Page Migration - Simple Pages
- [ ] 10.1 Migrate FAQ page to React component
- [ ] 10.2 Migrate History page with timeline component
- [ ] 10.3 Migrate Citations page with source listing
- [ ] 10.4 Migrate 2024 Cancellation page
- [ ] 10.5 Test simple pages across all themes

## 11. Page Migration - Home Page
- [ ] 11.1 Create Home page component structure
- [ ] 11.2 Build hero section with gradient background and stats
- [ ] 11.3 Implement "What is Lateral Entry" section
- [ ] 11.4 Create batches overview section with cards
- [ ] 11.5 Build recent appointments section with profile cards
- [ ] 11.6 Add call-to-action section
- [ ] 11.7 Test home page responsiveness

## 12. Page Migration - Analytics Page
- [ ] 12.1 Create Analytics page component
- [ ] 12.2 Build statistics dashboard with stat cards
- [ ] 12.3 Display existing analytics PNG images
- [ ] 12.4 Implement ministry distribution display
- [ ] 12.5 Add batch distribution visualization
- [ ] 12.6 Create position breakdown section
- [ ] 12.7 Test analytics page data loading

## 13. Page Migration - Profiles Page
- [ ] 13.1 Create Profiles page component with grid layout
- [ ] 13.2 Implement search bar integration with state
- [ ] 13.3 Build filter chips for batch, position, ministry
- [ ] 13.4 Add results count display
- [ ] 13.5 Implement profile grid with loading states
- [ ] 13.6 Add pagination or infinite scroll (if needed)
- [ ] 13.7 Create "no results" state
- [ ] 13.8 Test search and filter functionality

## 14. Page Migration - Batch Detail Pages
- [ ] 14.1 Create BatchDetail page component
- [ ] 14.2 Implement dynamic routing for batch years (2019, 2021, 2023)
- [ ] 14.3 Build batch statistics display
- [ ] 14.4 Add position distribution for batch
- [ ] 14.5 Display filtered profiles for batch
- [ ] 14.6 Test batch pages with all three years

## 15. Page Migration - Profile Detail Page
- [ ] 15.1 Create ProfileDetail page component
- [ ] 15.2 Implement dynamic routing with profile ID
- [ ] 15.3 Build detailed information sections
- [ ] 15.4 Display professional details and education
- [ ] 15.5 Add media coverage links
- [ ] 15.6 Implement back navigation
- [ ] 15.7 Test profile detail with various profiles

## 16. Production Optimization
- [ ] 16.1 Configure Vite build for production with minification
- [ ] 16.2 Set up code splitting for optimal bundle sizes
- [ ] 16.3 Implement lazy loading for routes
- [ ] 16.4 Optimize images and assets
- [ ] 16.5 Configure cache headers for static assets
- [ ] 16.6 Test production build locally with `vite preview`
- [ ] 16.7 Analyze bundle size with rollup-plugin-visualizer

## 17. Testing & Quality Assurance
- [ ] 17.1 Test all pages in Chrome, Firefox, Safari, Edge
- [ ] 17.2 Test mobile experience on iOS and Android devices
- [ ] 17.3 Verify all four themes work on every page
- [ ] 17.4 Test search functionality with various queries
- [ ] 17.5 Test filter combinations and edge cases
- [ ] 17.6 Verify navigation and routing (forward, back, refresh)
- [ ] 17.7 Test API fallback to static JSON
- [ ] 17.8 Keyboard navigation and accessibility testing
- [ ] 17.9 Test with slow network conditions (throttling)
- [ ] 17.10 Run Lighthouse audit for performance, accessibility, SEO

## 18. Documentation & Deployment
- [ ] 18.1 Update README.md with new setup instructions
- [ ] 18.2 Document npm scripts and development workflow
- [ ] 18.3 Create MIGRATION.md explaining changes
- [ ] 18.4 Document deployment process for production
- [ ] 18.5 Update AGENTS.md with new build commands
- [ ] 18.6 Create deployment package with dist/ output
- [ ] 18.7 Test deployment on staging environment
- [ ] 18.8 Deploy to production at prabhu.app/lateral-entry/
- [ ] 18.9 Archive old HTML files to backups/pre-react-migration/
- [ ] 18.10 Monitor for post-deployment issues

## 19. Post-Deployment Validation
- [ ] 19.1 Verify all routes work in production
- [ ] 19.2 Test theme persistence across sessions
- [ ] 19.3 Confirm search and filter work with production data
- [ ] 19.4 Verify mobile navigation functions correctly
- [ ] 19.5 Check console for errors or warnings
- [ ] 19.6 Confirm analytics and statistics load properly
- [ ] 19.7 Test profile detail pages with direct links
- [ ] 19.8 Verify base path handling for subdirectory deployment

## 20. Cleanup & Optimization
- [ ] 20.1 Remove unused dependencies
- [ ] 20.2 Clean up commented code and console logs
- [ ] 20.3 Optimize re-renders with React.memo where appropriate
- [ ] 20.4 Review and optimize Tailwind CSS usage
- [ ] 20.5 Document any technical debt for future work
- [ ] 20.6 Create tickets for potential improvements
- [ ] 20.7 Update project.md with new architecture details

---

## Dependencies & Sequencing

**Sequential Dependencies:**
- Tasks 1.x must complete before any other tasks (project setup)
- Tasks 2.x must complete before component development (core utilities)
- Tasks 3.x must complete before layout components (theme system)
- Tasks 4.x and 5.x must complete before page migration (layouts and UI components)
- Tasks 6.x and 7.x must complete before complex page migration (specialized components)
- Tasks 10-15 (page migration) can proceed page by page after dependencies met
- Tasks 16-18 can only start after all pages are migrated
- Tasks 19-20 are post-deployment

**Parallelizable Work:**
- Basic UI components (5.x) can be built in parallel
- Simple page migrations (10.x) can proceed independently
- Testing (17.x) can start as soon as pages are ready
- Documentation (18.1-18.5) can be written during development

**Critical Path:**
1. Project Setup → Core Infrastructure → Theme System
2. Layout Components → UI Components → Profile Components
3. State Management → Routing
4. Simple Pages → Home Page → Profiles Page → Complex Pages
5. Production Build → Testing → Deployment

**Estimated Timeline:** 25-30 working days for full migration with thorough testing
