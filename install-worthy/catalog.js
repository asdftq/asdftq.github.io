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
  }
];
