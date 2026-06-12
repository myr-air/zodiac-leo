/**
 * Suno Mellow Copilot - Injected Content Script
 * Resiliently targets and fills the React-based form on suno.com
 */

console.log("[Suno Mellow Copilot] Content script loaded and active.");

// Bulletproof value setter for React 16+ controlled inputs
function setReactValue(element, value) {
  if (!element) return false;

  try {
    const lastValue = element.value;
    element.value = value;

    // React 16+ value tracker override
    const tracker = element._valueTracker;
    if (tracker) {
      tracker.setValue(lastValue);
    }

    // Dispatch input event to notify React state
    const event = new Event('input', { bubbles: true });
    element.dispatchEvent(event);

    // Also dispatch change event just in case
    const changeEvent = new Event('change', { bubbles: true });
    element.dispatchEvent(changeEvent);

    return true;
  } catch (error) {
    console.error("[Suno Mellow Copilot] Failed to set value:", error);
    return false;
  }
}

// Get depth of an element in DOM tree to find the innermost leaf node
function getDepth(el) {
  let depth = 0;
  while (el.parentElement) {
    depth++;
    el = el.parentElement;
  }
  return depth;
}

// Simulates hovering on an element by dispatching pointer/mouse enter & over events
function simulateHover(element) {
  if (!element) return;
  try {
    element.dispatchEvent(new PointerEvent('pointerenter', { bubbles: true, cancelable: true, view: window }));
    element.dispatchEvent(new PointerEvent('pointerover', { bubbles: true, cancelable: true, view: window }));
    element.dispatchEvent(new MouseEvent('mouseenter', { bubbles: true, cancelable: true, view: window }));
    element.dispatchEvent(new MouseEvent('mouseover', { bubbles: true, cancelable: true, view: window }));
  } catch (err) {
    console.error("[Suno Mellow Copilot] Hover simulation failed:", err);
  }
}

// Bulletproof click simulator for React and complex web applications
function simulateClick(element) {
  if (!element) return;
  try {
    element.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true, cancelable: true, view: window }));
    element.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, cancelable: true, view: window }));
    element.dispatchEvent(new PointerEvent('pointerup', { bubbles: true, cancelable: true, view: window }));
    element.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, cancelable: true, view: window }));
    element.click();
  } catch (err) {
    console.error("[Suno Mellow Copilot] Failed to simulate click:", err);
    element.click(); // Fallback
  }
}

// Polls for a condition/element to support slow rendering states
function pollForElement(selectorFn, callback, timeoutMs = 1500, intervalMs = 50) {
  const startTime = Date.now();

  function check() {
    const element = selectorFn();
    if (element) {
      callback(element);
      return;
    }

    if (Date.now() - startTime < timeoutMs) {
      setTimeout(check, intervalMs);
    } else {
      callback(null); // Timeout
    }
  }

  check();
}

// Find absolute deepest visible element containing a specific text, avoiding background/row elements
// exactMatch=true: text must equal pattern exactly (prevents 'wav' matching 'waveform')
function findDropdownOption(textPattern, exactMatch = false) {
  // Prefer searching within context menu items for precision
  const menuSelectors = '.context-menu-item button, .context-menu-item span, [role="menuitem"], [role="menu"] button, [role="menu"] span';
  const allElements = Array.from(document.querySelectorAll(menuSelectors + ', div, span, button, p, li, a'));
  const patternLower = textPattern.toLowerCase();

  const candidateItems = allElements.filter(el => {
    // Exclude elements inside the song rows to avoid clicking main table
    if (el.closest('.clip-row') || el.closest('[data-testid="clip-row"]') || el.closest('[draggable="true"].e1vhawg90')) return false;

    // Ensure element is visible
    const rect = el.getBoundingClientRect();
    if (rect.width === 0 || rect.height === 0) return false;

    const text = el.textContent?.trim().toLowerCase() || '';
    if (exactMatch) {
      return text === patternLower;
    }
    return text === patternLower || text.includes(patternLower);
  });

  if (candidateItems.length === 0) return null;

  // Sort by depth (deepest/innermost first) so we click the leaf text node/span
  candidateItems.sort((a, b) => {
    const aDepth = getDepth(a);
    const bDepth = getDepth(b);
    return bDepth - aDepth;
  });

  return candidateItems[0];
}

// Waits dynamically for the download modal to open, process, download, and close successfully
function waitForModalToClose(callback, maxWaitMs = 35000) {
  const startTime = Date.now();
  let modalFound = false;

  function check() {
    if (!isBatchDownloading) return; // Stopped by user

    const dialog = document.querySelector('div[role="dialog"]');

    if (dialog) {
      modalFound = true;
      // We are still waiting for it to close
      if (Date.now() - startTime < maxWaitMs) {
        setTimeout(check, 100);
      } else {
        console.warn("[Suno Mellow Copilot] Modal close timeout reached.");
        callback();
      }
    } else {
      if (modalFound) {
        // Modal was found and has now closed!
        console.log("[Suno Mellow Copilot] Download modal closed successfully.");
        // Wait an additional 500ms for browser to settle before proceeding
        setTimeout(callback, 500);
      } else {
        // Modal hasn't appeared yet
        if (Date.now() - startTime < 8000) { // Wait up to 8s for modal to appear
          setTimeout(check, 100);
        } else {
          console.warn("[Suno Mellow Copilot] Download modal never appeared.");
          callback();
        }
      }
    }
  }

  check();
}

