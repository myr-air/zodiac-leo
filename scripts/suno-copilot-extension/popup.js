/**
 * Suno Mellow Copilot - Popup Script (Responsive Panel version)
 */

document.addEventListener('DOMContentLoaded', async () => {
  // Tab Bar Buttons
  const tabTracksBtn = document.getElementById('tab-tracks-btn');
  const tabAutoBtn = document.getElementById('tab-auto-btn');

  // Tab Content Panels
  const tabTracks = document.getElementById('tab-tracks');
  const tabAuto = document.getElementById('tab-auto');

  // Elements for Track List
  const trackListContainer = document.getElementById('track-list-container');
  const previewPanel = document.getElementById('preview-panel');
  const closePreviewBtn = document.getElementById('close-preview');

  // Track Preview labels
  const selectedTrackName = document.getElementById('selected-track-name');
  const selectedTrackBpm = document.getElementById('selected-track-bpm');
  const selectedTrackGenre = document.getElementById('selected-track-genre');
  const selectedTrackStylesText = document.getElementById('selected-track-styles-text');
  const selectedTrackLyricsText = document.getElementById('selected-track-lyrics-text');

  // Main Footer Elements
  const fillBtn = document.getElementById('fill-btn');
  const statusBar = document.getElementById('status-bar');

  // Automated Series Controls
  const delayInput = document.getElementById('delay-input');
  const startSeqBtn = document.getElementById('start-seq-btn');
  const startBatchDlBtn = document.getElementById('start-batch-dl-btn');
  const startFullRunBtn = document.getElementById('start-full-run-btn');
  const connectOsBtn = document.getElementById('connect-os-btn');
  const disconnectOsBtn = document.getElementById('disconnect-os-btn');
  const seqStatusBox = document.getElementById('seq-status-box');
  const seqCurrentTrack = document.getElementById('seq-current-track');
  const seqTrackName = document.getElementById('seq-track-name');
  const seqTimer = document.getElementById('seq-timer');
  const stopSeqBtn = document.getElementById('stop-seq-btn');
  const resetSeqBtn = document.getElementById('reset-seq-btn');

  // NEW Episode & Track Selector elements
  const episodeSelect = document.getElementById('episode-select');
  const startTrackSelect = document.getElementById('start-track-select');
  const episodeSubtitle = document.getElementById('episode-subtitle');

  let tracksDatabase = {};
  let activeEpisodeId = '';
  let currentSelectedTrackId = null;
  let activeTabId = null;
  let isSunoActive = false;

  // Automation sequence state
  let isSequenceRunning = false;
  let isBatchDlRunning = false;
  let isOsConnected = false;
  let osSocket = null;
  let pendingInjectResolver = null;
  let pendingCatalogResolver = null;
  let currentSeqIndex = 1;
  let totalTracks = 13;
  let sequenceTimerId = null;
  let fullRunCountdownTimerId = null;

  const FULL_RUN_WAIT_MINUTES = 5;
  let isFullRunMode = false;
  let isFullRunCountdownActive = false;

  // Select Episode
  function selectEpisode(epId) {
    if (isSequenceRunning) return;
    activeEpisodeId = epId;

    const epData = tracksDatabase[epId];
    if (!epData) return;

    episodeSubtitle.textContent = epData.name;

    // Update totalTracks based on loaded episode tracks
    const trackKeys = Object.keys(epData.tracks);
    totalTracks = trackKeys.length;

    // Re-populate start-track-select
    startTrackSelect.innerHTML = '';
    trackKeys.forEach(trackId => {
      const option = document.createElement('option');
      option.value = trackId;
      option.textContent = `Track ${trackId}`;
      startTrackSelect.appendChild(option);
    });

    // Save to storage
    chrome.storage.local.set({ activeEpisodeId: epId });

    // Re-render track list
    renderTrackList();

    // Clear selection
    currentSelectedTrackId = null;
    previewPanel.classList.add('hidden');
    updateFillButtonState();

    // Reset sequence index dynamically unless resuming
    currentSeqIndex = 1;
    startTrackSelect.value = "1";
    if (!isSequenceRunning) {
      seqStatusBox.classList.add('hidden');
      startSeqBtn.innerHTML = `<span>🚀</span> Start Auto Sequence (from Track 1)`;
      startBatchDlBtn.innerHTML = `<span class="btn-icon">📥</span> Batch Download All WAVs (${totalTracks * 2} Songs)`;
      startFullRunBtn.innerHTML = '<span class="btn-icon">⚡</span> Start Full Auto Run (Generate, Wait 5 mins, Download WAVs)';
      startFullRunBtn.disabled = false;
    }
  }

  // Load persisted state from chrome.storage.local
  async function loadPersistedState() {
    try {
      const stored = await chrome.storage.local.get(['activeEpisodeId', 'currentSeqIndex', 'delayValue']);

      if (stored.activeEpisodeId && tracksDatabase[stored.activeEpisodeId]) {
        activeEpisodeId = stored.activeEpisodeId;
        episodeSelect.value = activeEpisodeId;
      } else {
        activeEpisodeId = tracksDatabase['s01e03-rooftop-golden-hour-longplay']
          ? 's01e03-rooftop-golden-hour-longplay'
          : Object.keys(tracksDatabase)[0];
        episodeSelect.value = activeEpisodeId;
      }

      selectEpisode(activeEpisodeId);

      if (stored.currentSeqIndex) {
        currentSeqIndex = parseInt(stored.currentSeqIndex);
        startTrackSelect.value = String(currentSeqIndex);
      }
      if (stored.delayValue) {
        delayInput.value = stored.delayValue;
      }

      // If we restored a paused state, set up UI automatically!
      if (currentSeqIndex > 1 && currentSeqIndex <= totalTracks) {
        seqStatusBox.classList.remove('hidden');
        seqCurrentTrack.textContent = `${currentSeqIndex}/${totalTracks}`;
        seqTimer.textContent = "PAUSED";
        startSeqBtn.innerHTML = `<span>▶</span> Resume Series (Track ${currentSeqIndex})`;
        statusBar.textContent = `Restored previous run: Paused at Track ${currentSeqIndex}.`;
        statusBar.className = "status-message success";

        const track = tracksDatabase[activeEpisodeId]?.tracks[String(currentSeqIndex)];
        if (track) {
          seqTrackName.textContent = track.title;
        }
      } else {
        startSeqBtn.innerHTML = `<span>🚀</span> Start Auto Sequence (from Track ${currentSeqIndex})`;
        updateTimerDisplayFromDelay();
      }
    } catch (err) {
      console.error("Failed to load persisted state:", err);
    }
  }

  // 1. Tab Switching Logic
  function deactivateAllTabs() {
    [tabTracksBtn, tabAutoBtn].forEach(btn => btn.classList.remove('active'));
    [tabTracks, tabAuto].forEach(panel => panel.classList.remove('active'));
  }

  tabTracksBtn.addEventListener('click', () => {
    if (isSequenceRunning) return;
    deactivateAllTabs();
    tabTracksBtn.classList.add('active');
    tabTracks.classList.add('active');
    updateFillButtonState();
  });

  tabAutoBtn.addEventListener('click', () => {
    deactivateAllTabs();
    tabAutoBtn.classList.add('active');
    tabAuto.classList.add('active');
    previewPanel.classList.add('hidden');
    updateFillButtonState();
  });

  // Episode select change handler
  episodeSelect.addEventListener('change', (e) => {
    selectEpisode(e.target.value);
  });

  // Start track select change handler
  startTrackSelect.addEventListener('change', (e) => {
    currentSeqIndex = parseInt(e.target.value) || 1;
    chrome.storage.local.set({ currentSeqIndex });
    if (!isSequenceRunning) {
      startSeqBtn.innerHTML = `<span>🚀</span> Start Auto Sequence (from Track ${currentSeqIndex})`;
    }
  });

  // 2. Episode catalog loading (Local OS Server preferred, local file fallback)
  function renderEpisodeOptions() {
    episodeSelect.innerHTML = '';
    Object.keys(tracksDatabase).forEach(epId => {
      const option = document.createElement('option');
      option.value = epId;
      option.textContent = tracksDatabase[epId].name;
      episodeSelect.appendChild(option);
    });
  }

  function applyTracksDatabase(data) {
    tracksDatabase = data || {};
    if (!Object.keys(tracksDatabase).length) {
      trackListContainer.innerHTML = '<div class="loading-state" style="color: #ff4d4f;">No tracks loaded from catalog.</div>';
      return false;
    }

    renderEpisodeOptions();
    return true;
  }

  async function loadTracksFromLocalFile() {
    try {
      const response = await fetch('tracks.json');
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const data = await response.json();
      return applyTracksDatabase(data);
    } catch (error) {
      console.error("Failed to load tracks from local tracks.json:", error);
      trackListContainer.innerHTML = '<div class="loading-state" style="color: #ff4d4f;">Failed to load tracks.json</div>';
      return false;
    }
  }

  async function requestCatalogFromServer(timeoutMs = 2000) {
    const start = Date.now();
    while (!isOsConnected && Date.now() - start < timeoutMs) {
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    if (!isOsConnected || !osSocket || osSocket.readyState !== WebSocket.OPEN) {
      return false;
    }

    return new Promise((resolve) => {
      let done = false;
      const finish = (result) => {
        if (done) return;
        done = true;
        resolve(result);
      };

      const timeout = setTimeout(() => {
        if (!done) {
          pendingCatalogResolver = null;
          finish(false);
        }
      }, timeoutMs);

      pendingCatalogResolver = (tracks) => {
        clearTimeout(timeout);
        pendingCatalogResolver = null;
        finish(applyTracksDatabase(tracks));
      };

      try {
        osSocket.send(JSON.stringify({ action: "request_catalog" }));
      } catch (err) {
        clearTimeout(timeout);
        pendingCatalogResolver = null;
        finish(false);
      }
    });
  }

  async function initializeTrackDatabase() {
    connectToLocalServer();
    const serverLoaded = await requestCatalogFromServer();
    if (serverLoaded) {
      statusBar.textContent = "Tracks loaded from Local OS Server.";
      statusBar.className = "status-message success";
      return true;
    }

    const localLoaded = await loadTracksFromLocalFile();
    if (!localLoaded) {
      statusBar.textContent = "Cannot load track catalog.";
      statusBar.className = "status-message error";
      return false;
    }

    return true;
  }

  // 3. Render Track items in panel list
  function renderTrackList() {
    trackListContainer.innerHTML = '';

    const epData = tracksDatabase[activeEpisodeId];
    if (!epData || !epData.tracks) {
      trackListContainer.innerHTML = '<div class="loading-state">No tracks loaded.</div>';
      return;
    }

    Object.keys(epData.tracks).forEach(trackId => {
      const track = epData.tracks[trackId];

      const trackItem = document.createElement('div');
      trackItem.className = 'track-item';
      trackItem.dataset.id = trackId;

      const genreTag = track.styles.toLowerCase().includes('city-pop') ? 'City-Pop' : 'R&B';

      trackItem.innerHTML = `
        <div style="display: flex; align-items: center; gap: 10px;">
          <span class="track-num">${trackId}</span>
          <div class="track-info">
            <span class="track-title">${track.title}</span>
            <div class="track-meta-row">
              <span>⏱ ${track.bpm} BPM</span>
              <span>•</span>
              <span>✨ ${genreTag}</span>
            </div>
          </div>
        </div>
        <span style="font-size: 14px; color: var(--text-secondary);">➔</span>
      `;

      trackItem.addEventListener('click', () => selectTrack(trackId));
      trackListContainer.appendChild(trackItem);
    });
  }

  // 4. Select Track and display preview
  function selectTrack(trackId) {
    if (isSequenceRunning) return;

    document.querySelectorAll('.track-item').forEach(item => {
      item.classList.remove('selected');
      if (item.dataset.id === trackId) {
        item.classList.add('selected');
      }
    });

    currentSelectedTrackId = trackId;
    const track = tracksDatabase[activeEpisodeId]?.tracks[trackId];
    if (!track) return;

    selectedTrackName.textContent = `#${trackId} - ${track.title}`;
    selectedTrackBpm.textContent = `${track.bpm} BPM`;
    selectedTrackGenre.textContent = `W: ${track.weirdness} / I: ${track.influence}`;
    selectedTrackStylesText.textContent = track.styles;

    const lines = track.lyrics.split('\n');
    const snippet = lines.slice(0, 5).join('\n') + (lines.length > 5 ? '\n...' : '');
    selectedTrackLyricsText.textContent = snippet;

    previewPanel.classList.remove('hidden');
    updateFillButtonState();
  }

  // Close preview button listener
  closePreviewBtn.addEventListener('click', () => {
    previewPanel.classList.add('hidden');
    document.querySelectorAll('.track-item').forEach(item => item.classList.remove('selected'));
    currentSelectedTrackId = null;
    updateFillButtonState();
  });

  // 5. Check active tab matches suno.com/create or suno.com
  async function checkActiveTab() {
    try {
      const [tab] = await chrome.tabs.query({ active: true, lastFocusedWindow: true });
      if (tab && tab.url) {
        activeTabId = tab.id;
        if (tab.url.includes('suno.com')) {
          isSunoActive = true;
          statusBar.textContent = "Connected to Suno.com";
          statusBar.className = "status-message success";

          await ensureContentScriptInjected(activeTabId);
        } else {
          isSunoActive = false;
          statusBar.textContent = "Please open and switch to a Suno.com tab";
          statusBar.className = "status-message error";
        }
      }
    } catch (error) {
      printError("Error checking tab:", error);
      isSunoActive = false;
      statusBar.textContent = "Unable to access tab settings";
      statusBar.className = "status-message error";
    }
    updateFillButtonState();
  }

  // Pre-flight check to dynamically inject content script if inactive
  async function ensureContentScriptInjected(tabId) {
    try {
      const reply = await chrome.tabs.sendMessage(tabId, { action: "ping" });
      if (reply && reply.status === "ready") {
        statusBar.textContent = "Connected to Suno.com (Copilot Ready!)";
        statusBar.className = "status-message success";
        return true;
      }
    } catch (e) {
      console.log("[Suno Mellow Copilot] Content script not active. Injecting...");
      try {
        statusBar.textContent = "Injecting copilot helpers...";
        await chrome.scripting.executeScript({
          target: { tabId: tabId },
          files: ['content.js']
        });
        await new Promise(resolve => setTimeout(resolve, 200));
        statusBar.textContent = "Connected and active!";
        statusBar.className = "status-message success";
        return true;
      } catch (err) {
        console.error("[Suno Mellow Copilot] Dynamic injection failed:", err);
        statusBar.textContent = "Connection failed. Please refresh the page.";
        statusBar.className = "status-message error";
        return false;
      }
    }
    return false;
  }

  function printError(msg, err) {
    console.error(msg, err);
  }

  // Monitor message updates from background script regarding active tab changes
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "tabChanged") {
      checkActiveTab();
      sendResponse({ status: "acknowledged" });
      return true;
    }

    if (request.action === "batchSongDownloaded") {
      console.log("[Suno Mellow Copilot] Batch song downloaded notification:", request.title);
      if (isOsConnected && osSocket) {
        osSocket.send(JSON.stringify({
          action: "batch_download_completed",
          episodeId: request.episodeId,
          title: request.title
        }));
      }
      sendResponse({ status: "acknowledged" });
      return true;
    }

    if (request.action === "batchDownloadStopped") {
      console.log("[Suno Mellow Copilot] Batch download stopped:", request.reason);
      isBatchDlRunning = false;
      startBatchDlBtn.innerHTML = `<span class="btn-icon">📥</span> Batch Download All WAVs (${totalTracks * 2} Songs)`;
      startBatchDlBtn.style.background = '';
      if (request.reason === "timeout") {
        statusBar.textContent = "Batch download stopped: Page transition timed out.";
        statusBar.className = "status-message error";
      } else if (request.reason === "complete") {
        statusBar.textContent = "Batch download complete! All pages processed 🎉";
        statusBar.className = "status-message success";
      } else {
        statusBar.textContent = "Batch download stopped.";
        statusBar.className = "status-message";
      }
      sendResponse({ status: "acknowledged" });
      return true;
    }

    if (request.action === "createTimeout") {
      console.warn("[Suno Mellow Copilot] Create timeout:", request.reason, request.trackTitle || '');
      statusBar.textContent = request.trackTitle
        ? `Create timeout on "${request.trackTitle}". Auto sequence will continue to next track.`
        : "Create timeout detected. Auto sequence will continue.";
      statusBar.className = "status-message error";
      sendResponse({ status: "acknowledged" });
      return true;
    }
  });

  // Enable/Disable Fill button based on active page and form data existence
  function updateFillButtonState() {
    if (isSequenceRunning) {
      fillBtn.disabled = true;
      return;
    }

    if (!isSunoActive) {
      fillBtn.disabled = true;
      return;
    }

    const isTracksTabActive = tabTracks.classList.contains('active');

    if (isTracksTabActive) {
      fillBtn.disabled = (currentSelectedTrackId === null);
    } else {
      fillBtn.disabled = true; // Auto tab has its own runner buttons
    }
  }

  // 6. Manual Fill Action Event Listener
  fillBtn.addEventListener('click', async () => {
    if (!isSunoActive || !activeTabId || isSequenceRunning || !currentSelectedTrackId) return;

    statusBar.textContent = "Checking tab connection...";
    const ok = await ensureContentScriptInjected(activeTabId);
    if (!ok) return;

    const track = tracksDatabase[activeEpisodeId]?.tracks[currentSelectedTrackId];
    if (!track) return;

    const payload = {
      title: track.title,
      styles: track.styles,
      lyrics: track.lyrics,
      exclude: track.exclude,
      weirdness: track.weirdness,
      influence: track.influence
    };

    statusBar.textContent = "Injecting data into Suno form...";
    fillBtn.disabled = true;

    try {
      const response = await chrome.tabs.sendMessage(activeTabId, {
        action: "fillForm",
        data: payload
      });

      if (response && response.success) {
        statusBar.textContent = "Successfully injected! Ready to Generate ⚡";
        statusBar.className = "status-message success";

        fillBtn.style.background = 'linear-gradient(135deg, #52c41a 0%, #73d13d 100%)';
        fillBtn.style.boxShadow = '0 8px 32px 0 rgba(82, 196, 26, 0.2)';
        fillBtn.innerHTML = '<span>✓</span> Filled Successfully!';

        setTimeout(() => {
          fillBtn.style.background = '';
          fillBtn.style.boxShadow = '';
          fillBtn.innerHTML = '<span>⚡</span> Fill Active Suno Tab';
          updateFillButtonState();
        }, 2500);
      } else {
        statusBar.textContent = "Injection completed with incomplete state.";
        statusBar.className = "status-message error";
        updateFillButtonState();
      }
    } catch (error) {
      console.error("Failed to inject form data:", error);
      statusBar.textContent = "Injection failed. Make sure you are on Suno's Create page.";
      statusBar.className = "status-message error";
      updateFillButtonState();
    }
  });

  // ==========================================
  // 7. Automated Series Generation Logic
  // ==========================================

  startSeqBtn.addEventListener('click', async () => {
    await startAutoSequence(isFullRunMode);
  });

  startFullRunBtn.addEventListener('click', async () => {
    await startAutoSequence(true);
  });

  function getDefaultFullRunButtonText() {
    return '<span class="btn-icon">⚡</span> Start Full Auto Run (Generate, Wait 5 mins, Download WAVs)';
  }

  async function startAutoSequence(autoDownloadAfterFinish = false) {
    if (isSequenceRunning || isFullRunCountdownActive) return;

    if (!isSunoActive) {
      statusBar.textContent = "Cannot start sequence: Please switch to a Suno.com tab first.";
      statusBar.className = "status-message error";
      return;
    }

    statusBar.textContent = "Checking tab connection...";
    const ok = await ensureContentScriptInjected(activeTabId);
    if (!ok) return;

    if (currentSeqIndex > totalTracks || currentSeqIndex < 1) {
      currentSeqIndex = 1;
      startTrackSelect.value = "1";
      chrome.storage.local.set({ currentSeqIndex });
    }

    isSequenceRunning = true;
    isFullRunMode = autoDownloadAfterFinish;
    isFullRunCountdownActive = false;
    clearSequenceTimer();
    clearFullRunCountdown();

    startSeqBtn.disabled = true;
    startSeqBtn.innerHTML = isFullRunMode
      ? '<span>⚡</span> Generating Series + Auto Download...'
      : '<span>⚡</span> Generating Series...';
    episodeSelect.disabled = true;
    startTrackSelect.disabled = true;
    delayInput.disabled = true;
    fillBtn.disabled = true;
    tabTracksBtn.disabled = true;

    startFullRunBtn.disabled = isFullRunMode;
    seqStatusBox.classList.remove('hidden');

    statusBar.textContent = currentSeqIndex === 1
      ? (isFullRunMode
        ? "Starting full auto run and queueing auto-download..."
        : "Starting automated series generation sequence...")
      : (isFullRunMode
        ? `Resuming full auto sequence from Track ${currentSeqIndex}...`
        : `Resuming series from Track ${currentSeqIndex}...`);
    statusBar.className = "status-message success";

    runSequenceStep();
  }

  stopSeqBtn.addEventListener('click', pauseSequence);
  resetSeqBtn.addEventListener('click', resetSequence);

  function pauseSequence() {
    const wasCountdownRunning = isFullRunCountdownActive;

    isSequenceRunning = false;
    clearSequenceTimer();
    clearFullRunCountdown();

    if (currentSeqIndex > totalTracks) {
      currentSeqIndex = 1;
      startTrackSelect.value = "1";
    }

    if (wasCountdownRunning) {
      isFullRunMode = false;
    }

    startFullRunBtn.disabled = false;
    startFullRunBtn.innerHTML = getDefaultFullRunButtonText();

    // Restore tab controls for manual recovery
    tabTracksBtn.disabled = false;
    startBatchDlBtn.disabled = false;
    episodeSelect.disabled = false;
    startTrackSelect.disabled = false;

    // Re-enable manual fill
    fillBtn.disabled = false;

    if (sequenceTimerId) {
      clearInterval(sequenceTimerId);
      sequenceTimerId = null;
    }

    // Save state to local storage
    chrome.storage.local.set({ currentSeqIndex });

    // Update UI to Paused state
    startSeqBtn.disabled = false;
    startSeqBtn.innerHTML = `<span>▶</span> Resume Series (Track ${currentSeqIndex})`;
    delayInput.disabled = false; // Allow changing delay mid-run!

    if (wasCountdownRunning) {
      seqStatusBox.classList.add('hidden');
      statusBar.textContent = "Full auto run stopped by user. Countdown cancelled.";
    } else {
      statusBar.textContent = `Sequence paused at Track ${currentSeqIndex}.`;
    }
    statusBar.className = "status-message";
    seqTimer.textContent = "PAUSED";

    startFullRunBtn.style.background = '';
    startFullRunBtn.style.boxShadow = '';
    isSequenceRunning = false;
    startSeqBtn.style.background = '';
    updateFillButtonState();
  }

  function resetSequence() {
    isSequenceRunning = false;
    if (sequenceTimerId) {
      clearInterval(sequenceTimerId);
      sequenceTimerId = null;
    }

    clearFullRunCountdown();
    isFullRunMode = false;
    startFullRunBtn.innerHTML = getDefaultFullRunButtonText();
    startFullRunBtn.disabled = false;

    currentSeqIndex = 1;
    startTrackSelect.value = "1";
    chrome.storage.local.set({ currentSeqIndex: 1 }); // Clear persisted track index
    seqStatusBox.classList.add('hidden');

    startSeqBtn.disabled = false;
    startSeqBtn.innerHTML = '<span>🚀</span> Start Auto Sequence (from Track 1)';
    delayInput.disabled = false;
    fillBtn.disabled = false;
    startBatchDlBtn.disabled = false;
    episodeSelect.disabled = false;
    startTrackSelect.disabled = false;

    // Enable tabs
    tabTracksBtn.disabled = false;

    statusBar.textContent = "Auto Series reset back to Track 1.";
    statusBar.className = "status-message";
    updateTimerDisplayFromDelay();
    updateFillButtonState();
  }

  async function runSequenceStep() {
    if (!isSequenceRunning) return;

    if (currentSeqIndex > totalTracks) {
      isSequenceRunning = false;
      clearSequenceTimer();

      statusBar.textContent = "🎉 Auto Series Completed! All tracks generated successfully!";
      statusBar.className = "status-message success";

      currentSeqIndex = 1;
      startTrackSelect.value = "1";
      chrome.storage.local.set({ currentSeqIndex: 1 });

      startSeqBtn.style.background = 'linear-gradient(135deg, #52c41a 0%, #73d13d 100%)';
      startSeqBtn.innerHTML = '<span>✓</span> Completed Series!';

      if (isFullRunMode) {
        seqTrackName.textContent = "Auto Series complete. Starting batch WAV download in 5 minutes.";
        seqCurrentTrack.textContent = `${totalTracks}/${totalTracks}`;
        seqStatusBox.classList.remove('hidden');
        isFullRunCountdownActive = true;
        await startFullRunPostRunCountdown();
      } else {
        startBatchDlBtn.disabled = false;
        seqStatusBox.classList.add('hidden');
        startSeqBtn.disabled = false;
        fillBtn.disabled = false;
        tabTracksBtn.disabled = false;
        delayInput.disabled = false;

        setTimeout(() => {
          startSeqBtn.style.background = '';
          startSeqBtn.innerHTML = `<span>🚀</span> Start Auto Sequence (from Track 1)`;
        }, 5000);
      }

      return;
    }

    let track = null;

    if (isOsConnected) {
      statusBar.textContent = `Requesting Track ${currentSeqIndex} from Local OS Server...`;
      statusBar.className = "status-message success";

      // Request track details from the Python server
      osSocket.send(JSON.stringify({
        action: "request_track",
        episodeId: activeEpisodeId,
        trackId: currentSeqIndex
      }));

      // Wait for the server to reply with the inject_track payload!
      try {
        track = await new Promise((resolve, reject) => {
          pendingInjectResolver = resolve;
          // Set a fallback timeout of 10 seconds to reject if the server hangs
          setTimeout(() => {
            if (pendingInjectResolver === resolve) {
              pendingInjectResolver = null;
              reject(new Error("Local server timeout"));
            }
          }, 10000);
        });
      } catch (err) {
        console.error("Local server request failed:", err);
        statusBar.textContent = "Sync failed: Server response timeout.";
        statusBar.className = "status-message error";
        pauseSequence();
        return;
      }
    } else {
      track = tracksDatabase[activeEpisodeId]?.tracks[String(currentSeqIndex)];
    }

    if (!track) {
      currentSeqIndex++;
      runSequenceStep();
      return;
    }

    // Update Status Box UI
    seqCurrentTrack.textContent = `${currentSeqIndex}/${totalTracks}`;
    seqTrackName.textContent = track.title;

    statusBar.textContent = `Injecting Track ${currentSeqIndex}: ${track.title}`;
    statusBar.className = "status-message success";

    try {
      // Generate dynamic payload with autoClickCreate = true to fire generation instantly!
      const payload = {
        title: track.title,
        styles: track.styles,
        lyrics: track.lyrics,
        exclude: track.exclude,
        weirdness: track.weirdness,
        influence: track.influence,
        autoClickCreate: true // ENGAGE AUTOMATION!
      };

      const response = await chrome.tabs.sendMessage(activeTabId, {
        action: "fillForm",
        data: payload
      });

      if (!response || !response.success) {
        console.warn(`Injection on track ${currentSeqIndex} did not reply success.`);
      }

      // Notify local server about generation so it can auto-move WAV!
      if (isOsConnected) {
        osSocket.send(JSON.stringify({
          action: "track_completed",
          episodeId: activeEpisodeId,
          trackId: currentSeqIndex,
          title: track.title
        }));
      }
    } catch (err) {
      console.error(`Failed to inject track ${currentSeqIndex}:`, err);
      statusBar.textContent = `Inject error on track ${currentSeqIndex}. Continuing series...`;
      statusBar.className = "status-message error";
    }

    // Set up wait countdown timer
    const delayMinutes = parseFloat(delayInput.value) || 5;
    let secondsRemaining = Math.round(delayMinutes * 60);

    updateCountdownDisplay(secondsRemaining);

    if (sequenceTimerId) clearInterval(sequenceTimerId);

    sequenceTimerId = setInterval(() => {
      if (!isSequenceRunning) return;

      secondsRemaining--;
      updateCountdownDisplay(secondsRemaining);

      if (secondsRemaining <= 0) {
        clearInterval(sequenceTimerId);
        sequenceTimerId = null;
        currentSeqIndex++;
        chrome.storage.local.set({ currentSeqIndex }); // Persist incremented index
        runSequenceStep(); // Run next track
      }
    }, 1000);
  }

  function clearFullRunCountdown() {
    if (fullRunCountdownTimerId) {
      clearInterval(fullRunCountdownTimerId);
      fullRunCountdownTimerId = null;
    }
    isFullRunCountdownActive = false;
  }

  async function startFullRunPostRunCountdown() {
    let secondsRemaining = Math.round(FULL_RUN_WAIT_MINUTES * 60);
    startSeqBtn.disabled = true;
    startFullRunBtn.disabled = true;
    startBatchDlBtn.disabled = true;
    episodeSelect.disabled = true;
    startTrackSelect.disabled = true;

    updateCountdownDisplay(secondsRemaining);

    clearFullRunCountdown();
    isFullRunCountdownActive = true;

    fullRunCountdownTimerId = setInterval(async () => {
      if (!isFullRunCountdownActive) return;

      secondsRemaining -= 1;
      updateCountdownDisplay(secondsRemaining);

      const minStr = String(Math.floor(secondsRemaining / 60)).padStart(2, '0');
      const secStr = String(secondsRemaining % 60).padStart(2, '0');
      startFullRunBtn.innerHTML = `<span>⏳</span> Waiting ${minStr}:${secStr} then download WAVs`;

      if (secondsRemaining <= 0) {
        clearFullRunCountdown();
        await triggerAutoBatchDownloadAfterWait();
      }
    }, 1000);
  }

  async function triggerAutoBatchDownloadAfterWait() {
    if (!isFullRunMode) return;

    statusBar.textContent = "Wait complete. Starting automatic WAV batch download...";
    statusBar.className = "status-message success";
    isFullRunMode = false;

    await startBatchDownload(true);

    // Restore controls after starting the auto-download flow.
    startSeqBtn.style.background = '';
    startSeqBtn.innerHTML = `<span>🚀</span> Start Auto Sequence (from Track 1)`;
    startSeqBtn.disabled = false;
    startFullRunBtn.innerHTML = getDefaultFullRunButtonText();
    startFullRunBtn.disabled = false;
    delayInput.disabled = false;
    fillBtn.disabled = false;
    tabTracksBtn.disabled = false;
    startBatchDlBtn.disabled = false;
    episodeSelect.disabled = false;
    startTrackSelect.disabled = false;
  }

  function updateCountdownDisplay(sec) {
    const minStr = String(Math.floor(sec / 60)).padStart(2, '0');
    const secStr = String(sec % 60).padStart(2, '0');
    seqTimer.textContent = `${minStr}:${secStr}`;
  }

  function updateTimerDisplayFromDelay() {
    if (isSequenceRunning) return; // Don't interrupt active countdown
    const delayMinutes = parseFloat(delayInput.value) || 2;
    const sec = Math.round(delayMinutes * 60);
    const minStr = String(Math.floor(sec / 60)).padStart(2, '0');
    const secStr = String(sec % 60).padStart(2, '0');
    seqTimer.textContent = `${minStr}:${secStr}`;
  }

  // 8. Batch Download Event Listener
  function setBatchDownloadIdleUI() {
    startBatchDlBtn.innerHTML = `<span class="btn-icon">📥</span> Batch Download All WAVs (${totalTracks * 2} Songs)`;
    startBatchDlBtn.style.background = '';
  }

  async function stopBatchDownload() {
    isBatchDlRunning = false;
    setBatchDownloadIdleUI();
    statusBar.textContent = "Batch downloading stopped by user.";
    statusBar.className = "status-message";

    try {
      await chrome.tabs.sendMessage(activeTabId, { action: "stopBatchDownload" });
    } catch (e) {
      console.error(e);
    }
  }

  async function startBatchDownload(autoTriggered = false) {
    if (!isSunoActive || !activeTabId) {
      statusBar.textContent = "Please switch to a Suno.com tab first.";
      statusBar.className = "status-message error";
      return false;
    }

    statusBar.textContent = "Checking tab connection...";
    const ok = await ensureContentScriptInjected(activeTabId);
    if (!ok) return false;

    isBatchDlRunning = true;
    startBatchDlBtn.innerHTML = '<span class="btn-icon">🛑</span> Stop Batch Download';
    startBatchDlBtn.style.background = 'linear-gradient(135deg, #ff4d4f 0%, #ff7875 100%)';
    statusBar.textContent = autoTriggered
      ? "Auto run completed. Starting automatic batch WAV download..."
      : "Batch downloading all WAVs sequentially...";
    statusBar.className = "status-message success";

    try {
      await chrome.tabs.sendMessage(activeTabId, {
        action: "startBatchDownload",
        episodeId: activeEpisodeId
      });
      return true;
    } catch (error) {
      console.error(error);
      statusBar.textContent = "Failed to start batch download. Are you on the Create page?";
      statusBar.className = "status-message error";
      isBatchDlRunning = false;
      setBatchDownloadIdleUI();
      return false;
    }
  }

  function clearSequenceTimer() {
    if (sequenceTimerId) {
      clearInterval(sequenceTimerId);
      sequenceTimerId = null;
    }
  }

  startBatchDlBtn.addEventListener('click', async () => {
    if (!isSunoActive || !activeTabId) {
      statusBar.textContent = "Please switch to a Suno.com tab first.";
      statusBar.className = "status-message error";
      return;
    }

    if (isBatchDlRunning) {
      await stopBatchDownload();
      return;
    }

    await startBatchDownload(false);
  });

    // ==========================================
    // 9. Local OS WebSocket Connection Handlers
    // ==========================================

    function connectToLocalServer() {
      if (osSocket) {
        osSocket.close();
      }

      statusBar.textContent = "Connecting to Local Mellow OS Server...";
      statusBar.className = "status-message";

      osSocket = new WebSocket("ws://localhost:8080");

      osSocket.onopen = () => {
        isOsConnected = true;
        connectOsBtn.classList.add('hidden');
        disconnectOsBtn.classList.remove('hidden');

        statusBar.textContent = "Connected to Local Mellow OS Server 🚀";
        statusBar.className = "status-message success";
      };

      osSocket.onmessage = async (event) => {
        try {
          const message = JSON.parse(event.data);

          if (message.status === "connected") {
            console.log("[Suno Mellow Copilot] Local server greeting:", message.message);
            if (message.tracks && applyTracksDatabase(message.tracks)) {
              if (pendingCatalogResolver) {
                pendingCatalogResolver(message.tracks);
                pendingCatalogResolver = null;
              }
            }
          }

          if (message.status === "catalog") {
            if (message.tracks && applyTracksDatabase(message.tracks)) {
              if (pendingCatalogResolver) {
                pendingCatalogResolver(message.tracks);
                pendingCatalogResolver = null;
              }
            }
          }

          if (message.status === "error" && pendingCatalogResolver) {
            pendingCatalogResolver(null);
            pendingCatalogResolver = null;
          }

          if (message.status === "inject_track") {
            console.log("[Suno Mellow Copilot] Received inject track command:", message);
            if (pendingInjectResolver) {
              pendingInjectResolver(message.data);
              pendingInjectResolver = null;
            }
          }
        } catch (err) {
          console.error("Error handling WebSocket message:", err);
        }
      };

      osSocket.onclose = () => {
        disconnectLocalServer();
        statusBar.textContent = "Disconnected from Local Server.";
        statusBar.className = "status-message error";
      };

      osSocket.onerror = (err) => {
        console.error("WebSocket Error:", err);
        disconnectLocalServer();
        statusBar.textContent = "Connection to Local OS Server failed.";
        statusBar.className = "status-message error";
      };
    }

    function disconnectLocalServer() {
      isOsConnected = false;
      if (osSocket) {
        osSocket.onclose = null;
        osSocket.onerror = null;
        osSocket.close();
        osSocket = null;
      }
      connectOsBtn.classList.remove('hidden');
      disconnectOsBtn.classList.add('hidden');
    }

    // Connect OS event listeners
    connectOsBtn.addEventListener('click', () => connectToLocalServer());
    disconnectOsBtn.addEventListener('click', disconnectLocalServer);

    // Save delay inputs when edited
    delayInput.addEventListener('input', () => {
      chrome.storage.local.set({ delayValue: delayInput.value });
      updateTimerDisplayFromDelay();
    });

    await initializeTrackDatabase();

    // Run tab check immediately on launch
    await checkActiveTab();

    // Load saved sequence state
    if (Object.keys(tracksDatabase).length > 0) {
      await loadPersistedState();
    }
  });
