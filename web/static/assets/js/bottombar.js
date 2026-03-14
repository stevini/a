  (function() {
    const currentPath = window.location.pathname.replace(/^\/+|\/+$/g, '');
    const bottomItems = document.querySelectorAll(".bottom-bar .bottom-item");
    bottomItems.forEach(item => item.classList.remove("active"));
    bottomItems.forEach(item => {
      const linkPath = item.getAttribute("href").replace(/^\/+|\/+$/g, '');
      if (linkPath === currentPath) {
        item.classList.add("active");
      }
    });
  })();