// Activates Advanced tab if not already active
function activateAdvancedMode() {
  const advancedTab = document.querySelector('button[role="tab"][aria-label="Advanced"]');
  if (advancedTab) {
    const isSelected = advancedTab.getAttribute('aria-selected') === 'true' ||
                        advancedTab.classList.contains('active');

    if (!isSelected) {
      advancedTab.click();
      console.log("[Suno Mellow Copilot] Activated Advanced Tab.");
      return true; // We triggered a toggle click
    }
  }
  return false;
}

// Expands More Options panel if collapsed
function expandMoreOptions() {
  const labels = Array.from(document.querySelectorAll('div, span, button'));
  const moreOptionsTextEl = labels.find(el => el.textContent?.trim() === "More Options");

  if (moreOptionsTextEl) {
    const toggleBtn = moreOptionsTextEl.closest('[role="button"]') ||
                      moreOptionsTextEl.closest('.e1b3zbcs1') ||
                      moreOptionsTextEl.parentElement?.parentElement;

    if (toggleBtn) {
      const isExpanded = toggleBtn.getAttribute('aria-expanded') === 'true';
      if (!isExpanded) {
        toggleBtn.click();
        console.log("[Suno Mellow Copilot] Expanded More Options panel.");
        return true; // We triggered a toggle click
      }
    }
  }
  return false;
}

// Selects options from a labelled row of buttons (e.g., Vocal Gender, Lyrics Mode)
function selectOptionRow(label, desiredValue) {
  const span = Array.from(document.querySelectorAll('span')).find(el => el.textContent?.trim().toLowerCase() === label.toLowerCase());
  if (span) {
    const container = span.closest('.css-1b650h0') || span.parentElement?.parentElement;
    if (container) {
      const btn = Array.from(container.querySelectorAll('button')).find(b => b.textContent?.trim().toLowerCase() === desiredValue.toLowerCase());
      if (btn && btn.getAttribute('data-selected') === 'false') {
        btn.click();
        console.log(`[Suno Mellow Copilot] Clicked ${label} button: ${desiredValue}`);
        return true;
      }
    }
  }
  return false;
}

// Sets slider value (Weirdness & Style Influence) by double-clicking the text to trigger raw input editing
function setSliderValue(label, targetVal) {
  const cleanTarget = String(targetVal).replace('%', '').trim();
  const labelSpan = Array.from(document.querySelectorAll('span')).find(el => el.textContent?.trim().toLowerCase() === label.toLowerCase());

  if (labelSpan) {
    const container = labelSpan.closest('.css-1b650h0') || labelSpan.parentElement?.parentElement;
    if (container) {
      // Find the value label div (usually contains '%' or class 'css-zxcoun')
      const valueDiv = container.querySelector('.css-zxcoun') ||
                       Array.from(container.querySelectorAll('div')).find(d => d.textContent?.includes('%'));

      if (valueDiv) {
        // 1. Simulate double click to turn it into an input box
        valueDiv.dispatchEvent(new MouseEvent('dblclick', { bubbles: true, cancelable: true }));
        console.log(`[Suno Mellow Copilot] Double-clicked value label for ${label}.`);

        // 2. Wait a tiny bit for React to replace the label with the input element
        setTimeout(() => {
          const input = container.querySelector('input[type="text"]') ||
                        container.querySelector('input') ||
                        container.querySelector('.css-1in9m1f');

          if (input) {
            // Set input value
            setReactValue(input, cleanTarget);

            // Dispatch Enter key event to commit the value changes
            input.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true }));
            input.dispatchEvent(new KeyboardEvent('keyup', { key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true }));

            // Trigger blur to save
            input.blur();
            console.log(`[Suno Mellow Copilot] Successfully set ${label} to ${cleanTarget}% via double-click text input!`);
          } else {
            console.warn(`[Suno Mellow Copilot] Input element not found under ${label} container after double-click. Trying keyboard fallback...`);
            runKeyboardFallback(label, cleanTarget);
          }
        }, 80);
        return true;
      }
    }
  }

  // If double-click path is completely unavailable, trigger the keyboard navigation fallback
  return runKeyboardFallback(label, cleanTarget);
}

// Fallback slider keypress adjuster
function runKeyboardFallback(label, targetNum) {
  const slider = document.querySelector(`[role="slider"][aria-label="${label}" i]`);
  if (!slider) return false;

  let currentVal = parseInt(slider.getAttribute('aria-valuenow'));
  if (isNaN(currentVal)) {
    const textSibling = slider.parentElement?.querySelector('.css-zxcoun');
    if (textSibling) currentVal = parseInt(textSibling.textContent);
  }
  if (isNaN(currentVal)) currentVal = 50;

  const target = parseInt(targetNum);
  if (isNaN(target)) return false;

  const key = currentVal > target ? 'ArrowLeft' : 'ArrowRight';
  const steps = Math.abs(currentVal - target);

  for (let i = 0; i < steps; i++) {
    slider.dispatchEvent(new KeyboardEvent('keydown', { key: key, bubbles: true }));
  }
  console.log(`[Suno Mellow Copilot] Keyboard fallback: Adjusted slider "${label}" to ${target}%`);
  return true;
}

