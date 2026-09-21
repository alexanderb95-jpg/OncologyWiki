
(function () {
  const input = document.getElementById("wiki-search");
  const results = document.getElementById("search-results");
  const indexEl = document.getElementById("wiki-index");
  if (!input || !results || !indexEl) return;
  let index = [];
  try { index = JSON.parse(indexEl.textContent || "[]"); } catch (e) { index = []; }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c];
    });
  }

  function run() {
    const q = (input.value || "").trim().toLowerCase();
    if (q.length < 2) {
      results.hidden = true;
      results.innerHTML = "";
      return;
    }
    const hits = index.filter(function (row) {
      return (row.blob || "").indexOf(q) !== -1 || (row.title || "").toLowerCase().indexOf(q) !== -1;
    }).slice(0, 12);
    if (!hits.length) {
      results.hidden = false;
      results.innerHTML = "<div style='padding:0.4rem 0.5rem;color:#78716c'>No matches</div>";
      return;
    }
    results.hidden = false;
    results.innerHTML = hits.map(function (h) {
      return '<a href="' + h.href + '">' + escapeHtml(h.title) + "</a>";
    }).join("");
  }

  input.addEventListener("input", run);
  input.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      input.value = "";
      run();
    }
  });

  function decodeB64(b64) {
    try {
      const bin = atob(b64);
      if (typeof TextDecoder !== "undefined") {
        const bytes = new Uint8Array(bin.length);
        for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
        return new TextDecoder("utf-8").decode(bytes);
      }
      return decodeURIComponent(escape(bin));
    } catch (e) {
      return "";
    }
  }

  document.addEventListener("click", function (e) {
    const btn = e.target.closest(".copy-btn");
    if (!btn) return;
    const text = decodeB64(btn.getAttribute("data-copy-b64") || "");
    const done = function () {
      btn.classList.add("copied");
      btn.textContent = "Copied";
      setTimeout(function () {
        btn.classList.remove("copied");
        btn.textContent = "Copy";
      }, 1600);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done).catch(function () {
        fallbackCopy(text); done();
      });
    } else {
      fallbackCopy(text); done();
    }
  });

  function fallbackCopy(text) {
    const ta = document.createElement("textarea");
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand("copy"); } catch (e) {}
    document.body.removeChild(ta);
  }
})();
