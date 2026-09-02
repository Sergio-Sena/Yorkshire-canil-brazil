"use strict";

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
  if (!document.getElementById("famosos-grid") && !document.getElementById("emocoes-grid") && !document.getElementById("titulos-videos-grid")) return;
  try {
    const res = await fetch("data/media.json");
    const data = await res.json();

    const famososGrid = document.getElementById("famosos-grid");
    const emocoesGrid = document.getElementById("emocoes-grid");
    const titulosVideosGrid = document.getElementById("titulos-videos-grid");


    if (titulosVideosGrid && data.titulosVideos) {
      renderVideoSection(titulosVideosGrid, data.titulosVideos, "9/16");
    }

    if (famososGrid && data.famosos) {
      renderVideoSection(famososGrid, data.famosos, "16/9");
    }

    if (emocoesGrid && data.emocoes) {
      renderVideoSection(emocoesGrid, data.emocoes, "16/9");

      const btnVerTodos = document.getElementById("btn-ver-todos-emocoes");
      if (btnVerTodos && data.emocoesExtras) {
        btnVerTodos.addEventListener("click", () => {
          const allItems = [...data.emocoes, ...data.emocoesExtras];
          emocoesGrid.innerHTML = "";
          renderVideoSection(emocoesGrid, allItems, "16/9");
          btnVerTodos.remove();
        });
      }
    }
  } catch (e) {
    console.error("Erro ao carregar mídias:", e);
  }
}

function renderCarousel(container, items) {
  const wrapper = document.createElement("div");
  wrapper.className = "carousel";

  const track = document.createElement("div");
  track.className = "carousel-track";

  items.forEach(item => {
    track.innerHTML += `<div class="filhote-card">
      <img src="${item.src}" alt="${item.nome}" loading="lazy" width="280" height="280" />
      <div class="filhote-info">
        <h3>${item.nome}</h3>
        <p>${item.info}</p>
      </div>
    </div>`;
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

  function getScrollAmount() {
    const item = track.querySelector(".filhote-card");
    return item ? item.offsetWidth + parseInt(getComputedStyle(track).gap || 16) : 300;
  }

  btnPrev.addEventListener("click", () => {
    track.scrollBy({ left: -getScrollAmount(), behavior: "smooth" });
  });

  btnNext.addEventListener("click", () => {
    track.scrollBy({ left: getScrollAmount(), behavior: "smooth" });
  });

  track.addEventListener("scroll", () => {
    btnPrev.style.opacity = track.scrollLeft > 0 ? "1" : "0";
    btnNext.style.opacity = track.scrollLeft < track.scrollWidth - track.clientWidth - 10 ? "1" : "0";
  });

  btnPrev.style.opacity = "0";
  btnNext.style.opacity = items.length > 3 ? "1" : "0";
}

function renderVideoSection(container, items, aspect) {
  const first = items[0];
  const wrapper = document.createElement("div");
  wrapper.className = "video-section";

  const player = document.createElement("video");
  player.className = "video-section-player";
  player.controls = true;
  player.preload = "metadata";
  player.style.aspectRatio = aspect;
  if (first.poster) player.poster = first.poster;
  player.src = first.src;

  const thumbTrack = document.createElement("div");
  thumbTrack.className = "video-section-thumbs";

  items.forEach((item, i) => {
    const thumb = document.createElement("button");
    thumb.className = "video-section-thumb" + (i === 0 ? " active" : "");
    thumb.setAttribute("aria-label", item.nome || `Vídeo ${i + 1}`);
    if (item.poster) {
      thumb.style.backgroundImage = `url('${item.poster}')`;
    }
    thumb.addEventListener("click", () => {
      player.pause();
      player.src = item.src;
      if (item.poster) player.poster = item.poster;
      else player.removeAttribute("poster");
      player.load();
      player.play();
      thumbTrack.querySelectorAll(".video-section-thumb").forEach(t => t.classList.remove("active"));
      thumb.classList.add("active");
    });
    thumbTrack.appendChild(thumb);
  });

  wrapper.appendChild(player);
  if (items.length > 1) wrapper.appendChild(thumbTrack);
  container.appendChild(wrapper);
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

// WhatsApp UTM tracking — identifica origem do lead
(function () {
  const params = new URLSearchParams(window.location.search);
  const utmSource = params.get("utm_source");
  const utmMedium = params.get("utm_medium");
  const gclid = params.get("gclid");
  const isPago = gclid || (utmSource === "google" && utmMedium === "cpc");

  const msg = isPago
    ? "Olá! Vi vocês no Google e tenho interesse em um filhote de Yorkshire."
    : "Olá! Encontrei vocês pelo site e tenho interesse em um filhote de Yorkshire.";

  document.querySelectorAll('a[href*="wa.me/5511977118201"]').forEach((link) => {
    if (!link.closest("#form-lead")) {
      link.href = `https://wa.me/5511977118201?text=${encodeURIComponent(msg)}`;
    }
  });
})();
