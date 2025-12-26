// Default search engines configuration
export const DEFAULT_SEARCH_SITES = [
  {
    id: 'default-google',
    name: 'Google',
    url: 'https://www.google.com/search?q=%s',
    enabled: true,
    isDefault: true,
    order: 0
  },
  {
    id: 'default-duckduckgo',
    name: 'DuckDuckGo',
    url: 'https://duckduckgo.com/?q=%s',
    enabled: true,
    isDefault: true,
    order: 1
  },
  {
    id: 'default-bing',
    name: 'Bing',
    url: 'https://www.bing.com/search?q=%s',
    enabled: true,
    isDefault: true,
    order: 2
  },
  {
    id: 'default-wikipedia',
    name: 'Wikipedia',
    url: 'https://en.wikipedia.org/wiki/Special:Search?search=%s',
    enabled: true,
    isDefault: true,
    order: 3
  },
  {
    id: 'default-github',
    name: 'GitHub',
    url: 'https://github.com/search?q=%s&type=repositories',
    enabled: true,
    isDefault: true,
    order: 4
  },
  {
    id: 'default-stackoverflow',
    name: 'Stack Overflow',
    url: 'https://stackoverflow.com/search?q=%s',
    enabled: true,
    isDefault: true,
    order: 5
  },
  {
    id: 'default-youtube',
    name: 'YouTube',
    url: 'https://www.youtube.com/results?search_query=%s',
    enabled: true,
    isDefault: true,
    order: 6
  }
];
