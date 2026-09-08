// This is the only file to edit when a project or platform link changes.
// Product icons live in ./icons and should match the published app artwork.
// Add another item to `links` when a project becomes available on iOS,
// Android, another browser, or the web. Set `visible` to false to stage it.
window.INSTALL_WORTHY_CATALOG = [
  {
    id: "equilzer",
    name: "Equilzer",
    icon: "icons/equilzer.png",
    description: "Fix web audio with clear presets, safe output boost, and a full 10-band EQ.",
    firstStep: "Start audio in a normal tab, then click the Equilzer toolbar icon.",
    visible: true,
    links: [
      {
        platform: "Chrome",
        action: "Add to Chrome",
        url: "https://chromewebstore.google.com/detail/equilzer-%E2%80%94-private-audio/gicbonipopekbhmcblkphkakdddcipfd"
      }
    ]
  },
  {
    id: "focus-lane",
    name: "Focus Lane",
    icon: "icons/focus-lane.png",
    description: "Block distracting sites with one private focus switch and your own rules.",
    firstStep: "Click the Focus Lane toolbar icon to turn protection on. Right-click it for settings.",
    visible: true,
    links: [
      {
        platform: "Chrome",
        action: "Add to Chrome",
        url: "https://chromewebstore.google.com/detail/oogmofejcfflglfjhhpgmilhohnfckcb"
      }
    ]
  },
  {
    id: "right-click-share",
    name: "Right Click Share",
    icon: "icons/right-click-share.png",
    description: "Send pages, links, text, and actual media files through Chrome's share sheet.",
    firstStep: "Right-click a page, link, selection, image, audio, or video, then choose Share.",
    visible: true,
    links: [
      {
        platform: "Chrome",
        action: "Add to Chrome",
        url: "https://chromewebstore.google.com/detail/right-click-share/hbmhdadlnipjfaihpdfjpknbmdfnjhnd"
      }
    ]
  },
  {
    id: "quietsense",
    shortName: "QuietSense",
    name: "QuietSense: Apartment dB Meter",
    icon: "icons/quietsense.png",
    description: "Estimate everyday apartment sound levels on your iPhone, with a free 60-second room check and practical next steps.",
    firstStep: "Open QuietSense, choose your space and activity, and try your free 60-second check.",
    details: "QuietSense processes sound levels on device without saving raw audio or transcribing speech. Nearby-room values are modeled estimates, not measurements of another room. It is not a certified, legal, or safety sound meter. Unlimited checks require QuietSense Pro.",
    visible: true,
    links: [{ platform: "iOS", action: "Get on the App Store", url: "https://apps.apple.com/app/id6771237461" }]
  },
  {
    id: "jet-lag-bye",
    shortName: "Jet Lag Bye",
    name: "Jet Lag Bye: Travel Sleep Plan",
    icon: "icons/jet-lag-bye.png",
    description: "Turn your itinerary into a day-by-day travel sleep plan with timing for sleep, light, and caffeine. Your first complete plan is free.",
    firstStep: "Open Jet Lag Bye, set your usual sleep schedule, and enter your trip to create your first plan.",
    details: "Plan one-way or round-trip travel, follow a travel-day timeline, and revisit saved plans on your device. Additional plans are available through a Single Trip Plan purchase or Annual Unlimited. Jet Lag Bye provides general educational guidance, not medical advice.",
    visible: true,
    links: [{ platform: "iOS", action: "Get on the App Store", url: "https://apps.apple.com/app/id6747702706" }]
  },
  {
    id: "timerbar",
    shortName: "TimerBar",
    name: "TimerBar: Presentation Timer",
    icon: "icons/timerbar.png",
    description: "Keep presentations, meetings, and focus sessions on time with a fullscreen clock and a live progress bar.",
    firstStep: "Open TimerBar, choose a duration or end time, and start your timer.",
    details: "Set a timer by duration or end time, pause or restart it, and optionally show remaining time. TimerBar+ adds premium themes, fonts, and colors. Available for iPhone and iPad.",
    visible: true,
    links: [{ platform: "iOS", action: "Get on the App Store", url: "https://apps.apple.com/app/id6744717499" }]
  }
];
