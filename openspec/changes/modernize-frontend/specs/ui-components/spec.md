# UI Components Specification

## ADDED Requirements

### Requirement: Component Library
The system SHALL provide a reusable component library built with React 18 and TypeScript that encapsulates all UI patterns used across the portal.

#### Scenario: ProfileCard renders entrant data
- **WHEN** a ProfileCard component is rendered with entrant data
- **THEN** it displays name, position, ministry, department, appointment date, and batch year
- **AND** it applies the appropriate position badge styling (JS, Director, or DS)
- **AND** it conditionally hides department if it duplicates ministry information
- **AND** it generates the correct profile detail link based on current route context

#### Scenario: ThemeSwitcher allows theme selection
- **WHEN** a user clicks the ThemeSwitcher floating button
- **THEN** a menu displays with four theme options (regular, vintage, cyberpunk, minimalist)
- **AND** the current theme is highlighted as active
- **WHEN** a user selects a new theme
- **THEN** the theme changes immediately across the entire application
- **AND** the preference is persisted to localStorage

#### Scenario: SearchBar handles user input
- **WHEN** a user types in the SearchBar component
- **THEN** the input is debounced by 300ms to avoid excessive searches
- **AND** a clear button appears when text is entered
- **WHEN** the clear button is clicked
- **THEN** the input is cleared and search results reset

### Requirement: Badge System
The system SHALL provide consistent badge components for batches, positions, and categories with theme-aware styling.

#### Scenario: Batch badges display with correct colors
- **WHEN** a batch badge is rendered for year 2019
- **THEN** it displays with blue background and border
- **WHEN** a batch badge is rendered for year 2021
- **THEN** it displays with green background and border
- **WHEN** a batch badge is rendered for year 2023
- **THEN** it displays with purple background and border

#### Scenario: Position badges display with hierarchical styling
- **WHEN** a Joint Secretary position badge is rendered
- **THEN** it displays with gold gradient, diamond icon, and prominent shadow
- **WHEN** a Director position badge is rendered
- **THEN** it displays with yellow gradient, star icon, and medium shadow
- **WHEN** a Deputy Secretary position badge is rendered
- **THEN** it displays with bronze gradient, circle icon, and subtle shadow

### Requirement: Layout Components
The system SHALL provide layout components that establish consistent page structure, navigation, and responsive behavior.

#### Scenario: MainLayout renders on all pages
- **WHEN** any page is rendered
- **THEN** it is wrapped in MainLayout component
- **AND** the Header is displayed at the top with logo and navigation
- **AND** the Footer is displayed at the bottom with links
- **AND** the MobileNav is displayed on screens smaller than 768px
- **AND** the page content is rendered in the outlet area

#### Scenario: Header navigation highlights active page
- **WHEN** the user is on the Profiles page
- **THEN** the "All Profiles" link in the header is highlighted with accent color
- **WHEN** the user navigates to a different page
- **THEN** the active link updates to reflect the current page

#### Scenario: MobileNav appears on small screens
- **WHEN** the viewport width is less than 768px
- **THEN** the desktop navigation is hidden
- **AND** the MobileNav is fixed to the bottom of the screen
- **AND** it displays four navigation items (Home, Profiles, Stats, More)
- **AND** the active page is highlighted with accent color

### Requirement: Loading and Error States
The system SHALL provide loading and error components for graceful data fetching states.

#### Scenario: Loading spinner displays during data fetch
- **WHEN** data is being fetched from the API or JSON files
- **THEN** a loading spinner is displayed in the content area
- **AND** the spinner uses theme-aware colors
- **WHEN** the data finishes loading
- **THEN** the spinner is replaced with the content

#### Scenario: Error boundary catches component errors
- **WHEN** a runtime error occurs in a React component
- **THEN** the error boundary catches the error
- **AND** displays a user-friendly error message
- **AND** logs the error details to the console
- **AND** provides a button to reload the page

#### Scenario: Error message displays for failed requests
- **WHEN** an API request fails and JSON fallback also fails
- **THEN** an error message is displayed to the user
- **AND** it includes an icon and descriptive text
- **AND** it suggests possible actions (refresh, try again later)

### Requirement: Responsive Design
The system SHALL ensure all components adapt to different screen sizes and maintain usability on mobile devices.

#### Scenario: Profile cards stack on mobile
- **WHEN** viewing the profiles page on a mobile device (< 640px)
- **THEN** profile cards display in a single column
- **WHEN** viewing on tablet (640px - 1024px)
- **THEN** profile cards display in a two-column grid
- **WHEN** viewing on desktop (> 1024px)
- **THEN** profile cards display in a three-column grid

#### Scenario: Touch targets meet accessibility standards
- **WHEN** interactive elements are rendered on mobile
- **THEN** all buttons and links have minimum 44x44px touch targets
- **AND** adequate spacing prevents accidental taps

### Requirement: Accessibility
The system SHALL implement accessibility best practices for keyboard navigation, screen readers, and WCAG 2.1 AA compliance.

#### Scenario: Keyboard navigation works for all interactions
- **WHEN** a user navigates using keyboard only
- **THEN** all interactive elements are reachable via Tab key
- **AND** focused elements display visible focus indicators
- **AND** Enter or Space activates buttons and links
- **AND** Escape closes modals and menus

#### Scenario: Screen reader announces content correctly
- **WHEN** a screen reader user navigates the site
- **THEN** all images have descriptive alt text
- **AND** buttons and links have descriptive labels
- **AND** form inputs have associated labels
- **AND** page structure uses semantic HTML elements

### Requirement: Component Reusability
The system SHALL ensure components are modular, composable, and can be reused across different pages and contexts.

#### Scenario: Components accept props for customization
- **WHEN** a component is rendered with custom props
- **THEN** it applies the provided customization
- **AND** it falls back to sensible defaults when props are omitted
- **AND** TypeScript enforces correct prop types at compile time

#### Scenario: Components handle edge cases gracefully
- **WHEN** a component receives null or undefined data
- **THEN** it displays a fallback value or empty state
- **WHEN** a component receives invalid data
- **THEN** it logs a warning to the console
- **AND** displays an error state or skips rendering
