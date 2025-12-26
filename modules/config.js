/**
 * Centralized configuration constants for SearchScout extension
 */

// Storage constants
export const STORAGE_KEY = 'searchSites';

// Context menu constants
export const PARENT_MENU_ID = 'custom-search-parent';

// Validation constants
export const MAX_NAME_LENGTH = 50;
export const PLACEHOLDER_TOKEN = '%s';

// UI constants (imported by popup.js for validation)
export const MAX_SITES = 50; // Reasonable limit to prevent storage issues