// Find the active Create/Generate button in suno form
function findCreateButton() {
  const explicitCandidates = [
    document.querySelector('button[type="button"][aria-label*="Create" i]'),
    document.querySelector('button[type="submit"][aria-label*="Create" i]'),
    document.querySelector('button[type="button"][aria-label*="Generate" i]'),
    document.querySelector('button[type="submit"][aria-label*="Generate" i]')
  ].filter(Boolean);

  if (explicitCandidates.length > 0) {
    return explicitCandidates[0];
  }

  const textCandidates = Array.from(document.querySelectorAll('button')).filter(btn => {
    const txt = (btn.textContent || '').toLowerCase();
    const aria = (btn.getAttribute('aria-label') || '').toLowerCase();
    return txt.includes('create') || txt.includes('generate') || aria.includes('create') || aria.includes('generate');
  });

  return textCandidates[0] || null;
}

function isCreateButtonLoading(button) {
  if (!button) return true;
  if (button.disabled || button.hasAttribute('disabled')) return true;

  const text = (button.textContent || '').toLowerCase();
  const aria = (button.getAttribute('aria-label') || '').toLowerCase();
  const className = (button.className || '').toLowerCase();

  if (aria === 'true' || button.getAttribute('aria-busy') === 'true') return true;

  if (text.includes('loading') || text.includes('processing') || text.includes('generating') || text.includes('please wait')) {
    return true;
  }

  if (aria.includes('loading') || aria.includes('processing') || aria.includes('generating') || aria.includes('please wait')) {
    return true;
  }

  if (className.includes('loading') || className.includes('spinner') || className.includes('progress')) {
    return true;
  }

  return Boolean(
    button.querySelector('[role="progressbar"], .spinner, [class*="spinner"], [class*="loading"]') ||
    button.querySelector('svg[data-testid*="spinner" i]')
  );
}

function notifyCreateTimeout(trackTitle = '', timeoutMs = 30000) {
  try {
    chrome.runtime.sendMessage({
      action: "createTimeout",
      reason: `Create button stayed in loading state for ${timeoutMs}ms`,
      trackTitle
    });
  } catch (err) {
    console.error("[Suno Mellow Copilot] Failed to notify create timeout:", err);
  }
}

function clickCreateButtonWithRetry(data, attempt = 1, maxAttempts = 3) {
  const timeoutMs = 30000;
  const pollDelayMs = 250;
  const startTs = Date.now();

  const retry = () => {
    const submitBtn = findCreateButton();

    if (!submitBtn) {
      if (attempt < maxAttempts) {
        console.warn(`[Suno Mellow Copilot] Create button not found. Retry ${attempt}/${maxAttempts}...`);
        setTimeout(() => clickCreateButtonWithRetry(data, attempt + 1, maxAttempts), 500);
      } else {
        console.error("[Suno Mellow Copilot] Create button not found after retries.");
        notifyCreateTimeout(data?.title || '', timeoutMs);
      }
      return;
    }

    if (isCreateButtonLoading(submitBtn)) {
      if (Date.now() - startTs < timeoutMs) {
        setTimeout(retry, pollDelayMs);
        return;
      }

      console.warn(`[Suno Mellow Copilot] Create button stuck loading after ${timeoutMs}ms (attempt ${attempt}/${maxAttempts}).`);
      if (attempt < maxAttempts) {
        setTimeout(() => clickCreateButtonWithRetry(data, attempt + 1, maxAttempts), 600);
      } else {
        notifyCreateTimeout(data?.title || '', timeoutMs);
      }
      return;
    }

    simulateClick(submitBtn);
    console.log("[Suno Mellow Copilot] Clicked Create/Generate button successfully.");
  };

  retry();
}

// Find input elements on the page using precise selectors from DOM dump
function findFormFields() {
  const fields = {
    title: null,
    lyrics: null,
    styles: null,
    exclude: null,
    submit: null
  };

  // 1. Title Input
  fields.title = document.querySelector('input[placeholder*="Song Title" i]') ||
                 document.querySelector('input[placeholder*="Optional" i]') ||
                 document.querySelector('input[name="title"]');

  // 2. Lyrics Textarea
  fields.lyrics = document.querySelector('textarea[data-testid="lyrics-textarea"]') ||
                  document.querySelector('textarea[placeholder*="lyrics" i]');

  // 3. Styles Textarea
  fields.styles = document.querySelector('[data-testid="create-form-styles-wrapper"] textarea') ||
                  document.querySelector('textarea[placeholder*="drift-phonk" i]') ||
                  document.querySelector('textarea[placeholder*="styles" i]');

  // 4. Exclude Styles Input
  fields.exclude = document.querySelector('input[placeholder*="Exclude styles" i]');

  return fields;
}

