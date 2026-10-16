(() => {
  const measurementId = "G-16EJGQ5TKK";
  const storageKey = "asdftq.analytics-consent";
  if (!["www.asdftq.com", "asdftq.com"].includes(location.hostname)) return;

  let choice;
  let started = false;
  try { choice = localStorage.getItem(storageKey); } catch {}

  function start() {
    if (started) return;
    started = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window[`ga-disable-${measurementId}`] = false;
    gtag("consent", "default", {
      analytics_storage: "denied", ad_storage: "denied",
      ad_user_data: "denied", ad_personalization: "denied"
    });
    const canonical = document.querySelector('link[rel="canonical"]')?.href;
    const page = new URL(canonical || location.href);
    page.search = "";
    page.hash = "";
    let referrer = "";
    try {
      const url = new URL(document.referrer);
      referrer = url.origin + (url.hostname === location.hostname ? url.pathname : "/");
    } catch {}
    const campaign = {};
    const params = new URLSearchParams(location.search);
    for (const key of ["source", "medium", "name", "term", "content", "id"]) {
      const value = params.get(`utm_${key === "name" ? "campaign" : key}`);
      if (value && /^[a-zA-Z0-9_-]{1,80}$/.test(value)) campaign[`campaign_${key}`] = value;
    }
    // Apply sanitized URLs globally before any consent or measurement pings.
    gtag("set", { page_location: page.href, page_referrer: referrer });
    gtag("consent", "update", { analytics_storage: "granted" });
    gtag("js", new Date());
    gtag("config", measurementId, {
      page_location: page.href, page_referrer: referrer, page_title: document.title,
      allow_google_signals: false, allow_ad_personalization_signals: false,
      cookie_flags: "SameSite=Lax;Secure", ...campaign
    });
    const tag = document.createElement("script");
    tag.async = true;
    tag.src = `https://www.googletagmanager.com/gtag/js?id=${measurementId}`;
    document.head.append(tag);
  }

  const banner = document.createElement("section");
  banner.className = "site-analytics-choice";
  banner.setAttribute("aria-label", "Website analytics preference");
  banner.innerHTML = '<div><strong>A little insight helps.</strong><p>Allow Google Analytics to measure visits to this website? App data and form contents are never sent. <a href="/privacy.html">Website privacy</a></p></div><div class="site-analytics-actions"><button type="button" data-choice="granted">Allow analytics</button><button type="button" data-choice="denied">No thanks</button></div>';
  banner.hidden = choice === "granted" || choice === "denied";
  document.body.append(banner);

  banner.addEventListener("click", event => {
    const value = event.target.closest("[data-choice]")?.dataset.choice;
    if (!value) return;
    choice = value;
    try { localStorage.setItem(storageKey, value); } catch {}
    banner.hidden = true;
    if (value === "granted") {
      window[`ga-disable-${measurementId}`] = false;
      if (started) gtag("consent", "update", { analytics_storage: "granted" });
      start();
    } else {
      window[`ga-disable-${measurementId}`] = true;
      if (started) gtag("consent", "update", { analytics_storage: "denied" });
      for (const cookie of document.cookie.split(";")) {
        const name = cookie.trim().split("=")[0];
        if (name !== "_ga" && !name.startsWith("_ga_")) continue;
        for (const domain of ["", ";domain=www.asdftq.com", ";domain=asdftq.com"]) {
          document.cookie = `${name}=;max-age=0;path=/${domain};SameSite=Lax;Secure`;
        }
      }
    }
    settings?.focus();
  });
  const settings = document.querySelector("[data-analytics-settings]");
  if (settings) {
    settings.hidden = false;
    settings.addEventListener("click", () => {
      banner.hidden = false;
      banner.querySelector(choice === "granted" ? '[data-choice="denied"]' : '[data-choice="granted"]').focus();
    });
  }
  if (choice === "granted") start();
})();
