# Custom Search Chrome Extension

A Chrome extension that adds a right-click context menu to search selected text across multiple customizable search engines.

## Features

- **Right-click search**: Select any text on a webpage and search it instantly
- **Multiple search engines**: Choose from a submenu of search sites
- **Flat menu mode**: Optional setting to show each site as a top-level context menu item (disabled by default)
- **Pre-configured defaults**: Google, DuckDuckGo, Bing, Wikipedia, GitHub, Stack Overflow, YouTube
- **Fully customizable**: Add your own search sites with `%s` placeholder for search terms
- **Enable/disable sites**: Toggle visibility of any search engine
- **Drag-and-drop reordering**: Arrange search sites in your preferred order
- **Cross-device sync**: Settings sync across your Chrome browsers

## Installation

1. Download or clone this repository
2. Open Chrome and navigate to `chrome://extensions/`
3. Enable "Developer mode" in the top right corner
4. Click "Load unpacked"
5. Select the extension folder

## Usage

### Searching

1. Select any text on a webpage
2. Right-click to open the context menu
3. Hover over "Search for [selected text]"
4. Click on your preferred search engine

### Managing Search Sites

1. Click the extension icon in the toolbar
2. From the popup, you can:
   - **Flat menu**: Toggle to show each site as a top-level menu item (instead of nested submenu)
   - **Add**: Click the + button to add a new search site
   - **Edit**: Click the pencil icon to modify a site
   - **Delete**: Click the X icon to remove custom sites (defaults cannot be deleted)
   - **Toggle**: Use the switch to enable/disable a site
   - **Reorder**: Drag and drop sites to change their order

### Menu Modes

- **Nested (default)**: All search sites appear under a single "Search for..." submenu
- **Flat**: Each search site appears as a top-level menu item like "Search Google for..."

Toggle between modes using the "Flat menu" switch in the popup.

### Adding Custom Search Sites

When adding a new search site, you need:

- **Name**: A display name for the context menu (e.g., "Reddit")
- **URL**: The search URL with `%s` as placeholder for the search term

Example URLs:
- Reddit: `https://www.reddit.com/search/?q=%s`
- Amazon: `https://www.amazon.com/s?k=%s`
- MDN: `https://developer.mozilla.org/en-US/search?q=%s`

## Development

### Project Structure

```
chrome-extension-searchscope/
├── manifest.json          # Extension configuration
├── background.js          # Service worker for context menus
├── popup/
│   ├── popup.html         # Popup UI
│   ├── popup.css          # Popup styling
│   └── popup.js           # Popup logic
├── modules/
│   ├── storage.js         # Storage abstraction
│   └── defaults.js        # Default search engines
└── icons/                 # Extension icons
```

### Technologies

- Manifest V3
- Chrome Storage Sync API
- Chrome Context Menus API
- ES6 Modules

## License

MIT
