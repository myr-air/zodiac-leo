/**
 * Suno Mellow Copilot - Service Worker (background.js)
 * Enables side panel opening on extension action click
 */

chrome.sidePanel
  .setPanelBehavior({ openPanelOnActionClick: true })
  .catch((error) => console.error("Error setting panel behavior:", error));

// Optional: monitor tab updates to alert active state changes in the side panel
chrome.tabs.onActivated.addListener(async (activeInfo) => {
  try {
    // Send message to side panel if it's open to refresh its tab validation status
    await chrome.runtime.sendMessage({ action: "tabChanged", tabId: activeInfo.tabId });
  } catch (err) {
    // Silently ignore if side panel is not open
  }
});