// Main function to fill the form with retries to handle DOM rendering delays
function fillSunoForm(data, attemptsRemaining = 5) {
  console.log(`[Suno Mellow Copilot] Filling form. Attempts remaining: ${attemptsRemaining}`);

  // Ensure Advanced tab and More Options are active
  const toggledAdvanced = activateAdvancedMode();
  const toggledMoreOptions = expandMoreOptions();

  // Wait brief moment for DOM render if tab or panel was toggled
  const delay = (toggledAdvanced || toggledMoreOptions) ? 250 : 50;

  setTimeout(() => {
    const fields = findFormFields();

    let filledLyrics = false;
    let filledStyles = false;
    let filledTitle = false;
    let filledExclude = false;

    // 1. Fill basic input values
    if (fields.lyrics && data.lyrics) {
      filledLyrics = setReactValue(fields.lyrics, data.lyrics);
    }
    if (fields.styles && data.styles) {
      filledStyles = setReactValue(fields.styles, data.styles);
    }
    if (fields.title && data.title) {
      filledTitle = setReactValue(fields.title, data.title);
    }
    if (fields.exclude && data.exclude) {
      filledExclude = setReactValue(fields.exclude, data.exclude);
    }

    // 2. Click Option rows
    selectOptionRow('Vocal Gender', data.vocalGender || 'Female');
    selectOptionRow('Lyrics Mode', 'Manual');

    // 3. Adjust Sliders
    if (data.weirdness) {
      setSliderValue('Weirdness', data.weirdness);
    }
    if (data.influence) {
      setSliderValue('Style Influence', data.influence);
    }

    console.log("[Suno Mellow Copilot] Fill status:", {
      lyrics: filledLyrics,
      styles: filledStyles,
      title: filledTitle,
      exclude: filledExclude
    });

    // If not all fields are found or filled, and we have attempts left, retry!
    if ((!filledLyrics || !filledStyles || !filledTitle) && attemptsRemaining > 1) {
      fillSunoForm(data, attemptsRemaining - 1);
    } else {
      // Done. Add highlight visual cue to the filled fields to wow the user!
      [fields.lyrics, fields.styles, fields.title, fields.exclude].forEach(el => {
        if (el) {
          const originalBorder = el.style.borderColor;
          const originalTransition = el.style.transition;
          el.style.transition = 'all 0.5s ease';
          el.style.borderColor = '#ff7b54';
          el.style.boxShadow = '0 0 12px rgba(255, 123, 84, 0.4)';

          setTimeout(() => {
            el.style.borderColor = originalBorder;
            el.style.boxShadow = '';
            el.style.transition = originalTransition;
          }, 2000);
        }
      });

      // Auto-click Create button if specified
      if (data.autoClickCreate) {
        setTimeout(() => {
          clickCreateButtonWithRetry(data);
        }, 800); // 800ms delay to let React fully commit value states
      }
    }
  }, delay);

  return { success: true };
}

// Message Listener
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "ping") {
    sendResponse({ status: "ready" });
    return true;
  }

  if (request.action === "fillForm") {
    const result = fillSunoForm(request.data);
    sendResponse(result);
    return true;
  }

  if (request.action === "startBatchDownload") {
    activeEpisodeId = request.episodeId;
    const result = startBatchDownload();
    sendResponse(result);
    return true;
  }

  if (request.action === "stopBatchDownload") {
    stopBatchDownload();
    sendResponse({ success: true });
    return true;
  }
});

// =======================================================
// 8. Automated WAV Modal Detector & Clicker
// =======================================================

function watchAndAutoDownloadModal() {
  // 1. Direct search for any button containing "download file" (case-insensitive)
  const allButtons = Array.from(document.querySelectorAll('button'));
  let downloadBtn = allButtons.find(btn => {
    const text = btn.textContent?.trim().toLowerCase() || '';
    return text === 'download file' || text.includes('download file') ||
           (text.includes('download') && text.includes('file'));
  });

  // 2. Fallback: If not found, look inside any active dialog for a button containing "download"
  if (!downloadBtn) {
    const dialog = document.querySelector('div[role="dialog"]') ||
                   document.querySelector('div[class*="modal" i]') ||
                   document.querySelector('div[class*="dialog" i]') ||
                   document.querySelector('[data-state="open"]');
    if (dialog && !dialog.hasAttribute('data-copilot-processed')) {
      const dialogTextElements = Array.from(dialog.querySelectorAll('h1, h2, h3, h4, span, div, p'));
      const isDownloadWavModal = dialogTextElements.some(el => {
        const text = el.textContent?.trim().toLowerCase() || '';
        return text.includes('download') || text.includes('wav') || text.includes('audio') || text.includes('export');
      });

      if (isDownloadWavModal) {
        downloadBtn = Array.from(dialog.querySelectorAll('button')).find(btn => {
          const text = btn.textContent?.toLowerCase() || '';
          return text.includes('download') || text.includes('file') || text.includes('wav');
        });
      }
    }
  }

  if (downloadBtn) {
    // Check if we already clicked this exact button
    if (downloadBtn.hasAttribute('data-copilot-clicked')) return;

    // Check if the button is currently active (not disabled)
    if (!downloadBtn.disabled && !downloadBtn.hasAttribute('disabled')) {
      // Mark as clicked immediately to prevent duplicate triggers
      downloadBtn.setAttribute('data-copilot-clicked', 'true');

      console.log("[Suno Mellow Copilot] Found active download button! Simulating click...");
      simulateClick(downloadBtn);

      // Look for parent dialog to mark as processed if possible
      const parentDialog = downloadBtn.closest('div[role="dialog"]') ||
                           downloadBtn.closest('div[class*="modal" i]') ||
                           downloadBtn.closest('div[class*="dialog" i]') ||
                           downloadBtn.closest('[data-state="open"]');
      if (parentDialog) {
        parentDialog.setAttribute('data-copilot-processed', 'true');
      }

      // Wait 4.0s for the browser to initialize the download stream, then auto-close the modal!
      setTimeout(() => {
        // Try finding the close button inside the same modal/dialog first
        let closeBtn = null;
        if (parentDialog) {
          closeBtn = parentDialog.querySelector('button[aria-label="Close" i]') ||
                     parentDialog.querySelector('button[class*="close" i]') ||
                     Array.from(parentDialog.querySelectorAll('button')).find(btn => {
                       const label = (btn.getAttribute('aria-label') || btn.textContent || '').toLowerCase();
                       return label.includes('close') || label.includes('dismiss') || label.includes('x');
                     });
        }

        // Fallback to global search for close button
        if (!closeBtn) {
          closeBtn = document.querySelector('button[aria-label="Close" i]') ||
                     document.querySelector('button[class*="close" i]') ||
                     Array.from(document.querySelectorAll('button')).find(btn => {
                       const label = (btn.getAttribute('aria-label') || btn.textContent || '').toLowerCase();
                       return label.includes('close') || label.includes('dismiss') || label.includes('x');
                     });
        }

        if (closeBtn) {
          simulateClick(closeBtn);
          console.log("[Suno Mellow Copilot] Auto-closed download modal.");
        }
      }, 20000);
    } else {
      console.log("[Suno Mellow Copilot] Download button found, but it is currently disabled/loading. Waiting...");
    }
  }
}

