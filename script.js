// 🎲 Random Post Button
const pages = [ "ABSDBS", "adena_rover", "backyard_astronomy", "cardboard_computer", "celestial_oceans_and_islands", "cell_tower_dystopia", "code_ode", "cosmic_scale", "desiderata", "explorers_and_innovators", "fallout_4_was_made_for_me", "fisher_observatory", "friday_the_13th", "goonies_treasure_map_replica", "great_american_eclipse", "green_lamp", "hopewell_v1-0", "hopewell_v1-5", "innocence_ending", "junkbot_alpha", "lie_down", "music_projects", "nature-tech_romance", "nomads_sky", "orbits_for_dummies", "play_with_your_food", "primal_astronomy", "puppet_monster", "puzzle_box", "second_star_to_the_right", "spaceship_cross-section", "the_a_i_scare", "tic-tac-toe_BASH", "turtle_feeder", "virus_mutation_simulation", "white_whale", "why_i_love_stargazing", "yellow_house_recording_studio" ]; // ← overwritten by update.py

function goRandom() {
  const random = pages[Math.floor(Math.random() * pages.length)];
  window.location.href = random + ".html";
}


document.addEventListener("DOMContentLoaded", function () {

  // === Load Archive Automatically ===
  fetch("archive.html")
    .then(response => response.text())
    .then(data => {

      const archiveList = document.getElementById("archive-list");

      if (archiveList) {
        archiveList.innerHTML = data;
      }

      // === Archive Search (must run AFTER archive loads) ===
      const searchInput = document.getElementById("search-input");

      if (searchInput) {

        const archiveLinks = archiveList.querySelectorAll("li");

        searchInput.addEventListener("input", () => {

          const query = searchInput.value.toLowerCase();

          archiveLinks.forEach(li => {

            const text = li.textContent.toLowerCase();

            li.style.display = text.includes(query)
              ? "block"
              : "none";

          });

        });

      }

    })
    .catch(err => console.error("Archive load failed:", err));


  // === Lightbox ===
  const imgs = document.querySelectorAll('.thumbnail, .post-image');
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = document.getElementById('lightbox-img');

  imgs.forEach(img => {

    img.addEventListener('click', () => {

      const fullSrc = img.dataset.full || img.src;

      lightboxImg.src = fullSrc;
      lightbox.style.display = 'flex';

    });

  });

  if (lightbox) {

    lightbox.addEventListener('click', () => {

      lightbox.style.display = 'none';
      lightboxImg.src = '';

    });

  }


  // === Mobile Archive Toggle ===
  const archive = document.getElementById('archive');

  if (window.innerWidth <= 768 && archive) {

    const toggle = document.createElement('button');

    toggle.id = 'archive-toggle';
    toggle.textContent = 'Show Archive';

    toggle.style.cssText = `
      display:block;
      text-align:center;
      background:#2C3E50;
      color:#fff;
      padding:0.75rem;
      font-size:1rem;
      border:none;
      width:100%;
      cursor:pointer;
      font-family:inherit;
    `;

    archive.parentNode.insertBefore(toggle, archive);
    archive.classList.remove('open');

    toggle.addEventListener('click', () => {

      archive.classList.toggle('open');

      toggle.textContent =
        archive.classList.contains('open')
        ? 'Hide Archive'
        : 'Show Archive';

    });

    archive.addEventListener('click', e => {

      if (e.target.tagName === "A") {

        archive.classList.remove('open');
        toggle.textContent = 'Show Archive';

      }

    });

  }


  // === Audio Playlist Code ===
  document.querySelectorAll('[id$="-tracklist"]').forEach(tracklist => {

    const albumId = tracklist.id.replace('-tracklist', '');
    const player = document.getElementById(albumId + '-player');

    if (!player) return;

    tracklist.addEventListener('click', function(e) {

      if (e.target.tagName.toLowerCase() === 'a' && e.target.dataset.src) {

        e.preventDefault();

        player.src = e.target.dataset.src;
        player.play();

        tracklist.querySelectorAll('a').forEach(a => a.style.fontWeight = "");
        e.target.style.fontWeight = "bold";

      }

    });

  });


  // 🌙 Dark Mode Toggle
  const toggle = document.getElementById("toggle-dark-mode");

  if (toggle) {

    toggle.addEventListener("click", () => {

      document.body.classList.toggle("dark");

      localStorage.setItem(
        "darkMode",
        document.body.classList.contains("dark")
      );

    });

    if (localStorage.getItem("darkMode") === "true") {

      document.body.classList.add("dark");

    }

  }

});