"use strict";

// Theme toggle
const themeBtn = document.querySelector(".theme-toggle");
const stored = localStorage.getItem("theme");

if (stored) {
  document.documentElement.setAttribute("data-theme", stored);
} else {
  document.documentElement.setAttribute("data-theme", "light");
}

if (themeBtn) {
  themeBtn.addEventListener("click", () => {
    const current = document.documentElement.getAttribute("data-theme");
    const next = current === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);
  });
}

// Mobile menu
const toggle = document.querySelector(".menu-toggle");
const nav = document.querySelector(".nav-links");

if (toggle && nav) {
  toggle.addEventListener("click", () => {
    const expanded = toggle.getAttribute("aria-expanded") === "true";
    toggle.setAttribute("aria-expanded", String(!expanded));
    nav.classList.toggle("active");
  });

  nav.addEventListener("click", (e) => {
    if (e.target.tagName === "A") {
      nav.classList.remove("active");
      toggle.setAttribute("aria-expanded", "false");
    }
  });
}

// Lead form → WhatsApp
const formLead = document.getElementById("form-lead");

if (formLead) {
  formLead.addEventListener("submit", (e) => {
    e.preventDefault();
    const nome = document.getElementById("lead-nome").value.trim();
    const whatsapp = document.getElementById("lead-whatsapp").value.trim();
    const cleaned = whatsapp.replace(/\D/g, "");

    if (cleaned.length < 10 || cleaned.length > 11) {
      document.getElementById("lead-whatsapp").setCustomValidity("Informe um WhatsApp válido com DDD");
      document.getElementById("lead-whatsapp").reportValidity();
      return;
    }

    document.getElementById("lead-whatsapp").setCustomValidity("");
    const msg = encodeURIComponent(
      `Olá! Meu nome é ${nome}, meu WhatsApp é ${whatsapp}. Gostaria de ser avisado(a) quando houver filhotes de Yorkshire disponíveis. Obrigado!`
    );
    if (typeof fbq !== "undefined") fbq("track", "Lead");
    window.open(`https://wa.me/5511977118201?text=${msg}`, "_blank");
  });
}

// Scroll reveal animations
const reveals = document.querySelectorAll("section, .titulo-card, #diferenciais article, .depoimento, .blog-card, .filhotes-info");

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("revealed");
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.1, rootMargin: "0px 0px -50px 0px" });

reveals.forEach((el) => {
  el.classList.add("reveal");
  revealObserver.observe(el);
});

// Dynamic media loader with carousel
async function loadMedia() {
  try {
    const res = await fetch("data/media.json");
    const data = await res.json();

    const filhotesGrid = document.getElementById("filhotes-grid");
    const famososGrid = document.getElementById("famosos-grid");
    const emocoesGrid = document.getElementById("emocoes-grid");
    const titulosVideosGrid = document.getElementById("titulos-videos-grid");

    if (filhotesGrid && data.filhotes) {
      renderCarousel(filhotesGrid, data.filhotes, "filhote");
    }

    if (titulosVideosGrid && data.titulosVideos) {
      renderCarousel(titulosVideosGrid, data.titulosVideos, "video");
      lazyLoadVideos(titulosVideosGrid);
    }

    if (famososGrid && data.famosos) {
      renderCarousel(famososGrid, data.famosos, "video");
      lazyLoadVideos(famososGrid);
    }

    if (emocoesGrid && data.emocoes) {
      renderCarousel(emocoesGrid, data.emocoes, "video");
      lazyLoadVideos(emocoesGrid);

      const btnVerTodos = document.getElementById("btn-ver-todos-emocoes");
      if (btnVerTodos && data.emocoesExtras) {
        btnVerTodos.addEventListener("click", () => {
          const track = emocoesGrid.querySelector(".carousel-track");
          data.emocoesExtras.forEach(item => {
            track.innerHTML += `<div class="video-item"><video controls preload="none" data-src="${item.src}"></video></div>`;
          });
          lazyLoadVideos(emocoesGrid);
          btnVerTodos.remove();
        });
      }
    }
  } catch (e) {
    console.error("Erro ao carregar mídias:", e);
  }
}

function renderCarousel(container, items, type) {
  const wrapper = document.createElement("div");
  wrapper.className = "carousel";

  const track = document.createElement("div");
  track.className = "carousel-track";

  items.forEach(item => {
    if (type === "filhote") {
      track.innerHTML += `<div class="filhote-card">
        <img src="${item.src}" alt="${item.nome}" loading="lazy" width="280" height="280" />
        <div class="filhote-info">
          <h3>${item.nome}</h3>
          <p>${item.info}</p>
        </div>
      </div>`;
    } else {
      track.innerHTML += `<div class="video-item">
        <video controls preload="metadata" data-src="${item.src}">
        </video>
      </div>`;
    }
  });

  const btnPrev = document.createElement("button");
  btnPrev.className = "carousel-btn carousel-btn-prev";
  btnPrev.setAttribute("aria-label", "Anterior");
  btnPrev.innerHTML = "&#10094;";

  const btnNext = document.createElement("button");
  btnNext.className = "carousel-btn carousel-btn-next";
  btnNext.setAttribute("aria-label", "Próximo");
  btnNext.innerHTML = "&#10095;";

  wrapper.appendChild(btnPrev);
  wrapper.appendChild(track);
  wrapper.appendChild(btnNext);
  container.appendChild(wrapper);

  const scrollAmount = track.querySelector(".filhote-card, .video-item")?.offsetWidth + 16 || 300;

  btnPrev.addEventListener("click", () => {
    track.scrollBy({ left: -scrollAmount, behavior: "smooth" });
  });

  btnNext.addEventListener("click", () => {
    track.scrollBy({ left: scrollAmount, behavior: "smooth" });
  });

  track.addEventListener("scroll", () => {
    btnPrev.style.opacity = track.scrollLeft > 0 ? "1" : "0";
    btnNext.style.opacity = track.scrollLeft < track.scrollWidth - track.clientWidth - 10 ? "1" : "0";
  });

  // Initial state
  btnPrev.style.opacity = "0";
  btnNext.style.opacity = items.length > 3 ? "1" : "0";
}

loadMedia();

// Lazy load videos only when visible
function lazyLoadVideos(container) {
  const videos = container.querySelectorAll("video[data-src]");
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const video = entry.target;
        const src = video.getAttribute("data-src");
        video.innerHTML = `<source src="${src}" type="video/mp4">`;
        video.removeAttribute("data-src");
        video.load();
        observer.unobserve(video);
      }
    });
  }, { rootMargin: "200px" });

  videos.forEach((video) => observer.observe(video));
}