// Continuously check for the download modal every 400ms for instant reaction
setInterval(watchAndAutoDownloadModal, 400);

// =======================================================
// 9. Batch Download Automation Loop
// =======================================================

// Returns the clip row selector string (supports old and new Suno UI)
function getClipRowSelector() {
  return '[data-testid="clip-row"], .clip-row, [draggable="true"].e1vhawg90';
}

function findThreeDotButtons() {
  // Query all actual song rows on the page to restrict the scope
  const rows = Array.from(document.querySelectorAll(getClipRowSelector()));

  const buttons = [];
  rows.forEach(row => {
    // 1. Try explicit three-dot menu selectors (works for both old and new Suno UI)
    let btn = row.querySelector('button[data-context-menu-trigger="true"]') ||
              row.querySelector('button[aria-label="More options"]') ||
              row.querySelector('button[aria-haspopup="menu"]') ||
              row.querySelector('button.context-menu-button') ||
              row.querySelector('[data-testid="more-options-button"]') ||
              row.querySelector('[aria-label*="more option" i]');

    // 2. If not found, look at all button-like elements inside the row and filter out known non-menu elements
    if (!btn) {
      const candidates = Array.from(row.querySelectorAll('button, [role="button"], [tabindex="0"]'));
      btn = candidates.find(el => {
        const label = (el.getAttribute('aria-label') || el.textContent || el.className || '').toLowerCase();

        // Skip obvious other controls
        if (label.includes('play') || label.includes('pause') ||
            label.includes('like') || label.includes('dislike') ||
            label.includes('heart') || label.includes('share') ||
            label.includes('select') || label.includes('deselect') ||
            label.includes('pin') || label.includes('edit') ||
            label.includes('remix') || label.includes('publish')) {
          return false;
        }

        // Check if it has menu traits
        const hasMenuAttr = el.hasAttribute('aria-haspopup') || el.hasAttribute('data-context-menu-trigger');
        const hasMenuClass = el.className.toLowerCase().includes('menu') || el.className.toLowerCase().includes('more');
        const hasMenuLabel = label.includes('more') || label.includes('option');

        return hasMenuAttr || hasMenuClass || hasMenuLabel;
      });
    }

    // 3. Fallback: take the last button in the row that isn't Play/Like/Dislike/Share/Select/Remix/Publish
    if (!btn) {
      const allRowButtons = Array.from(row.querySelectorAll('button'));
      // Take the LAST button — which is typically "More options" (⋯)
      const filtered = allRowButtons.filter(b => {
        const label = (b.getAttribute('aria-label') || '').toLowerCase();
        return !label.includes('play') && !label.includes('like') &&
               !label.includes('dislike') && !label.includes('share') &&
               !label.includes('select') && !label.includes('pin') &&
               !label.includes('edit') && !label.includes('remix') &&
               !label.includes('publish');
      });
      btn = filtered[filtered.length - 1] || null;
    }

    if (btn) {
      buttons.push(btn);
    }
  });

  console.log(`[Suno Mellow Copilot] Found ${buttons.length} context menu buttons inside song rows.`);
  return buttons;
}

let isBatchDownloading = false;
let batchTimerId = null;
let downloadedClipIds = new Set();
let currentSongRetries = 0;
let activeEpisodeId = null;

