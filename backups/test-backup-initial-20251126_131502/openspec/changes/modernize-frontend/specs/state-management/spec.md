# State Management Specification

## ADDED Requirements

### Requirement: Theme State Management
The system SHALL manage theme selection state globally using Zustand and persist preferences to localStorage.

#### Scenario: Theme initializes from localStorage
- **WHEN** the application loads
- **THEN** it checks localStorage for saved theme preference
- **AND** applies the saved theme if found
- **AND** defaults to "regular" theme if no preference exists

#### Scenario: Theme changes update entire application
- **WHEN** a user selects a different theme
- **THEN** the Zustand store updates the theme state
- **AND** all components re-render with new theme classes
- **AND** the new theme is saved to localStorage
- **AND** CSS custom properties update to match the theme

#### Scenario: Theme state is accessible anywhere
- **WHEN** any component needs access to current theme
- **THEN** it can use the `useTheme` hook to read theme state
- **AND** it can call theme setter functions to update theme

### Requirement: Profiles State Management
The system SHALL manage profiles data, search queries, and filter state using Zustand stores and React Query for server state.

#### Scenario: Profiles data is fetched with React Query
- **WHEN** the profiles page is mounted
- **THEN** React Query fetches profiles data from API or JSON fallback
- **AND** the data is cached for subsequent requests
- **AND** loading state is available during fetch
- **AND** error state is available if fetch fails

#### Scenario: Search query updates filter profiles
- **WHEN** a user types in the search bar
- **THEN** the search input is debounced by 300ms
- **AND** the profiles store updates the search query
- **AND** profiles are filtered to match name, ministry, department, or position
- **AND** the UI updates to show filtered results

#### Scenario: Filter chips update profile list
- **WHEN** a user clicks a batch filter chip
- **THEN** the filters store toggles that batch filter
- **AND** profiles are filtered to include only selected batches
- **WHEN** a user clicks a position filter chip
- **THEN** profiles are filtered to match the selected position
- **WHEN** multiple filters are active
- **THEN** profiles match ALL active filters (AND logic)

#### Scenario: Clear filters resets to all profiles
- **WHEN** a user clears all filters
- **THEN** the filters store resets to default state
- **AND** all profiles are displayed
- **AND** filter chips return to inactive state

### Requirement: Statistics State Management
The system SHALL fetch and cache statistics data for efficient display across multiple pages.

#### Scenario: Stats data is fetched once and cached
- **WHEN** the application loads and any page needs statistics
- **THEN** React Query fetches statistics from API or JSON
- **AND** the data is cached globally
- **WHEN** another page needs the same statistics
- **THEN** it uses the cached data without refetching

#### Scenario: Stats data updates dynamically
- **WHEN** the statistics data is fetched
- **THEN** the home page displays total appointees, batches, ministries, positions
- **AND** the profiles page shows results count
- **AND** the analytics page displays all distribution statistics
- **AND** batch pages show batch-specific statistics

### Requirement: Custom Hooks
The system SHALL provide custom React hooks that encapsulate data fetching, filtering, and state management logic.

#### Scenario: useProfiles hook fetches and filters profiles
- **WHEN** a component calls `useProfiles` hook
- **THEN** it receives profiles data, loading state, and error state
- **AND** it can pass filters and search query as parameters
- **AND** the hook returns filtered profiles based on parameters

#### Scenario: useSearch hook provides debounced search
- **WHEN** a component calls `useSearch` hook
- **THEN** it receives current search query and setter function
- **AND** the setter debounces input by 300ms
- **AND** it returns debouncedQuery for filtering logic

#### Scenario: useFilters hook manages filter state
- **WHEN** a component calls `useFilters` hook
- **THEN** it receives active filters and toggle functions
- **AND** it can toggle batch filters, position filters, ministry filters
- **AND** it provides a clear all filters function
- **AND** it returns a count of active filters

#### Scenario: useTheme hook manages theme state
- **WHEN** a component calls `useTheme` hook
- **THEN** it receives current theme and theme setter function
- **AND** it provides helper functions like `isTheme`, `themeClass`
- **AND** it automatically handles localStorage persistence

#### Scenario: useStats hook fetches statistics
- **WHEN** a component calls `useStats` hook
- **THEN** it receives stats data from React Query
- **AND** it provides loading and error states
- **AND** it returns helper functions for accessing specific stats (by batch, ministry, position)

### Requirement: React Query Configuration
The system SHALL configure React Query with sensible defaults for caching, refetching, and error handling.

#### Scenario: Queries cache for 5 minutes
- **WHEN** data is successfully fetched
- **THEN** it is cached for 5 minutes (staleTime)
- **AND** it remains in cache for 10 minutes (cacheTime)
- **WHEN** the same query is needed within cache time
- **THEN** cached data is returned immediately

#### Scenario: Failed queries retry with backoff
- **WHEN** a query fails due to network error
- **THEN** React Query retries up to 3 times
- **AND** it uses exponential backoff between retries
- **AND** it displays loading state during retries
- **AND** it displays error state if all retries fail

#### Scenario: Background refetch keeps data fresh
- **WHEN** a user returns to a tab with stale data
- **THEN** React Query refetches in the background
- **AND** it shows the stale data while refetching
- **AND** it updates with fresh data when available

### Requirement: Optimistic Updates
The system SHALL provide optimistic UI updates where appropriate to improve perceived performance.

#### Scenario: Theme changes apply immediately
- **WHEN** a user selects a new theme
- **THEN** the UI updates instantly without waiting
- **AND** the state is persisted asynchronously to localStorage

#### Scenario: Filter changes update UI immediately
- **WHEN** a user clicks a filter chip
- **THEN** the filter activates instantly
- **AND** profiles re-filter synchronously
- **AND** the UI reflects the new filtered state immediately

### Requirement: State Persistence
The system SHALL persist relevant user preferences to localStorage for continuity across sessions.

#### Scenario: Theme preference persists across sessions
- **WHEN** a user selects a theme and closes the browser
- **AND** later reopens the portal
- **THEN** the selected theme is restored from localStorage

#### Scenario: Invalid persisted state is handled gracefully
- **WHEN** localStorage contains corrupted or invalid data
- **THEN** the application defaults to safe initial state
- **AND** it logs a warning to the console
- **AND** it overwrites the invalid data with valid defaults

### Requirement: Type Safety
The system SHALL use TypeScript for all state management logic to ensure type safety and prevent runtime errors.

#### Scenario: Zustand stores are fully typed
- **WHEN** a store is created with Zustand
- **THEN** all state properties have explicit TypeScript types
- **AND** all actions have typed parameters and return values
- **AND** TypeScript enforces correct usage at compile time

#### Scenario: React Query hooks are typed
- **WHEN** a React Query hook is used
- **THEN** the returned data has the correct TypeScript type
- **AND** TypeScript enforces correct query key usage
- **AND** mutation variables are type-checked
