
(function () {
  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c];
    });
  }

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

  function decodeB64Json(b64) {
    try { return JSON.parse(decodeB64(b64)); } catch (e) { return []; }
  }

  function setupSearch() {
    const input = document.getElementById("wiki-search");
    const results = document.getElementById("search-results");
    const indexEl = document.getElementById("wiki-index");
    if (!input || !results || !indexEl) return;
    let index = [];
    try { index = JSON.parse(indexEl.textContent || "[]"); } catch (e) { index = []; }

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
  }

  const KEYNOTE_564_FIELDS = [
    {
      id: "histology",
      label: "Clear-cell component",
      options: [
        ["", "Select…"],
        ["clear-cell", "Confirmed clear-cell component"],
        ["non-clear-cell", "Non-clear-cell or not confirmed"]
      ]
    },
    {
      id: "pt-stage",
      label: "Pathologic T stage",
      options: [
        ["", "Select…"],
        ["pt1", "pT1"],
        ["pt2", "pT2"],
        ["pt3", "pT3"],
        ["pt4", "pT4"],
        ["unknown", "pTx / unknown / other"]
      ]
    },
    {
      id: "grade",
      label: "Grade",
      options: [
        ["", "Select…"],
        ["grade-1-3", "Grade 1–3"],
        ["grade-4", "Grade 4"],
        ["unknown", "Unknown / not reported"]
      ]
    },
    {
      id: "sarcomatoid",
      label: "Sarcomatoid features",
      options: [
        ["", "Select…"],
        ["absent", "Absent"],
        ["present", "Present"],
        ["unknown", "Unknown / not reported"]
      ]
    },
    {
      id: "n-stage",
      label: "Pathologic N stage",
      options: [
        ["", "Select…"],
        ["n0", "N0"],
        ["n-plus", "N+"],
        ["unknown", "Unknown / not reported"]
      ]
    },
    {
      id: "m1-ned",
      label: "M1 NED status and timing",
      options: [
        ["", "Select…"],
        ["m0", "M0 (no M1 NED)"],
        ["qualifying", "Qualifying M1 NED: resected at nephrectomy or within 1 year"],
        ["nonqualifying", "M1 disease: M1 NED criteria or timing not met"],
        ["unknown", "Unknown / not documented"]
      ]
    }
  ];

  function incomplete(detail) {
    return detail ? "Incomplete — " + detail : "Complete calculator fields";
  }

  function keynote564Category(values) {
    if (!values.histology || !values["m1-ned"]) {
      return incomplete("select histology and M1 NED status");
    }
    if (values.histology !== "clear-cell") return "Not eligible";
    if (values["m1-ned"] === "qualifying") return "M1 NED";
    if (values["m1-ned"] === "nonqualifying") return "Not eligible";
    if (values["m1-ned"] === "unknown") return incomplete("document M1 NED status and timing");
    if (!values["n-stage"]) return incomplete("select pathologic N stage");
    if (values["n-stage"] === "n-plus") return "High risk";
    if (values["n-stage"] === "unknown") return incomplete("document pathologic N stage");
    if (!values["pt-stage"]) return incomplete("select pathologic T stage");
    if (values["pt-stage"] === "pt4") return "High risk";
    if (values["pt-stage"] === "pt3") return "Intermediate-high risk";
    if (values["pt-stage"] === "pt1") return "Not eligible";
    if (values["pt-stage"] === "unknown") return incomplete("document pathologic T stage");
    if (values["grade"] === "grade-4" || values.sarcomatoid === "present") {
      return "Intermediate-high risk";
    }
    if (!values.grade || !values.sarcomatoid) {
      return incomplete("select grade and sarcomatoid features");
    }
    if (values.grade === "unknown" || values.sarcomatoid === "unknown") {
      return incomplete("document grade and sarcomatoid features");
    }
    return "Not eligible";
  }

  function mountKeynote564Calculator(root, setPhraseValue) {
    const fieldsEl = root.querySelector(".calculator-fields");
    const resultEl = root.querySelector(".calculator-result");
    if (!fieldsEl || !resultEl) return;
    const values = {};
    KEYNOTE_564_FIELDS.forEach(function (field) {
      const wrapper = document.createElement("div");
      wrapper.className = "calculator-field";
      const label = document.createElement("label");
      const select = document.createElement("select");
      const selectId = "calculator-keynote-564-" + field.id;
      label.htmlFor = selectId;
      label.textContent = field.label;
      select.id = selectId;
      select.setAttribute("data-calculator-field", field.id);
      field.options.forEach(function (optionSpec) {
        const option = document.createElement("option");
        option.value = optionSpec[0];
        option.textContent = optionSpec[1];
        select.appendChild(option);
      });
      select.addEventListener("input", function () {
        values[field.id] = select.value;
        update();
      });
      wrapper.appendChild(label);
      wrapper.appendChild(select);
      fieldsEl.appendChild(wrapper);
    });

    function update() {
      const category = keynote564Category(values);
      resultEl.textContent = category;
      setPhraseValue(category);
    }
    update();
  }

  function setupPhraseTools() {
    const toolsets = document.querySelectorAll(".phrase-tools");
    toolsets.forEach(function (tools) {
      const controls = decodeB64Json(tools.getAttribute("data-phrase-controls-b64") || "");
      const template = decodeB64(tools.getAttribute("data-phrase-template-b64") || "");
      const values = {};

      function setPhraseValue(controlId, value) {
        values[controlId] = value;
        const phrase = tools.closest(".phrase");
        if (!phrase) return;
        phrase.querySelectorAll("[data-phrase-control]").forEach(function (slot) {
          if (slot.getAttribute("data-phrase-control") === controlId) {
            slot.textContent = value;
          }
        });
      }

      controls.forEach(function (control) {
        setPhraseValue(control.id, "Not selected");
        const controlEl = tools.querySelector(
          '[data-phrase-control-id="' + control.id + '"]'
        );
        if (!controlEl) return;
        if (control.kind === "select") {
          controlEl.addEventListener("input", function () {
            setPhraseValue(control.id, controlEl.value || "Not selected");
          });
          return;
        }
        if (control.kind === "calc" && control.id === "keynote-564") {
          mountKeynote564Calculator(controlEl, function (value) {
            setPhraseValue(control.id, value);
          });
        }
      });

      tools.getPhraseText = function () {
        return controls.reduce(function (text, control) {
          return text.split(control.token).join(values[control.id] || "Not selected");
        }, template);
      };
    });
  }

  function fallbackCopy(text) {
    const ta = document.createElement("textarea");
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand("copy"); } catch (e) {}
    document.body.removeChild(ta);
  }

  function setupCopy() {
    document.addEventListener("click", function (e) {
      const btn = e.target.closest(".copy-btn");
      if (!btn) return;
      const phrase = btn.closest(".phrase");
      const tools = phrase && phrase.querySelector(".phrase-tools");
      const text = tools && typeof tools.getPhraseText === "function"
        ? tools.getPhraseText()
        : decodeB64(btn.getAttribute("data-copy-b64") || "");
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
  }

  setupSearch();
  setupPhraseTools();
  setupCopy();
})();