function getClipIdFromRow(row) {
  if (!row) return null;

  // 1. Try to find a link with a clip/song UUID in href (most reliable)
  const links = Array.from(row.querySelectorAll('a'));
  for (const a of links) {
    const href = a.getAttribute('href') || '';
    const match = href.match(/\/(?:clip|song)\/([a-f0-9-]{36})/i);
    if (match) return match[1];
  }

  // 2. Try data-clip-id attribute on the row element itself
  const idAttr = row.getAttribute('data-clip-id') || row.getAttribute('id');
  if (idAttr) {
    const match = idAttr.match(/([a-f0-9-]{36})/i);
    if (match) return match[1];
  }

  // 3. Use the More options button's data-button-id — unique per button per clip
  // (Suno uses base-ui IDs like _r_3vq_ which are unique for each rendered element)
  const moreBtn = row.querySelector('button[data-context-menu-trigger="true"][data-button-id]');
  if (moreBtn) {
    const btnId = moreBtn.getAttribute('data-button-id') || moreBtn.getAttribute('id') || '';
    if (btnId) return 'btn:' + btnId;
  }

  // 4. Use the play button's aria-label + ALL image UUIDs in the row joined
  // (join ALL UUIDs found in the row so both variations get unique combined IDs)
  const rowHtml = row.innerHTML;
  const allUuids = [...rowHtml.matchAll(/([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/gi)];
  if (allUuids.length > 0) {
    // Use the FIRST image UUID that appears (image src, not data-src, to be more specific)
    const imgSrcMatch = rowHtml.match(/src="[^"]*\/image_([a-f0-9-]{36})[^"]*"/i);
    const baseId = imgSrcMatch ? imgSrcMatch[1] : allUuids[0][1];

    // Make the ID unique by appending the occurrence index of this baseId in the current list of rows
    const allRows = Array.from(document.querySelectorAll(getClipRowSelector()));
    const matchingRows = allRows.filter(r => r.innerHTML.includes(baseId));
    const occurrenceIndex = matchingRows.indexOf(row);
    return occurrenceIndex >= 0 ? `${baseId}_occ:${occurrenceIndex}` : baseId;
  }

  // 5. Last resort: use DOM position index combined with page number (always unique, never collides)
  const pageNum = getCurrentPageNumber() || 1;
  const allRows = Array.from(document.querySelectorAll(getClipRowSelector()));
  const idx = allRows.indexOf(row);
  return idx >= 0 ? `p${pageNum}_idx:${idx}` : null;
}

function autoScanAndLoadAllClips(callback) {
  console.log("[Suno Mellow Copilot] Starting active scroll-scan to load all clips...");
  const scroller = document.querySelector('.clip-browser-list-scroller') ||
                   document.querySelector('[class*="scroller"]') ||
                   window;

  let lastClipCount = 0;
  let stableAttempts = 0;

  function scrollStep() {
    if (!isBatchDownloading) return; // Stopped by user

    const rows = document.querySelectorAll(getClipRowSelector());
    const currentCount = rows.length;
    console.log(`[Suno Mellow Copilot] Scanner found ${currentCount} clips in DOM.`);

    if (currentCount === lastClipCount) {
      stableAttempts++;
    } else {
      stableAttempts = 0;
      lastClipCount = currentCount;
    }

    // If it has been stable (no new clips loaded) for 3 consecutive checks, we are at the bottom!
    if (stableAttempts >= 3 || currentCount >= 60) { // Safety limit of 60 tracks
      console.log(`[Suno Mellow Copilot] Scan complete! Loaded ${currentCount} clips in total.`);
      // Scroll back to the top of the container instantly
      if (scroller === window) {
        window.scrollTo({ top: 0, behavior: 'auto' });
      } else {
        scroller.scrollTop = 0;
      }

      // Wait 500ms for layout to settle, then run callback
      setTimeout(callback, 500);
      return;
    }

    // Scroll to the bottom of the scroller
    if (scroller === window) {
      window.scrollTo(0, document.body.scrollHeight);
    } else {
      scroller.scrollTop = scroller.scrollHeight;
    }

    // Wait 600ms for network/React lazy rendering before next check
    setTimeout(scrollStep, 600);
  }

  scrollStep();
}

function getNextPageButton() {
  const nextBtn = document.querySelector('button[aria-label="Next page"]');
  if (nextBtn && !nextBtn.disabled && !nextBtn.hasAttribute('disabled')) {
    return nextBtn;
  }
  return null;
}

function getCurrentPageNumber() {
  const input = document.querySelector('input[aria-label="Current page number"]') ||
                document.querySelector('input[aria-label*="page" i]') ||
                document.querySelector('input[type="number"]');
  if (input) {
    const val = parseInt(input.value);
    if (!isNaN(val)) return val;
  }

  // Try finding any active page button or text
  const paginationContainer = document.querySelector('.pagination') ||
                                document.querySelector('[class*="pagination" i]');
  if (paginationContainer) {
    const activeBtn = paginationContainer.querySelector('[class*="active" i], [class*="selected" i]');
    if (activeBtn) {
      const val = parseInt(activeBtn.textContent);
      if (!isNaN(val)) return val;
    }
  }

  return null;
}

function getVisibleClipIds() {
  const rows = Array.from(document.querySelectorAll(getClipRowSelector()));
  return rows.map(row => getClipIdFromRow(row)).filter(Boolean);
}

function isSameClipList(arr1, arr2) {
  if (arr1.length !== arr2.length) return false;
  for (let i = 0; i < arr1.length; i++) {
    if (arr1[i] !== arr2[i]) return false;
  }
  return true;
}

function goToFirstPage(callback) {
  const prevBtn = document.querySelector('button[aria-label="Previous page"]');
  if (prevBtn && !prevBtn.disabled && !prevBtn.hasAttribute('disabled')) {
    console.log("[Suno Mellow Copilot] Not on Page 1. Navigating to previous page...");
    simulateClick(prevBtn);
    setTimeout(() => {
      goToFirstPage(callback);
    }, 1500);
  } else {
    console.log("[Suno Mellow Copilot] Arrived at Page 1.");
    callback();
  }
}

function stopBatchDownload() {
  isBatchDownloading = false;
  if (batchTimerId) {
    clearTimeout(batchTimerId);
    batchTimerId = null;
  }
  console.log("[Suno Mellow Copilot] Batch download stopped.");
}

function startBatchDownload() {
  if (isBatchDownloading) return { success: false, message: "Already running" };

  isBatchDownloading = true;
  console.log("[Suno Mellow Copilot] Starting batch download with auto-scanner and page tracker...");

  // Clear downloaded clip IDs and DOM attributes to allow a fresh run
  downloadedClipIds.clear();
  document.querySelectorAll('[data-copilot-downloaded]').forEach(el => {
    el.removeAttribute('data-copilot-downloaded');
  });

  // 1. Go to the first page first to ensure we scan from the beginning!
  goToFirstPage(() => {
    // 2. Scan and load all clips on Page 1
    autoScanAndLoadAllClips(() => {
      // 3. Run the sequential download step!
      runBatchDownloadStep();
    });
  });

  return { success: true };
}

function runBatchDownloadStep() {
  if (!isBatchDownloading) return;

  // Find all context menu buttons on the page
  const allButtons = findThreeDotButtons();

  // Filter out already processed rows using unique UUIDs
  const unProcessed = allButtons.filter(btn => {
    const row = btn.closest(getClipRowSelector());
    if (!row) return false;

    const clipId = getClipIdFromRow(row);
    if (clipId) {
      return !downloadedClipIds.has(clipId);
    }
    return !btn.hasAttribute('data-copilot-downloaded'); // Fallback
  });

  console.log(`[Suno Mellow Copilot] Batch Download Status: ${allButtons.length - unProcessed.length} processed, ${unProcessed.length} remaining on this page.`);

  if (unProcessed.length === 0) {
    // All items on the current page are processed!
    // Check if there is a next page to navigate to!
    const nextBtn = getNextPageButton();
    if (nextBtn) {
      console.log("[Suno Mellow Copilot] Found Next Page! Navigating...");
      const pageBeforeClick = getCurrentPageNumber();
      const clipsBeforeClick = getVisibleClipIds();

      simulateClick(nextBtn);

      let pageChangeAttempts = 0;
      const maxPageChangeAttempts = 4; // Check every 1.5s for up to 6s total

      function verifyPageChanged() {
        if (!isBatchDownloading) return;

        const pageAfterClick = getCurrentPageNumber();
        const clipsAfterClick = getVisibleClipIds();

        let changed = false;
        if (pageBeforeClick !== null && pageAfterClick !== null) {
          changed = pageAfterClick !== pageBeforeClick;
          console.log(`[Suno Mellow Copilot] Page detection: Before=${pageBeforeClick}, After=${pageAfterClick}. Changed=${changed}`);
        } else {
          // Fallback to clip list comparison
          changed = !isSameClipList(clipsBeforeClick, clipsAfterClick);
          console.log(`[Suno Mellow Copilot] Clip list detection: Changed=${changed}`);
        }

        if (changed) {
          console.log("[Suno Mellow Copilot] Page change verified. Loading new clips...");
          // Scan the loaded page
          autoScanAndLoadAllClips(() => {
            runBatchDownloadStep();
          });
        } else {
          pageChangeAttempts++;
          if (pageChangeAttempts < maxPageChangeAttempts) {
            console.log(`[Suno Mellow Copilot] Page hasn't changed yet (attempt ${pageChangeAttempts}/${maxPageChangeAttempts}). Waiting 1.5s longer...`);
            // Try clicking again on the 2nd attempt in case the first click was ignored/intercepted
            if (pageChangeAttempts === 2) {
              console.log("[Suno Mellow Copilot] Re-clicking Next Page button in case click was missed...");
              simulateClick(nextBtn);
            }
            batchTimerId = setTimeout(verifyPageChanged, 1500);
          } else {
            // Check if we actually downloaded everything visible on the screen
            const visibleIds = getVisibleClipIds();
            const allVisibleProcessed = visibleIds.length > 0 && visibleIds.every(id => downloadedClipIds.has(id));

            isBatchDownloading = false;

            if (allVisibleProcessed) {
              console.log("[Suno Mellow Copilot] All visible songs are already processed. Finishing successfully!");
              chrome.runtime.sendMessage({
                action: "batchDownloadStopped",
                reason: "complete"
              });
            } else {
              console.warn("[Suno Mellow Copilot] Timeout waiting for page change. Stopping batch download to prevent infinite loop.");
              chrome.runtime.sendMessage({
                action: "batchDownloadStopped",
                reason: "timeout"
              });
            }
          }
        }
      }

      batchTimerId = setTimeout(verifyPageChanged, 3500);
    } else {
      isBatchDownloading = false;
      console.log("[Suno Mellow Copilot] Batch download complete. All pages and songs processed!");
      chrome.runtime.sendMessage({
        action: "batchDownloadStopped",
        reason: "complete"
      });
    }
    return;
  }

  // Process the first unprocessed song context menu button
  const targetBtn = unProcessed[0];
  const targetRow = targetBtn.closest(getClipRowSelector());
  const clipId = targetRow ? getClipIdFromRow(targetRow) : null;

  // Scroll element into view instantly (no smooth scroll animation lag to disrupt click targets)
  targetBtn.scrollIntoView({ block: 'center', behavior: 'auto' });

  // Force-reveal the hover-fade-in container that hides buttons behind CSS :hover
  // (CSS :hover cannot be triggered by JS events — must override with inline style)
  const hoverContainer = targetRow ? targetRow.querySelector('.hover-fade-in, [class*="hover-fade-in"]') : null;
  let originalOpacity = null;
  let originalPointerEvents = null;
  if (hoverContainer) {
    originalOpacity = hoverContainer.style.opacity;
    originalPointerEvents = hoverContainer.style.pointerEvents;
    hoverContainer.style.opacity = '1';
    hoverContainer.style.pointerEvents = 'auto';
    hoverContainer.style.visibility = 'visible';
  }

  // Wait 350ms for scroll and force-reveal to settle
  batchTimerId = setTimeout(() => {
    simulateClick(targetBtn);
    console.log(`[Suno Mellow Copilot] Clicked context menu (Attempt ${currentSongRetries + 1}). Polling for 'Download' option...`);

    // Poll for the "Download" menu option to support slow dropdown mounts
    pollForElement(() => {
      return findDropdownOption('download');
    }, (downloadOption) => {
      if (downloadOption) {
        // Hover and click the download option
        simulateHover(downloadOption);
        simulateClick(downloadOption);
        console.log("[Suno Mellow Copilot] Clicked 'Download' menu option. Polling for WAV sub-option...");

          // Poll for WAV sub-menu option — use aria-label first (most reliable), then text fallback
        pollForElement(() => {
          // Direct aria-label query (Suno uses aria-label="WAV Audio")
          return document.querySelector('button[aria-label="WAV Audio"], button[aria-label*="WAV" i]') ||
                 findDropdownOption('wav audio') || // text "WAV Audio"
                 findDropdownOption('wav', true);   // exact text 'wav' fallback
        }, (wavOption) => {
          if (wavOption) {
            // Hover and click the WAV option
            simulateHover(wavOption);
            simulateClick(wavOption);
            console.log("[Suno Mellow Copilot] Clicked 'WAV' download sub-option.");

            // Mark as downloaded ONLY upon successful click trigger of the WAV option!
            if (clipId) {
              downloadedClipIds.add(clipId);
            }
            targetBtn.setAttribute('data-copilot-downloaded', 'true');
            currentSongRetries = 0; // Reset retries on success

            // Wait dynamically for the download modal to open, prepare, trigger, and close!
            waitForModalToClose(() => {
              // Extract song title and notify popup.js to auto-move the file
              // Try multiple selectors for song title (supports old and new Suno UI)
              const songTitle = targetRow.getAttribute('aria-label') ||
                                targetRow.querySelector('.css-qs19a1')?.textContent ||
                                targetRow.querySelector('[class*="e1yitp9f11"]')?.textContent ||
                                targetRow.querySelector('.css-1a6mtca')?.textContent || '';
              if (songTitle && activeEpisodeId) {
                chrome.runtime.sendMessage({
                  action: "batchSongDownloaded",
                  title: songTitle,
                  episodeId: activeEpisodeId
                });
              }

              runBatchDownloadStep();
            });
          } else {
            console.warn("[Suno Mellow Copilot] WAV option not found in submenu.");
            handleStepFailure(targetBtn);
          }
        }, 1500, 50);
      } else {
        console.warn("[Suno Mellow Copilot] 'Download' option not found in dropdown.");
        handleStepFailure(targetBtn);
      }
    }, 1500, 50);
  }, 350);
}

function handleStepFailure(targetBtn) {
  dismissMenus();
  currentSongRetries++;

  if (currentSongRetries < 3) {
    console.log("[Suno Mellow Copilot] Retrying current song in 1.5 seconds...");
    batchTimerId = setTimeout(() => {
      runBatchDownloadStep();
    }, 1500);
  } else {
    console.error("[Suno Mellow Copilot] Failed to download current song after 3 attempts. Skipping to prevent endless loops.");
    // Mark as failed so it gets skipped and we don't block the rest of the list
    const targetRow = targetBtn.closest(getClipRowSelector());
    const clipId = targetRow ? getClipIdFromRow(targetRow) : null;
    if (clipId) {
      downloadedClipIds.add(clipId);
    }
    targetBtn.setAttribute('data-copilot-downloaded', 'failed');
    currentSongRetries = 0; // Reset retries for next song
    batchTimerId = setTimeout(() => {
      runBatchDownloadStep();
    }, 1000);
  }
}

function dismissMenus() {
  document.body.click(); // Click empty space to dismiss context menus
}
