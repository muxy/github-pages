---
title: Add Twitch Viewer Interactions to Your Game
description: Use Muxy Gateway to add actions, polls, game text, and other Twitch viewer
  interactions without building or publishing a Twitch Extension.
slug: index
product: Muxy Platform
audience: developers
status: current
owner: Developer Experience
source_of_truth: muxy/github-pages
version: v1
last_verified: '2026-07-14'
review_state: approved
hide:
- toc
page_type: concept
approved_by: peter-bonanni
approved_at: '2026-07-14T20:34:54Z'
approval_method: user-authorized-codex-assisted-source-review
approved_content_sha256: dbfcbc946bf8c2f5dd71085083cbefe4eaf9f375fb1607e8b467878b1aa72910
---

<div class="muxy-home" markdown>

<section class="muxy-hero" markdown>
<div markdown>
<p class="muxy-eyebrow">The fast path for game developers</p>

# Add Twitch viewer interactions to your game

<p class="muxy-hero-copy"><strong>Gateway</strong> is for developers who want to quickly add actions, polls, game text, and other live viewer interactions to a game—without building, reviewing, or publishing their own Twitch Extension. Start with a prefab or a small amount of game code and let Muxy handle the extension experience.</p>

<div class="muxy-actions">
  <a class="muxy-button muxy-button-primary" href="docs/unity-gateway-tutorial/">Start with Gateway</a>
  <a class="muxy-button" href="docs/unity-gamelink-tutorial/">Build with GameLink</a>
  <a class="muxy-button" href="docs/quick-start/">Build a Twitch Extension</a>
</div>
</div>

<div class="muxy-quick-panel">
  <a class="muxy-quick-link" href="docs/unity-gateway-tutorial/">
    <span class="muxy-icon" aria-hidden="true">G</span>
    <span><strong>Gateway for Unity</strong><span>The quickest route from an interaction idea to a playable build</span></span>
  </a>
  <a class="muxy-quick-link" href="docs/unity-gamelink-tutorial/">
    <span class="muxy-icon" aria-hidden="true">L</span>
    <span><strong>GameLink for Unity</strong><span>Connect a game to your own Twitch Extension</span></span>
  </a>
  <a class="muxy-quick-link" href="docs/getting-started-with-medkit/">
    <span class="muxy-icon" aria-hidden="true">M</span>
    <span><strong>MEDKit</strong><span>Build custom viewer-facing Twitch Extension experiences</span></span>
  </a>
</div>
</section>

<section class="muxy-section" markdown>
## Choose the right integration path

<p class="muxy-section-lede">Start with the amount of extension infrastructure you want to own. Gateway is the default for fast game integration; GameLink and MEDKit give you more control when you need a custom Twitch Extension.</p>

<div class="muxy-card-grid">
  <article class="muxy-card">
  <h3>Gateway: move fast</h3>
  <p><strong>You build the interaction; Muxy supplies the Twitch Extension.</strong> Add viewer actions, polls, game text, and Bits support directly from your game. This is the best starting point for quickly prototyping and shipping viewer interactions.</p>
  <p><a href="docs/unity-gateway-tutorial/">Start the Gateway tutorial</a></p>
  </article>

  <article class="muxy-card">
  <h3>GameLink: connect your extension</h3>
  <p>Use GameLink when your game needs real-time communication with a Twitch Extension you control. Build authentication, state, polling, transactions, and messaging into the game runtime.</p>
  <p><a href="docs/unity-gamelink-tutorial/">Start the GameLink tutorial</a></p>
  </article>

  <article class="muxy-card">
  <h3>MEDKit and REST: own the experience</h3>
  <p>Use MEDKit and the REST API to build custom viewer and broadcaster surfaces, persistent state, aggregation, and extension-specific workflows.</p>
  <p><a href="docs/quick-start/">Build a Twitch Extension</a></p>
  </article>
</div>
</section>

<section class="muxy-section" markdown>
## What do I use it for?

<div class="muxy-card-grid">
  <article class="muxy-card">
  <h3>Game Developers</h3>
  <ul>
    <li>Quickly test viewer-interaction ideas with Gateway.</li>
    <li>Add engagement and monetization without publishing an extension.</li>
    <li>Move to GameLink when you need a fully custom experience.</li>
  </ul>
  </article>

  <article class="muxy-card">
  <h3>Extension Writers</h3>
  <ul>
    <li>Create streamer engagement tools.</li>
    <li>Offer new revenue options for streamers.</li>
    <li>Build experiences around state, polling, trivia, and messaging.</li>
  </ul>
  </article>

  <article class="muxy-card">
  <h3>Streamers</h3>
  <ul>
    <li>Find new ways to monetize an audience.</li>
    <li>Promote viewer engagement.</li>
    <li>Create quizzes, votes, and reward-driven events.</li>
  </ul>
  </article>
</div>
</section>

<section class="muxy-section" markdown>
## Muxy features and services for Twitch extensions

<div class="muxy-feature-grid">
  <article class="muxy-feature">
  <h3>Extension State</h3>
  <p>The Muxy server maintains persistent state information about Twitch extensions, broadcasters, and viewers, and makes it available through MEDKit, the REST API, GameLink, and the WebSocket protocol.</p>
  </article>

  <article class="muxy-feature">
  <h3>Scaling Up</h3>
  <p>Muxy data aggregation tools help you create viewer engagement activities for large audiences, from accumulation to ranking, polling, voting, and trivia.</p>
  </article>

  <article class="muxy-feature">
  <h3>Access Control and Messaging</h3>
  <p>User roles gate access to protected functionality. Messaging tools let clients broadcast, publish, subscribe, and coordinate extension activity across channels.</p>
  </article>

  <article class="muxy-feature">
  <h3>Game Integration</h3>
  <p>Gateway and GameLink help developers connect live Twitch interactions to Unity, Unreal, and custom game runtimes with partner-ready authentication, action handling, and state flows.</p>
  </article>
</div>
</section>

</div>
