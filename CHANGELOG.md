# Changelog

All notable changes to SearchScout will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-12-26

### Added
- Centralized configuration module (`modules/config.js`) with shared constants
- CSS variables for theming and dimensions in popup stylesheet
- Linting configuration (`.eslintrc.json`, `.prettierrc`, `.editorconfig`)

### Changed
- Refactored storage module to use helper functions and standardize error handling
- Refactored popup UI code to eliminate duplication with `getSiteElements()` helper
- Updated all modules to import constants from centralized config
- Validation now uses config constants with dynamic error messages
- All color and dimension values now use CSS variables for easier theming

### Improved
- Code maintainability with reduced duplication across modules
- Consistent error handling patterns (all storage operations now throw errors)
- Better JSDoc documentation with error behavior documented

## [1.1.0] - 2025-12-26

### Added
- Comprehensive accessibility features for keyboard users and screen readers
- ARIA labels and roles throughout popup interface
- Keyboard navigation support (Tab, Enter, Space, Escape keys)
- Focus-visible styles for all interactive elements
- Error handling for Chrome API calls in background service worker
- Error handling for popup UI operations (toggle, drag-and-drop)
- Debouncing (300ms) for storage change listener to prevent race conditions
- Minimum Chrome version requirement (v92) in manifest

### Changed
- Info icon tooltip now accessible via keyboard focus
- Modal can be closed with Escape key
- Toggle switches have proper ARIA labels with site-specific context
- Edit/delete buttons have descriptive ARIA labels
- Empty state uses live region for screen reader announcements

### Fixed
- GitHub URL in privacy policy (searchscope → searchscout)
- Race condition in context menu creation during rapid storage changes
- Missing error callbacks in `chrome.contextMenus.create()` calls
- Missing error callback in `chrome.tabs.create()` call

## [1.0.0] - 2025-12-25

### Added
- Initial release of SearchScout Chrome extension
- Right-click context menu for searching selected text
- Smart menu behavior: single item for one site, nested menu for multiple sites
- Customizable search engines with drag-and-drop reordering
- Pre-configured default search engines (Google, DuckDuckGo, Bing, Wikipedia, GitHub, Stack Overflow, YouTube)
- Enable/disable toggle for each search site
- Add/edit/delete custom search engines
- Chrome Storage Sync for cross-device settings synchronization
- Dark mode support (follows system preferences)
- Popup interface with modern, accessible design
- Build scripts for packaging extension (bash and PowerShell)
- Privacy policy and documentation
- Chrome Web Store listing screenshots and images

### Technical
- Manifest V3 Chrome extension
- Vanilla JavaScript with ES6 modules
- Service worker for background operations
- Chrome Storage Sync API integration
- Context Menus API integration

[1.2.0]: https://github.com/ryankhart/chrome-extension-searchscout/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/ryankhart/chrome-extension-searchscout/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/ryankhart/chrome-extension-searchscout/releases/tag/v1.0.0
